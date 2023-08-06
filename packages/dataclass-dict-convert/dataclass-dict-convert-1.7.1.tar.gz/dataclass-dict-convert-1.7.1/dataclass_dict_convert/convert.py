import collections
import dataclasses
import json
import threading
from abc import ABC, abstractmethod
from collections.abc import Mapping
from datetime import datetime
from enum import Enum
from typing import Callable, Optional, Any, Dict, Type, Union, List

from dataclass_dict_convert.rfc3339 import dump_rfc3339, parse_rfc3339


class DataclassConvertError(Exception):
    def __init__(self, message):
        self.message = message


class UnknownFieldError(Exception):
    def __init__(self, message):
        self.message = message


class TypeConvertorError(Exception):
    def __init__(self, message):
        self.message = message


class TypeConvertor(ABC):
    @abstractmethod
    def get_type(self) -> Type:
        raise NotImplementedError()

    @abstractmethod
    def convert_from_dict(self, val: Union[Dict, List, int, float, str, bool]) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def convert_to_dict(self, val: Any) -> Union[Dict, List, int, float, str, bool]:
        raise NotImplementedError()


@dataclasses.dataclass
class SimpleTypeConvertor(TypeConvertor):
    type: Type
    from_dict: Callable[[Union[Dict, List, int, float, str, bool]], Any]
    to_dict: Callable[[Any], Union[Dict, List, int, float, str, bool]]

    def get_type(self) -> Type:
        return self.type

    def convert_from_dict(self, val: Union[Dict, List, int, float, str, bool]) -> Any:
        return self.from_dict(val)

    def convert_to_dict(self, val: Any) -> Union[Dict, List, int, float, str, bool]:
        return self.to_dict(val)


@dataclasses.dataclass
class _DataclassDictConvertFieldMetaData:
    field_name: str
    dict_field_name: str
    alt_dict_field_name: Optional[str]
    to_dict_convertor: Callable[[Any], Any]
    from_dict_convertor: Callable[[Any], Any]


def _remove_none_recursive(val: Any) -> Any:
    if val is None:
        return None
    if isinstance(val, str) or isinstance(val, int) or isinstance(val, float) or isinstance(val, bool):
        return val
    if isinstance(val, list):
        # return [remove_none_recursive(v) for v in val if v is not None]
        return [_remove_none_recursive(v) for v in val]  # List is allowed to include None!
    if isinstance(val, dict):
        return {k: _remove_none_recursive(v) for k, v in val.items() if v is not None}
    raise ValueError('remove_none_recursive does not know how to handle type "{}"'.format(type(val)))


def _is_optional(a_type: type):
    if not (hasattr(a_type, '__origin__') and \
            a_type.__origin__ is Union and \
            len(a_type.__args__) == 2):
        return False
    t1 = a_type.__args__[0]
    t2 = a_type.__args__[1]
    for t in (t1,t2):
        if hasattr(t, '__origin__'):
            continue
        if isinstance(None, t):
            return True
    return False


def _get_optional_type(a_type: type):
    return a_type.__args__[0] if a_type.__args__[0] else a_type.__args__[1]


def _is_list(a_type: type):
    return hasattr(a_type, '__origin__') and a_type.__origin__ is list


def _is_dict(a_type: type):
    return hasattr(a_type, '__origin__') and a_type.__origin__ is dict


def _is_enum(a_type: type):
    if hasattr(a_type, '__origin__'):
        return False
    try:
        return issubclass(a_type, Enum)
    except TypeError:
        # could be prevented by checking inspect.isclass(a_type)
        return False


def _is_class(a_type: type):
    try:
        return issubclass(a_type, a_type)
    except TypeError:
        # could be prevented by checking inspect.isclass(a_type)
        return False


def _is_json_primitive(a_type: type):
    return a_type is int or a_type is bool or a_type is float or a_type is str


