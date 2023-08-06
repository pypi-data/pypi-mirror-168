"""_747.py

ConicalMeshFlankManufacturingConfig
"""


from mastapy.gears.manufacturing.bevel.control_parameters import (
    _783, _784, _785, _786
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel.basic_machine_settings import _790, _789
from mastapy.gears.manufacturing.bevel import _748
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_FLANK_MANUFACTURING_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalMeshFlankManufacturingConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshFlankManufacturingConfig',)


class ConicalMeshFlankManufacturingConfig(_748.ConicalMeshFlankMicroGeometryConfig):
    """ConicalMeshFlankManufacturingConfig

    This is a mastapy class.
    """

    TYPE = _CONICAL_MESH_FLANK_MANUFACTURING_CONFIG

    def __init__(self, instance_to_wrap: 'ConicalMeshFlankManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def control_parameters(self) -> '_783.ConicalGearManufacturingControlParameters':
        """ConicalGearManufacturingControlParameters: 'ControlParameters' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ControlParameters

        if temp is None:
            return None

        if _783.ConicalGearManufacturingControlParameters.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast control_parameters to ConicalGearManufacturingControlParameters. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def control_parameters_of_type_conical_manufacturing_sgm_control_parameters(self) -> '_784.ConicalManufacturingSGMControlParameters':
        """ConicalManufacturingSGMControlParameters: 'ControlParameters' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ControlParameters

        if temp is None:
            return None

        if _784.ConicalManufacturingSGMControlParameters.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast control_parameters to ConicalManufacturingSGMControlParameters. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def control_parameters_of_type_conical_manufacturing_sgt_control_parameters(self) -> '_785.ConicalManufacturingSGTControlParameters':
        """ConicalManufacturingSGTControlParameters: 'ControlParameters' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ControlParameters

        if temp is None:
            return None

        if _785.ConicalManufacturingSGTControlParameters.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast control_parameters to ConicalManufacturingSGTControlParameters. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def control_parameters_of_type_conical_manufacturing_smt_control_parameters(self) -> '_786.ConicalManufacturingSMTControlParameters':
        """ConicalManufacturingSMTControlParameters: 'ControlParameters' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ControlParameters

        if temp is None:
            return None

        if _786.ConicalManufacturingSMTControlParameters.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast control_parameters to ConicalManufacturingSMTControlParameters. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def specified_cradle_style_machine_settings(self) -> '_790.CradleStyleConicalMachineSettingsGenerated':
        """CradleStyleConicalMachineSettingsGenerated: 'SpecifiedCradleStyleMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecifiedCradleStyleMachineSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def specified_phoenix_style_machine_settings(self) -> '_789.BasicConicalGearMachineSettingsGenerated':
        """BasicConicalGearMachineSettingsGenerated: 'SpecifiedPhoenixStyleMachineSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecifiedPhoenixStyleMachineSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
