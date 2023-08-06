"""_2219.py

PlanetCarrier
"""


from typing import List, Optional

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2211, _2214
from mastapy.system_model.connections_and_sockets import _2039
from mastapy.system_model.part_model.shaft_model import _2232
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PlanetCarrier')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrier',)


class PlanetCarrier(_2214.MountableComponent):
    """PlanetCarrier

    This is a mastapy class.
    """

    TYPE = _PLANET_CARRIER

    def __init__(self, instance_to_wrap: 'PlanetCarrier.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def length(self) -> 'float':
        """float: 'Length' is the original name of this property."""

        temp = self.wrapped.Length

        if temp is None:
            return None

        return temp

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value else 0.0

    @property
    def number_of_planetary_sockets(self) -> 'int':
        """int: 'NumberOfPlanetarySockets' is the original name of this property."""

        temp = self.wrapped.NumberOfPlanetarySockets

        if temp is None:
            return None

        return temp

    @number_of_planetary_sockets.setter
    def number_of_planetary_sockets(self, value: 'int'):
        self.wrapped.NumberOfPlanetarySockets = int(value) if value else 0

    @property
    def load_sharing_settings(self) -> '_2211.LoadSharingSettings':
        """LoadSharingSettings: 'LoadSharingSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadSharingSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetary_sockets(self) -> 'List[_2039.PlanetarySocket]':
        """List[PlanetarySocket]: 'PlanetarySockets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlanetarySockets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def attach_carrier_shaft(self, shaft: '_2232.Shaft', offset: Optional['float'] = float('nan')):
        """ 'AttachCarrierShaft' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)
        """

        offset = float(offset)
        self.wrapped.AttachCarrierShaft(shaft.wrapped if shaft else None, offset if offset else 0.0)

    def attach_pin_shaft(self, shaft: '_2232.Shaft', offset: Optional['float'] = float('nan')):
        """ 'AttachPinShaft' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)
        """

        offset = float(offset)
        self.wrapped.AttachPinShaft(shaft.wrapped if shaft else None, offset if offset else 0.0)
