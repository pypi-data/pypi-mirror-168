"""_5208.py

PointLoadMultibodyDynamicsAnalysis
"""


from mastapy._math.vector_3d import Vector3D
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2221
from mastapy.system_model.analyses_and_results.static_loads import _6665
from mastapy.system_model.analyses_and_results.mbd_analyses import _5249
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'PointLoadMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadMultibodyDynamicsAnalysis',)


class PointLoadMultibodyDynamicsAnalysis(_5249.VirtualComponentMultibodyDynamicsAnalysis):
    """PointLoadMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _POINT_LOAD_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'PointLoadMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def applied_force(self) -> 'Vector3D':
        """Vector3D: 'AppliedForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AppliedForce

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def applied_moment(self) -> 'Vector3D':
        """Vector3D: 'AppliedMoment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AppliedMoment

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def component_design(self) -> '_2221.PointLoad':
        """PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6665.PointLoadLoadCase':
        """PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
