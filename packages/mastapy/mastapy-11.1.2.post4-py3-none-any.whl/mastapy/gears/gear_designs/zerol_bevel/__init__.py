"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._915 import ZerolBevelGearDesign
    from ._916 import ZerolBevelGearMeshDesign
    from ._917 import ZerolBevelGearSetDesign
    from ._918 import ZerolBevelMeshedGearDesign
