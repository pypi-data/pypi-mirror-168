"""_6527.py

LoadCase
"""


from typing import List

from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.bearing_results.rolling import _1729, _1734, _1828
from mastapy.system_model import _1965, _1968, _1978
from mastapy.gears import _309
from mastapy.bearings.bearing_results.rolling.iso_rating_results import _1868
from mastapy.system_model.analyses_and_results.static_loads import (
    _6534, _6666, _6706, _6700,
    _6531, _6530, _6532, _6543,
    _6555, _6554, _6560, _6573,
    _6592, _6607, _6611, _6612,
    _6542, _6620, _6647, _6648,
    _6651, _6653, _6655, _6662,
    _6665, _6675, _6679, _6708,
    _6709, _6677, _6564, _6566,
    _6608, _6610, _6537, _6539,
    _6546, _6548, _6549, _6550,
    _6551, _6553, _6567, _6571,
    _6584, _6588, _6589, _6614,
    _6619, _6631, _6633, _6638,
    _6640, _6641, _6643, _6644,
    _6646, _6660, _6681, _6683,
    _6687, _6689, _6690, _6692,
    _6693, _6694, _6710, _6712,
    _6713, _6715, _6580, _6582,
    _6670, _6658, _6657, _6545,
    _6558, _6557, _6563, _6562,
    _6576, _6575, _6578, _6579,
    _6667, _6676, _6674, _6672,
    _6686, _6685, _6696, _6695,
    _6697, _6698, _6701, _6702,
    _6703, _6678, _6577, _6544,
    _6559, _6572, _6637, _6659,
    _6673, _6533, _6547, _6565,
    _6609, _6688, _6552, _6569,
    _6538, _6586, _6632, _6639,
    _6642, _6645, _6682, _6691,
    _6711, _6714, _6616, _6581,
    _6583, _6671, _6656, _6556,
    _6561, _6574, _6684
)
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4129
from mastapy.system_model.connections_and_sockets.couplings import (
    _2103, _2099, _2093, _2095,
    _2097, _2101
)
from mastapy.system_model.part_model import (
    _2187, _2186, _2188, _2191,
    _2193, _2194, _2195, _2198,
    _2199, _2202, _2203, _2204,
    _2185, _2205, _2212, _2213,
    _2214, _2216, _2218, _2219,
    _2221, _2222, _2224, _2226,
    _2227, _2229
)
from mastapy.system_model.part_model.shaft_model import _2232
from mastapy.system_model.part_model.gears import (
    _2270, _2271, _2277, _2278,
    _2262, _2263, _2264, _2265,
    _2266, _2267, _2268, _2269,
    _2272, _2273, _2274, _2275,
    _2276, _2279, _2281, _2283,
    _2284, _2285, _2286, _2287,
    _2288, _2289, _2290, _2291,
    _2292, _2293, _2294, _2295,
    _2296, _2297, _2298, _2299,
    _2300, _2301, _2302, _2303
)
from mastapy.system_model.part_model.cycloidal import _2317, _2318, _2319
from mastapy.system_model.part_model.couplings import (
    _2337, _2338, _2325, _2327,
    _2328, _2330, _2331, _2332,
    _2333, _2335, _2336, _2339,
    _2347, _2345, _2346, _2349,
    _2350, _2351, _2353, _2354,
    _2355, _2356, _2357, _2359
)
from mastapy.system_model.connections_and_sockets import (
    _2046, _2024, _2019, _2020,
    _2023, _2032, _2038, _2043,
    _2016
)
from mastapy.system_model.connections_and_sockets.gears import (
    _2052, _2056, _2062, _2076,
    _2054, _2058, _2050, _2060,
    _2066, _2069, _2070, _2071,
    _2074, _2078, _2080, _2082,
    _2064
)
from mastapy.system_model.connections_and_sockets.cycloidal import _2086, _2089, _2092
from mastapy._internal.python_net import python_net_import
from mastapy.system_model.analyses_and_results import _2399

_TORQUE_CONVERTER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'TorqueConverterConnection')
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'PartToPartShearCouplingConnection')
_CLUTCH_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ClutchConnection')
_CONCEPT_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ConceptCouplingConnection')
_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'CouplingConnection')
_SPRING_DAMPER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'SpringDamperConnection')
_ABSTRACT_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaft')
_ABSTRACT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractAssembly')
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaftOrHousing')
_BEARING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bearing')
_BOLT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bolt')
_BOLTED_JOINT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'BoltedJoint')
_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')
_DATUM = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Datum')
_EXTERNAL_CAD_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'ExternalCADModel')
_FE_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FEPart')
_FLEXIBLE_PIN_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FlexiblePinAssembly')
_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Assembly')
_GUIDE_DXF_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'GuideDxfModel')
_MASS_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MassDisc')
_MEASUREMENT_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MeasurementComponent')
_MOUNTABLE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MountableComponent')
_OIL_SEAL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'OilSeal')
_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Part')
_PLANET_CARRIER = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PlanetCarrier')
_POINT_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PointLoad')
_POWER_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PowerLoad')
_ROOT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'RootAssembly')
_SPECIALISED_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'SpecialisedAssembly')
_UNBALANCED_MASS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'UnbalancedMass')
_VIRTUAL_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'VirtualComponent')
_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ShaftModel', 'Shaft')
_CONCEPT_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGear')
_CONCEPT_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGearSet')
_FACE_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGear')
_FACE_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGearSet')
_AGMA_GLEASON_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGear')
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGearSet')
_BEVEL_DIFFERENTIAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGear')
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGearSet')
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialPlanetGear')
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialSunGear')
_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGear')
_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGearSet')
_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGear')
_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGearSet')
_CYLINDRICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGear')
_CYLINDRICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGearSet')
_CYLINDRICAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalPlanetGear')
_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'Gear')
_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'GearSet')
_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGear')
_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGear')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGearSet')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGear')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGear')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearSet')
_PLANETARY_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'PlanetaryGearSet')
_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGear')
_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGearSet')
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGear')
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGearSet')
_STRAIGHT_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGear')
_STRAIGHT_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGearSet')
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelPlanetGear')
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelSunGear')
_WORM_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGear')
_WORM_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGearSet')
_ZEROL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGear')
_ZEROL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGearSet')
_CYCLOIDAL_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalAssembly')
_CYCLOIDAL_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalDisc')
_RING_PINS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'RingPins')
_PART_TO_PART_SHEAR_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCoupling')
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCouplingHalf')
_BELT_DRIVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'BeltDrive')
_CLUTCH = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Clutch')
_CLUTCH_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ClutchHalf')
_CONCEPT_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCoupling')
_CONCEPT_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCouplingHalf')
_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Coupling')
_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CouplingHalf')
_CVT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVT')
_CVT_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVTPulley')
_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Pulley')
_SHAFT_HUB_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ShaftHubConnection')
_ROLLING_RING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRing')
_ROLLING_RING_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRingAssembly')
_SPRING_DAMPER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamper')
_SPRING_DAMPER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamperHalf')
_SYNCHRONISER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Synchroniser')
_SYNCHRONISER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserHalf')
_SYNCHRONISER_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserPart')
_SYNCHRONISER_SLEEVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserSleeve')
_TORQUE_CONVERTER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverter')
_TORQUE_CONVERTER_PUMP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterPump')
_TORQUE_CONVERTER_TURBINE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterTurbine')
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ShaftToMountableComponentConnection')
_CVT_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CVTBeltConnection')
_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'BeltConnection')
_COAXIAL_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CoaxialConnection')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'InterMountableComponentConnection')
_PLANETARY_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'PlanetaryConnection')
_ROLLING_RING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'RollingRingConnection')
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'AbstractShaftToMountableComponentConnection')
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelDifferentialGearMesh')
_CONCEPT_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConceptGearMesh')
_FACE_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'FaceGearMesh')
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelDiffGearMesh')
_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelGearMesh')
_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConicalGearMesh')
_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'AGMAGleasonConicalGearMesh')
_CYLINDRICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'CylindricalGearMesh')
_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'HypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidConicalGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidHypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearMesh')
_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'SpiralBevelGearMesh')
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelGearMesh')
_WORM_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'WormGearMesh')
_ZEROL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ZerolBevelGearMesh')
_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'GearMesh')
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscCentralBearingConnection')
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscPlanetaryBearingConnection')
_RING_PINS_TO_DISC_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'RingPinsToDiscConnection')
_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'LoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadCase',)


