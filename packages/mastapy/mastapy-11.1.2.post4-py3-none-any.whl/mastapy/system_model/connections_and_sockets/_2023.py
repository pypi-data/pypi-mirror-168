"""_2023.py

Connection
"""


from mastapy._internal import constructor
from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.part_model import (
    _2195, _2187, _2188, _2191,
    _2193, _2198, _2199, _2202,
    _2203, _2205, _2212, _2213,
    _2214, _2216, _2219, _2221,
    _2222, _2227, _2229
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2232
from mastapy.system_model.part_model.gears import (
    _2262, _2264, _2266, _2267,
    _2268, _2270, _2272, _2274,
    _2276, _2277, _2279, _2283,
    _2285, _2287, _2289, _2292,
    _2294, _2296, _2298, _2299,
    _2300, _2302
)
from mastapy.system_model.part_model.cycloidal import _2318, _2319
from mastapy.system_model.part_model.couplings import (
    _2328, _2331, _2333, _2336,
    _2338, _2339, _2345, _2347,
    _2350, _2353, _2354, _2355,
    _2357, _2359
)
from mastapy.system_model.connections_and_sockets import (
    _2047, _2017, _2018, _2025,
    _2027, _2029, _2030, _2031,
    _2033, _2034, _2035, _2036,
    _2037, _2039, _2040, _2041,
    _2044, _2045
)
from mastapy.system_model.connections_and_sockets.gears import (
    _2051, _2053, _2055, _2057,
    _2059, _2061, _2063, _2065,
    _2067, _2068, _2072, _2073,
    _2075, _2077, _2079, _2081,
    _2083
)
from mastapy.system_model.connections_and_sockets.cycloidal import (
    _2084, _2085, _2087, _2088,
    _2090, _2091
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _2094, _2096, _2098, _2100,
    _2102, _2104, _2105
)
from mastapy._internal.python_net import python_net_import
from mastapy.system_model import _1960

_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Socket')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')


__docformat__ = 'restructuredtext en'
__all__ = ('Connection',)


