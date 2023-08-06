"""_2769.py

CVTSteadyStateSynchronousResponse
"""


from mastapy.system_model.part_model.couplings import _2335
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2737
from mastapy._internal.python_net import python_net_import

_CVT_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'CVTSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTSteadyStateSynchronousResponse',)


class CVTSteadyStateSynchronousResponse(_2737.BeltDriveSteadyStateSynchronousResponse):
    """CVTSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE = _CVT_STEADY_STATE_SYNCHRONOUS_RESPONSE

    def __init__(self, instance_to_wrap: 'CVTSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2335.CVT':
        """CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
