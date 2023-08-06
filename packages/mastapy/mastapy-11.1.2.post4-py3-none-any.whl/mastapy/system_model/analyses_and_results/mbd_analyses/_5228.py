"""_5228.py

SpringDamperHalfMultibodyDynamicsAnalysis
"""


from mastapy._math.vector_3d import Vector3D
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.couplings import _2350
from mastapy.system_model.analyses_and_results.static_loads import _6685
from mastapy.system_model.analyses_and_results.mbd_analyses import _5152
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'SpringDamperHalfMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfMultibodyDynamicsAnalysis',)


class SpringDamperHalfMultibodyDynamicsAnalysis(_5152.CouplingHalfMultibodyDynamicsAnalysis):
    """SpringDamperHalfMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_HALF_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'SpringDamperHalfMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def spring_relative_displacement(self) -> 'Vector3D':
        """Vector3D: 'SpringRelativeDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpringRelativeDisplacement

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def spring_relative_rotation(self) -> 'Vector3D':
        """Vector3D: 'SpringRelativeRotation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpringRelativeRotation

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def component_design(self) -> '_2350.SpringDamperHalf':
        """SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6685.SpringDamperHalfLoadCase':
        """SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
