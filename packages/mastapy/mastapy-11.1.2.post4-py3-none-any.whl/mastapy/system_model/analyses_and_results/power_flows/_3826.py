"""_3826.py

DatumPowerFlow
"""


from mastapy.system_model.part_model import _2199
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6592
from mastapy.system_model.analyses_and_results.power_flows import _3799
from mastapy._internal.python_net import python_net_import

_DATUM_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'DatumPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumPowerFlow',)


class DatumPowerFlow(_3799.ComponentPowerFlow):
    """DatumPowerFlow

    This is a mastapy class.
    """

    TYPE = _DATUM_POWER_FLOW

    def __init__(self, instance_to_wrap: 'DatumPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2199.Datum':
        """Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6592.DatumLoadCase':
        """DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
