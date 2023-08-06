"""_2198.py

Connector
"""


from typing import Optional

from mastapy.system_model.part_model import (
    _2187, _2195, _2196, _2214
)
from mastapy._internal import constructor
from mastapy.system_model.part_model.shaft_model import _2232
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.cycloidal import _2318
from mastapy.system_model.connections_and_sockets import (
    _2023, _2016, _2019, _2020,
    _2024, _2032, _2038, _2043,
    _2046, _2027, _2017, _2018,
    _2025, _2030, _2031, _2033,
    _2034, _2035, _2036, _2037,
    _2039, _2040, _2041, _2044,
    _2045
)
from mastapy.system_model.connections_and_sockets.gears import (
    _2050, _2052, _2054, _2056,
    _2058, _2060, _2062, _2064,
    _2066, _2069, _2070, _2071,
    _2074, _2076, _2078, _2080,
    _2082, _2061
)
from mastapy.system_model.connections_and_sockets.cycloidal import (
    _2086, _2089, _2092, _2084,
    _2085, _2087, _2088, _2090,
    _2091
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _2093, _2095, _2097, _2099,
    _2101, _2103, _2094, _2096,
    _2098, _2100, _2102, _2104,
    _2105
)
from mastapy._internal.python_net import python_net_import

_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')


__docformat__ = 'restructuredtext en'
__all__ = ('Connector',)


