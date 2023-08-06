"""_3859.py

PlanetaryGearSetPowerFlow
"""


from mastapy.system_model.part_model.gears import _2291
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3824
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'PlanetaryGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetPowerFlow',)


class PlanetaryGearSetPowerFlow(_3824.CylindricalGearSetPowerFlow):
    """PlanetaryGearSetPowerFlow

    This is a mastapy class.
    """

    TYPE = _PLANETARY_GEAR_SET_POWER_FLOW

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2291.PlanetaryGearSet':
        """PlanetaryGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
