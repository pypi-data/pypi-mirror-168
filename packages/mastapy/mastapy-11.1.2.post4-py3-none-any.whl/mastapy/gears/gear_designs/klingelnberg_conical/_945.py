"""_945.py

KlingelnbergConicalGearMeshDesign
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.gears.gear_designs.conical import _1109
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CONICAL_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.KlingelnbergConical', 'KlingelnbergConicalGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergConicalGearMeshDesign',)


class KlingelnbergConicalGearMeshDesign(_1109.ConicalGearMeshDesign):
    """KlingelnbergConicalGearMeshDesign

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CONICAL_GEAR_MESH_DESIGN

    def __init__(self, instance_to_wrap: 'KlingelnbergConicalGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def application_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ApplicationFactor' is the original name of this property."""

        temp = self.wrapped.ApplicationFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @application_factor.setter
    def application_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ApplicationFactor = value

    @property
    def effective_face_width(self) -> 'float':
        """float: 'EffectiveFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveFaceWidth

        if temp is None:
            return None

        return temp

    @property
    def load_distribution_factor_longitudinal(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'LoadDistributionFactorLongitudinal' is the original name of this property."""

        temp = self.wrapped.LoadDistributionFactorLongitudinal

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @load_distribution_factor_longitudinal.setter
    def load_distribution_factor_longitudinal(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.LoadDistributionFactorLongitudinal = value

    @property
    def net_face_width(self) -> 'float':
        """float: 'NetFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NetFaceWidth

        if temp is None:
            return None

        return temp
