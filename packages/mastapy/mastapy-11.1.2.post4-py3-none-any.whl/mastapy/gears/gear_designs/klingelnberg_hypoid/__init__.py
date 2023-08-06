"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._940 import KlingelnbergCycloPalloidHypoidGearDesign
    from ._941 import KlingelnbergCycloPalloidHypoidGearMeshDesign
    from ._942 import KlingelnbergCycloPalloidHypoidGearSetDesign
    from ._943 import KlingelnbergCycloPalloidHypoidMeshedGearDesign
