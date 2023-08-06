"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1251 import AssemblyMethods
    from ._1252 import CalculationMethods
    from ._1253 import InterferenceFitDesign
    from ._1254 import InterferenceFitHalfDesign
    from ._1255 import StressRegions
    from ._1256 import Table4JointInterfaceTypes
