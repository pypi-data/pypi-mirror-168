"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._919 import WormDesign
    from ._920 import WormGearDesign
    from ._921 import WormGearMeshDesign
    from ._922 import WormGearSetDesign
    from ._923 import WormWheelDesign
