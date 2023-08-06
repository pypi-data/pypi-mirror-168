import _thread
import copy
import dataclasses
import datetime
import logging
from inspect import isclass
from typing import Optional, Any, List, Union, Callable, TypeVar


#
# dataclasses utils that have nothing to do with coverting to/from json/dict
#

def _field_type_name(field_type) -> str:
    try:
        return field_type.__name__
    except AttributeError:
        return '{!r}'.format(field_type)


def dataclass_field_simple_type_check(obj: Any, field_name: str, required_type: type) -> None:
    """
    use dataclass_field_auto_type_check instead!
    :param obj:
    :param field_name:
    :param required_type:
    :return:
    """
    field_val = getattr(obj, field_name)
    if not isinstance(field_val, required_type):
        raise TypeError("{}.{} must be {}, not {}".
                        format(type(obj).__name__, field_name, required_type.__name__, type(field_val).__name__))


def dataclass_field_type_check(obj: Any, field_name: str) -> None:
    field = next(field for field in dataclasses.fields(obj) if field.name == field_name)
    field_val = getattr(obj, field_name)
    if not isinstance(field_val, field.type):
        raise TypeError("{}.{} must be {}, not {}".
                        format(type(obj).__name__, field_name, _field_type_name(field.type), type(field_val).__name__))


def dataclass_field_datetime_check(obj: Any, field_name: str) -> None:
    field = next(field for field in dataclasses.fields(obj) if field.name == field_name)
    field_val = getattr(obj, field_name)
    assert field.type == datetime.datetime
    if not isinstance(field_val, datetime.datetime):
        raise TypeError("{}.{} must be datetime.datetime, not {}".
                        format(type(obj).__name__, field_name, type(field_val).__name__))
    if field_val.tzinfo is None:
        raise TypeError("{}.{} must be non-naive datetime.datetime, but it is naive!".
                        format(type(obj).__name__, field_name))


def dataclass_field_listof_check(obj: Any, field_name: str, list_item_type: type) -> None:
    field_val = getattr(obj, field_name)
    if not isinstance(field_val, list):
        raise TypeError("{}.{} must be {}, not {}".
                        format(type(obj).__name__, field_name, list.__name__, type(field_val).__name__))
    for item in field_val:
        if not isinstance(item, list_item_type):
            raise TypeError("{}.{} items must be {}, not {}".
                            format(type(obj).__name__, field_name, list_item_type.__name__, type(item).__name__))


def dataclass_field_optional_check(obj: Any, field_name: str, optional_of_type: type) -> None:
    field_val = getattr(obj, field_name)
    if field_val is None:
        return
    if not isinstance(field_val, optional_of_type):
        raise TypeError("{}.{} must be Optional[{}], not Optional[{}]".
                        format(type(obj).__name__, field_name, optional_of_type.__name__, type(field_val).__name__))


def dataclass_field_optional_datetime_check(obj: Any, field_name: str) -> None:
    field_val = getattr(obj, field_name)
    if field_val is None:
        return
    if not isinstance(field_val, datetime.datetime):
        raise TypeError("{}.{} must be Optional[datetime.datetime], not Optional[{}]".
                        format(type(obj).__name__, field_name, type(field_val).__name__))
    if field_val.tzinfo is None:
        raise TypeError("{}.{} must be None or a non-naive datetime.datetime, but it is naive!".
                        format(type(obj).__name__, field_name))


def dataclass_field_optional_union_check(obj: Any, field_name: str, *args: type) -> None:
    field_val = getattr(obj, field_name)
    if field_val is None:
        return
    for optional_of_type in args:
        if isinstance(field_val, optional_of_type):
            return
    raise TypeError("{}.{} must be Optional[{}], not Optional[{}]".
                    format(type(obj).__name__,
                           field_name,
                           [optional_of_type.__name__ for optional_of_type in args],
                           type(field_val).__name__)
                    )


def dataclass_field_union_check(obj: Any, field_name: str, *args: type) -> None:
    field_val = getattr(obj, field_name)
    for acceptable_type in args:
        if isinstance(field_val, acceptable_type):
            return
    raise TypeError("{}.{} must be one of {}, not {}".
                    format(type(obj).__name__,
                           field_name,
                           [acceptable_type.__name__ for acceptable_type in args],
                           type(field_val).__name__)
                    )


