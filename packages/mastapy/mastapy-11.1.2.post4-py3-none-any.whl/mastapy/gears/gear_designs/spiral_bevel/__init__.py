"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._932 import SpiralBevelGearDesign
    from ._933 import SpiralBevelGearMeshDesign
    from ._934 import SpiralBevelGearSetDesign
    from ._935 import SpiralBevelMeshedGearDesign
