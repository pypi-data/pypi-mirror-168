"""_211.py

RealCMSResults
"""


from mastapy.nodal_analysis.states import _120, _119
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.nodal_analysis.component_mode_synthesis import _208
from mastapy._internal.python_net import python_net_import

_REAL_CMS_RESULTS = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'RealCMSResults')


__docformat__ = 'restructuredtext en'
__all__ = ('RealCMSResults',)


class RealCMSResults(_208.CMSResults):
    """RealCMSResults

    This is a mastapy class.
    """

    TYPE = _REAL_CMS_RESULTS

    def __init__(self, instance_to_wrap: 'RealCMSResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def node_displacements(self) -> '_120.NodeVectorState':
        """NodeVectorState: 'NodeDisplacements' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NodeDisplacements

        if temp is None:
            return None

        if _120.NodeVectorState.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast node_displacements to NodeVectorState. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
