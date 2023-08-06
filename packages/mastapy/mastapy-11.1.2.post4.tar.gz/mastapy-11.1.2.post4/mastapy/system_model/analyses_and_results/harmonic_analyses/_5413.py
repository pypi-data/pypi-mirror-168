"""_5413.py

AbstractPeriodicExcitationDetail
"""


from mastapy.system_model.analyses_and_results.static_loads import (
    _6622, _6570, _6587, _6596,
    _6597, _6598, _6599, _6600,
    _6618, _6664, _6680, _6707
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ABSTRACT_PERIODIC_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'AbstractPeriodicExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractPeriodicExcitationDetail',)


class AbstractPeriodicExcitationDetail(_0.APIBase):
    """AbstractPeriodicExcitationDetail

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_PERIODIC_EXCITATION_DETAIL

    def __init__(self, instance_to_wrap: 'AbstractPeriodicExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def harmonic_load_data(self) -> '_6622.HarmonicLoadDataBase':
        """HarmonicLoadDataBase: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6622.HarmonicLoadDataBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to HarmonicLoadDataBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_conical_gear_set_harmonic_load_data(self) -> '_6570.ConicalGearSetHarmonicLoadData':
        """ConicalGearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6570.ConicalGearSetHarmonicLoadData.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ConicalGearSetHarmonicLoadData. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_cylindrical_gear_set_harmonic_load_data(self) -> '_6587.CylindricalGearSetHarmonicLoadData':
        """CylindricalGearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6587.CylindricalGearSetHarmonicLoadData.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to CylindricalGearSetHarmonicLoadData. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data(self) -> '_6596.ElectricMachineHarmonicLoadData':
        """ElectricMachineHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6596.ElectricMachineHarmonicLoadData.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadData. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_excel(self) -> '_6597.ElectricMachineHarmonicLoadDataFromExcel':
        """ElectricMachineHarmonicLoadDataFromExcel: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6597.ElectricMachineHarmonicLoadDataFromExcel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromExcel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_flux(self) -> '_6598.ElectricMachineHarmonicLoadDataFromFlux':
        """ElectricMachineHarmonicLoadDataFromFlux: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6598.ElectricMachineHarmonicLoadDataFromFlux.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromFlux. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_jmag(self) -> '_6599.ElectricMachineHarmonicLoadDataFromJMAG':
        """ElectricMachineHarmonicLoadDataFromJMAG: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6599.ElectricMachineHarmonicLoadDataFromJMAG.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromJMAG. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_motor_cad(self) -> '_6600.ElectricMachineHarmonicLoadDataFromMotorCAD':
        """ElectricMachineHarmonicLoadDataFromMotorCAD: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6600.ElectricMachineHarmonicLoadDataFromMotorCAD.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromMotorCAD. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_gear_set_harmonic_load_data(self) -> '_6618.GearSetHarmonicLoadData':
        """GearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6618.GearSetHarmonicLoadData.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to GearSetHarmonicLoadData. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_point_load_harmonic_load_data(self) -> '_6664.PointLoadHarmonicLoadData':
        """PointLoadHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6664.PointLoadHarmonicLoadData.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to PointLoadHarmonicLoadData. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_speed_dependent_harmonic_load_data(self) -> '_6680.SpeedDependentHarmonicLoadData':
        """SpeedDependentHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6680.SpeedDependentHarmonicLoadData.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to SpeedDependentHarmonicLoadData. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_load_data_of_type_unbalanced_mass_harmonic_load_data(self) -> '_6707.UnbalancedMassHarmonicLoadData':
        """UnbalancedMassHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicLoadData

        if temp is None:
            return None

        if _6707.UnbalancedMassHarmonicLoadData.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to UnbalancedMassHarmonicLoadData. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
