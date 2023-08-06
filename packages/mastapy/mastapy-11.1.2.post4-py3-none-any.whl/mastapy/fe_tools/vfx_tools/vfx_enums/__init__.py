"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1191 import ProSolveMpcType
    from ._1192 import ProSolveSolverType
