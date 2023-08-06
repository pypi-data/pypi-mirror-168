"""_983.py

CylindricalGearMeshFlankDesign
"""


from mastapy._internal import constructor
from mastapy.utility_gui.charts import (
    _1634, _1625, _1630, _1631
)
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_FLANK_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearMeshFlankDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshFlankDesign',)


class CylindricalGearMeshFlankDesign(_0.APIBase):
    """CylindricalGearMeshFlankDesign

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MESH_FLANK_DESIGN

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshFlankDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def degree_of_tooth_loss(self) -> 'float':
        """float: 'DegreeOfToothLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DegreeOfToothLoss

        if temp is None:
            return None

        return temp

    @property
    def flank_name(self) -> 'str':
        """str: 'FlankName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FlankName

        if temp is None:
            return None

        return temp

    @property
    def length_of_contact(self) -> 'float':
        """float: 'LengthOfContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthOfContact

        if temp is None:
            return None

        return temp

    @property
    def specific_sliding_chart(self) -> '_1634.TwoDChartDefinition':
        """TwoDChartDefinition: 'SpecificSlidingChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecificSlidingChart

        if temp is None:
            return None

        if _1634.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast specific_sliding_chart to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tooth_loss_factor(self) -> 'float':
        """float: 'ToothLossFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothLossFactor

        if temp is None:
            return None

        return temp

    @property
    def total_contact_ratio(self) -> 'float':
        """float: 'TotalContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalContactRatio

        if temp is None:
            return None

        return temp

    @property
    def transverse_contact_ratio(self) -> 'float':
        """float: 'TransverseContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseContactRatio

        if temp is None:
            return None

        return temp

    @property
    def virtual_contact_ratio(self) -> 'float':
        """float: 'VirtualContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualContactRatio

        if temp is None:
            return None

        return temp

    @property
    def working_normal_pressure_angle(self) -> 'float':
        """float: 'WorkingNormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkingNormalPressureAngle

        if temp is None:
            return None

        return temp

    @property
    def working_transverse_pressure_angle(self) -> 'float':
        """float: 'WorkingTransversePressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkingTransversePressureAngle

        if temp is None:
            return None

        return temp