def _find_convertor(
        field_name, field_type,
        default_datetime_convertor: Optional[Callable[[datetime], Any]],
        custom_dict_convertors: Dict[str, Callable[[Any], Any]],
        custom_type_convertors: List[TypeConvertor],
        direct_fields: List[str],
        is_from: bool) -> Optional[Callable[[Any], Any]]:
    try:
        if field_name in custom_dict_convertors:
            return custom_dict_convertors[field_name]
        if _is_json_primitive(field_type) or field_name in direct_fields:
            return lambda p: p
        for custom_type_convertor in custom_type_convertors:
            if field_type is custom_type_convertor.get_type():
                if is_from:
                    return custom_type_convertor.convert_from_dict
                else:
                    return custom_type_convertor.convert_to_dict
        # custom_type_convertor takes precedence, so you can use it to override datetime convert as well.
        if field_type is datetime:
            return default_datetime_convertor
        if _is_optional(field_type):
            sub_convertor = _find_convertor(
                field_name, _get_optional_type(field_type),
                default_datetime_convertor, custom_dict_convertors, custom_type_convertors, direct_fields,
                is_from)
            if sub_convertor is None:
                return None

            def _opt_convert_helper(orig_val):
                if orig_val is None:
                    return None
                else:
                    return sub_convertor(orig_val)
            return _opt_convert_helper
        if _is_list(field_type):
            sub_convertor = _find_convertor(
                field_name, field_type.__args__[0],
                default_datetime_convertor, custom_dict_convertors, custom_type_convertors, direct_fields,
                is_from)
            if sub_convertor is None:
                return None

            def _opt_convert_helper(orig_val):
                return [sub_convertor(orig_el) for orig_el in orig_val]
            return _opt_convert_helper
        if _is_dict(field_type):
            if not hasattr(field_type, '__args__') or len(field_type.__args__) != 2 or \
                    not _is_class(field_type.__args__[0]) or not _is_class(field_type.__args__[1]):
                # this is type "dict" or "Dict" (without key/value types specified)
                # We don't convert types inside! We only do that if subtypes are specified.

                # Note: for some reason, sometimes Dict results in a type with 2 args,
                #       but they are not classes (key is ~KT). We handle that case above as well.
                if is_from:
                    def dict_handler(d):
                        if not isinstance(d, Mapping):
                            raise DataclassConvertError(
                                "field {field_name!r} of expected type dict is a {type(d)!r} instead")
                        return dict(d)
                    return dict_handler
                else:
                    return lambda d: d
            else:
                # this is type "dict" or "Dict" (with key/value types specified)
                dict_key_type = field_type.__args__[0]
                dict_value_type = field_type.__args__[1]
                dict_key_handler = _find_convertor(
                    field_name, dict_key_type,
                    default_datetime_convertor, custom_dict_convertors, custom_type_convertors, direct_fields,
                    is_from)
                dict_value_handler = _find_convertor(
                    field_name, dict_value_type,
                    default_datetime_convertor, custom_dict_convertors, custom_type_convertors, direct_fields,
                    is_from)
                if dict_key_handler is None or dict_value_handler is None:
                    raise DataclassConvertError(
                        f'Error while searching convertor for field {field_name!r} of type {field_type!r} '
                        f'is_from={is_from} '
                        f'dict_key_handler found={dict_key_handler is not None} '
                        f'dict_value_handler found={dict_value_handler is not None}')
                if is_from:
                    def dict_handler(d):
                        if not isinstance(d, Mapping):
                            raise DataclassConvertError(
                                "field {} of expected type dict is a {} instead".format(field_name, type(d)))
                        return {dict_key_handler(k): dict_value_handler(v) for k, v in d.items()}
                    return dict_handler
                else:
                    return lambda d: {dict_key_handler(k): dict_value_handler(v) for k, v in d.items()}
        if _is_enum(field_type):
            if is_from:
                return field_type.__members__.get
            else:
                return lambda enum_value: enum_value.name if enum_value is not None else None
        if dataclasses.is_dataclass(field_type):
            # assume dataclass has to_dict and from_dict
            if not hasattr(field_type, 'from_dict'):
                raise DataclassConvertError("Subclass {field_type!r} of field {field_name!r} does not have from_dict()")
            if not hasattr(field_type, 'to_dict'):
                raise DataclassConvertError("Subclass {field_type!r} of field {field_name!r} does not have to_dict()")
            if is_from:
                return lambda value: field_type.from_dict(value)
            else:
                return lambda value: value.to_dict(alt_case=_get_alt_case())
    except:
        raise DataclassConvertError(f'Error while searching convertor for field {field_name!r} '
                                    f'of type {field_type!r} is_from={is_from}')
    return None


def create_wrap_in_list_from_convertor(type_in_list: Type) -> Callable[[Any], List]:
    def wrap(val: str):
        val_type = type(val)
        if val_type is list:
            return val
        if val_type is type_in_list:
            return [val]
        raise TypeError('Unexpected type {} (expected {type_in_list} or List[{type_in_list}])'
                        .format(val_type, type_in_list=type_in_list))

    return wrap


