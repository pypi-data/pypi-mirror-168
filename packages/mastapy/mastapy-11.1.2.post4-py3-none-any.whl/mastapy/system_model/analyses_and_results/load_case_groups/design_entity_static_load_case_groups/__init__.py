"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._5406 import AbstractAssemblyStaticLoadCaseGroup
    from ._5407 import ComponentStaticLoadCaseGroup
    from ._5408 import ConnectionStaticLoadCaseGroup
    from ._5409 import DesignEntityStaticLoadCaseGroup
    from ._5410 import GearSetStaticLoadCaseGroup
    from ._5411 import PartStaticLoadCaseGroup
