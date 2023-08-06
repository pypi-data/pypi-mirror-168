"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._924 import StraightBevelGearDesign
    from ._925 import StraightBevelGearMeshDesign
    from ._926 import StraightBevelGearSetDesign
    from ._927 import StraightBevelMeshedGearDesign