class LoadCase(_2399.Context):
    """LoadCase

    This is a mastapy class.
    """

    TYPE = _LOAD_CASE

    def __init__(self, instance_to_wrap: 'LoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def air_density(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'AirDensity' is the original name of this property."""

        temp = self.wrapped.AirDensity

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @air_density.setter
    def air_density(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.AirDensity = value

    @property
    def ball_bearing_contact_calculation(self) -> '_1729.BallBearingContactCalculation':
        """BallBearingContactCalculation: 'BallBearingContactCalculation' is the original name of this property."""

        temp = self.wrapped.BallBearingContactCalculation

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1729.BallBearingContactCalculation)(value) if value is not None else None

    @ball_bearing_contact_calculation.setter
    def ball_bearing_contact_calculation(self, value: '_1729.BallBearingContactCalculation'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BallBearingContactCalculation = value

    @property
    def ball_bearing_friction_model_for_gyroscopic_moment(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment':
        """enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment: 'BallBearingFrictionModelForGyroscopicMoment' is the original name of this property."""

        temp = self.wrapped.BallBearingFrictionModelForGyroscopicMoment

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @ball_bearing_friction_model_for_gyroscopic_moment.setter
    def ball_bearing_friction_model_for_gyroscopic_moment(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FrictionModelForGyroscopicMoment.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.BallBearingFrictionModelForGyroscopicMoment = value

    @property
    def characteristic_specific_acoustic_impedance(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'CharacteristicSpecificAcousticImpedance' is the original name of this property."""

        temp = self.wrapped.CharacteristicSpecificAcousticImpedance

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @characteristic_specific_acoustic_impedance.setter
    def characteristic_specific_acoustic_impedance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.CharacteristicSpecificAcousticImpedance = value

    @property
    def energy_convergence_absolute_tolerance(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'EnergyConvergenceAbsoluteTolerance' is the original name of this property."""

        temp = self.wrapped.EnergyConvergenceAbsoluteTolerance

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @energy_convergence_absolute_tolerance.setter
    def energy_convergence_absolute_tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.EnergyConvergenceAbsoluteTolerance = value

    @property
    def expand_grounded_nodes_for_thermal_effects(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'ExpandGroundedNodesForThermalEffects' is the original name of this property."""

        temp = self.wrapped.ExpandGroundedNodesForThermalEffects

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else None

    @expand_grounded_nodes_for_thermal_effects.setter
    def expand_grounded_nodes_for_thermal_effects(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.ExpandGroundedNodesForThermalEffects = value

    @property
    def force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes(self) -> 'bool':
        """bool: 'ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes' is the original name of this property."""

        temp = self.wrapped.ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes

        if temp is None:
            return None

        return temp

    @force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes.setter
    def force_multiple_mesh_nodes_for_unloaded_cylindrical_gear_meshes(self, value: 'bool'):
        self.wrapped.ForceMultipleMeshNodesForUnloadedCylindricalGearMeshes = bool(value) if value else False

    @property
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        """float: 'GearMeshNodesPerUnitLengthToDiameterRatio' is the original name of this property."""

        temp = self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio

        if temp is None:
            return None

        return temp

    @gear_mesh_nodes_per_unit_length_to_diameter_ratio.setter
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def grid_refinement_factor_contact_width(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'GridRefinementFactorContactWidth' is the original name of this property."""

        temp = self.wrapped.GridRefinementFactorContactWidth

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @grid_refinement_factor_contact_width.setter
    def grid_refinement_factor_contact_width(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.GridRefinementFactorContactWidth = value

    @property
    def grid_refinement_factor_rib_height(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'GridRefinementFactorRibHeight' is the original name of this property."""

        temp = self.wrapped.GridRefinementFactorRibHeight

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @grid_refinement_factor_rib_height.setter
    def grid_refinement_factor_rib_height(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.GridRefinementFactorRibHeight = value

    @property
    def hypoid_gear_wind_up_removal_method_for_misalignments(self) -> '_1965.HypoidWindUpRemovalMethod':
        """HypoidWindUpRemovalMethod: 'HypoidGearWindUpRemovalMethodForMisalignments' is the original name of this property."""

        temp = self.wrapped.HypoidGearWindUpRemovalMethodForMisalignments

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1965.HypoidWindUpRemovalMethod)(value) if value is not None else None

    @hypoid_gear_wind_up_removal_method_for_misalignments.setter
    def hypoid_gear_wind_up_removal_method_for_misalignments(self, value: '_1965.HypoidWindUpRemovalMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidGearWindUpRemovalMethodForMisalignments = value

    @property
    def include_bearing_centrifugal_ring_expansion(self) -> 'bool':
        """bool: 'IncludeBearingCentrifugalRingExpansion' is the original name of this property."""

        temp = self.wrapped.IncludeBearingCentrifugalRingExpansion

        if temp is None:
            return None

        return temp

    @include_bearing_centrifugal_ring_expansion.setter
    def include_bearing_centrifugal_ring_expansion(self, value: 'bool'):
        self.wrapped.IncludeBearingCentrifugalRingExpansion = bool(value) if value else False

    @property
    def include_bearing_centrifugal(self) -> 'bool':
        """bool: 'IncludeBearingCentrifugal' is the original name of this property."""

        temp = self.wrapped.IncludeBearingCentrifugal

        if temp is None:
            return None

        return temp

    @include_bearing_centrifugal.setter
    def include_bearing_centrifugal(self, value: 'bool'):
        self.wrapped.IncludeBearingCentrifugal = bool(value) if value else False

    @property
    def include_fitting_effects(self) -> 'bool':
        """bool: 'IncludeFittingEffects' is the original name of this property."""

        temp = self.wrapped.IncludeFittingEffects

        if temp is None:
            return None

        return temp

    @include_fitting_effects.setter
    def include_fitting_effects(self, value: 'bool'):
        self.wrapped.IncludeFittingEffects = bool(value) if value else False

    @property
    def include_gear_blank_elastic_distortion(self) -> 'bool':
        """bool: 'IncludeGearBlankElasticDistortion' is the original name of this property."""

        temp = self.wrapped.IncludeGearBlankElasticDistortion

        if temp is None:
            return None

        return temp

    @include_gear_blank_elastic_distortion.setter
    def include_gear_blank_elastic_distortion(self, value: 'bool'):
        self.wrapped.IncludeGearBlankElasticDistortion = bool(value) if value else False

    @property
    def include_gravity(self) -> 'bool':
        """bool: 'IncludeGravity' is the original name of this property."""

        temp = self.wrapped.IncludeGravity

        if temp is None:
            return None

        return temp

    @include_gravity.setter
    def include_gravity(self, value: 'bool'):
        self.wrapped.IncludeGravity = bool(value) if value else False

    @property
    def include_inner_race_distortion_for_flexible_pin_spindle(self) -> 'bool':
        """bool: 'IncludeInnerRaceDistortionForFlexiblePinSpindle' is the original name of this property."""

        temp = self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle

        if temp is None:
            return None

        return temp

    @include_inner_race_distortion_for_flexible_pin_spindle.setter
    def include_inner_race_distortion_for_flexible_pin_spindle(self, value: 'bool'):
        self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle = bool(value) if value else False

    @property
    def include_planetary_centrifugal(self) -> 'bool':
        """bool: 'IncludePlanetaryCentrifugal' is the original name of this property."""

        temp = self.wrapped.IncludePlanetaryCentrifugal

        if temp is None:
            return None

        return temp

    @include_planetary_centrifugal.setter
    def include_planetary_centrifugal(self, value: 'bool'):
        self.wrapped.IncludePlanetaryCentrifugal = bool(value) if value else False

    @property
    def include_profile_modifications_and_manufacturing_errors_during_cycloidal_analysis(self) -> 'bool':
        """bool: 'IncludeProfileModificationsAndManufacturingErrorsDuringCycloidalAnalysis' is the original name of this property."""

        temp = self.wrapped.IncludeProfileModificationsAndManufacturingErrorsDuringCycloidalAnalysis

        if temp is None:
            return None

        return temp

    @include_profile_modifications_and_manufacturing_errors_during_cycloidal_analysis.setter
    def include_profile_modifications_and_manufacturing_errors_during_cycloidal_analysis(self, value: 'bool'):
        self.wrapped.IncludeProfileModificationsAndManufacturingErrorsDuringCycloidalAnalysis = bool(value) if value else False

    @property
    def include_rib_contact_analysis(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'IncludeRibContactAnalysis' is the original name of this property."""

        temp = self.wrapped.IncludeRibContactAnalysis

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else None

    @include_rib_contact_analysis.setter
    def include_rib_contact_analysis(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.IncludeRibContactAnalysis = value

    @property
    def include_ring_ovality(self) -> 'bool':
        """bool: 'IncludeRingOvality' is the original name of this property."""

        temp = self.wrapped.IncludeRingOvality

        if temp is None:
            return None

        return temp

    @include_ring_ovality.setter
    def include_ring_ovality(self, value: 'bool'):
        self.wrapped.IncludeRingOvality = bool(value) if value else False

    @property
    def include_thermal_expansion_effects(self) -> 'bool':
        """bool: 'IncludeThermalExpansionEffects' is the original name of this property."""

        temp = self.wrapped.IncludeThermalExpansionEffects

        if temp is None:
            return None

        return temp

    @include_thermal_expansion_effects.setter
    def include_thermal_expansion_effects(self, value: 'bool'):
        self.wrapped.IncludeThermalExpansionEffects = bool(value) if value else False

    @property
    def include_tilt_stiffness_for_bevel_hypoid_gears(self) -> 'bool':
        """bool: 'IncludeTiltStiffnessForBevelHypoidGears' is the original name of this property."""

        temp = self.wrapped.IncludeTiltStiffnessForBevelHypoidGears

        if temp is None:
            return None

        return temp

    @include_tilt_stiffness_for_bevel_hypoid_gears.setter
    def include_tilt_stiffness_for_bevel_hypoid_gears(self, value: 'bool'):
        self.wrapped.IncludeTiltStiffnessForBevelHypoidGears = bool(value) if value else False

    @property
    def maximum_shaft_section_cross_sectional_area_ratio(self) -> 'float':
        """float: 'MaximumShaftSectionCrossSectionalAreaRatio' is the original name of this property."""

        temp = self.wrapped.MaximumShaftSectionCrossSectionalAreaRatio

        if temp is None:
            return None

        return temp

    @maximum_shaft_section_cross_sectional_area_ratio.setter
    def maximum_shaft_section_cross_sectional_area_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionCrossSectionalAreaRatio = float(value) if value else 0.0

    @property
    def maximum_shaft_section_length_to_diameter_ratio(self) -> 'float':
        """float: 'MaximumShaftSectionLengthToDiameterRatio' is the original name of this property."""

        temp = self.wrapped.MaximumShaftSectionLengthToDiameterRatio

        if temp is None:
            return None

        return temp

    @maximum_shaft_section_length_to_diameter_ratio.setter
    def maximum_shaft_section_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def maximum_shaft_section_polar_area_moment_of_inertia_ratio(self) -> 'float':
        """float: 'MaximumShaftSectionPolarAreaMomentOfInertiaRatio' is the original name of this property."""

        temp = self.wrapped.MaximumShaftSectionPolarAreaMomentOfInertiaRatio

        if temp is None:
            return None

        return temp

    @maximum_shaft_section_polar_area_moment_of_inertia_ratio.setter
    def maximum_shaft_section_polar_area_moment_of_inertia_ratio(self, value: 'float'):
        self.wrapped.MaximumShaftSectionPolarAreaMomentOfInertiaRatio = float(value) if value else 0.0

    @property
    def mesh_stiffness_model(self) -> 'enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel':
        """enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel: 'MeshStiffnessModel' is the original name of this property."""

        temp = self.wrapped.MeshStiffnessModel

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @mesh_stiffness_model.setter
    def mesh_stiffness_model(self, value: 'enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_MeshStiffnessModel.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.MeshStiffnessModel = value

    @property
    def micro_geometry_model_in_system_deflection(self) -> 'overridable.Overridable_MicroGeometryModel':
        """overridable.Overridable_MicroGeometryModel: 'MicroGeometryModelInSystemDeflection' is the original name of this property."""

        temp = self.wrapped.MicroGeometryModelInSystemDeflection

        if temp is None:
            return None

        value = overridable.Overridable_MicroGeometryModel.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @micro_geometry_model_in_system_deflection.setter
    def micro_geometry_model_in_system_deflection(self, value: 'overridable.Overridable_MicroGeometryModel.implicit_type()'):
        wrapper_type = overridable.Overridable_MicroGeometryModel.wrapper_type()
        enclosed_type = overridable.Overridable_MicroGeometryModel.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value is not None else None, is_overridden)
        self.wrapped.MicroGeometryModelInSystemDeflection = value

    @property
    def minimum_force_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinimumForceForBearingToBeConsideredLoaded' is the original name of this property."""

        temp = self.wrapped.MinimumForceForBearingToBeConsideredLoaded

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @minimum_force_for_bearing_to_be_considered_loaded.setter
    def minimum_force_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumForceForBearingToBeConsideredLoaded = value

    @property
    def minimum_moment_for_bearing_to_be_considered_loaded(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinimumMomentForBearingToBeConsideredLoaded' is the original name of this property."""

        temp = self.wrapped.MinimumMomentForBearingToBeConsideredLoaded

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @minimum_moment_for_bearing_to_be_considered_loaded.setter
    def minimum_moment_for_bearing_to_be_considered_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumMomentForBearingToBeConsideredLoaded = value

    @property
    def minimum_number_of_gear_mesh_nodes(self) -> 'int':
        """int: 'MinimumNumberOfGearMeshNodes' is the original name of this property."""

        temp = self.wrapped.MinimumNumberOfGearMeshNodes

        if temp is None:
            return None

        return temp

    @minimum_number_of_gear_mesh_nodes.setter
    def minimum_number_of_gear_mesh_nodes(self, value: 'int'):
        self.wrapped.MinimumNumberOfGearMeshNodes = int(value) if value else 0

    @property
    def minimum_power_for_gear_mesh_to_be_loaded(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinimumPowerForGearMeshToBeLoaded' is the original name of this property."""

        temp = self.wrapped.MinimumPowerForGearMeshToBeLoaded

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @minimum_power_for_gear_mesh_to_be_loaded.setter
    def minimum_power_for_gear_mesh_to_be_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumPowerForGearMeshToBeLoaded = value

    @property
    def minimum_torque_for_gear_mesh_to_be_loaded(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinimumTorqueForGearMeshToBeLoaded' is the original name of this property."""

        temp = self.wrapped.MinimumTorqueForGearMeshToBeLoaded

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @minimum_torque_for_gear_mesh_to_be_loaded.setter
    def minimum_torque_for_gear_mesh_to_be_loaded(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumTorqueForGearMeshToBeLoaded = value

    @property
    def model_bearing_mounting_clearances_automatically(self) -> 'bool':
        """bool: 'ModelBearingMountingClearancesAutomatically' is the original name of this property."""

        temp = self.wrapped.ModelBearingMountingClearancesAutomatically

        if temp is None:
            return None

        return temp

    @model_bearing_mounting_clearances_automatically.setter
    def model_bearing_mounting_clearances_automatically(self, value: 'bool'):
        self.wrapped.ModelBearingMountingClearancesAutomatically = bool(value) if value else False

    @property
    def number_of_grid_points_across_rib_contact_width(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfGridPointsAcrossRibContactWidth' is the original name of this property."""

        temp = self.wrapped.NumberOfGridPointsAcrossRibContactWidth

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @number_of_grid_points_across_rib_contact_width.setter
    def number_of_grid_points_across_rib_contact_width(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfGridPointsAcrossRibContactWidth = value

    @property
    def number_of_grid_points_across_rib_height(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfGridPointsAcrossRibHeight' is the original name of this property."""

        temp = self.wrapped.NumberOfGridPointsAcrossRibHeight

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @number_of_grid_points_across_rib_height.setter
    def number_of_grid_points_across_rib_height(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfGridPointsAcrossRibHeight = value

    @property
    def number_of_strips_for_roller_calculation(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfStripsForRollerCalculation' is the original name of this property."""

        temp = self.wrapped.NumberOfStripsForRollerCalculation

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @number_of_strips_for_roller_calculation.setter
    def number_of_strips_for_roller_calculation(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfStripsForRollerCalculation = value

    @property
    def peak_load_factor_for_shafts(self) -> 'float':
        """float: 'PeakLoadFactorForShafts' is the original name of this property."""

        temp = self.wrapped.PeakLoadFactorForShafts

        if temp is None:
            return None

        return temp

    @peak_load_factor_for_shafts.setter
    def peak_load_factor_for_shafts(self, value: 'float'):
        self.wrapped.PeakLoadFactorForShafts = float(value) if value else 0.0

    @property
    def refine_grid_around_contact_point(self) -> 'overridable.Overridable_bool':
        """overridable.Overridable_bool: 'RefineGridAroundContactPoint' is the original name of this property."""

        temp = self.wrapped.RefineGridAroundContactPoint

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_bool)(temp) if temp is not None else None

    @refine_grid_around_contact_point.setter
    def refine_grid_around_contact_point(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else False, is_overridden)
        self.wrapped.RefineGridAroundContactPoint = value

    @property
    def relative_tolerance_for_convergence(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RelativeToleranceForConvergence' is the original name of this property."""

        temp = self.wrapped.RelativeToleranceForConvergence

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @relative_tolerance_for_convergence.setter
    def relative_tolerance_for_convergence(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RelativeToleranceForConvergence = value

    @property
    def ring_ovality_scaling(self) -> 'float':
        """float: 'RingOvalityScaling' is the original name of this property."""

        temp = self.wrapped.RingOvalityScaling

        if temp is None:
            return None

        return temp

    @ring_ovality_scaling.setter
    def ring_ovality_scaling(self, value: 'float'):
        self.wrapped.RingOvalityScaling = float(value) if value else 0.0

    @property
    def roller_analysis_method(self) -> '_1828.RollerAnalysisMethod':
        """RollerAnalysisMethod: 'RollerAnalysisMethod' is the original name of this property."""

        temp = self.wrapped.RollerAnalysisMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1828.RollerAnalysisMethod)(value) if value is not None else None

    @roller_analysis_method.setter
    def roller_analysis_method(self, value: '_1828.RollerAnalysisMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RollerAnalysisMethod = value

    @property
    def speed_of_sound(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'SpeedOfSound' is the original name of this property."""

        temp = self.wrapped.SpeedOfSound

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @speed_of_sound.setter
    def speed_of_sound(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.SpeedOfSound = value

    @property
    def spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        """float: 'SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio' is the original name of this property."""

        temp = self.wrapped.SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio

        if temp is None:
            return None

        return temp

    @spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio.setter
    def spline_rigid_bond_detailed_connection_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.SplineRigidBondDetailedConnectionNodesPerUnitLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def stress_concentration_method_for_rating(self) -> 'enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod':
        """enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod: 'StressConcentrationMethodForRating' is the original name of this property."""

        temp = self.wrapped.StressConcentrationMethodForRating

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @stress_concentration_method_for_rating.setter
    def stress_concentration_method_for_rating(self, value: 'enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_StressConcentrationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.StressConcentrationMethodForRating = value

    @property
    def tolerance_factor_for_axial_internal_clearances(self) -> 'float':
        """float: 'ToleranceFactorForAxialInternalClearances' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForAxialInternalClearances

        if temp is None:
            return None

        return temp

    @tolerance_factor_for_axial_internal_clearances.setter
    def tolerance_factor_for_axial_internal_clearances(self, value: 'float'):
        self.wrapped.ToleranceFactorForAxialInternalClearances = float(value) if value else 0.0

    @property
    def tolerance_factor_for_inner_fit(self) -> 'float':
        """float: 'ToleranceFactorForInnerFit' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForInnerFit

        if temp is None:
            return None

        return temp

    @tolerance_factor_for_inner_fit.setter
    def tolerance_factor_for_inner_fit(self, value: 'float'):
        self.wrapped.ToleranceFactorForInnerFit = float(value) if value else 0.0

    @property
    def tolerance_factor_for_inner_mounting_sleeve_bore(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForInnerMountingSleeveBore' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForInnerMountingSleeveBore

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @tolerance_factor_for_inner_mounting_sleeve_bore.setter
    def tolerance_factor_for_inner_mounting_sleeve_bore(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerMountingSleeveBore = value

    @property
    def tolerance_factor_for_inner_mounting_sleeve_outer_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForInnerMountingSleeveOuterDiameter' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForInnerMountingSleeveOuterDiameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @tolerance_factor_for_inner_mounting_sleeve_outer_diameter.setter
    def tolerance_factor_for_inner_mounting_sleeve_outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerMountingSleeveOuterDiameter = value

    @property
    def tolerance_factor_for_inner_ring(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForInnerRing' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForInnerRing

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @tolerance_factor_for_inner_ring.setter
    def tolerance_factor_for_inner_ring(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerRing = value

    @property
    def tolerance_factor_for_inner_support(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForInnerSupport' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForInnerSupport

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @tolerance_factor_for_inner_support.setter
    def tolerance_factor_for_inner_support(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForInnerSupport = value

    @property
    def tolerance_factor_for_outer_fit(self) -> 'float':
        """float: 'ToleranceFactorForOuterFit' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForOuterFit

        if temp is None:
            return None

        return temp

    @tolerance_factor_for_outer_fit.setter
    def tolerance_factor_for_outer_fit(self, value: 'float'):
        self.wrapped.ToleranceFactorForOuterFit = float(value) if value else 0.0

    @property
    def tolerance_factor_for_outer_mounting_sleeve_bore(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForOuterMountingSleeveBore' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForOuterMountingSleeveBore

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @tolerance_factor_for_outer_mounting_sleeve_bore.setter
    def tolerance_factor_for_outer_mounting_sleeve_bore(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterMountingSleeveBore = value

    @property
    def tolerance_factor_for_outer_mounting_sleeve_outer_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForOuterMountingSleeveOuterDiameter' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForOuterMountingSleeveOuterDiameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @tolerance_factor_for_outer_mounting_sleeve_outer_diameter.setter
    def tolerance_factor_for_outer_mounting_sleeve_outer_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterMountingSleeveOuterDiameter = value

    @property
    def tolerance_factor_for_outer_ring(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForOuterRing' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForOuterRing

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @tolerance_factor_for_outer_ring.setter
    def tolerance_factor_for_outer_ring(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterRing = value

    @property
    def tolerance_factor_for_outer_support(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToleranceFactorForOuterSupport' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForOuterSupport

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @tolerance_factor_for_outer_support.setter
    def tolerance_factor_for_outer_support(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToleranceFactorForOuterSupport = value

    @property
    def tolerance_factor_for_radial_internal_clearances(self) -> 'float':
        """float: 'ToleranceFactorForRadialInternalClearances' is the original name of this property."""

        temp = self.wrapped.ToleranceFactorForRadialInternalClearances

        if temp is None:
            return None

        return temp

    @tolerance_factor_for_radial_internal_clearances.setter
    def tolerance_factor_for_radial_internal_clearances(self, value: 'float'):
        self.wrapped.ToleranceFactorForRadialInternalClearances = float(value) if value else 0.0

    @property
    def use_default_temperatures(self) -> 'bool':
        """bool: 'UseDefaultTemperatures' is the original name of this property."""

        temp = self.wrapped.UseDefaultTemperatures

        if temp is None:
            return None

        return temp

    @use_default_temperatures.setter
    def use_default_temperatures(self, value: 'bool'):
        self.wrapped.UseDefaultTemperatures = bool(value) if value else False

    @property
    def use_node_per_bearing_row_inner(self) -> 'bool':
        """bool: 'UseNodePerBearingRowInner' is the original name of this property."""

        temp = self.wrapped.UseNodePerBearingRowInner

        if temp is None:
            return None

        return temp

    @use_node_per_bearing_row_inner.setter
    def use_node_per_bearing_row_inner(self, value: 'bool'):
        self.wrapped.UseNodePerBearingRowInner = bool(value) if value else False

    @property
    def use_node_per_bearing_row_outer(self) -> 'bool':
        """bool: 'UseNodePerBearingRowOuter' is the original name of this property."""

        temp = self.wrapped.UseNodePerBearingRowOuter

        if temp is None:
            return None

        return temp

    @use_node_per_bearing_row_outer.setter
    def use_node_per_bearing_row_outer(self, value: 'bool'):
        self.wrapped.UseNodePerBearingRowOuter = bool(value) if value else False

    @property
    def use_single_node_for_cylindrical_gear_meshes(self) -> 'bool':
        """bool: 'UseSingleNodeForCylindricalGearMeshes' is the original name of this property."""

        temp = self.wrapped.UseSingleNodeForCylindricalGearMeshes

        if temp is None:
            return None

        return temp

    @use_single_node_for_cylindrical_gear_meshes.setter
    def use_single_node_for_cylindrical_gear_meshes(self, value: 'bool'):
        self.wrapped.UseSingleNodeForCylindricalGearMeshes = bool(value) if value else False

    @property
    def use_single_node_for_spline_rigid_bond_detailed_connection_connections(self) -> 'bool':
        """bool: 'UseSingleNodeForSplineRigidBondDetailedConnectionConnections' is the original name of this property."""

        temp = self.wrapped.UseSingleNodeForSplineRigidBondDetailedConnectionConnections

        if temp is None:
            return None

        return temp

    @use_single_node_for_spline_rigid_bond_detailed_connection_connections.setter
    def use_single_node_for_spline_rigid_bond_detailed_connection_connections(self, value: 'bool'):
        self.wrapped.UseSingleNodeForSplineRigidBondDetailedConnectionConnections = bool(value) if value else False

    @property
    def additional_acceleration(self) -> '_6534.AdditionalAccelerationOptions':
        """AdditionalAccelerationOptions: 'AdditionalAcceleration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdditionalAcceleration

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def input_power_load(self) -> '_6666.PowerLoadLoadCase':
        """PowerLoadLoadCase: 'InputPowerLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InputPowerLoad

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def output_power_load(self) -> '_6666.PowerLoadLoadCase':
        """PowerLoadLoadCase: 'OutputPowerLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OutputPowerLoad

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def parametric_study_tool_options(self) -> '_4129.ParametricStudyToolOptions':
        """ParametricStudyToolOptions: 'ParametricStudyToolOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParametricStudyToolOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def temperatures(self) -> '_1978.TransmissionTemperatureSet':
        """TransmissionTemperatureSet: 'Temperatures' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Temperatures

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def transmission_efficiency_settings(self) -> '_6706.TransmissionEfficiencySettings':
        """TransmissionEfficiencySettings: 'TransmissionEfficiencySettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransmissionEfficiencySettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_loads(self) -> 'List[_6666.PowerLoadLoadCase]':
        """List[PowerLoadLoadCase]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def delete(self):
        """ 'Delete' is the original name of this method."""

        self.wrapped.Delete()

    def inputs_for_torque_converter_connection(self, design_entity: '_2103.TorqueConverterConnection') -> '_6700.TorqueConverterConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_abstract_shaft(self, design_entity: '_2187.AbstractShaft') -> '_6531.AbstractShaftLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaft)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractShaftLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ABSTRACT_SHAFT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_abstract_assembly(self, design_entity: '_2186.AbstractAssembly') -> '_6530.AbstractAssemblyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ABSTRACT_ASSEMBLY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_abstract_shaft_or_housing(self, design_entity: '_2188.AbstractShaftOrHousing') -> '_6532.AbstractShaftOrHousingLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ABSTRACT_SHAFT_OR_HOUSING](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bearing(self, design_entity: '_2191.Bearing') -> '_6543.BearingLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEARING](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bolt(self, design_entity: '_2193.Bolt') -> '_6555.BoltLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BOLT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bolted_joint(self, design_entity: '_2194.BoltedJoint') -> '_6554.BoltedJointLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BOLTED_JOINT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_component(self, design_entity: '_2195.Component') -> '_6560.ComponentLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_COMPONENT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_connector(self, design_entity: '_2198.Connector') -> '_6573.ConnectorLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONNECTOR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_datum(self, design_entity: '_2199.Datum') -> '_6592.DatumLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_DATUM](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_external_cad_model(self, design_entity: '_2202.ExternalCADModel') -> '_6607.ExternalCADModelLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_EXTERNAL_CAD_MODEL](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_fe_part(self, design_entity: '_2203.FEPart') -> '_6611.FEPartLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FEPart)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FEPartLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_FE_PART](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_flexible_pin_assembly(self, design_entity: '_2204.FlexiblePinAssembly') -> '_6612.FlexiblePinAssemblyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_FLEXIBLE_PIN_ASSEMBLY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_assembly(self, design_entity: '_2185.Assembly') -> '_6542.AssemblyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ASSEMBLY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_guide_dxf_model(self, design_entity: '_2205.GuideDxfModel') -> '_6620.GuideDxfModelLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_GUIDE_DXF_MODEL](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_mass_disc(self, design_entity: '_2212.MassDisc') -> '_6647.MassDiscLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_MASS_DISC](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_measurement_component(self, design_entity: '_2213.MeasurementComponent') -> '_6648.MeasurementComponentLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_MEASUREMENT_COMPONENT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_mountable_component(self, design_entity: '_2214.MountableComponent') -> '_6651.MountableComponentLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_MOUNTABLE_COMPONENT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_oil_seal(self, design_entity: '_2216.OilSeal') -> '_6653.OilSealLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_OIL_SEAL](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_part(self, design_entity: '_2218.Part') -> '_6655.PartLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PART](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_planet_carrier(self, design_entity: '_2219.PlanetCarrier') -> '_6662.PlanetCarrierLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PLANET_CARRIER](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_point_load(self, design_entity: '_2221.PointLoad') -> '_6665.PointLoadLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_POINT_LOAD](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_power_load(self, design_entity: '_2222.PowerLoad') -> '_6666.PowerLoadLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_POWER_LOAD](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_root_assembly(self, design_entity: '_2224.RootAssembly') -> '_6675.RootAssemblyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ROOT_ASSEMBLY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_specialised_assembly(self, design_entity: '_2226.SpecialisedAssembly') -> '_6679.SpecialisedAssemblyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SPECIALISED_ASSEMBLY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_unbalanced_mass(self, design_entity: '_2227.UnbalancedMass') -> '_6708.UnbalancedMassLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_UNBALANCED_MASS](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_virtual_component(self, design_entity: '_2229.VirtualComponent') -> '_6709.VirtualComponentLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_VIRTUAL_COMPONENT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_shaft(self, design_entity: '_2232.Shaft') -> '_6677.ShaftLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SHAFT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_concept_gear(self, design_entity: '_2270.ConceptGear') -> '_6564.ConceptGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_concept_gear_set(self, design_entity: '_2271.ConceptGearSet') -> '_6566.ConceptGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_face_gear(self, design_entity: '_2277.FaceGear') -> '_6608.FaceGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_FACE_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_face_gear_set(self, design_entity: '_2278.FaceGearSet') -> '_6610.FaceGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_FACE_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_agma_gleason_conical_gear(self, design_entity: '_2262.AGMAGleasonConicalGear') -> '_6537.AGMAGleasonConicalGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_agma_gleason_conical_gear_set(self, design_entity: '_2263.AGMAGleasonConicalGearSet') -> '_6539.AGMAGleasonConicalGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_gear(self, design_entity: '_2264.BevelDifferentialGear') -> '_6546.BevelDifferentialGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_gear_set(self, design_entity: '_2265.BevelDifferentialGearSet') -> '_6548.BevelDifferentialGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_planet_gear(self, design_entity: '_2266.BevelDifferentialPlanetGear') -> '_6549.BevelDifferentialPlanetGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_sun_gear(self, design_entity: '_2267.BevelDifferentialSunGear') -> '_6550.BevelDifferentialSunGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_SUN_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_gear(self, design_entity: '_2268.BevelGear') -> '_6551.BevelGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_gear_set(self, design_entity: '_2269.BevelGearSet') -> '_6553.BevelGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_conical_gear(self, design_entity: '_2272.ConicalGear') -> '_6567.ConicalGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_conical_gear_set(self, design_entity: '_2273.ConicalGearSet') -> '_6571.ConicalGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cylindrical_gear(self, design_entity: '_2274.CylindricalGear') -> '_6584.CylindricalGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cylindrical_gear_set(self, design_entity: '_2275.CylindricalGearSet') -> '_6588.CylindricalGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cylindrical_planet_gear(self, design_entity: '_2276.CylindricalPlanetGear') -> '_6589.CylindricalPlanetGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_gear(self, design_entity: '_2279.Gear') -> '_6614.GearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_gear_set(self, design_entity: '_2281.GearSet') -> '_6619.GearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_hypoid_gear(self, design_entity: '_2283.HypoidGear') -> '_6631.HypoidGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_HYPOID_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_hypoid_gear_set(self, design_entity: '_2284.HypoidGearSet') -> '_6633.HypoidGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2285.KlingelnbergCycloPalloidConicalGear') -> '_6638.KlingelnbergCycloPalloidConicalGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2286.KlingelnbergCycloPalloidConicalGearSet') -> '_6640.KlingelnbergCycloPalloidConicalGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2287.KlingelnbergCycloPalloidHypoidGear') -> '_6641.KlingelnbergCycloPalloidHypoidGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2288.KlingelnbergCycloPalloidHypoidGearSet') -> '_6643.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2289.KlingelnbergCycloPalloidSpiralBevelGear') -> '_6644.KlingelnbergCycloPalloidSpiralBevelGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2290.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_6646.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_planetary_gear_set(self, design_entity: '_2291.PlanetaryGearSet') -> '_6660.PlanetaryGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PLANETARY_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_spiral_bevel_gear(self, design_entity: '_2292.SpiralBevelGear') -> '_6681.SpiralBevelGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_spiral_bevel_gear_set(self, design_entity: '_2293.SpiralBevelGearSet') -> '_6683.SpiralBevelGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_diff_gear(self, design_entity: '_2294.StraightBevelDiffGear') -> '_6687.StraightBevelDiffGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_diff_gear_set(self, design_entity: '_2295.StraightBevelDiffGearSet') -> '_6689.StraightBevelDiffGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_gear(self, design_entity: '_2296.StraightBevelGear') -> '_6690.StraightBevelGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_gear_set(self, design_entity: '_2297.StraightBevelGearSet') -> '_6692.StraightBevelGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_planet_gear(self, design_entity: '_2298.StraightBevelPlanetGear') -> '_6693.StraightBevelPlanetGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_PLANET_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_sun_gear(self, design_entity: '_2299.StraightBevelSunGear') -> '_6694.StraightBevelSunGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_SUN_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_worm_gear(self, design_entity: '_2300.WormGear') -> '_6710.WormGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_WORM_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_worm_gear_set(self, design_entity: '_2301.WormGearSet') -> '_6712.WormGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_WORM_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_zerol_bevel_gear(self, design_entity: '_2302.ZerolBevelGear') -> '_6713.ZerolBevelGearLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ZEROL_BEVEL_GEAR](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_zerol_bevel_gear_set(self, design_entity: '_2303.ZerolBevelGearSet') -> '_6715.ZerolBevelGearSetLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ZEROL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cycloidal_assembly(self, design_entity: '_2317.CycloidalAssembly') -> '_6580.CycloidalAssemblyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CycloidalAssemblyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYCLOIDAL_ASSEMBLY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cycloidal_disc(self, design_entity: '_2318.CycloidalDisc') -> '_6582.CycloidalDiscLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalDisc)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYCLOIDAL_DISC](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_ring_pins(self, design_entity: '_2319.RingPins') -> '_6670.RingPinsLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.RingPins)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RingPinsLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_RING_PINS](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_part_to_part_shear_coupling(self, design_entity: '_2337.PartToPartShearCoupling') -> '_6658.PartToPartShearCouplingLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_part_to_part_shear_coupling_half(self, design_entity: '_2338.PartToPartShearCouplingHalf') -> '_6657.PartToPartShearCouplingHalfLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_belt_drive(self, design_entity: '_2325.BeltDrive') -> '_6545.BeltDriveLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BELT_DRIVE](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_clutch(self, design_entity: '_2327.Clutch') -> '_6558.ClutchLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CLUTCH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_clutch_half(self, design_entity: '_2328.ClutchHalf') -> '_6557.ClutchHalfLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CLUTCH_HALF](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_concept_coupling(self, design_entity: '_2330.ConceptCoupling') -> '_6563.ConceptCouplingLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_COUPLING](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_concept_coupling_half(self, design_entity: '_2331.ConceptCouplingHalf') -> '_6562.ConceptCouplingHalfLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_coupling(self, design_entity: '_2332.Coupling') -> '_6576.CouplingLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_COUPLING](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_coupling_half(self, design_entity: '_2333.CouplingHalf') -> '_6575.CouplingHalfLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_COUPLING_HALF](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cvt(self, design_entity: '_2335.CVT') -> '_6578.CVTLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CVT](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cvt_pulley(self, design_entity: '_2336.CVTPulley') -> '_6579.CVTPulleyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CVT_PULLEY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_pulley(self, design_entity: '_2339.Pulley') -> '_6667.PulleyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PULLEY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_shaft_hub_connection(self, design_entity: '_2347.ShaftHubConnection') -> '_6676.ShaftHubConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SHAFT_HUB_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_rolling_ring(self, design_entity: '_2345.RollingRing') -> '_6674.RollingRingLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ROLLING_RING](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_rolling_ring_assembly(self, design_entity: '_2346.RollingRingAssembly') -> '_6672.RollingRingAssemblyLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ROLLING_RING_ASSEMBLY](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_spring_damper(self, design_entity: '_2349.SpringDamper') -> '_6686.SpringDamperLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SPRING_DAMPER](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_spring_damper_half(self, design_entity: '_2350.SpringDamperHalf') -> '_6685.SpringDamperHalfLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SPRING_DAMPER_HALF](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_synchroniser(self, design_entity: '_2351.Synchroniser') -> '_6696.SynchroniserLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_synchroniser_half(self, design_entity: '_2353.SynchroniserHalf') -> '_6695.SynchroniserHalfLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER_HALF](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_synchroniser_part(self, design_entity: '_2354.SynchroniserPart') -> '_6697.SynchroniserPartLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER_PART](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_synchroniser_sleeve(self, design_entity: '_2355.SynchroniserSleeve') -> '_6698.SynchroniserSleeveLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SYNCHRONISER_SLEEVE](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_torque_converter(self, design_entity: '_2356.TorqueConverter') -> '_6701.TorqueConverterLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_torque_converter_pump(self, design_entity: '_2357.TorqueConverterPump') -> '_6702.TorqueConverterPumpLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER_PUMP](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_torque_converter_turbine(self, design_entity: '_2359.TorqueConverterTurbine') -> '_6703.TorqueConverterTurbineLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_TORQUE_CONVERTER_TURBINE](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_shaft_to_mountable_component_connection(self, design_entity: '_2046.ShaftToMountableComponentConnection') -> '_6678.ShaftToMountableComponentConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cvt_belt_connection(self, design_entity: '_2024.CVTBeltConnection') -> '_6577.CVTBeltConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CVT_BELT_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_belt_connection(self, design_entity: '_2019.BeltConnection') -> '_6544.BeltConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BELT_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_coaxial_connection(self, design_entity: '_2020.CoaxialConnection') -> '_6559.CoaxialConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_COAXIAL_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_connection(self, design_entity: '_2023.Connection') -> '_6572.ConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_inter_mountable_component_connection(self, design_entity: '_2032.InterMountableComponentConnection') -> '_6637.InterMountableComponentConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_INTER_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_planetary_connection(self, design_entity: '_2038.PlanetaryConnection') -> '_6659.PlanetaryConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PLANETARY_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_rolling_ring_connection(self, design_entity: '_2043.RollingRingConnection') -> '_6673.RollingRingConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ROLLING_RING_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_abstract_shaft_to_mountable_component_connection(self, design_entity: '_2016.AbstractShaftToMountableComponentConnection') -> '_6533.AbstractShaftToMountableComponentConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AbstractShaftToMountableComponentConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_differential_gear_mesh(self, design_entity: '_2052.BevelDifferentialGearMesh') -> '_6547.BevelDifferentialGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_concept_gear_mesh(self, design_entity: '_2056.ConceptGearMesh') -> '_6565.ConceptGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_face_gear_mesh(self, design_entity: '_2062.FaceGearMesh') -> '_6609.FaceGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_FACE_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_diff_gear_mesh(self, design_entity: '_2076.StraightBevelDiffGearMesh') -> '_6688.StraightBevelDiffGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_bevel_gear_mesh(self, design_entity: '_2054.BevelGearMesh') -> '_6552.BevelGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_conical_gear_mesh(self, design_entity: '_2058.ConicalGearMesh') -> '_6569.ConicalGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_agma_gleason_conical_gear_mesh(self, design_entity: '_2050.AGMAGleasonConicalGearMesh') -> '_6538.AGMAGleasonConicalGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cylindrical_gear_mesh(self, design_entity: '_2060.CylindricalGearMesh') -> '_6586.CylindricalGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYLINDRICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_hypoid_gear_mesh(self, design_entity: '_2066.HypoidGearMesh') -> '_6632.HypoidGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_2069.KlingelnbergCycloPalloidConicalGearMesh') -> '_6639.KlingelnbergCycloPalloidConicalGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_2070.KlingelnbergCycloPalloidHypoidGearMesh') -> '_6642.KlingelnbergCycloPalloidHypoidGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_2071.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_6645.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_spiral_bevel_gear_mesh(self, design_entity: '_2074.SpiralBevelGearMesh') -> '_6682.SpiralBevelGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_straight_bevel_gear_mesh(self, design_entity: '_2078.StraightBevelGearMesh') -> '_6691.StraightBevelGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_STRAIGHT_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_worm_gear_mesh(self, design_entity: '_2080.WormGearMesh') -> '_6711.WormGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_WORM_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_zerol_bevel_gear_mesh(self, design_entity: '_2082.ZerolBevelGearMesh') -> '_6714.ZerolBevelGearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_ZEROL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_gear_mesh(self, design_entity: '_2064.GearMesh') -> '_6616.GearMeshLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_GEAR_MESH](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cycloidal_disc_central_bearing_connection(self, design_entity: '_2086.CycloidalDiscCentralBearingConnection') -> '_6581.CycloidalDiscCentralBearingConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscCentralBearingConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_cycloidal_disc_planetary_bearing_connection(self, design_entity: '_2089.CycloidalDiscPlanetaryBearingConnection') -> '_6583.CycloidalDiscPlanetaryBearingConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscPlanetaryBearingConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_ring_pins_to_disc_connection(self, design_entity: '_2092.RingPinsToDiscConnection') -> '_6671.RingPinsToDiscConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.RingPinsToDiscConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_RING_PINS_TO_DISC_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_part_to_part_shear_coupling_connection(self, design_entity: '_2099.PartToPartShearCouplingConnection') -> '_6656.PartToPartShearCouplingConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_clutch_connection(self, design_entity: '_2093.ClutchConnection') -> '_6556.ClutchConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CLUTCH_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_concept_coupling_connection(self, design_entity: '_2095.ConceptCouplingConnection') -> '_6561.ConceptCouplingConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_CONCEPT_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_coupling_connection(self, design_entity: '_2097.CouplingConnection') -> '_6574.CouplingConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def inputs_for_spring_damper_connection(self, design_entity: '_2101.SpringDamperConnection') -> '_6684.SpringDamperConnectionLoadCase':
        """ 'InputsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase
        """

        method_result = self.wrapped.InputsFor.Overloads[_SPRING_DAMPER_CONNECTION](design_entity.wrapped if design_entity else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
