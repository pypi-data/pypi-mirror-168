"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1195 import DetailedRigidConnectorDesign
    from ._1196 import DetailedRigidConnectorHalfDesign
