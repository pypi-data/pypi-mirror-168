"""_2494.py

CylindricalPlanetGearSystemDeflection
"""


from mastapy.system_model.part_model.gears import _2276
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3825
from mastapy.system_model.analyses_and_results.system_deflections import _2491
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CylindricalPlanetGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearSystemDeflection',)


class CylindricalPlanetGearSystemDeflection(_2491.CylindricalGearSystemDeflectionWithLTCAResults):
    """CylindricalPlanetGearSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_PLANET_GEAR_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2276.CylindricalPlanetGear':
        """CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results(self) -> '_3825.CylindricalPlanetGearPowerFlow':
        """CylindricalPlanetGearPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
