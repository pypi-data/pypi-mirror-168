"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1343 import IndividualContactPosition
    from ._1344 import SurfaceToSurfaceContact