class Connector(_2214.MountableComponent):
    """Connector

    This is a mastapy class.
    """

    TYPE = _CONNECTOR

    def __init__(self, instance_to_wrap: 'Connector.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def outer_component(self) -> '_2187.AbstractShaft':
        """AbstractShaft: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterComponent

        if temp is None:
            return None

        if _2187.AbstractShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_component to AbstractShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_component_of_type_shaft(self) -> '_2232.Shaft':
        """Shaft: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterComponent

        if temp is None:
            return None

        if _2232.Shaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_component to Shaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_component_of_type_cycloidal_disc(self) -> '_2318.CycloidalDisc':
        """CycloidalDisc: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterComponent

        if temp is None:
            return None

        if _2318.CycloidalDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_component to CycloidalDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection(self) -> '_2023.Connection':
        """Connection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2023.Connection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to Connection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_2016.AbstractShaftToMountableComponentConnection':
        """AbstractShaftToMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2016.AbstractShaftToMountableComponentConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_belt_connection(self) -> '_2019.BeltConnection':
        """BeltConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2019.BeltConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BeltConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_coaxial_connection(self) -> '_2020.CoaxialConnection':
        """CoaxialConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2020.CoaxialConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CoaxialConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_cvt_belt_connection(self) -> '_2024.CVTBeltConnection':
        """CVTBeltConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2024.CVTBeltConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CVTBeltConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_inter_mountable_component_connection(self) -> '_2032.InterMountableComponentConnection':
        """InterMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2032.InterMountableComponentConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to InterMountableComponentConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_planetary_connection(self) -> '_2038.PlanetaryConnection':
        """PlanetaryConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2038.PlanetaryConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to PlanetaryConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_rolling_ring_connection(self) -> '_2043.RollingRingConnection':
        """RollingRingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2043.RollingRingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to RollingRingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_shaft_to_mountable_component_connection(self) -> '_2046.ShaftToMountableComponentConnection':
        """ShaftToMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2046.ShaftToMountableComponentConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ShaftToMountableComponentConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_agma_gleason_conical_gear_mesh(self) -> '_2050.AGMAGleasonConicalGearMesh':
        """AGMAGleasonConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2050.AGMAGleasonConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to AGMAGleasonConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_bevel_differential_gear_mesh(self) -> '_2052.BevelDifferentialGearMesh':
        """BevelDifferentialGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2052.BevelDifferentialGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BevelDifferentialGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_bevel_gear_mesh(self) -> '_2054.BevelGearMesh':
        """BevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2054.BevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_concept_gear_mesh(self) -> '_2056.ConceptGearMesh':
        """ConceptGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2056.ConceptGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConceptGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_conical_gear_mesh(self) -> '_2058.ConicalGearMesh':
        """ConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2058.ConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_cylindrical_gear_mesh(self) -> '_2060.CylindricalGearMesh':
        """CylindricalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2060.CylindricalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CylindricalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_face_gear_mesh(self) -> '_2062.FaceGearMesh':
        """FaceGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2062.FaceGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to FaceGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_gear_mesh(self) -> '_2064.GearMesh':
        """GearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2064.GearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to GearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_hypoid_gear_mesh(self) -> '_2066.HypoidGearMesh':
        """HypoidGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2066.HypoidGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to HypoidGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_2069.KlingelnbergCycloPalloidConicalGearMesh':
        """KlingelnbergCycloPalloidConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2069.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_2070.KlingelnbergCycloPalloidHypoidGearMesh':
        """KlingelnbergCycloPalloidHypoidGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2070.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2071.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        """KlingelnbergCycloPalloidSpiralBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2071.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_spiral_bevel_gear_mesh(self) -> '_2074.SpiralBevelGearMesh':
        """SpiralBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2074.SpiralBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to SpiralBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_straight_bevel_diff_gear_mesh(self) -> '_2076.StraightBevelDiffGearMesh':
        """StraightBevelDiffGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2076.StraightBevelDiffGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to StraightBevelDiffGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_straight_bevel_gear_mesh(self) -> '_2078.StraightBevelGearMesh':
        """StraightBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2078.StraightBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to StraightBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_worm_gear_mesh(self) -> '_2080.WormGearMesh':
        """WormGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2080.WormGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to WormGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_zerol_bevel_gear_mesh(self) -> '_2082.ZerolBevelGearMesh':
        """ZerolBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2082.ZerolBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ZerolBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2086.CycloidalDiscCentralBearingConnection':
        """CycloidalDiscCentralBearingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2086.CycloidalDiscCentralBearingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2089.CycloidalDiscPlanetaryBearingConnection':
        """CycloidalDiscPlanetaryBearingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2089.CycloidalDiscPlanetaryBearingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_ring_pins_to_disc_connection(self) -> '_2092.RingPinsToDiscConnection':
        """RingPinsToDiscConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2092.RingPinsToDiscConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to RingPinsToDiscConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_clutch_connection(self) -> '_2093.ClutchConnection':
        """ClutchConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2093.ClutchConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ClutchConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_concept_coupling_connection(self) -> '_2095.ConceptCouplingConnection':
        """ConceptCouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2095.ConceptCouplingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConceptCouplingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_coupling_connection(self) -> '_2097.CouplingConnection':
        """CouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2097.CouplingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CouplingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_part_to_part_shear_coupling_connection(self) -> '_2099.PartToPartShearCouplingConnection':
        """PartToPartShearCouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2099.PartToPartShearCouplingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to PartToPartShearCouplingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_spring_damper_connection(self) -> '_2101.SpringDamperConnection':
        """SpringDamperConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2101.SpringDamperConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to SpringDamperConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_connection_of_type_torque_converter_connection(self) -> '_2103.TorqueConverterConnection':
        """TorqueConverterConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConnection

        if temp is None:
            return None

        if _2103.TorqueConverterConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to TorqueConverterConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket(self) -> '_2027.CylindricalSocket':
        """CylindricalSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2027.CylindricalSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CylindricalSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_bearing_inner_socket(self) -> '_2017.BearingInnerSocket':
        """BearingInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2017.BearingInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to BearingInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_bearing_outer_socket(self) -> '_2018.BearingOuterSocket':
        """BearingOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2018.BearingOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to BearingOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_cvt_pulley_socket(self) -> '_2025.CVTPulleySocket':
        """CVTPulleySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2025.CVTPulleySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CVTPulleySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_inner_shaft_socket(self) -> '_2030.InnerShaftSocket':
        """InnerShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2030.InnerShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to InnerShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_inner_shaft_socket_base(self) -> '_2031.InnerShaftSocketBase':
        """InnerShaftSocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2031.InnerShaftSocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to InnerShaftSocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_mountable_component_inner_socket(self) -> '_2033.MountableComponentInnerSocket':
        """MountableComponentInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2033.MountableComponentInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_mountable_component_outer_socket(self) -> '_2034.MountableComponentOuterSocket':
        """MountableComponentOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2034.MountableComponentOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_mountable_component_socket(self) -> '_2035.MountableComponentSocket':
        """MountableComponentSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2035.MountableComponentSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to MountableComponentSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_outer_shaft_socket(self) -> '_2036.OuterShaftSocket':
        """OuterShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2036.OuterShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to OuterShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_outer_shaft_socket_base(self) -> '_2037.OuterShaftSocketBase':
        """OuterShaftSocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2037.OuterShaftSocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to OuterShaftSocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_planetary_socket(self) -> '_2039.PlanetarySocket':
        """PlanetarySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2039.PlanetarySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PlanetarySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_planetary_socket_base(self) -> '_2040.PlanetarySocketBase':
        """PlanetarySocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2040.PlanetarySocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PlanetarySocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_pulley_socket(self) -> '_2041.PulleySocket':
        """PulleySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2041.PulleySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PulleySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_rolling_ring_socket(self) -> '_2044.RollingRingSocket':
        """RollingRingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2044.RollingRingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to RollingRingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_shaft_socket(self) -> '_2045.ShaftSocket':
        """ShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2045.ShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_cylindrical_gear_teeth_socket(self) -> '_2061.CylindricalGearTeethSocket':
        """CylindricalGearTeethSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2061.CylindricalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CylindricalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_axial_left_socket(self) -> '_2084.CycloidalDiscAxialLeftSocket':
        """CycloidalDiscAxialLeftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2084.CycloidalDiscAxialLeftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_axial_right_socket(self) -> '_2085.CycloidalDiscAxialRightSocket':
        """CycloidalDiscAxialRightSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2085.CycloidalDiscAxialRightSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscAxialRightSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_inner_socket(self) -> '_2087.CycloidalDiscInnerSocket':
        """CycloidalDiscInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2087.CycloidalDiscInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_outer_socket(self) -> '_2088.CycloidalDiscOuterSocket':
        """CycloidalDiscOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2088.CycloidalDiscOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2090.CycloidalDiscPlanetaryBearingSocket':
        """CycloidalDiscPlanetaryBearingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2090.CycloidalDiscPlanetaryBearingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_ring_pins_socket(self) -> '_2091.RingPinsSocket':
        """RingPinsSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2091.RingPinsSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to RingPinsSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_clutch_socket(self) -> '_2094.ClutchSocket':
        """ClutchSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2094.ClutchSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ClutchSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_concept_coupling_socket(self) -> '_2096.ConceptCouplingSocket':
        """ConceptCouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2096.ConceptCouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ConceptCouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_coupling_socket(self) -> '_2098.CouplingSocket':
        """CouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2098.CouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_part_to_part_shear_coupling_socket(self) -> '_2100.PartToPartShearCouplingSocket':
        """PartToPartShearCouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2100.PartToPartShearCouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PartToPartShearCouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_spring_damper_socket(self) -> '_2102.SpringDamperSocket':
        """SpringDamperSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2102.SpringDamperSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to SpringDamperSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_torque_converter_pump_socket(self) -> '_2104.TorqueConverterPumpSocket':
        """TorqueConverterPumpSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2104.TorqueConverterPumpSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to TorqueConverterPumpSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def outer_socket_of_type_torque_converter_turbine_socket(self) -> '_2105.TorqueConverterTurbineSocket':
        """TorqueConverterTurbineSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSocket

        if temp is None:
            return None

        if _2105.TorqueConverterTurbineSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to TorqueConverterTurbineSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def house_in(self, shaft: '_2187.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_2023.Connection':
        """ 'HouseIn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.connections_and_sockets.Connection
        """

        offset = float(offset)
        method_result = self.wrapped.HouseIn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def other_component(self, component: '_2195.Component') -> '_2187.AbstractShaft':
        """ 'OtherComponent' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.AbstractShaft
        """

        method_result = self.wrapped.OtherComponent(component.wrapped if component else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def try_house_in(self, shaft: '_2187.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_2196.ComponentsConnectedResult':
        """ 'TryHouseIn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        """

        offset = float(offset)
        method_result = self.wrapped.TryHouseIn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
