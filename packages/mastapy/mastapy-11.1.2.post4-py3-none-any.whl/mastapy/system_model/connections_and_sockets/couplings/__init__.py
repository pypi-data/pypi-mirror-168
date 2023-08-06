"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2093 import ClutchConnection
    from ._2094 import ClutchSocket
    from ._2095 import ConceptCouplingConnection
    from ._2096 import ConceptCouplingSocket
    from ._2097 import CouplingConnection
    from ._2098 import CouplingSocket
    from ._2099 import PartToPartShearCouplingConnection
    from ._2100 import PartToPartShearCouplingSocket
    from ._2101 import SpringDamperConnection
    from ._2102 import SpringDamperSocket
    from ._2103 import TorqueConverterConnection
    from ._2104 import TorqueConverterPumpSocket
    from ._2105 import TorqueConverterTurbineSocket