def create_dict_of_dataclasses_from_convertor(type_of_dict_value, field_name_for_debug: Optional[str] = None) \
        -> Callable[[Dict[str, Any]], Dict]:
    def wrap(the_dict: dict):
        assert type(the_dict) is dict
        if not the_dict:
            return the_dict
        try:
            return {key: type_of_dict_value.from_dict(val) for key, val in the_dict.items()}
        except AttributeError:
            firstval = next(iter(the_dict.values()))
            raise DataclassConvertError(
                'Field {!r} has type {!r} which has no from_dict()'
                    .format(field_name_for_debug if field_name_for_debug else 'unknown', type(firstval)))

    return wrap


def create_dict_of_dataclasses_to_convertor(field_name_for_debug: Optional[str] = None) \
        -> Callable[[Dict[str, Any]], Dict]:
    def wrap(the_dict: dict):
        assert type(the_dict) is dict
        if not the_dict:
            return the_dict
        try:
            return {key: val.to_dict() for key, val in the_dict.items()}
        except AttributeError:
            _, firstval = next(iter(the_dict.values()))
            raise DataclassConvertError(
                'Field {} has type {} which has no to_dict()'
                    .format(field_name_for_debug if field_name_for_debug else 'unknown', type(firstval)))

    return wrap


@dataclasses.dataclass(frozen=True)
class _DataclassDictConvertMetaData:
    on_unknown_field: Callable[[str], None]
    metadata_by_fields: Dict[str, _DataclassDictConvertFieldMetaData]
    metadata_by_dict_fields: Dict[str, _DataclassDictConvertFieldMetaData]


# This is a bit of a hack, used to pass on_unknown_field_override to nested dataclasses
# It also passes alt_case
_dataclass_dict_convert_threadLocal = threading.local()


def _set_alt_case(alt_case: bool):
    _dataclass_dict_convert_threadLocal.alt_case = alt_case


def _get_alt_case() -> bool:
    return getattr(_dataclass_dict_convert_threadLocal, 'alt_case', False)


def _set_current_on_unknown_field(on_unknown_field: Optional[Callable[[str], None]]):
    assert getattr(_dataclass_dict_convert_threadLocal, 'depth', 0) == 0
    _dataclass_dict_convert_threadLocal.depth = 1
    _dataclass_dict_convert_threadLocal.on_unknown_field = on_unknown_field


def _dec_depth_current_on_unknown_field():
    assert getattr(_dataclass_dict_convert_threadLocal, 'depth', 0) > 0
    _dataclass_dict_convert_threadLocal.depth = getattr(_dataclass_dict_convert_threadLocal, 'depth', 0) - 1
    if _dataclass_dict_convert_threadLocal.depth < 1:
        _dataclass_dict_convert_threadLocal.depth = 0
        _dataclass_dict_convert_threadLocal.on_unknown_field = None


def _inc_depth_current_on_unknown_field():
    assert getattr(_dataclass_dict_convert_threadLocal, 'depth', 0) > 0
    _dataclass_dict_convert_threadLocal.depth += 1


def _get_current_on_unknown_field() -> Optional[Callable[[str], None]]:
    assert getattr(_dataclass_dict_convert_threadLocal, 'depth', 0) > 0
    return getattr(_dataclass_dict_convert_threadLocal, 'on_unknown_field', None)


def _has_current_on_unknown_field() -> Optional[Callable[[str], None]]:
    return getattr(_dataclass_dict_convert_threadLocal, 'depth', 0) > 0


