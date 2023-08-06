"""_2021.py

ComponentConnection
"""


from PIL.Image import Image

from mastapy._internal import constructor, conversion
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
from mastapy.system_model.connections_and_sockets import _2022
from mastapy._internal.python_net import python_net_import

_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ComponentConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentConnection',)


class ComponentConnection(_2022.ComponentMeasurer):
    """ComponentConnection

    This is a mastapy class.
    """

    TYPE = _COMPONENT_CONNECTION

    def __init__(self, instance_to_wrap: 'ComponentConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_view(self) -> 'Image':
        """Image: 'AssemblyView' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyView

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def connected_components_socket(self) -> 'str':
        """str: 'ConnectedComponentsSocket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponentsSocket

        if temp is None:
            return None

        return temp

    @property
    def detail_view(self) -> 'Image':
        """Image: 'DetailView' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DetailView

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def socket(self) -> 'str':
        """str: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Socket

        if temp is None:
            return None

        return temp

    @property
    def connected_component(self) -> '_2195.Component':
        """Component: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2195.Component.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Component. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_abstract_shaft(self) -> '_2187.AbstractShaft':
        """AbstractShaft: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2187.AbstractShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to AbstractShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_abstract_shaft_or_housing(self) -> '_2188.AbstractShaftOrHousing':
        """AbstractShaftOrHousing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2188.AbstractShaftOrHousing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to AbstractShaftOrHousing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_bearing(self) -> '_2191.Bearing':
        """Bearing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2191.Bearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Bearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_bolt(self) -> '_2193.Bolt':
        """Bolt: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2193.Bolt.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Bolt. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_connector(self) -> '_2198.Connector':
        """Connector: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2198.Connector.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Connector. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_datum(self) -> '_2199.Datum':
        """Datum: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2199.Datum.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Datum. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_external_cad_model(self) -> '_2202.ExternalCADModel':
        """ExternalCADModel: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2202.ExternalCADModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ExternalCADModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_fe_part(self) -> '_2203.FEPart':
        """FEPart: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2203.FEPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to FEPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_guide_dxf_model(self) -> '_2205.GuideDxfModel':
        """GuideDxfModel: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2205.GuideDxfModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to GuideDxfModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_mass_disc(self) -> '_2212.MassDisc':
        """MassDisc: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2212.MassDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MassDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_measurement_component(self) -> '_2213.MeasurementComponent':
        """MeasurementComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2213.MeasurementComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MeasurementComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_mountable_component(self) -> '_2214.MountableComponent':
        """MountableComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2214.MountableComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MountableComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_oil_seal(self) -> '_2216.OilSeal':
        """OilSeal: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2216.OilSeal.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to OilSeal. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_planet_carrier(self) -> '_2219.PlanetCarrier':
        """PlanetCarrier: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2219.PlanetCarrier.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PlanetCarrier. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_point_load(self) -> '_2221.PointLoad':
        """PointLoad: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2221.PointLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PointLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_power_load(self) -> '_2222.PowerLoad':
        """PowerLoad: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2222.PowerLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PowerLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_unbalanced_mass(self) -> '_2227.UnbalancedMass':
        """UnbalancedMass: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2227.UnbalancedMass.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to UnbalancedMass. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_virtual_component(self) -> '_2229.VirtualComponent':
        """VirtualComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2229.VirtualComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to VirtualComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_shaft(self) -> '_2232.Shaft':
        """Shaft: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2232.Shaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Shaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_agma_gleason_conical_gear(self) -> '_2262.AGMAGleasonConicalGear':
        """AGMAGleasonConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2262.AGMAGleasonConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to AGMAGleasonConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_bevel_differential_gear(self) -> '_2264.BevelDifferentialGear':
        """BevelDifferentialGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2264.BevelDifferentialGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_bevel_differential_planet_gear(self) -> '_2266.BevelDifferentialPlanetGear':
        """BevelDifferentialPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2266.BevelDifferentialPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_bevel_differential_sun_gear(self) -> '_2267.BevelDifferentialSunGear':
        """BevelDifferentialSunGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2267.BevelDifferentialSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_bevel_gear(self) -> '_2268.BevelGear':
        """BevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2268.BevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_concept_gear(self) -> '_2270.ConceptGear':
        """ConceptGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2270.ConceptGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConceptGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_conical_gear(self) -> '_2272.ConicalGear':
        """ConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2272.ConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_cylindrical_gear(self) -> '_2274.CylindricalGear':
        """CylindricalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2274.CylindricalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CylindricalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_cylindrical_planet_gear(self) -> '_2276.CylindricalPlanetGear':
        """CylindricalPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2276.CylindricalPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CylindricalPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_face_gear(self) -> '_2277.FaceGear':
        """FaceGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2277.FaceGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to FaceGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_gear(self) -> '_2279.Gear':
        """Gear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2279.Gear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Gear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_hypoid_gear(self) -> '_2283.HypoidGear':
        """HypoidGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2283.HypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to HypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2285.KlingelnbergCycloPalloidConicalGear':
        """KlingelnbergCycloPalloidConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2285.KlingelnbergCycloPalloidConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2287.KlingelnbergCycloPalloidHypoidGear':
        """KlingelnbergCycloPalloidHypoidGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2287.KlingelnbergCycloPalloidHypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2289.KlingelnbergCycloPalloidSpiralBevelGear':
        """KlingelnbergCycloPalloidSpiralBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2289.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_spiral_bevel_gear(self) -> '_2292.SpiralBevelGear':
        """SpiralBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2292.SpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_straight_bevel_diff_gear(self) -> '_2294.StraightBevelDiffGear':
        """StraightBevelDiffGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2294.StraightBevelDiffGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelDiffGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_straight_bevel_gear(self) -> '_2296.StraightBevelGear':
        """StraightBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2296.StraightBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_straight_bevel_planet_gear(self) -> '_2298.StraightBevelPlanetGear':
        """StraightBevelPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2298.StraightBevelPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_straight_bevel_sun_gear(self) -> '_2299.StraightBevelSunGear':
        """StraightBevelSunGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2299.StraightBevelSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_worm_gear(self) -> '_2300.WormGear':
        """WormGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2300.WormGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to WormGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_zerol_bevel_gear(self) -> '_2302.ZerolBevelGear':
        """ZerolBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2302.ZerolBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ZerolBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_cycloidal_disc(self) -> '_2318.CycloidalDisc':
        """CycloidalDisc: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2318.CycloidalDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CycloidalDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_ring_pins(self) -> '_2319.RingPins':
        """RingPins: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2319.RingPins.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to RingPins. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_clutch_half(self) -> '_2328.ClutchHalf':
        """ClutchHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2328.ClutchHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ClutchHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_concept_coupling_half(self) -> '_2331.ConceptCouplingHalf':
        """ConceptCouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2331.ConceptCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConceptCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_coupling_half(self) -> '_2333.CouplingHalf':
        """CouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2333.CouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_cvt_pulley(self) -> '_2336.CVTPulley':
        """CVTPulley: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2336.CVTPulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CVTPulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_part_to_part_shear_coupling_half(self) -> '_2338.PartToPartShearCouplingHalf':
        """PartToPartShearCouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2338.PartToPartShearCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PartToPartShearCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_pulley(self) -> '_2339.Pulley':
        """Pulley: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2339.Pulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Pulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_rolling_ring(self) -> '_2345.RollingRing':
        """RollingRing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2345.RollingRing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to RollingRing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_shaft_hub_connection(self) -> '_2347.ShaftHubConnection':
        """ShaftHubConnection: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2347.ShaftHubConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ShaftHubConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_spring_damper_half(self) -> '_2350.SpringDamperHalf':
        """SpringDamperHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2350.SpringDamperHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SpringDamperHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_synchroniser_half(self) -> '_2353.SynchroniserHalf':
        """SynchroniserHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2353.SynchroniserHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_synchroniser_part(self) -> '_2354.SynchroniserPart':
        """SynchroniserPart: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2354.SynchroniserPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_synchroniser_sleeve(self) -> '_2355.SynchroniserSleeve':
        """SynchroniserSleeve: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2355.SynchroniserSleeve.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserSleeve. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_torque_converter_pump(self) -> '_2357.TorqueConverterPump':
        """TorqueConverterPump: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2357.TorqueConverterPump.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to TorqueConverterPump. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connected_component_of_type_torque_converter_turbine(self) -> '_2359.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectedComponent

        if temp is None:
            return None

        if _2359.TorqueConverterTurbine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast connected_component to TorqueConverterTurbine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def delete(self):
        """ 'Delete' is the original name of this method."""

        self.wrapped.Delete()

    def swap(self):
        """ 'Swap' is the original name of this method."""

        self.wrapped.Swap()
