"""_735.py

ShavingDynamicsConfiguration
"""


from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _732, _717, _718, _719,
    _724, _725, _721
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHAVING_DYNAMICS_CONFIGURATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ShavingDynamicsConfiguration')


__docformat__ = 'restructuredtext en'
__all__ = ('ShavingDynamicsConfiguration',)


class ShavingDynamicsConfiguration(_0.APIBase):
    """ShavingDynamicsConfiguration

    This is a mastapy class.
    """

    TYPE = _SHAVING_DYNAMICS_CONFIGURATION

    def __init__(self, instance_to_wrap: 'ShavingDynamicsConfiguration.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def conventional_shaving_dynamics(self) -> '_732.ShavingDynamicsCalculation[_717.ConventionalShavingDynamics]':
        """ShavingDynamicsCalculation[ConventionalShavingDynamics]: 'ConventionalShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConventionalShavingDynamics

        if temp is None:
            return None

        if _732.ShavingDynamicsCalculation[_717.ConventionalShavingDynamics].TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast conventional_shaving_dynamics to ShavingDynamicsCalculation[ConventionalShavingDynamics]. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_717.ConventionalShavingDynamics](temp) if temp is not None else None

    @property
    def conventional_shaving_dynamics_of_type_conventional_shaving_dynamics_calculation_for_designed_gears(self) -> '_718.ConventionalShavingDynamicsCalculationForDesignedGears':
        """ConventionalShavingDynamicsCalculationForDesignedGears: 'ConventionalShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConventionalShavingDynamics

        if temp is None:
            return None

        if _718.ConventionalShavingDynamicsCalculationForDesignedGears.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast conventional_shaving_dynamics to ConventionalShavingDynamicsCalculationForDesignedGears. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def conventional_shaving_dynamics_of_type_conventional_shaving_dynamics_calculation_for_hobbed_gears(self) -> '_719.ConventionalShavingDynamicsCalculationForHobbedGears':
        """ConventionalShavingDynamicsCalculationForHobbedGears: 'ConventionalShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConventionalShavingDynamics

        if temp is None:
            return None

        if _719.ConventionalShavingDynamicsCalculationForHobbedGears.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast conventional_shaving_dynamics to ConventionalShavingDynamicsCalculationForHobbedGears. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def conventional_shaving_dynamics_of_type_plunge_shaving_dynamics_calculation_for_designed_gears(self) -> '_724.PlungeShavingDynamicsCalculationForDesignedGears':
        """PlungeShavingDynamicsCalculationForDesignedGears: 'ConventionalShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConventionalShavingDynamics

        if temp is None:
            return None

        if _724.PlungeShavingDynamicsCalculationForDesignedGears.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast conventional_shaving_dynamics to PlungeShavingDynamicsCalculationForDesignedGears. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def conventional_shaving_dynamics_of_type_plunge_shaving_dynamics_calculation_for_hobbed_gears(self) -> '_725.PlungeShavingDynamicsCalculationForHobbedGears':
        """PlungeShavingDynamicsCalculationForHobbedGears: 'ConventionalShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConventionalShavingDynamics

        if temp is None:
            return None

        if _725.PlungeShavingDynamicsCalculationForHobbedGears.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast conventional_shaving_dynamics to PlungeShavingDynamicsCalculationForHobbedGears. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def plunge_shaving_dynamics(self) -> '_732.ShavingDynamicsCalculation[_721.PlungeShaverDynamics]':
        """ShavingDynamicsCalculation[PlungeShaverDynamics]: 'PlungeShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlungeShavingDynamics

        if temp is None:
            return None

        if _732.ShavingDynamicsCalculation[_721.PlungeShaverDynamics].TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast plunge_shaving_dynamics to ShavingDynamicsCalculation[PlungeShaverDynamics]. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_721.PlungeShaverDynamics](temp) if temp is not None else None

    @property
    def plunge_shaving_dynamics_of_type_conventional_shaving_dynamics_calculation_for_designed_gears(self) -> '_718.ConventionalShavingDynamicsCalculationForDesignedGears':
        """ConventionalShavingDynamicsCalculationForDesignedGears: 'PlungeShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlungeShavingDynamics

        if temp is None:
            return None

        if _718.ConventionalShavingDynamicsCalculationForDesignedGears.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast plunge_shaving_dynamics to ConventionalShavingDynamicsCalculationForDesignedGears. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def plunge_shaving_dynamics_of_type_conventional_shaving_dynamics_calculation_for_hobbed_gears(self) -> '_719.ConventionalShavingDynamicsCalculationForHobbedGears':
        """ConventionalShavingDynamicsCalculationForHobbedGears: 'PlungeShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlungeShavingDynamics

        if temp is None:
            return None

        if _719.ConventionalShavingDynamicsCalculationForHobbedGears.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast plunge_shaving_dynamics to ConventionalShavingDynamicsCalculationForHobbedGears. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def plunge_shaving_dynamics_of_type_plunge_shaving_dynamics_calculation_for_designed_gears(self) -> '_724.PlungeShavingDynamicsCalculationForDesignedGears':
        """PlungeShavingDynamicsCalculationForDesignedGears: 'PlungeShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlungeShavingDynamics

        if temp is None:
            return None

        if _724.PlungeShavingDynamicsCalculationForDesignedGears.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast plunge_shaving_dynamics to PlungeShavingDynamicsCalculationForDesignedGears. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def plunge_shaving_dynamics_of_type_plunge_shaving_dynamics_calculation_for_hobbed_gears(self) -> '_725.PlungeShavingDynamicsCalculationForHobbedGears':
        """PlungeShavingDynamicsCalculationForHobbedGears: 'PlungeShavingDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlungeShavingDynamics

        if temp is None:
            return None

        if _725.PlungeShavingDynamicsCalculationForHobbedGears.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast plunge_shaving_dynamics to PlungeShavingDynamicsCalculationForHobbedGears. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
