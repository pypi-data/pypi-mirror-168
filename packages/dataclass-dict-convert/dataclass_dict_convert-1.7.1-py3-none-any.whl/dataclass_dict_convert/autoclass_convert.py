import copy
import importlib
from typing import Optional, Callable


def _wrap_autoclass_dataclass_dict_convert(cls):
    orig_from_dict = cls.from_dict
    orig_to_dict = cls.to_dict

    def _auto_from_dict(cls, d: dict, *, on_unknown_field_override: Optional[Callable[[str], None]] = None):
        assert '_classname' in d
        classname = d['_classname']

        clz_parts = classname.split('.')
        mod_name = '.'.join(clz_parts[:len(clz_parts) - 1])
        clz_name = clz_parts[len(clz_parts) - 1]
        module = importlib.import_module(mod_name)
        if not module:
            raise ValueError(f'Unsupported class: {classname!r}')
        clz = getattr(module, clz_name)
        if not clz:
            raise ValueError(f'Unsupported class: {classname!r}')
        assert issubclass(clz, cls)
        d = copy.deepcopy(d)
        del d['_classname']
        if hasattr(clz, '_orig_from_dict'):
            # subclass also has autoclass annotation (which is actually required for _classname)
            # So we us it's original from_dict
            return clz._orig_from_dict(d, on_unknown_field_override=on_unknown_field_override)
        else:
            return orig_from_dict(d, on_unknown_field_override=on_unknown_field_override)

    def _auto_to_dict(self, *, remove_none=False, alt_case=False) -> dict:
        res = orig_to_dict(self, remove_none=remove_none, alt_case=alt_case)
        res['_classname'] = self.__class__.__module__ + '.' + self.__class__.__qualname__
        return res

    cls.from_dict = classmethod(_auto_from_dict)
    cls.to_dict = _auto_to_dict
    cls._orig_to_dict = orig_to_dict
    cls._orig_from_dict = orig_from_dict
    return cls


def autoclass_dataclass_dict_convert(
        _cls=None
):
    """
    This has complex logic to allow decorating with both:
      @autoclass_dataclass_dict_convert
      @autoclass_dataclass_dict_convert()

    It makes .to_dict and .from_dict "polymorph" by adding _classname to the dict/json

    You need to add it to both the parent and child class

    example:
        @autoclass_dataclass_dict_convert
        @dataclass_dict_convert
        @dataclass(frozen=True)
        class Parent:
            nr: int

        @autoclass_dataclass_dict_convert
        @dataclass_dict_convert
        @dataclass(frozen=True)
        class Child(Parent):
            foo: str

        orig_child = Child(1, 'bar')
        child_d = orig_child.to_dict()
        reconstructed_child = Parent.from_dict(child_d)
        assert reconstructed_child == orig_child
        assert isinstance(reconstructed_child, Child)
    """

    def wrap(cls):
        # check if @dataclass_dict_convert has been applied
        assert cls.to_dict
        assert cls.from_dict
        assert cls.to_json
        assert cls.from_json
        assert cls.from_dict_list
        assert cls.to_dict_list
        return _wrap_autoclass_dataclass_dict_convert(cls)

    if _cls is None:
        return wrap
    return wrap(_cls)