def _check_list_type_elements_helper(obj, field_name: str, list_val: Any, list_element_type):
    for i in list(list_val):
        if not isinstance(i, list_element_type):
            raise TypeError("{}.{} must contain list of {}, but the list has a {}".format(
                type(obj).__name__, field_name,
                _field_type_name(list_element_type), type(i).__name__))
        if isclass(list_element_type) and issubclass(list_element_type, datetime.datetime) and i.tzinfo is None:
            raise TypeError("{}.{} must contain list of non-naive {}, but the list has a naive {}".format(
                type(obj).__name__, field_name,
                _field_type_name(list_element_type), type(i).__name__))


def _check_dict_type_value_helper(obj, field_name: str, dict_val: Any, dict_key_type, dict_value_type):
    for key, val in dict_val.items():
        if dict_key_type is not Any:
            if not isinstance(key, dict_key_type):
                raise TypeError("{}.{} must contain dict with keys of {}, but a key is a {}".format(
                    type(obj).__name__, field_name,
                    _field_type_name(dict_key_type), type(key).__name__))
            if isclass(dict_key_type) and issubclass(dict_key_type, datetime.datetime) and key.tzinfo is None:
                raise TypeError("{}.{} must contain keys of non-naive {}, but a key has a naive {}".format(
                    type(obj).__name__, field_name,
                    _field_type_name(dict_key_type), type(key).__name__))

        if dict_value_type is not Any:
            if hasattr(dict_value_type, '__origin__') and dict_value_type.__origin__ is list and hasattr(dict_value_type, '__args__'):
                if isinstance(val, list):
                    list_element_type = dict_value_type.__args__[0]
                    _check_list_type_elements_helper(obj, '{}.{}[{!r}]'.format(type(obj).__name__, field_name, key),
                                                     val, list_element_type)
            elif not isinstance(val, dict_value_type):
                raise TypeError("{}.{} must contain dict with values of {}, but a value is a {}".format(
                    type(obj).__name__, field_name,
                    _field_type_name(dict_value_type), type(val).__name__))
            else:
                if isclass(dict_value_type) and issubclass(dict_value_type, datetime.datetime) and val.tzinfo is None:
                    raise TypeError("{}.{} must contain values of non-naive {}, but a value has a naive {}".format(
                        type(obj).__name__, field_name,
                        _field_type_name(dict_value_type), type(val).__name__))


def _dict_type_has_2_valid_type_args(dict_type) -> bool:
    if not hasattr(dict_type, '__args__'):
        return False
    if not dict_type.__args__:
        return False
    if len(dict_type.__args__) != 2:
        return False
    dict_key_type = dict_type.__args__[0]
    dict_value_type = dict_type.__args__[1]
    # this is a special case. Not sure why or when it pops up.
    if isinstance(dict_key_type, TypeVar):
        return False
    if isinstance(dict_value_type, TypeVar):
        return False
    return True


