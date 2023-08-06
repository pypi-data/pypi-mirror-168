"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2360 import ActiveFESubstructureSelection
    from ._2361 import ActiveFESubstructureSelectionGroup
    from ._2362 import ActiveShaftDesignSelection
    from ._2363 import ActiveShaftDesignSelectionGroup
    from ._2364 import BearingDetailConfiguration
    from ._2365 import BearingDetailSelection
    from ._2366 import PartDetailConfiguration
    from ._2367 import PartDetailSelection
