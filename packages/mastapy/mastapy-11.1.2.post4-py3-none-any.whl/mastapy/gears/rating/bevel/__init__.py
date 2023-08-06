"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._520 import BevelGearMeshRating
    from ._521 import BevelGearRating
    from ._522 import BevelGearSetRating