def _wrap_dataclass_dict_convert(
        cls,
        dict_letter_case: Callable[[str], str],
        alt_dict_letter_case: Optional[Callable[[str], str]],
        on_unknown_field: Callable[[str], None],
        extra_field_defaults: Dict[str, Union[Any, Callable[[Any], Any]]],
        direct_fields: List[str],
        default_to_datetime_convertor: Callable[[Any], datetime],
        default_from_datetime_convertor: Optional[Callable[[datetime], Any]],
        custom_to_dict_convertors: Dict[str, Callable[[Any], Any]],
        custom_from_dict_convertors: Dict[str, Callable[[Any], Any]],
        custom_type_convertors: List[TypeConvertor],
        preprocess_from_dict: Optional[Callable[[Dict], Dict]],
        postprocess_to_dict: Optional[Callable[[Dict], Dict]],
):
    metadata_by_fields = {}
    metadata_by_dict_fields = {}

    # if superclass has extra_field_defaults, we want to use these as well.
    inherited_extra_field_defaults = {}
    for sc in cls.__mro__:
        if hasattr(sc, '_dataclass_dict_convert_extra_field_defaults') and sc._dataclass_dict_convert_extra_field_defaults:
            inherited_extra_field_defaults = dict(sc._dataclass_dict_convert_extra_field_defaults)
    inherited_extra_field_defaults.update(extra_field_defaults)

    all_fields = dataclasses.fields(cls)

    for field in all_fields:
        meta = _DataclassDictConvertFieldMetaData(
            field.name,
            dict_letter_case(field.name),
            alt_dict_letter_case(field.name) if alt_dict_letter_case else None,
            _find_convertor(field.name, field.type,
                            default_to_datetime_convertor, custom_to_dict_convertors, custom_type_convertors, direct_fields,
                            is_from=False),
            _find_convertor(field.name, field.type,
                            default_from_datetime_convertor, custom_from_dict_convertors, custom_type_convertors, direct_fields,
                            is_from=True)
        )
        if meta.to_dict_convertor is None:
            raise DataclassConvertError("""Unhandled "to" type '{}' of field '{}'""".format(field.type, field.name))
        if meta.from_dict_convertor is None:
            raise DataclassConvertError("""Unhandled "from" type '{}' of field '{}'""".format(field.type, field.name))
        metadata_by_fields[field.name] = meta
        metadata_by_dict_fields[meta.dict_field_name] = meta
        if meta.alt_dict_field_name:
            metadata_by_dict_fields[meta.alt_dict_field_name] = meta

    meta = _DataclassDictConvertMetaData(
        on_unknown_field, metadata_by_fields, metadata_by_dict_fields
    )
    # cls._dataclass_dict_convert_metadata = meta

    def _from_dict(cls2, d: dict, *, on_unknown_field_override: Optional[Callable[[str], None]] = None):
        if _has_current_on_unknown_field():
            _inc_depth_current_on_unknown_field()
            on_unknown_field_override = _get_current_on_unknown_field()
        else:
            _set_current_on_unknown_field(on_unknown_field_override)
        try:
            if not isinstance(d, collections.abc.Mapping):
                raise ValueError('from_dict(d) (possibly nested) where d is {} instead of dict: {!r}'.format(type(d), d))
            assert cls is cls2  # minor sanity check
            init_args = {}
            d = dict(d)  # make a copy (undeep!) to make sure we don't change callers dict
            if preprocess_from_dict:
                d = preprocess_from_dict(d)
                assert d is not None, 'preprocess_from_dict should not return None'
                assert isinstance(d, collections.abc.Mapping), f'preprocess_from_dict should return Dict, not {type(d)}'
            for key, value in inherited_extra_field_defaults.items():
                key = dict_letter_case(key)
                alt_key = alt_dict_letter_case(key) if alt_dict_letter_case else None
                if key not in d and ((not alt_key) or alt_key not in d):
                    if isinstance(value, Callable):
                        d[key] = value()
                    else:
                        d[key] = value
            for key, value in d.items():
                field_meta = meta.metadata_by_dict_fields.get(key, None)
                if not field_meta:
                    on_unknown_field_override(key) if on_unknown_field_override else meta.on_unknown_field(key)
                    continue  # ignore this field
                assert key == field_meta.dict_field_name or \
                       (field_meta.alt_dict_field_name and key == field_meta.alt_dict_field_name)
                try:
                    init_args[field_meta.field_name] = field_meta.from_dict_convertor(value)
                except Exception as e:
                    if isinstance(e, TypeConvertorError):
                        # don't add more errors
                        raise
                    else:
                        raise TypeConvertorError(f'Error using custom from_dict_convertor '
                                                 f'for field {field_meta.dict_field_name!r}')
            return cls2(**init_args)
        finally:
            _dec_depth_current_on_unknown_field()

    def _to_dict(self, *, remove_none=False, alt_case=False):
        _set_alt_case(alt_case)  # hack for working on embedded dataclasses
        res = {}
        for key, field_meta in meta.metadata_by_fields.items():
            assert key == field_meta.field_name
            value = getattr(self, field_meta.field_name)
            try:
                used_val = field_meta.to_dict_convertor(value)
            except Exception as e:
                if isinstance(e, TypeConvertorError):
                    # don't add more errors
                    raise
                else:
                    raise TypeConvertorError(f'Error using custom to_dict_convertor '
                                             f'for field {field_meta.dict_field_name!r}')
            if used_val is not None or not remove_none:
                res[field_meta.dict_field_name if not alt_case else field_meta.alt_dict_field_name] = \
                    _remove_none_recursive(used_val) if remove_none else used_val
        if postprocess_to_dict:
            res = postprocess_to_dict(res)
            # Can't allow these, because they would break to_json
            assert res is not None, 'postprocess_to_dict should not return None'
            assert isinstance(res, collections.abc.Mapping), f'postprocess_to_dict should return Dict, not {type(res)}'
        return res

    def _from_json(cls2, json_in: str, *, on_unknown_field_override: Optional[Callable[[str], None]] = None):
        assert cls is cls2  # minor sanity check
        return cls2.from_dict(json.loads(json_in), on_unknown_field_override=on_unknown_field_override)

    def _to_json(self, *, remove_none=False, alt_case=False) -> str:
        return json.dumps(self.to_dict(remove_none=remove_none, alt_case=alt_case))

    def _from_dict_list(cls2, l: list, *, on_unknown_field_override: Optional[Callable[[str], None]] = None):
        assert cls is cls2  # minor sanity check
        return [_from_dict(cls, d, on_unknown_field_override=on_unknown_field_override) for d in l]

    def _to_dict_list(inst_list: list):
        return [inst.to_dict() for inst in inst_list]

    cls.from_dict = classmethod(_from_dict)
    cls.to_dict = _to_dict
    cls.from_json = classmethod(_from_json)
    cls.to_json = _to_json
    cls.from_dict_list = classmethod(_from_dict_list)
    cls.to_dict_list = staticmethod(_to_dict_list)
    cls._dataclass_dict_convert_extra_field_defaults = inherited_extra_field_defaults
    return cls


