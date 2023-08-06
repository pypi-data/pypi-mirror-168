"""_5176.py

GuideDxfModelMultibodyDynamicsAnalysis
"""


from mastapy.system_model.part_model import _2205
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6620
from mastapy.system_model.analyses_and_results.mbd_analyses import _5139
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'GuideDxfModelMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelMultibodyDynamicsAnalysis',)


class GuideDxfModelMultibodyDynamicsAnalysis(_5139.ComponentMultibodyDynamicsAnalysis):
    """GuideDxfModelMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _GUIDE_DXF_MODEL_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'GuideDxfModelMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2205.GuideDxfModel':
        """GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6620.GuideDxfModelLoadCase':
        """GuideDxfModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
