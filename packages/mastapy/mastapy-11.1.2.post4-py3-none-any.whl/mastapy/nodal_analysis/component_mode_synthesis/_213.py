"""_213.py

StaticCMSResults
"""


from mastapy.nodal_analysis.states import _120, _119
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.nodal_analysis.component_mode_synthesis import _211
from mastapy._internal.python_net import python_net_import

_STATIC_CMS_RESULTS = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'StaticCMSResults')


__docformat__ = 'restructuredtext en'
__all__ = ('StaticCMSResults',)


class StaticCMSResults(_211.RealCMSResults):
    """StaticCMSResults

    This is a mastapy class.
    """

    TYPE = _STATIC_CMS_RESULTS

    def __init__(self, instance_to_wrap: 'StaticCMSResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def node_stress_tensors(self) -> '_120.NodeVectorState':
        """NodeVectorState: 'NodeStressTensors' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NodeStressTensors

        if temp is None:
            return None

        if _120.NodeVectorState.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast node_stress_tensors to NodeVectorState. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def calculate_stress(self):
        """ 'CalculateStress' is the original name of this method."""

        self.wrapped.CalculateStress()
