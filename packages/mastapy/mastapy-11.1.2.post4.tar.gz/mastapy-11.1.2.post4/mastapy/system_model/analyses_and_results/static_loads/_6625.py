"""_6625.py

HarmonicLoadDataFluxImport
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6636, _6623, _6603
from mastapy._internal.python_net import python_net_import

_HARMONIC_LOAD_DATA_FLUX_IMPORT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HarmonicLoadDataFluxImport')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicLoadDataFluxImport',)


class HarmonicLoadDataFluxImport(_6623.HarmonicLoadDataCSVImport['_6603.ElectricMachineHarmonicLoadFluxImportOptions']):
    """HarmonicLoadDataFluxImport

    This is a mastapy class.
    """

    TYPE = _HARMONIC_LOAD_DATA_FLUX_IMPORT

    def __init__(self, instance_to_wrap: 'HarmonicLoadDataFluxImport.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def diameter_of_node_ring_from_flux_file(self) -> 'float':
        """float: 'DiameterOfNodeRingFromFluxFile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DiameterOfNodeRingFromFluxFile

        if temp is None:
            return None

        return temp

    @property
    def inner_diameter_reference(self) -> '_6636.InnerDiameterReference':
        """InnerDiameterReference: 'InnerDiameterReference' is the original name of this property."""

        temp = self.wrapped.InnerDiameterReference

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_6636.InnerDiameterReference)(value) if value is not None else None

    @inner_diameter_reference.setter
    def inner_diameter_reference(self, value: '_6636.InnerDiameterReference'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.InnerDiameterReference = value

    def select_flux_file(self):
        """ 'SelectFluxFile' is the original name of this method."""

        self.wrapped.SelectFluxFile()