def dataclass_dict_convert(
        _cls=None, *,
        dict_letter_case: Optional[Callable[[str], str]]=None,
        alt_dict_letter_case: Optional[Callable[[str], str]]=None,
        on_unknown_field: Optional[Callable[[str], None]]=None,
        extra_field_defaults: Dict[str, Union[Any, Callable[[Any], Any]]]=None,
        direct_fields: Optional[List[str]]=None,
        default_to_datetime_convertor: Optional[Callable[[Any], datetime]]=None,
        default_from_datetime_convertor: Optional[Callable[[datetime], Any]]=None,
        custom_to_dict_convertors: Optional[Dict[str, Callable[[Any], Any]]]=None,
        custom_from_dict_convertors: Optional[Dict[str, Callable[[Any], Any]]]=None,
        custom_type_convertors: List[TypeConvertor]=None,
        preprocess_from_dict: Optional[Callable[[Dict], Dict]]=None,
        postprocess_to_dict: Optional[Callable[[Dict], Dict]]=None,
):
    """
    This has complex logic to allow decorating with both:
      @dataclass_dict_convert
      @dataclass_dict_convert()

    dataclass_dict_convert takes parameters:

    example:
    @dataclass_dict_convert
    @dataclass(frozen=True)
    class DemoSub:
        int nr: int

    @dataclass_dict_convert(
         dict_letter_case=camelcase,
         on_undefined=None,  # default: raise exception
         default_to_datetime_convertor=parse_rfc3339,
         default_from_datetime_convertor=dump_rfc3339,
         custom_to_dict_convertors={
         },
         custom_from_dict_convertors={
             'str_lst': str_or_str_list_from_dict
         },
    )
    @dataclass(frozen=True)
    class Demo:
       nr: int
       text: str
       sometime: datetime
       opt_val: Optional[float]
       str_lst: List[str]
       sub: DemoSub
       list_sub: List[DemoSub]
       opt_sub: Optional[DemoSub]


    """
    def default_on_unknown(fieldname: str):
        raise UnknownFieldError('Unknown field encountered: {}'.format(fieldname))

    def wrap(cls):
        return _wrap_dataclass_dict_convert(
            cls,
            dict_letter_case if dict_letter_case else lambda s: s,
            alt_dict_letter_case,
            on_unknown_field if on_unknown_field else default_on_unknown,
            extra_field_defaults if extra_field_defaults else {},
            direct_fields if direct_fields else [],
            default_to_datetime_convertor if default_to_datetime_convertor else dump_rfc3339,
            default_from_datetime_convertor if default_to_datetime_convertor else parse_rfc3339,
            custom_to_dict_convertors if custom_to_dict_convertors else {},
            custom_from_dict_convertors if custom_from_dict_convertors else {},
            custom_type_convertors if custom_type_convertors else [],
            preprocess_from_dict, postprocess_to_dict)

    if _cls is None:
        return wrap
    return wrap(_cls)


def ignore_unknown_fields(field_name: str):
    """unknown field handler that silently ignores unknown fields"""
    pass
