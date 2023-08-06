"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1245 import KeyedJointDesign
    from ._1246 import KeyTypes
    from ._1247 import KeywayJointHalfDesign
    from ._1248 import NumberOfKeys
