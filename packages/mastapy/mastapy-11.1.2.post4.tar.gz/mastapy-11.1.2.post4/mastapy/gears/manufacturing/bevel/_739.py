"""_739.py

BevelMachineSettingOptimizationResult
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.bevel import _740
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BEVEL_MACHINE_SETTING_OPTIMIZATION_RESULT = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'BevelMachineSettingOptimizationResult')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelMachineSettingOptimizationResult',)


class BevelMachineSettingOptimizationResult(_0.APIBase):
    """BevelMachineSettingOptimizationResult

    This is a mastapy class.
    """

    TYPE = _BEVEL_MACHINE_SETTING_OPTIMIZATION_RESULT

    def __init__(self, instance_to_wrap: 'BevelMachineSettingOptimizationResult.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum_absolute_residual(self) -> 'float':
        """float: 'MaximumAbsoluteResidual' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumAbsoluteResidual

        if temp is None:
            return None

        return temp

    @property
    def sum_of_squared_residuals(self) -> 'float':
        """float: 'SumOfSquaredResiduals' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SumOfSquaredResiduals

        if temp is None:
            return None

        return temp

    @property
    def calculated_deviations_concave(self) -> '_740.ConicalFlankDeviationsData':
        """ConicalFlankDeviationsData: 'CalculatedDeviationsConcave' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CalculatedDeviationsConcave

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def calculated_deviations_convex(self) -> '_740.ConicalFlankDeviationsData':
        """ConicalFlankDeviationsData: 'CalculatedDeviationsConvex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CalculatedDeviationsConvex

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def imported_deviations_concave(self) -> '_740.ConicalFlankDeviationsData':
        """ConicalFlankDeviationsData: 'ImportedDeviationsConcave' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ImportedDeviationsConcave

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def imported_deviations_convex(self) -> '_740.ConicalFlankDeviationsData':
        """ConicalFlankDeviationsData: 'ImportedDeviationsConvex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ImportedDeviationsConvex

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
