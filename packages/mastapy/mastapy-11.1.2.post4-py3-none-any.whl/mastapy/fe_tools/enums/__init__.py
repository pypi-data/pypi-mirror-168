"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1193 import ElementPropertyClass
    from ._1194 import MaterialPropertyClass
