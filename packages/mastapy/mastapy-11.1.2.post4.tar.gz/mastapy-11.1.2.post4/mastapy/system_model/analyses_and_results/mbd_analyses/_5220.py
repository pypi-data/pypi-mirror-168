"""_5220.py

ShaftMultibodyDynamicsAnalysis
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2232
from mastapy.system_model.analyses_and_results.static_loads import _6677
from mastapy.system_model.analyses_and_results.mbd_analyses import _5112
from mastapy._internal.python_net import python_net_import

_SHAFT_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ShaftMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftMultibodyDynamicsAnalysis',)


class ShaftMultibodyDynamicsAnalysis(_5112.AbstractShaftMultibodyDynamicsAnalysis):
    """ShaftMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _SHAFT_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'ShaftMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angular_velocities(self) -> 'List[float]':
        """List[float]: 'AngularVelocities' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularVelocities

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def elastic_local_x_deflections(self) -> 'List[float]':
        """List[float]: 'ElasticLocalXDeflections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticLocalXDeflections

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def elastic_local_y_deflections(self) -> 'List[float]':
        """List[float]: 'ElasticLocalYDeflections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticLocalYDeflections

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def elastic_local_z_deflections(self) -> 'List[float]':
        """List[float]: 'ElasticLocalZDeflections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticLocalZDeflections

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def elastic_local_theta_x_deflections(self) -> 'List[float]':
        """List[float]: 'ElasticLocalThetaXDeflections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticLocalThetaXDeflections

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def elastic_local_theta_y_deflections(self) -> 'List[float]':
        """List[float]: 'ElasticLocalThetaYDeflections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticLocalThetaYDeflections

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def elastic_radial_deflections(self) -> 'List[float]':
        """List[float]: 'ElasticRadialDeflections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticRadialDeflections

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def elastic_twists(self) -> 'List[float]':
        """List[float]: 'ElasticTwists' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticTwists

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def component_design(self) -> '_2232.Shaft':
        """Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6677.ShaftLoadCase':
        """ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[ShaftMultibodyDynamicsAnalysis]':
        """List[ShaftMultibodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
