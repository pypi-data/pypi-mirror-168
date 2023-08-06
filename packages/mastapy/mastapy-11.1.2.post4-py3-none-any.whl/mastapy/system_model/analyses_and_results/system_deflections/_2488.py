"""_2488.py

CylindricalGearSetSystemDeflectionWithLTCAResults
"""


from mastapy.gears.ltca.cylindrical import _826, _828
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.system_deflections import _2486
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_SYSTEM_DEFLECTION_WITH_LTCA_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CylindricalGearSetSystemDeflectionWithLTCAResults')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetSystemDeflectionWithLTCAResults',)


class CylindricalGearSetSystemDeflectionWithLTCAResults(_2486.CylindricalGearSetSystemDeflection):
    """CylindricalGearSetSystemDeflectionWithLTCAResults

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_SET_SYSTEM_DEFLECTION_WITH_LTCA_RESULTS

    def __init__(self, instance_to_wrap: 'CylindricalGearSetSystemDeflectionWithLTCAResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def advanced_ltca_results(self) -> '_826.CylindricalGearSetLoadDistributionAnalysis':
        """CylindricalGearSetLoadDistributionAnalysis: 'AdvancedLTCAResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdvancedLTCAResults

        if temp is None:
            return None

        if _826.CylindricalGearSetLoadDistributionAnalysis.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast advanced_ltca_results to CylindricalGearSetLoadDistributionAnalysis. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def advanced_ltca_results_only_first_planetary_mesh(self) -> '_826.CylindricalGearSetLoadDistributionAnalysis':
        """CylindricalGearSetLoadDistributionAnalysis: 'AdvancedLTCAResultsOnlyFirstPlanetaryMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdvancedLTCAResultsOnlyFirstPlanetaryMesh

        if temp is None:
            return None

        if _826.CylindricalGearSetLoadDistributionAnalysis.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast advanced_ltca_results_only_first_planetary_mesh to CylindricalGearSetLoadDistributionAnalysis. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def basic_ltca_results(self) -> '_826.CylindricalGearSetLoadDistributionAnalysis':
        """CylindricalGearSetLoadDistributionAnalysis: 'BasicLTCAResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicLTCAResults

        if temp is None:
            return None

        if _826.CylindricalGearSetLoadDistributionAnalysis.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast basic_ltca_results to CylindricalGearSetLoadDistributionAnalysis. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def basic_ltca_results_only_first_planetary_mesh(self) -> '_826.CylindricalGearSetLoadDistributionAnalysis':
        """CylindricalGearSetLoadDistributionAnalysis: 'BasicLTCAResultsOnlyFirstPlanetaryMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicLTCAResultsOnlyFirstPlanetaryMesh

        if temp is None:
            return None

        if _826.CylindricalGearSetLoadDistributionAnalysis.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast basic_ltca_results_only_first_planetary_mesh to CylindricalGearSetLoadDistributionAnalysis. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