def _dataclass_field_auto_type_check(obj, field_name, field_val, field_type):
    # Note: this gets angry about naive datetime, and won't allow them
    try:
        # Union also cover Optional[X], which is Union[X, NoneType]
        if hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
            for allowed_type in field_type.__args__:
                if hasattr(allowed_type, '__origin__') and allowed_type.__origin__ is list:
                    assert hasattr(allowed_type, '__args__')
                    if isinstance(field_val, list):
                        list_element_type = allowed_type.__args__[0]
                        _check_list_type_elements_helper(obj, field_name, field_val, list_element_type)
                        return
                elif hasattr(allowed_type, '__origin__') and allowed_type.__origin__ is dict:
                    if _dict_type_has_2_valid_type_args(allowed_type):
                        # Dict[?, ?]
                        assert len(allowed_type.__args__) == 2, 'Dict subtype MUST have 0 or 2 arguments (Dict[?, ?])'
                        if isinstance(field_val, dict):
                            dict_key_type = allowed_type.__args__[0]
                            dict_value_type = allowed_type.__args__[1]
                            if not isinstance(field_val, dict):
                                raise TypeError("{}.{} must be dict, not {}".format(
                                    type(obj).__name__, field_name, type(field_val).__name__))
                            try:
                                _check_dict_type_value_helper(obj, field_name, field_val, dict_key_type, dict_value_type)
                            except:
                                def error_handle(a: Callable) -> str:
                                    try:
                                        return a()
                                    except Exception as e:
                                        return f'ERROR: {e}'
                                logging.error(f'Failure checking Union[Dict[?, ?]] type with '
                                              f'field_name={field_name!r} '
                                              f'field_type={field_type!r} '
                                              f'len(allowed_type.__args__)={len(allowed_type.__args__)} '
                                              f'allowed_type.__args__={allowed_type.__args__!r} '
                                              f'allowed_type={allowed_type!r} '
                                              f'dict_key_type={dict_key_type!r} '
                                              f'dict_value_type={dict_value_type!r}'
                                              f'type(dict_key_type)={type(dict_key_type)!r} '
                                              f'type(dict_value_type)={type(dict_value_type)!r}'
                                              f'dict_key_type.__origin__={error_handle(lambda: dict_key_type.__origin__)!r} '
                                              f'dict_value_type.__origin__={error_handle(lambda: dict_value_type.__origin__)!r}')
                                raise
                            return
                    else:
                        # Dict or Dict[]
                        if isinstance(field_val, dict):
                            return
                else:
                    if isinstance(field_val, allowed_type):
                        must_reraise = False
                        try:
                            if isclass(allowed_type) and issubclass(allowed_type, datetime.datetime) and field_val.tzinfo is None:
                                must_reraise = True
                                raise TypeError("{}.{} must be {}, and it is a {}, but a naive one".format(
                                    type(obj).__name__, field_name,
                                    _field_type_name(allowed_type), type(field_val).__name__))
                            return
                        except:
                            # it's not a datetime.datetime, so we can ignore that issubclass doesn't work at this point
                            # (if allowed_type=typing.Dict then issubclass doesn't work)
                            if must_reraise:
                                raise
                            else:
                                return
                            # raise TypeError("{}.{} must be {}, but it is {} and "
                            #                 "something went wrong because of {!r}".format(
                            #     type(obj).__name__, field_name,
                            #     _field_type_name(allowed_type), type(field_val).__name__,
                            #     allowed_type))
            raise TypeError("{}.{} must be one of {}, not {} ({!r} {!r})".format(
                type(obj).__name__, field_name,
                [_field_type_name(t) for t in field_type.__args__], type(field_val).__name__,
                field_type.__args__, type(field_val)))

        if hasattr(field_type, '__origin__') and field_type.__origin__ is list:
            list_element_type = field_type.__args__[0]
            if not isinstance(field_val, list):
                raise TypeError("{}.{} must be list, not {}".format(
                    type(obj).__name__, field_name, type(field_val).__name__))
            _check_list_type_elements_helper(obj, field_name, field_val, list_element_type)
            return

        if hasattr(field_type, '__origin__') and field_type.__origin__ is dict:
            if not _dict_type_has_2_valid_type_args(field_type):
                # this is type "dict" or "Dict" (without subtypes specified)
                field_type = dict
                # no return, just check if it's a generic dict
            else:
                dict_key_type = field_type.__args__[0]
                dict_value_type = field_type.__args__[1]
                # if dict_key_type is not str:
                #     raise NotImplementedError("deep Dict type check with non-str keys is not implemented")
                if not isinstance(field_val, dict):
                    raise TypeError("{}.{} must be dict, not {}".format(
                        type(obj).__name__, field_name, type(field_val).__name__))
                _check_dict_type_value_helper(obj, field_name, field_val, dict_key_type, dict_value_type)
                return

        if not isinstance(field_val, field_type):
            raise TypeError("{}.{} must be {}, not {}".format(
                type(obj).__name__, field_name,
                _field_type_name(field_type), type(field_val).__name__))

        if isclass(field_type) and issubclass(field_type, datetime.datetime) and field_val.tzinfo is None:
            raise TypeError("{}.{} must be non-nave {}, not is it a naive {}".format(
                type(obj).__name__, field_name,
                _field_type_name(field_type), type(field_val).__name__))
    except:
        logging.error(f'Failure checking type for field_name={field_name!r} field_type={field_type!r}')
        raise


def dataclass_field_auto_type_check(obj, field_name):
    field = next(field for field in dataclasses.fields(obj) if field.name == field_name)
    field_val = getattr(obj, field_name)
    _dataclass_field_auto_type_check(obj, field_name, field_val, field.type)


def dataclass_fields_type_check(
        obj: Any,
        field_names_included: Optional[List[str]] = None,
        field_names_excluded: Optional[List[str]] = None) -> None:
    for field in dataclasses.fields(obj):
        if (not field_names_included or field.name in field_names_included) and \
                not (field_names_excluded and field.name in field_names_excluded):
            field_val = getattr(obj, field.name)
            _dataclass_field_auto_type_check(obj, field.name, field_val, field.type)
            # if not isinstance(field_val, field.type):
            #     raise TypeError("{}.{} must be {}, not {}".format(type(obj).__name__, field.name, _field_type_name(field.type), type(field_val).__name__))


