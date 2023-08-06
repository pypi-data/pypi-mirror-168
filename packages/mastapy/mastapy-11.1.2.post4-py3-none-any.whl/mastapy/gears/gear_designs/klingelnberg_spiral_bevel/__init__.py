"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._936 import KlingelnbergCycloPalloidSpiralBevelGearDesign
    from ._937 import KlingelnbergCycloPalloidSpiralBevelGearMeshDesign
    from ._938 import KlingelnbergCycloPalloidSpiralBevelGearSetDesign
    from ._939 import KlingelnbergCycloPalloidSpiralBevelMeshedGearDesign
