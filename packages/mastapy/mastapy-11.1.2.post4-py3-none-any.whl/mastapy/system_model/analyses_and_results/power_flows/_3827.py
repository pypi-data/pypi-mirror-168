"""_3827.py

ExternalCADModelPowerFlow
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model import _2202
from mastapy.system_model.analyses_and_results.static_loads import _6607
from mastapy.system_model.analyses_and_results.power_flows import _3799
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ExternalCADModelPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelPowerFlow',)


class ExternalCADModelPowerFlow(_3799.ComponentPowerFlow):
    """ExternalCADModelPowerFlow

    This is a mastapy class.
    """

    TYPE = _EXTERNAL_CAD_MODEL_POWER_FLOW

    def __init__(self, instance_to_wrap: 'ExternalCADModelPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def speed(self) -> 'float':
        """float: 'Speed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Speed

        if temp is None:
            return None

        return temp

    @property
    def component_design(self) -> '_2202.ExternalCADModel':
        """ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6607.ExternalCADModelLoadCase':
        """ExternalCADModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
