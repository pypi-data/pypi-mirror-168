"""_835.py

ConicalMeshedGearLoadDistributionAnalysis
"""


from mastapy._internal import constructor
from mastapy.gears.cylindrical import (
    _1165, _1163, _1164, _1162
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.ltca.conical import _833
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CONICAL_MESHED_GEAR_LOAD_DISTRIBUTION_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.LTCA.Conical', 'ConicalMeshedGearLoadDistributionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshedGearLoadDistributionAnalysis',)


class ConicalMeshedGearLoadDistributionAnalysis(_0.APIBase):
    """ConicalMeshedGearLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE = _CONICAL_MESHED_GEAR_LOAD_DISTRIBUTION_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConicalMeshedGearLoadDistributionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def estimated_gear_stiffness_from_fe_model(self) -> 'float':
        """float: 'EstimatedGearStiffnessFromFEModel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EstimatedGearStiffnessFromFEModel

        if temp is None:
            return None

        return temp

    @property
    def max_tensile_principal_root_stress_compression_side(self) -> 'float':
        """float: 'MaxTensilePrincipalRootStressCompressionSide' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaxTensilePrincipalRootStressCompressionSide

        if temp is None:
            return None

        return temp

    @property
    def max_tensile_principal_root_stress_tension_side(self) -> 'float':
        """float: 'MaxTensilePrincipalRootStressTensionSide' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaxTensilePrincipalRootStressTensionSide

        if temp is None:
            return None

        return temp

    @property
    def maximum_von_mises_root_stress_compression_side(self) -> 'float':
        """float: 'MaximumVonMisesRootStressCompressionSide' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumVonMisesRootStressCompressionSide

        if temp is None:
            return None

        return temp

    @property
    def maximum_von_mises_root_stress_tension_side(self) -> 'float':
        """float: 'MaximumVonMisesRootStressTensionSide' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumVonMisesRootStressTensionSide

        if temp is None:
            return None

        return temp

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @property
    def torque(self) -> 'float':
        """float: 'Torque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Torque

        if temp is None:
            return None

        return temp

    @property
    def contact_charts(self) -> '_1165.GearLTCAContactCharts':
        """GearLTCAContactCharts: 'ContactCharts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactCharts

        if temp is None:
            return None

        if _1165.GearLTCAContactCharts.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast contact_charts to GearLTCAContactCharts. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def contact_charts_as_text_file(self) -> '_1164.GearLTCAContactChartDataAsTextFile':
        """GearLTCAContactChartDataAsTextFile: 'ContactChartsAsTextFile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactChartsAsTextFile

        if temp is None:
            return None

        if _1164.GearLTCAContactChartDataAsTextFile.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast contact_charts_as_text_file to GearLTCAContactChartDataAsTextFile. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_load_distribution_analysis(self) -> '_833.ConicalGearLoadDistributionAnalysis':
        """ConicalGearLoadDistributionAnalysis: 'GearLoadDistributionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearLoadDistributionAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
