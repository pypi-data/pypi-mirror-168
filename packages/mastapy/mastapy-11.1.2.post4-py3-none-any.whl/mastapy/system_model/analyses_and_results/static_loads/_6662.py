"""_6662.py

PlanetCarrierLoadCase
"""


from typing import List

from mastapy.system_model.part_model import _2219
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6661, _6651
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PlanetCarrierLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierLoadCase',)


class PlanetCarrierLoadCase(_6651.MountableComponentLoadCase):
    """PlanetCarrierLoadCase

    This is a mastapy class.
    """

    TYPE = _PLANET_CARRIER_LOAD_CASE

    def __init__(self, instance_to_wrap: 'PlanetCarrierLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2219.PlanetCarrier':
        """PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planet_manufacture_errors(self) -> 'List[_6661.PlanetarySocketManufactureError]':
        """List[PlanetarySocketManufactureError]: 'PlanetManufactureErrors' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlanetManufactureErrors

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