class Connection(_1960.DesignEntity):
    """Connection

    This is a mastapy class.
    """

    TYPE = _CONNECTION

    def __init__(self, instance_to_wrap: 'Connection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_id(self) -> 'str':
        """str: 'ConnectionID' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionID

        if temp is None:
            return None

        return temp

    @property
    def drawing_position(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'DrawingPosition' is the original name of this property."""

        temp = self.wrapped.DrawingPosition

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else None

    @drawing_position.setter
    def drawing_position(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.DrawingPosition = value

    @property
    def speed_ratio_from_a_to_b(self) -> 'float':
        """float: 'SpeedRatioFromAToB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpeedRatioFromAToB

        if temp is None:
            return None

        return temp

    @property
    def torque_ratio_from_a_to_b(self) -> 'float':
        """float: 'TorqueRatioFromAToB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueRatioFromAToB

        if temp is None:
            return None

        return temp

    @property
    def unique_name(self) -> 'str':
        """str: 'UniqueName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UniqueName

        if temp is None:
            return None

        return temp

    @property
    def owner_a(self) -> '_2195.Component':
        """Component: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2195.Component.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Component. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_abstract_shaft(self) -> '_2187.AbstractShaft':
        """AbstractShaft: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2187.AbstractShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AbstractShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_abstract_shaft_or_housing(self) -> '_2188.AbstractShaftOrHousing':
        """AbstractShaftOrHousing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2188.AbstractShaftOrHousing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AbstractShaftOrHousing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_bearing(self) -> '_2191.Bearing':
        """Bearing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2191.Bearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Bearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_bolt(self) -> '_2193.Bolt':
        """Bolt: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2193.Bolt.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Bolt. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_connector(self) -> '_2198.Connector':
        """Connector: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2198.Connector.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Connector. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_datum(self) -> '_2199.Datum':
        """Datum: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2199.Datum.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Datum. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_external_cad_model(self) -> '_2202.ExternalCADModel':
        """ExternalCADModel: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2202.ExternalCADModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ExternalCADModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_fe_part(self) -> '_2203.FEPart':
        """FEPart: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2203.FEPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to FEPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_guide_dxf_model(self) -> '_2205.GuideDxfModel':
        """GuideDxfModel: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2205.GuideDxfModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to GuideDxfModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_mass_disc(self) -> '_2212.MassDisc':
        """MassDisc: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2212.MassDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MassDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_measurement_component(self) -> '_2213.MeasurementComponent':
        """MeasurementComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2213.MeasurementComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MeasurementComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_mountable_component(self) -> '_2214.MountableComponent':
        """MountableComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2214.MountableComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MountableComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_oil_seal(self) -> '_2216.OilSeal':
        """OilSeal: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2216.OilSeal.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to OilSeal. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_planet_carrier(self) -> '_2219.PlanetCarrier':
        """PlanetCarrier: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2219.PlanetCarrier.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PlanetCarrier. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_point_load(self) -> '_2221.PointLoad':
        """PointLoad: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2221.PointLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PointLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_power_load(self) -> '_2222.PowerLoad':
        """PowerLoad: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2222.PowerLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PowerLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_unbalanced_mass(self) -> '_2227.UnbalancedMass':
        """UnbalancedMass: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2227.UnbalancedMass.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to UnbalancedMass. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_virtual_component(self) -> '_2229.VirtualComponent':
        """VirtualComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2229.VirtualComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to VirtualComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_shaft(self) -> '_2232.Shaft':
        """Shaft: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2232.Shaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Shaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_agma_gleason_conical_gear(self) -> '_2262.AGMAGleasonConicalGear':
        """AGMAGleasonConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2262.AGMAGleasonConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AGMAGleasonConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_bevel_differential_gear(self) -> '_2264.BevelDifferentialGear':
        """BevelDifferentialGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2264.BevelDifferentialGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_bevel_differential_planet_gear(self) -> '_2266.BevelDifferentialPlanetGear':
        """BevelDifferentialPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2266.BevelDifferentialPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_bevel_differential_sun_gear(self) -> '_2267.BevelDifferentialSunGear':
        """BevelDifferentialSunGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2267.BevelDifferentialSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_bevel_gear(self) -> '_2268.BevelGear':
        """BevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2268.BevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_concept_gear(self) -> '_2270.ConceptGear':
        """ConceptGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2270.ConceptGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConceptGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_conical_gear(self) -> '_2272.ConicalGear':
        """ConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2272.ConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_cylindrical_gear(self) -> '_2274.CylindricalGear':
        """CylindricalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2274.CylindricalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CylindricalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_cylindrical_planet_gear(self) -> '_2276.CylindricalPlanetGear':
        """CylindricalPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2276.CylindricalPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CylindricalPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_face_gear(self) -> '_2277.FaceGear':
        """FaceGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2277.FaceGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to FaceGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_gear(self) -> '_2279.Gear':
        """Gear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2279.Gear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Gear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_hypoid_gear(self) -> '_2283.HypoidGear':
        """HypoidGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2283.HypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to HypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2285.KlingelnbergCycloPalloidConicalGear':
        """KlingelnbergCycloPalloidConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2285.KlingelnbergCycloPalloidConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2287.KlingelnbergCycloPalloidHypoidGear':
        """KlingelnbergCycloPalloidHypoidGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2287.KlingelnbergCycloPalloidHypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2289.KlingelnbergCycloPalloidSpiralBevelGear':
        """KlingelnbergCycloPalloidSpiralBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2289.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_spiral_bevel_gear(self) -> '_2292.SpiralBevelGear':
        """SpiralBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2292.SpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_straight_bevel_diff_gear(self) -> '_2294.StraightBevelDiffGear':
        """StraightBevelDiffGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2294.StraightBevelDiffGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelDiffGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_straight_bevel_gear(self) -> '_2296.StraightBevelGear':
        """StraightBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2296.StraightBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_straight_bevel_planet_gear(self) -> '_2298.StraightBevelPlanetGear':
        """StraightBevelPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2298.StraightBevelPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_straight_bevel_sun_gear(self) -> '_2299.StraightBevelSunGear':
        """StraightBevelSunGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2299.StraightBevelSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_worm_gear(self) -> '_2300.WormGear':
        """WormGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2300.WormGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to WormGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_zerol_bevel_gear(self) -> '_2302.ZerolBevelGear':
        """ZerolBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2302.ZerolBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ZerolBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_cycloidal_disc(self) -> '_2318.CycloidalDisc':
        """CycloidalDisc: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2318.CycloidalDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CycloidalDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_ring_pins(self) -> '_2319.RingPins':
        """RingPins: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2319.RingPins.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to RingPins. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_clutch_half(self) -> '_2328.ClutchHalf':
        """ClutchHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2328.ClutchHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ClutchHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_concept_coupling_half(self) -> '_2331.ConceptCouplingHalf':
        """ConceptCouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2331.ConceptCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConceptCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_coupling_half(self) -> '_2333.CouplingHalf':
        """CouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2333.CouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_cvt_pulley(self) -> '_2336.CVTPulley':
        """CVTPulley: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2336.CVTPulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CVTPulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_part_to_part_shear_coupling_half(self) -> '_2338.PartToPartShearCouplingHalf':
        """PartToPartShearCouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2338.PartToPartShearCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PartToPartShearCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_pulley(self) -> '_2339.Pulley':
        """Pulley: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2339.Pulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Pulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_rolling_ring(self) -> '_2345.RollingRing':
        """RollingRing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2345.RollingRing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to RollingRing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_shaft_hub_connection(self) -> '_2347.ShaftHubConnection':
        """ShaftHubConnection: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2347.ShaftHubConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ShaftHubConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_spring_damper_half(self) -> '_2350.SpringDamperHalf':
        """SpringDamperHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2350.SpringDamperHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SpringDamperHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_synchroniser_half(self) -> '_2353.SynchroniserHalf':
        """SynchroniserHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2353.SynchroniserHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_synchroniser_part(self) -> '_2354.SynchroniserPart':
        """SynchroniserPart: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2354.SynchroniserPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_synchroniser_sleeve(self) -> '_2355.SynchroniserSleeve':
        """SynchroniserSleeve: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2355.SynchroniserSleeve.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserSleeve. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_torque_converter_pump(self) -> '_2357.TorqueConverterPump':
        """TorqueConverterPump: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2357.TorqueConverterPump.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to TorqueConverterPump. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_a_of_type_torque_converter_turbine(self) -> '_2359.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerA

        if temp is None:
            return None

        if _2359.TorqueConverterTurbine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_a to TorqueConverterTurbine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b(self) -> '_2195.Component':
        """Component: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2195.Component.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Component. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_abstract_shaft(self) -> '_2187.AbstractShaft':
        """AbstractShaft: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2187.AbstractShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AbstractShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_abstract_shaft_or_housing(self) -> '_2188.AbstractShaftOrHousing':
        """AbstractShaftOrHousing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2188.AbstractShaftOrHousing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AbstractShaftOrHousing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_bearing(self) -> '_2191.Bearing':
        """Bearing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2191.Bearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Bearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_bolt(self) -> '_2193.Bolt':
        """Bolt: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2193.Bolt.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Bolt. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_connector(self) -> '_2198.Connector':
        """Connector: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2198.Connector.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Connector. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_datum(self) -> '_2199.Datum':
        """Datum: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2199.Datum.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Datum. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_external_cad_model(self) -> '_2202.ExternalCADModel':
        """ExternalCADModel: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2202.ExternalCADModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ExternalCADModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_fe_part(self) -> '_2203.FEPart':
        """FEPart: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2203.FEPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to FEPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_guide_dxf_model(self) -> '_2205.GuideDxfModel':
        """GuideDxfModel: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2205.GuideDxfModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to GuideDxfModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_mass_disc(self) -> '_2212.MassDisc':
        """MassDisc: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2212.MassDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MassDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_measurement_component(self) -> '_2213.MeasurementComponent':
        """MeasurementComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2213.MeasurementComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MeasurementComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_mountable_component(self) -> '_2214.MountableComponent':
        """MountableComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2214.MountableComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MountableComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_oil_seal(self) -> '_2216.OilSeal':
        """OilSeal: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2216.OilSeal.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to OilSeal. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_planet_carrier(self) -> '_2219.PlanetCarrier':
        """PlanetCarrier: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2219.PlanetCarrier.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PlanetCarrier. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_point_load(self) -> '_2221.PointLoad':
        """PointLoad: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2221.PointLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PointLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_power_load(self) -> '_2222.PowerLoad':
        """PowerLoad: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2222.PowerLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PowerLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_unbalanced_mass(self) -> '_2227.UnbalancedMass':
        """UnbalancedMass: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2227.UnbalancedMass.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to UnbalancedMass. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_virtual_component(self) -> '_2229.VirtualComponent':
        """VirtualComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2229.VirtualComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to VirtualComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_shaft(self) -> '_2232.Shaft':
        """Shaft: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2232.Shaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Shaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_agma_gleason_conical_gear(self) -> '_2262.AGMAGleasonConicalGear':
        """AGMAGleasonConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2262.AGMAGleasonConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AGMAGleasonConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_bevel_differential_gear(self) -> '_2264.BevelDifferentialGear':
        """BevelDifferentialGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2264.BevelDifferentialGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_bevel_differential_planet_gear(self) -> '_2266.BevelDifferentialPlanetGear':
        """BevelDifferentialPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2266.BevelDifferentialPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_bevel_differential_sun_gear(self) -> '_2267.BevelDifferentialSunGear':
        """BevelDifferentialSunGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2267.BevelDifferentialSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_bevel_gear(self) -> '_2268.BevelGear':
        """BevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2268.BevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_concept_gear(self) -> '_2270.ConceptGear':
        """ConceptGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2270.ConceptGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConceptGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_conical_gear(self) -> '_2272.ConicalGear':
        """ConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2272.ConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_cylindrical_gear(self) -> '_2274.CylindricalGear':
        """CylindricalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2274.CylindricalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CylindricalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_cylindrical_planet_gear(self) -> '_2276.CylindricalPlanetGear':
        """CylindricalPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2276.CylindricalPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CylindricalPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_face_gear(self) -> '_2277.FaceGear':
        """FaceGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2277.FaceGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to FaceGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_gear(self) -> '_2279.Gear':
        """Gear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2279.Gear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Gear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_hypoid_gear(self) -> '_2283.HypoidGear':
        """HypoidGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2283.HypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to HypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2285.KlingelnbergCycloPalloidConicalGear':
        """KlingelnbergCycloPalloidConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2285.KlingelnbergCycloPalloidConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2287.KlingelnbergCycloPalloidHypoidGear':
        """KlingelnbergCycloPalloidHypoidGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2287.KlingelnbergCycloPalloidHypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2289.KlingelnbergCycloPalloidSpiralBevelGear':
        """KlingelnbergCycloPalloidSpiralBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2289.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_spiral_bevel_gear(self) -> '_2292.SpiralBevelGear':
        """SpiralBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2292.SpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_straight_bevel_diff_gear(self) -> '_2294.StraightBevelDiffGear':
        """StraightBevelDiffGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2294.StraightBevelDiffGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelDiffGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_straight_bevel_gear(self) -> '_2296.StraightBevelGear':
        """StraightBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2296.StraightBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_straight_bevel_planet_gear(self) -> '_2298.StraightBevelPlanetGear':
        """StraightBevelPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2298.StraightBevelPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_straight_bevel_sun_gear(self) -> '_2299.StraightBevelSunGear':
        """StraightBevelSunGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2299.StraightBevelSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_worm_gear(self) -> '_2300.WormGear':
        """WormGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2300.WormGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to WormGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_zerol_bevel_gear(self) -> '_2302.ZerolBevelGear':
        """ZerolBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2302.ZerolBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ZerolBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_cycloidal_disc(self) -> '_2318.CycloidalDisc':
        """CycloidalDisc: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2318.CycloidalDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CycloidalDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_ring_pins(self) -> '_2319.RingPins':
        """RingPins: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2319.RingPins.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to RingPins. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_clutch_half(self) -> '_2328.ClutchHalf':
        """ClutchHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2328.ClutchHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ClutchHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_concept_coupling_half(self) -> '_2331.ConceptCouplingHalf':
        """ConceptCouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2331.ConceptCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConceptCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_coupling_half(self) -> '_2333.CouplingHalf':
        """CouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2333.CouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_cvt_pulley(self) -> '_2336.CVTPulley':
        """CVTPulley: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2336.CVTPulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CVTPulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_part_to_part_shear_coupling_half(self) -> '_2338.PartToPartShearCouplingHalf':
        """PartToPartShearCouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2338.PartToPartShearCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PartToPartShearCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_pulley(self) -> '_2339.Pulley':
        """Pulley: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2339.Pulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Pulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_rolling_ring(self) -> '_2345.RollingRing':
        """RollingRing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2345.RollingRing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to RollingRing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_shaft_hub_connection(self) -> '_2347.ShaftHubConnection':
        """ShaftHubConnection: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2347.ShaftHubConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ShaftHubConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_spring_damper_half(self) -> '_2350.SpringDamperHalf':
        """SpringDamperHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2350.SpringDamperHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SpringDamperHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_synchroniser_half(self) -> '_2353.SynchroniserHalf':
        """SynchroniserHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2353.SynchroniserHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_synchroniser_part(self) -> '_2354.SynchroniserPart':
        """SynchroniserPart: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2354.SynchroniserPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_synchroniser_sleeve(self) -> '_2355.SynchroniserSleeve':
        """SynchroniserSleeve: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2355.SynchroniserSleeve.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserSleeve. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_torque_converter_pump(self) -> '_2357.TorqueConverterPump':
        """TorqueConverterPump: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2357.TorqueConverterPump.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to TorqueConverterPump. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def owner_b_of_type_torque_converter_turbine(self) -> '_2359.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OwnerB

        if temp is None:
            return None

        if _2359.TorqueConverterTurbine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast owner_b to TorqueConverterTurbine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a(self) -> '_2047.Socket':
        """Socket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2047.Socket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to Socket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_bearing_inner_socket(self) -> '_2017.BearingInnerSocket':
        """BearingInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2017.BearingInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BearingInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_bearing_outer_socket(self) -> '_2018.BearingOuterSocket':
        """BearingOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2018.BearingOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BearingOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cvt_pulley_socket(self) -> '_2025.CVTPulleySocket':
        """CVTPulleySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2025.CVTPulleySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CVTPulleySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cylindrical_socket(self) -> '_2027.CylindricalSocket':
        """CylindricalSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2027.CylindricalSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CylindricalSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_electric_machine_stator_socket(self) -> '_2029.ElectricMachineStatorSocket':
        """ElectricMachineStatorSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2029.ElectricMachineStatorSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ElectricMachineStatorSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_inner_shaft_socket(self) -> '_2030.InnerShaftSocket':
        """InnerShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2030.InnerShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to InnerShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_inner_shaft_socket_base(self) -> '_2031.InnerShaftSocketBase':
        """InnerShaftSocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2031.InnerShaftSocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to InnerShaftSocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_mountable_component_inner_socket(self) -> '_2033.MountableComponentInnerSocket':
        """MountableComponentInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2033.MountableComponentInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_mountable_component_outer_socket(self) -> '_2034.MountableComponentOuterSocket':
        """MountableComponentOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2034.MountableComponentOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_mountable_component_socket(self) -> '_2035.MountableComponentSocket':
        """MountableComponentSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2035.MountableComponentSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_outer_shaft_socket(self) -> '_2036.OuterShaftSocket':
        """OuterShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2036.OuterShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to OuterShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_outer_shaft_socket_base(self) -> '_2037.OuterShaftSocketBase':
        """OuterShaftSocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2037.OuterShaftSocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to OuterShaftSocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_planetary_socket(self) -> '_2039.PlanetarySocket':
        """PlanetarySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2039.PlanetarySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PlanetarySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_planetary_socket_base(self) -> '_2040.PlanetarySocketBase':
        """PlanetarySocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2040.PlanetarySocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PlanetarySocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_pulley_socket(self) -> '_2041.PulleySocket':
        """PulleySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2041.PulleySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PulleySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_rolling_ring_socket(self) -> '_2044.RollingRingSocket':
        """RollingRingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2044.RollingRingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to RollingRingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_shaft_socket(self) -> '_2045.ShaftSocket':
        """ShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2045.ShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_agma_gleason_conical_gear_teeth_socket(self) -> '_2051.AGMAGleasonConicalGearTeethSocket':
        """AGMAGleasonConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2051.AGMAGleasonConicalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to AGMAGleasonConicalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_bevel_differential_gear_teeth_socket(self) -> '_2053.BevelDifferentialGearTeethSocket':
        """BevelDifferentialGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2053.BevelDifferentialGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BevelDifferentialGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_bevel_gear_teeth_socket(self) -> '_2055.BevelGearTeethSocket':
        """BevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2055.BevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_concept_gear_teeth_socket(self) -> '_2057.ConceptGearTeethSocket':
        """ConceptGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2057.ConceptGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConceptGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_conical_gear_teeth_socket(self) -> '_2059.ConicalGearTeethSocket':
        """ConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2059.ConicalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConicalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cylindrical_gear_teeth_socket(self) -> '_2061.CylindricalGearTeethSocket':
        """CylindricalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2061.CylindricalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CylindricalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_face_gear_teeth_socket(self) -> '_2063.FaceGearTeethSocket':
        """FaceGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2063.FaceGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to FaceGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_gear_teeth_socket(self) -> '_2065.GearTeethSocket':
        """GearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2065.GearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to GearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_hypoid_gear_teeth_socket(self) -> '_2067.HypoidGearTeethSocket':
        """HypoidGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2067.HypoidGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to HypoidGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_klingelnberg_conical_gear_teeth_socket(self) -> '_2068.KlingelnbergConicalGearTeethSocket':
        """KlingelnbergConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2068.KlingelnbergConicalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergConicalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_klingelnberg_hypoid_gear_teeth_socket(self) -> '_2072.KlingelnbergHypoidGearTeethSocket':
        """KlingelnbergHypoidGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2072.KlingelnbergHypoidGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergHypoidGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_klingelnberg_spiral_bevel_gear_teeth_socket(self) -> '_2073.KlingelnbergSpiralBevelGearTeethSocket':
        """KlingelnbergSpiralBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2073.KlingelnbergSpiralBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergSpiralBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_spiral_bevel_gear_teeth_socket(self) -> '_2075.SpiralBevelGearTeethSocket':
        """SpiralBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2075.SpiralBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to SpiralBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_straight_bevel_diff_gear_teeth_socket(self) -> '_2077.StraightBevelDiffGearTeethSocket':
        """StraightBevelDiffGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2077.StraightBevelDiffGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to StraightBevelDiffGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_straight_bevel_gear_teeth_socket(self) -> '_2079.StraightBevelGearTeethSocket':
        """StraightBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2079.StraightBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to StraightBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_worm_gear_teeth_socket(self) -> '_2081.WormGearTeethSocket':
        """WormGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2081.WormGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to WormGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_zerol_bevel_gear_teeth_socket(self) -> '_2083.ZerolBevelGearTeethSocket':
        """ZerolBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2083.ZerolBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ZerolBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_axial_left_socket(self) -> '_2084.CycloidalDiscAxialLeftSocket':
        """CycloidalDiscAxialLeftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2084.CycloidalDiscAxialLeftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_axial_right_socket(self) -> '_2085.CycloidalDiscAxialRightSocket':
        """CycloidalDiscAxialRightSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2085.CycloidalDiscAxialRightSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscAxialRightSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_inner_socket(self) -> '_2087.CycloidalDiscInnerSocket':
        """CycloidalDiscInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2087.CycloidalDiscInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_outer_socket(self) -> '_2088.CycloidalDiscOuterSocket':
        """CycloidalDiscOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2088.CycloidalDiscOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2090.CycloidalDiscPlanetaryBearingSocket':
        """CycloidalDiscPlanetaryBearingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2090.CycloidalDiscPlanetaryBearingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_ring_pins_socket(self) -> '_2091.RingPinsSocket':
        """RingPinsSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2091.RingPinsSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to RingPinsSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_clutch_socket(self) -> '_2094.ClutchSocket':
        """ClutchSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2094.ClutchSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ClutchSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_concept_coupling_socket(self) -> '_2096.ConceptCouplingSocket':
        """ConceptCouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2096.ConceptCouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConceptCouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_coupling_socket(self) -> '_2098.CouplingSocket':
        """CouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2098.CouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_part_to_part_shear_coupling_socket(self) -> '_2100.PartToPartShearCouplingSocket':
        """PartToPartShearCouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2100.PartToPartShearCouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PartToPartShearCouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_spring_damper_socket(self) -> '_2102.SpringDamperSocket':
        """SpringDamperSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2102.SpringDamperSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to SpringDamperSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_torque_converter_pump_socket(self) -> '_2104.TorqueConverterPumpSocket':
        """TorqueConverterPumpSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2104.TorqueConverterPumpSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to TorqueConverterPumpSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_a_of_type_torque_converter_turbine_socket(self) -> '_2105.TorqueConverterTurbineSocket':
        """TorqueConverterTurbineSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketA

        if temp is None:
            return None

        if _2105.TorqueConverterTurbineSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_a to TorqueConverterTurbineSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b(self) -> '_2047.Socket':
        """Socket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2047.Socket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to Socket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_bearing_inner_socket(self) -> '_2017.BearingInnerSocket':
        """BearingInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2017.BearingInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BearingInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_bearing_outer_socket(self) -> '_2018.BearingOuterSocket':
        """BearingOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2018.BearingOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BearingOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cvt_pulley_socket(self) -> '_2025.CVTPulleySocket':
        """CVTPulleySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2025.CVTPulleySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CVTPulleySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cylindrical_socket(self) -> '_2027.CylindricalSocket':
        """CylindricalSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2027.CylindricalSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CylindricalSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_electric_machine_stator_socket(self) -> '_2029.ElectricMachineStatorSocket':
        """ElectricMachineStatorSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2029.ElectricMachineStatorSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ElectricMachineStatorSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_inner_shaft_socket(self) -> '_2030.InnerShaftSocket':
        """InnerShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2030.InnerShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to InnerShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_inner_shaft_socket_base(self) -> '_2031.InnerShaftSocketBase':
        """InnerShaftSocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2031.InnerShaftSocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to InnerShaftSocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_mountable_component_inner_socket(self) -> '_2033.MountableComponentInnerSocket':
        """MountableComponentInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2033.MountableComponentInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_mountable_component_outer_socket(self) -> '_2034.MountableComponentOuterSocket':
        """MountableComponentOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2034.MountableComponentOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_mountable_component_socket(self) -> '_2035.MountableComponentSocket':
        """MountableComponentSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2035.MountableComponentSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_outer_shaft_socket(self) -> '_2036.OuterShaftSocket':
        """OuterShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2036.OuterShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to OuterShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_outer_shaft_socket_base(self) -> '_2037.OuterShaftSocketBase':
        """OuterShaftSocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2037.OuterShaftSocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to OuterShaftSocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_planetary_socket(self) -> '_2039.PlanetarySocket':
        """PlanetarySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2039.PlanetarySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PlanetarySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_planetary_socket_base(self) -> '_2040.PlanetarySocketBase':
        """PlanetarySocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2040.PlanetarySocketBase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PlanetarySocketBase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_pulley_socket(self) -> '_2041.PulleySocket':
        """PulleySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2041.PulleySocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PulleySocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_rolling_ring_socket(self) -> '_2044.RollingRingSocket':
        """RollingRingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2044.RollingRingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to RollingRingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_shaft_socket(self) -> '_2045.ShaftSocket':
        """ShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2045.ShaftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ShaftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_agma_gleason_conical_gear_teeth_socket(self) -> '_2051.AGMAGleasonConicalGearTeethSocket':
        """AGMAGleasonConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2051.AGMAGleasonConicalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to AGMAGleasonConicalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_bevel_differential_gear_teeth_socket(self) -> '_2053.BevelDifferentialGearTeethSocket':
        """BevelDifferentialGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2053.BevelDifferentialGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BevelDifferentialGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_bevel_gear_teeth_socket(self) -> '_2055.BevelGearTeethSocket':
        """BevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2055.BevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_concept_gear_teeth_socket(self) -> '_2057.ConceptGearTeethSocket':
        """ConceptGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2057.ConceptGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConceptGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_conical_gear_teeth_socket(self) -> '_2059.ConicalGearTeethSocket':
        """ConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2059.ConicalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConicalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cylindrical_gear_teeth_socket(self) -> '_2061.CylindricalGearTeethSocket':
        """CylindricalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2061.CylindricalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CylindricalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_face_gear_teeth_socket(self) -> '_2063.FaceGearTeethSocket':
        """FaceGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2063.FaceGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to FaceGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_gear_teeth_socket(self) -> '_2065.GearTeethSocket':
        """GearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2065.GearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to GearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_hypoid_gear_teeth_socket(self) -> '_2067.HypoidGearTeethSocket':
        """HypoidGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2067.HypoidGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to HypoidGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_klingelnberg_conical_gear_teeth_socket(self) -> '_2068.KlingelnbergConicalGearTeethSocket':
        """KlingelnbergConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2068.KlingelnbergConicalGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergConicalGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_klingelnberg_hypoid_gear_teeth_socket(self) -> '_2072.KlingelnbergHypoidGearTeethSocket':
        """KlingelnbergHypoidGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2072.KlingelnbergHypoidGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergHypoidGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_klingelnberg_spiral_bevel_gear_teeth_socket(self) -> '_2073.KlingelnbergSpiralBevelGearTeethSocket':
        """KlingelnbergSpiralBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2073.KlingelnbergSpiralBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergSpiralBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_spiral_bevel_gear_teeth_socket(self) -> '_2075.SpiralBevelGearTeethSocket':
        """SpiralBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2075.SpiralBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to SpiralBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_straight_bevel_diff_gear_teeth_socket(self) -> '_2077.StraightBevelDiffGearTeethSocket':
        """StraightBevelDiffGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2077.StraightBevelDiffGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to StraightBevelDiffGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_straight_bevel_gear_teeth_socket(self) -> '_2079.StraightBevelGearTeethSocket':
        """StraightBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2079.StraightBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to StraightBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_worm_gear_teeth_socket(self) -> '_2081.WormGearTeethSocket':
        """WormGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2081.WormGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to WormGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_zerol_bevel_gear_teeth_socket(self) -> '_2083.ZerolBevelGearTeethSocket':
        """ZerolBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2083.ZerolBevelGearTeethSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ZerolBevelGearTeethSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_axial_left_socket(self) -> '_2084.CycloidalDiscAxialLeftSocket':
        """CycloidalDiscAxialLeftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2084.CycloidalDiscAxialLeftSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_axial_right_socket(self) -> '_2085.CycloidalDiscAxialRightSocket':
        """CycloidalDiscAxialRightSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2085.CycloidalDiscAxialRightSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscAxialRightSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_inner_socket(self) -> '_2087.CycloidalDiscInnerSocket':
        """CycloidalDiscInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2087.CycloidalDiscInnerSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscInnerSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_outer_socket(self) -> '_2088.CycloidalDiscOuterSocket':
        """CycloidalDiscOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2088.CycloidalDiscOuterSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscOuterSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2090.CycloidalDiscPlanetaryBearingSocket':
        """CycloidalDiscPlanetaryBearingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2090.CycloidalDiscPlanetaryBearingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_ring_pins_socket(self) -> '_2091.RingPinsSocket':
        """RingPinsSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2091.RingPinsSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to RingPinsSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_clutch_socket(self) -> '_2094.ClutchSocket':
        """ClutchSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2094.ClutchSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ClutchSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_concept_coupling_socket(self) -> '_2096.ConceptCouplingSocket':
        """ConceptCouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2096.ConceptCouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConceptCouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_coupling_socket(self) -> '_2098.CouplingSocket':
        """CouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2098.CouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_part_to_part_shear_coupling_socket(self) -> '_2100.PartToPartShearCouplingSocket':
        """PartToPartShearCouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2100.PartToPartShearCouplingSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PartToPartShearCouplingSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_spring_damper_socket(self) -> '_2102.SpringDamperSocket':
        """SpringDamperSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2102.SpringDamperSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to SpringDamperSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_torque_converter_pump_socket(self) -> '_2104.TorqueConverterPumpSocket':
        """TorqueConverterPumpSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2104.TorqueConverterPumpSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to TorqueConverterPumpSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def socket_b_of_type_torque_converter_turbine_socket(self) -> '_2105.TorqueConverterTurbineSocket':
        """TorqueConverterTurbineSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SocketB

        if temp is None:
            return None

        if _2105.TorqueConverterTurbineSocket.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast socket_b to TorqueConverterTurbineSocket. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def other_owner(self, component: '_2195.Component') -> '_2195.Component':
        """ 'OtherOwner' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.Component
        """

        method_result = self.wrapped.OtherOwner(component.wrapped if component else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def other_socket_for_component(self, component: '_2195.Component') -> '_2047.Socket':
        """ 'OtherSocket' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        """

        method_result = self.wrapped.OtherSocket.Overloads[_COMPONENT](component.wrapped if component else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def other_socket(self, socket: '_2047.Socket') -> '_2047.Socket':
        """ 'OtherSocket' is the original name of this method.

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        """

        method_result = self.wrapped.OtherSocket.Overloads[_SOCKET](socket.wrapped if socket else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def socket_for(self, component: '_2195.Component') -> '_2047.Socket':
        """ 'SocketFor' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        """

        method_result = self.wrapped.SocketFor(component.wrapped if component else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