def _add_auto_type_check_to_class(cls,
                                  field_names_included: Optional[List[str]] = None,
                                  field_names_excluded: Optional[List[str]] = None):

    has_post_init = hasattr(cls, '__post_init__')

    if has_post_init:
        # print('adding auto type check to {!r} (adding to __post_init__)'.format(cls))
        old_post_init = cls.__post_init__

        def updated_post_init(self, *args, **kwargs):
            old_post_init(self, *args, **kwargs)
            dataclass_fields_type_check(self, field_names_included, field_names_excluded)
        cls.__post_init__ = updated_post_init
    else:
        # print('adding auto type check to {!r} (new __post_init__)'.format(cls))

        def new_post_init(self):
            dataclass_fields_type_check(self, field_names_included, field_names_excluded)
        cls.__post_init__ = new_post_init

    return cls


def _add_copy_method_to_class(cls):
    def make_copy(self):
        return copy.deepcopy(self)

    cls.make_copy = make_copy
    return cls


def dataclass_auto_type_check(_cls=None, *,
                              field_names_included: Optional[List[str]] = None,
                              field_names_excluded: Optional[List[str]] = None):
    """
        This assumes @dataclass !  (but not @dataclass_json or @dataclass_dict_convert)
        It must be placed both BELOW @dataclass/@dataclass_dict_convert !
                (otherwise, it won't work if you have no __post_init__ yet!!!)

    this has complex logic to allow decorating with both:
          @dataclass_auto_type_check
          @dataclass_auto_type_check(field_names_excluded=['aFieldName'])

    example:
          @dataclass
          @dataclass_auto_type_check(field_names_excluded=['field_a'])
          class X:
             field_a: int
             ...
    """

    def wrap(cls):
        return _add_auto_type_check_to_class(cls, field_names_included, field_names_excluded)

    if _cls is None:
        return wrap
    return wrap(_cls)


def dataclass_copy_method(_cls=None):
    """
    This assumes @dataclass
    It works both below and above @dataclass_json/@dataclass_dict_convert and @dataclass

    this has complex logic to allow decorating with both:
      @dataclass_copy_method
      @dataclass_copy_method()

    example:
      @dataclass_copy_method
      @dataclass_dict_convert
      @dataclass
      class X:
         field_a: int
         ...
    """

    def wrap(cls):
        return _add_copy_method_to_class(cls)

    if _cls is None:
        return wrap
    return wrap(_cls)


def _add_dataclass_multiline_repr_method_to_class(cls):
    # recursive_repr function is based on "recursive_repr" function in reprlib and dataclasses _repr_fn
    # This version doesn't use helper functions

    repr_running = set()

    def dataclasses_multiline_repr_helper(self):
        key = _thread.get_ident()
        if key in repr_running:
            return '...'
        repr_running.add(key)
        try:
            all_fields = dataclasses.fields(self)
            field_repr_list = []
            for field in all_fields:
                field_val = getattr(self, field.name)
                field_repr = f"   {field.name}={field_val!r}"
                field_repr = field_repr.replace('\n', '\n   ')
                field_repr_list.append(field_repr)
            fields_repr = '\n' + ',\n'.join(field_repr_list)
            result = f"{self.__class__.__qualname__}({fields_repr})"
        finally:
            repr_running.discard(key)
        return result

    cls.__repr__ = dataclasses_multiline_repr_helper
    return cls


def dataclass_multiline_repr(_cls=None):
    """
    Make repr use newlines between fields, for much more readable output.

    This assumes @dataclass
    It works both below and above @dataclass, but if above @dataclass, you need: @dataclass(repr=False)

    this has complex logic to allow decorating with both:
      @dataclass_multiline_repr
      @dataclass_multiline_repr()

    example:
      @dataclass_multiline_repr
      @dataclass(repr=False)
      class X:
         field_a: int
         ...

    or same:
      @dataclass
      @dataclass_multiline_repr
      class X:
         field_a: int
         ...

    """
    def wrap(cls):
        return _add_dataclass_multiline_repr_method_to_class(cls)

    if _cls is None:
        return wrap
    return wrap(_cls)
