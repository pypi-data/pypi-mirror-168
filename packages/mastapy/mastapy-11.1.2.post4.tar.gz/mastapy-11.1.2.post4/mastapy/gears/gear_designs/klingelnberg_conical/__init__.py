"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._944 import KlingelnbergConicalGearDesign
    from ._945 import KlingelnbergConicalGearMeshDesign
    from ._946 import KlingelnbergConicalGearSetDesign
    from ._947 import KlingelnbergConicalMeshedGearDesign
