"""_2332.py

Coupling
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.couplings import (
    _2333, _2328, _2331, _2336,
    _2338, _2339, _2345, _2350,
    _2353, _2354, _2355, _2357,
    _2359
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model import _2226
from mastapy._internal.python_net import python_net_import

_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Coupling')


__docformat__ = 'restructuredtext en'
__all__ = ('Coupling',)


class Coupling(_2226.SpecialisedAssembly):
    """Coupling

    This is a mastapy class.
    """

    TYPE = _COUPLING

    def __init__(self, instance_to_wrap: 'Coupling.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_stiffness(self) -> 'float':
        """float: 'AxialStiffness' is the original name of this property."""

        temp = self.wrapped.AxialStiffness

        if temp is None:
            return None

        return temp

    @axial_stiffness.setter
    def axial_stiffness(self, value: 'float'):
        self.wrapped.AxialStiffness = float(value) if value else 0.0

    @property
    def radial_stiffness(self) -> 'float':
        """float: 'RadialStiffness' is the original name of this property."""

        temp = self.wrapped.RadialStiffness

        if temp is None:
            return None

        return temp

    @radial_stiffness.setter
    def radial_stiffness(self, value: 'float'):
        self.wrapped.RadialStiffness = float(value) if value else 0.0

    @property
    def tilt_stiffness(self) -> 'float':
        """float: 'TiltStiffness' is the original name of this property."""

        temp = self.wrapped.TiltStiffness

        if temp is None:
            return None

        return temp

    @tilt_stiffness.setter
    def tilt_stiffness(self, value: 'float'):
        self.wrapped.TiltStiffness = float(value) if value else 0.0

    @property
    def torsional_stiffness(self) -> 'float':
        """float: 'TorsionalStiffness' is the original name of this property."""

        temp = self.wrapped.TorsionalStiffness

        if temp is None:
            return None

        return temp

    @torsional_stiffness.setter
    def torsional_stiffness(self, value: 'float'):
        self.wrapped.TorsionalStiffness = float(value) if value else 0.0

    @property
    def halves(self) -> 'List[_2333.CouplingHalf]':
        """List[CouplingHalf]: 'Halves' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Halves

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def half_a(self) -> '_2333.CouplingHalf':
        """CouplingHalf: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfA

        if temp is None:
            return None

        if _2333.CouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_a to CouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_a_of_type_clutch_half(self) -> '_2328.ClutchHalf':
        """ClutchHalf: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfA

        if temp is None:
            return None

        if _2328.ClutchHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_a to ClutchHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_a_of_type_concept_coupling_half(self) -> '_2331.ConceptCouplingHalf':
        """ConceptCouplingHalf: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfA

        if temp is None:
            return None

        if _2331.ConceptCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_a to ConceptCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_a_of_type_cvt_pulley(self) -> '_2336.CVTPulley':
        """CVTPulley: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfA

        if temp is None:
            return None

        if _2336.CVTPulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_a to CVTPulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_a_of_type_part_to_part_shear_coupling_half(self) -> '_2338.PartToPartShearCouplingHalf':
        """PartToPartShearCouplingHalf: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfA

        if temp is None:
            return None

        if _2338.PartToPartShearCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_a to PartToPartShearCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_a_of_type_pulley(self) -> '_2339.Pulley':
        """Pulley: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfA

        if temp is None:
            return None

        if _2339.Pulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_a to Pulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_a_of_type_rolling_ring(self) -> '_2345.RollingRing':
        """RollingRing: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfA

        if temp is None:
            return None

        if _2345.RollingRing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_a to RollingRing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_a_of_type_spring_damper_half(self) -> '_2350.SpringDamperHalf':
        """SpringDamperHalf: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfA

        if temp is None:
            return None

        if _2350.SpringDamperHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_a to SpringDamperHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_a_of_type_synchroniser_half(self) -> '_2353.SynchroniserHalf':
        """SynchroniserHalf: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfA

        if temp is None:
            return None

        if _2353.SynchroniserHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_a to SynchroniserHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_a_of_type_synchroniser_part(self) -> '_2354.SynchroniserPart':
        """SynchroniserPart: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfA

        if temp is None:
            return None

        if _2354.SynchroniserPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_a to SynchroniserPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_a_of_type_synchroniser_sleeve(self) -> '_2355.SynchroniserSleeve':
        """SynchroniserSleeve: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfA

        if temp is None:
            return None

        if _2355.SynchroniserSleeve.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_a to SynchroniserSleeve. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_a_of_type_torque_converter_pump(self) -> '_2357.TorqueConverterPump':
        """TorqueConverterPump: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfA

        if temp is None:
            return None

        if _2357.TorqueConverterPump.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_a to TorqueConverterPump. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_a_of_type_torque_converter_turbine(self) -> '_2359.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfA

        if temp is None:
            return None

        if _2359.TorqueConverterTurbine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_a to TorqueConverterTurbine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_b(self) -> '_2333.CouplingHalf':
        """CouplingHalf: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfB

        if temp is None:
            return None

        if _2333.CouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_b to CouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_b_of_type_clutch_half(self) -> '_2328.ClutchHalf':
        """ClutchHalf: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfB

        if temp is None:
            return None

        if _2328.ClutchHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_b to ClutchHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_b_of_type_concept_coupling_half(self) -> '_2331.ConceptCouplingHalf':
        """ConceptCouplingHalf: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfB

        if temp is None:
            return None

        if _2331.ConceptCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_b to ConceptCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_b_of_type_cvt_pulley(self) -> '_2336.CVTPulley':
        """CVTPulley: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfB

        if temp is None:
            return None

        if _2336.CVTPulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_b to CVTPulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_b_of_type_part_to_part_shear_coupling_half(self) -> '_2338.PartToPartShearCouplingHalf':
        """PartToPartShearCouplingHalf: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfB

        if temp is None:
            return None

        if _2338.PartToPartShearCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_b to PartToPartShearCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_b_of_type_pulley(self) -> '_2339.Pulley':
        """Pulley: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfB

        if temp is None:
            return None

        if _2339.Pulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_b to Pulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_b_of_type_rolling_ring(self) -> '_2345.RollingRing':
        """RollingRing: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfB

        if temp is None:
            return None

        if _2345.RollingRing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_b to RollingRing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_b_of_type_spring_damper_half(self) -> '_2350.SpringDamperHalf':
        """SpringDamperHalf: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfB

        if temp is None:
            return None

        if _2350.SpringDamperHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_b to SpringDamperHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_b_of_type_synchroniser_half(self) -> '_2353.SynchroniserHalf':
        """SynchroniserHalf: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfB

        if temp is None:
            return None

        if _2353.SynchroniserHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_b to SynchroniserHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_b_of_type_synchroniser_part(self) -> '_2354.SynchroniserPart':
        """SynchroniserPart: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfB

        if temp is None:
            return None

        if _2354.SynchroniserPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_b to SynchroniserPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_b_of_type_synchroniser_sleeve(self) -> '_2355.SynchroniserSleeve':
        """SynchroniserSleeve: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfB

        if temp is None:
            return None

        if _2355.SynchroniserSleeve.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_b to SynchroniserSleeve. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_b_of_type_torque_converter_pump(self) -> '_2357.TorqueConverterPump':
        """TorqueConverterPump: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfB

        if temp is None:
            return None

        if _2357.TorqueConverterPump.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_b to TorqueConverterPump. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def half_b_of_type_torque_converter_turbine(self) -> '_2359.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfB

        if temp is None:
            return None

        if _2359.TorqueConverterTurbine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast half_b to TorqueConverterTurbine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
