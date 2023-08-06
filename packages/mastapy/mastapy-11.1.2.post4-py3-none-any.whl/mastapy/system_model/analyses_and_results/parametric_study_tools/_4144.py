"""_4144.py

RingPinsToDiscConnectionParametricStudyTool
"""


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2092
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6671
from mastapy.system_model.analyses_and_results.system_deflections import _2539
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4108
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'RingPinsToDiscConnectionParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionParametricStudyTool',)


class RingPinsToDiscConnectionParametricStudyTool(_4108.InterMountableComponentConnectionParametricStudyTool):
    """RingPinsToDiscConnectionParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _RING_PINS_TO_DISC_CONNECTION_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2092.RingPinsToDiscConnection':
        """RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6671.RingPinsToDiscConnectionLoadCase':
        """RingPinsToDiscConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2539.RingPinsToDiscConnectionSystemDeflection]':
        """List[RingPinsToDiscConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
