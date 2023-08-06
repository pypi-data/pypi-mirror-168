"""_2016.py

AbstractShaftToMountableComponentConnection
"""


from mastapy.system_model.part_model import (
    _2214, _2191, _2198, _2212,
    _2213, _2216, _2219, _2221,
    _2222, _2227, _2229, _2187
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.gears import (
    _2262, _2264, _2266, _2267,
    _2268, _2270, _2272, _2274,
    _2276, _2277, _2279, _2283,
    _2285, _2287, _2289, _2292,
    _2294, _2296, _2298, _2299,
    _2300, _2302
)
from mastapy.system_model.part_model.cycloidal import _2319, _2318
from mastapy.system_model.part_model.couplings import (
    _2328, _2331, _2333, _2336,
    _2338, _2339, _2345, _2347,
    _2350, _2353, _2354, _2355,
    _2357, _2359
)
from mastapy.system_model.part_model.shaft_model import _2232
from mastapy.system_model.connections_and_sockets import _2023
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'AbstractShaftToMountableComponentConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftToMountableComponentConnection',)


class AbstractShaftToMountableComponentConnection(_2023.Connection):
    """AbstractShaftToMountableComponentConnection

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION

    def __init__(self, instance_to_wrap: 'AbstractShaftToMountableComponentConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mountable_component(self) -> '_2214.MountableComponent':
        """MountableComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2214.MountableComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MountableComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_bearing(self) -> '_2191.Bearing':
        """Bearing: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2191.Bearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Bearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_connector(self) -> '_2198.Connector':
        """Connector: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2198.Connector.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Connector. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_mass_disc(self) -> '_2212.MassDisc':
        """MassDisc: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2212.MassDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MassDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_measurement_component(self) -> '_2213.MeasurementComponent':
        """MeasurementComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2213.MeasurementComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MeasurementComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_oil_seal(self) -> '_2216.OilSeal':
        """OilSeal: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2216.OilSeal.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to OilSeal. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_planet_carrier(self) -> '_2219.PlanetCarrier':
        """PlanetCarrier: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2219.PlanetCarrier.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PlanetCarrier. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_point_load(self) -> '_2221.PointLoad':
        """PointLoad: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2221.PointLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PointLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_power_load(self) -> '_2222.PowerLoad':
        """PowerLoad: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2222.PowerLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PowerLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_unbalanced_mass(self) -> '_2227.UnbalancedMass':
        """UnbalancedMass: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2227.UnbalancedMass.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to UnbalancedMass. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_virtual_component(self) -> '_2229.VirtualComponent':
        """VirtualComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2229.VirtualComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to VirtualComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_agma_gleason_conical_gear(self) -> '_2262.AGMAGleasonConicalGear':
        """AGMAGleasonConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2262.AGMAGleasonConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to AGMAGleasonConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_bevel_differential_gear(self) -> '_2264.BevelDifferentialGear':
        """BevelDifferentialGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2264.BevelDifferentialGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_bevel_differential_planet_gear(self) -> '_2266.BevelDifferentialPlanetGear':
        """BevelDifferentialPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2266.BevelDifferentialPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_bevel_differential_sun_gear(self) -> '_2267.BevelDifferentialSunGear':
        """BevelDifferentialSunGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2267.BevelDifferentialSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_bevel_gear(self) -> '_2268.BevelGear':
        """BevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2268.BevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_concept_gear(self) -> '_2270.ConceptGear':
        """ConceptGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2270.ConceptGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConceptGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_conical_gear(self) -> '_2272.ConicalGear':
        """ConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2272.ConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_cylindrical_gear(self) -> '_2274.CylindricalGear':
        """CylindricalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2274.CylindricalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CylindricalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_cylindrical_planet_gear(self) -> '_2276.CylindricalPlanetGear':
        """CylindricalPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2276.CylindricalPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CylindricalPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_face_gear(self) -> '_2277.FaceGear':
        """FaceGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2277.FaceGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to FaceGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_gear(self) -> '_2279.Gear':
        """Gear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2279.Gear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Gear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_hypoid_gear(self) -> '_2283.HypoidGear':
        """HypoidGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2283.HypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to HypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2285.KlingelnbergCycloPalloidConicalGear':
        """KlingelnbergCycloPalloidConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2285.KlingelnbergCycloPalloidConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2287.KlingelnbergCycloPalloidHypoidGear':
        """KlingelnbergCycloPalloidHypoidGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2287.KlingelnbergCycloPalloidHypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2289.KlingelnbergCycloPalloidSpiralBevelGear':
        """KlingelnbergCycloPalloidSpiralBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2289.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_spiral_bevel_gear(self) -> '_2292.SpiralBevelGear':
        """SpiralBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2292.SpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_straight_bevel_diff_gear(self) -> '_2294.StraightBevelDiffGear':
        """StraightBevelDiffGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2294.StraightBevelDiffGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelDiffGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_straight_bevel_gear(self) -> '_2296.StraightBevelGear':
        """StraightBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2296.StraightBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_straight_bevel_planet_gear(self) -> '_2298.StraightBevelPlanetGear':
        """StraightBevelPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2298.StraightBevelPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_straight_bevel_sun_gear(self) -> '_2299.StraightBevelSunGear':
        """StraightBevelSunGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2299.StraightBevelSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_worm_gear(self) -> '_2300.WormGear':
        """WormGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2300.WormGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to WormGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_zerol_bevel_gear(self) -> '_2302.ZerolBevelGear':
        """ZerolBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2302.ZerolBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ZerolBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_ring_pins(self) -> '_2319.RingPins':
        """RingPins: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2319.RingPins.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to RingPins. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_clutch_half(self) -> '_2328.ClutchHalf':
        """ClutchHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2328.ClutchHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ClutchHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_concept_coupling_half(self) -> '_2331.ConceptCouplingHalf':
        """ConceptCouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2331.ConceptCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConceptCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_coupling_half(self) -> '_2333.CouplingHalf':
        """CouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2333.CouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_cvt_pulley(self) -> '_2336.CVTPulley':
        """CVTPulley: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2336.CVTPulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CVTPulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_part_to_part_shear_coupling_half(self) -> '_2338.PartToPartShearCouplingHalf':
        """PartToPartShearCouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2338.PartToPartShearCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PartToPartShearCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_pulley(self) -> '_2339.Pulley':
        """Pulley: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2339.Pulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Pulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_rolling_ring(self) -> '_2345.RollingRing':
        """RollingRing: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2345.RollingRing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to RollingRing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_shaft_hub_connection(self) -> '_2347.ShaftHubConnection':
        """ShaftHubConnection: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2347.ShaftHubConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ShaftHubConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_spring_damper_half(self) -> '_2350.SpringDamperHalf':
        """SpringDamperHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2350.SpringDamperHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SpringDamperHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_synchroniser_half(self) -> '_2353.SynchroniserHalf':
        """SynchroniserHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2353.SynchroniserHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_synchroniser_part(self) -> '_2354.SynchroniserPart':
        """SynchroniserPart: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2354.SynchroniserPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_synchroniser_sleeve(self) -> '_2355.SynchroniserSleeve':
        """SynchroniserSleeve: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2355.SynchroniserSleeve.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserSleeve. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_torque_converter_pump(self) -> '_2357.TorqueConverterPump':
        """TorqueConverterPump: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2357.TorqueConverterPump.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to TorqueConverterPump. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mountable_component_of_type_torque_converter_turbine(self) -> '_2359.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MountableComponent

        if temp is None:
            return None

        if _2359.TorqueConverterTurbine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to TorqueConverterTurbine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def shaft(self) -> '_2187.AbstractShaft':
        """AbstractShaft: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shaft

        if temp is None:
            return None

        if _2187.AbstractShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast shaft to AbstractShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def shaft_of_type_shaft(self) -> '_2232.Shaft':
        """Shaft: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shaft

        if temp is None:
            return None

        if _2232.Shaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast shaft to Shaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def shaft_of_type_cycloidal_disc(self) -> '_2318.CycloidalDisc':
        """CycloidalDisc: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shaft

        if temp is None:
            return None

        if _2318.CycloidalDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast shaft to CycloidalDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
