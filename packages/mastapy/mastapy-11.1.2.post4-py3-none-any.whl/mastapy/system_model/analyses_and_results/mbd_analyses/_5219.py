"""_5219.py

ShaftHubConnectionMultibodyDynamicsAnalysis
"""


from typing import List

from mastapy._math.vector_3d import Vector3D
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.couplings import _2347
from mastapy.system_model.analyses_and_results.static_loads import _6676
from mastapy.system_model.analyses_and_results.mbd_analyses.reporting import _5259, _5261
from mastapy.system_model.analyses_and_results.mbd_analyses import _5150
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ShaftHubConnectionMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionMultibodyDynamicsAnalysis',)


class ShaftHubConnectionMultibodyDynamicsAnalysis(_5150.ConnectorMultibodyDynamicsAnalysis):
    """ShaftHubConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _SHAFT_HUB_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def force(self) -> 'Vector3D':
        """Vector3D: 'Force' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Force

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def force_angular(self) -> 'Vector3D':
        """Vector3D: 'ForceAngular' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceAngular

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def relative_angular_displacement(self) -> 'Vector3D':
        """Vector3D: 'RelativeAngularDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeAngularDisplacement

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def relative_linear_displacement(self) -> 'Vector3D':
        """Vector3D: 'RelativeLinearDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeLinearDisplacement

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def component_design(self) -> '_2347.ShaftHubConnection':
        """ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6676.ShaftHubConnectionLoadCase':
        """ShaftHubConnectionLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def peak_dynamic_force(self) -> '_5259.DynamicForceVector3DResult':
        """DynamicForceVector3DResult: 'PeakDynamicForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeakDynamicForce

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def peak_dynamic_force_angular(self) -> '_5261.DynamicTorqueVector3DResult':
        """DynamicTorqueVector3DResult: 'PeakDynamicForceAngular' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeakDynamicForceAngular

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionMultibodyDynamicsAnalysis]':
        """List[ShaftHubConnectionMultibodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
