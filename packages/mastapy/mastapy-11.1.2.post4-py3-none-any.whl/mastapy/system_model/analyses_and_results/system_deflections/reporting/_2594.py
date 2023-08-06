"""_2594.py

SplineFlankContactReporting
"""


from mastapy._internal import constructor, conversion
from mastapy._math.vector_3d import Vector3D
from mastapy.math_utility.measured_vectors import _1371
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SPLINE_FLANK_CONTACT_REPORTING = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Reporting', 'SplineFlankContactReporting')


__docformat__ = 'restructuredtext en'
__all__ = ('SplineFlankContactReporting',)


class SplineFlankContactReporting(_0.APIBase):
    """SplineFlankContactReporting

    This is a mastapy class.
    """

    TYPE = _SPLINE_FLANK_CONTACT_REPORTING

    def __init__(self, instance_to_wrap: 'SplineFlankContactReporting.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angle(self) -> 'float':
        """float: 'Angle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Angle

        if temp is None:
            return None

        return temp

    @property
    def entity_name(self) -> 'str':
        """str: 'EntityName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EntityName

        if temp is None:
            return None

        return temp

    @property
    def normal_deflection(self) -> 'float':
        """float: 'NormalDeflection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalDeflection

        if temp is None:
            return None

        return temp

    @property
    def normal_force(self) -> 'float':
        """float: 'NormalForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalForce

        if temp is None:
            return None

        return temp

    @property
    def normal_stiffness(self) -> 'float':
        """float: 'NormalStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalStiffness

        if temp is None:
            return None

        return temp

    @property
    def relative_deflection_misalignment(self) -> 'float':
        """float: 'RelativeDeflectionMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeDeflectionMisalignment

        if temp is None:
            return None

        return temp

    @property
    def surface_penetration(self) -> 'float':
        """float: 'SurfacePenetration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfacePenetration

        if temp is None:
            return None

        return temp

    @property
    def tangential_deflection(self) -> 'float':
        """float: 'TangentialDeflection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TangentialDeflection

        if temp is None:
            return None

        return temp

    @property
    def tangential_force(self) -> 'float':
        """float: 'TangentialForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TangentialForce

        if temp is None:
            return None

        return temp

    @property
    def tangential_stiffness(self) -> 'float':
        """float: 'TangentialStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TangentialStiffness

        if temp is None:
            return None

        return temp

    @property
    def tilt_moment(self) -> 'float':
        """float: 'TiltMoment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TiltMoment

        if temp is None:
            return None

        return temp

    @property
    def contact_position_lcs(self) -> 'Vector3D':
        """Vector3D: 'ContactPositionLCS' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactPositionLCS

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def contact_position_wcs(self) -> 'Vector3D':
        """Vector3D: 'ContactPositionWCS' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactPositionWCS

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def force_on_inner_contact_coordinate_system(self) -> '_1371.VectorWithLinearAndAngularComponents':
        """VectorWithLinearAndAngularComponents: 'ForceOnInnerContactCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceOnInnerContactCoordinateSystem

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def force_on_inner_wcs(self) -> '_1371.VectorWithLinearAndAngularComponents':
        """VectorWithLinearAndAngularComponents: 'ForceOnInnerWCS' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceOnInnerWCS

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def normal_direction_lcs(self) -> 'Vector3D':
        """Vector3D: 'NormalDirectionLCS' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalDirectionLCS

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def normal_direction_wcs(self) -> 'Vector3D':
        """Vector3D: 'NormalDirectionWCS' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalDirectionWCS

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @property
    def relative_deflection_lcs(self) -> '_1371.VectorWithLinearAndAngularComponents':
        """VectorWithLinearAndAngularComponents: 'RelativeDeflectionLCS' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeDeflectionLCS

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def relative_deflection_wcs(self) -> '_1371.VectorWithLinearAndAngularComponents':
        """VectorWithLinearAndAngularComponents: 'RelativeDeflectionWCS' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeDeflectionWCS

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
