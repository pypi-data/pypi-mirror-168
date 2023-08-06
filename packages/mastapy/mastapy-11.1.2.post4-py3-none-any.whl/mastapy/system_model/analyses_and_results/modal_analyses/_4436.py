"""_4436.py

TorqueConverterConnectionModalAnalysis
"""


from mastapy.system_model.connections_and_sockets.couplings import _2103
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6700
from mastapy.system_model.analyses_and_results.system_deflections import _2572
from mastapy.system_model.analyses_and_results.modal_analyses import _4350
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'TorqueConverterConnectionModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionModalAnalysis',)


class TorqueConverterConnectionModalAnalysis(_4350.CouplingConnectionModalAnalysis):
    """TorqueConverterConnectionModalAnalysis

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_CONNECTION_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2103.TorqueConverterConnection':
        """TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6700.TorqueConverterConnectionLoadCase':
        """TorqueConverterConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2572.TorqueConverterConnectionSystemDeflection':
        """TorqueConverterConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
