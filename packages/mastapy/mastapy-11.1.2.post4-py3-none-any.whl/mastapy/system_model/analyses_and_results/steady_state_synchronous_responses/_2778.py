"""_2778.py

DatumSteadyStateSynchronousResponse
"""


from mastapy.system_model.part_model import _2199
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6592
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2752
from mastapy._internal.python_net import python_net_import

_DATUM_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'DatumSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumSteadyStateSynchronousResponse',)


class DatumSteadyStateSynchronousResponse(_2752.ComponentSteadyStateSynchronousResponse):
    """DatumSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE = _DATUM_STEADY_STATE_SYNCHRONOUS_RESPONSE

    def __init__(self, instance_to_wrap: 'DatumSteadyStateSynchronousResponse.TYPE'):
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
