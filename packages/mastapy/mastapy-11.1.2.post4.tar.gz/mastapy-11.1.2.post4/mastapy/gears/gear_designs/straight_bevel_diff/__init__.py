"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._928 import StraightBevelDiffGearDesign
    from ._929 import StraightBevelDiffGearMeshDesign
    from ._930 import StraightBevelDiffGearSetDesign
    from ._931 import StraightBevelDiffMeshedGearDesign
