"""_1621.py

MASTAGUI
"""


from typing import List, Dict

from mastapy._internal import constructor, conversion, enum_with_selected_value_runtime
from mastapy.system_model import _1956, _1960
from mastapy._math.color import Color
from mastapy.utility.operation_modes import _1569
from mastapy._math.vector_3d import Vector3D
from mastapy.system_model.connections_and_sockets import (
    _2016, _2019, _2020, _2023,
    _2024, _2032, _2038, _2043,
    _2046
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _2050, _2052, _2054, _2056,
    _2058, _2060, _2062, _2064,
    _2066, _2069, _2070, _2071,
    _2074, _2076, _2078, _2080,
    _2082
)
from mastapy.system_model.connections_and_sockets.cycloidal import _2086, _2089, _2092
from mastapy.system_model.connections_and_sockets.couplings import (
    _2093, _2095, _2097, _2099,
    _2101, _2103
)
from mastapy.system_model.part_model import (
    _2185, _2186, _2187, _2188,
    _2191, _2193, _2194, _2195,
    _2198, _2199, _2202, _2203,
    _2204, _2205, _2212, _2213,
    _2214, _2216, _2218, _2219,
    _2221, _2222, _2224, _2226,
    _2227, _2229
)
from mastapy.system_model.part_model.shaft_model import _2232
from mastapy.system_model.part_model.gears import (
    _2262, _2263, _2264, _2265,
    _2266, _2267, _2268, _2269,
    _2270, _2271, _2272, _2273,
    _2274, _2275, _2276, _2277,
    _2278, _2279, _2281, _2283,
    _2284, _2285, _2286, _2287,
    _2288, _2289, _2290, _2291,
    _2292, _2293, _2294, _2295,
    _2296, _2297, _2298, _2299,
    _2300, _2301, _2302, _2303
)
from mastapy.system_model.part_model.cycloidal import _2317, _2318, _2319
from mastapy.system_model.part_model.couplings import (
    _2325, _2327, _2328, _2330,
    _2331, _2332, _2333, _2335,
    _2336, _2337, _2338, _2339,
    _2345, _2346, _2347, _2349,
    _2350, _2351, _2353, _2354,
    _2355, _2356, _2357, _2359
)
from mastapy.math_utility import _1318, _1299
from mastapy.nodal_analysis.geometry_modeller_link import _150
from mastapy._internal.python_net import python_net_import
from mastapy import _0

_FACETED_BODY = python_net_import('SMT.MastaAPI.MathUtility', 'FacetedBody')
_STRING = python_net_import('System', 'String')
_MASTAGUI = python_net_import('SMT.MastaAPI.SystemModelGUI', 'MASTAGUI')


__docformat__ = 'restructuredtext en'
__all__ = ('MASTAGUI',)


class MASTAGUI(_0.APIBase):
    """MASTAGUI

    This is a mastapy class.
    """

    TYPE = _MASTAGUI

    def __init__(self, instance_to_wrap: 'MASTAGUI.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_initialised(self) -> 'bool':
        """bool: 'IsInitialised' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IsInitialised

        if temp is None:
            return None

        return temp

    @property
    def is_paused(self) -> 'bool':
        """bool: 'IsPaused' is the original name of this property."""

        temp = self.wrapped.IsPaused

        if temp is None:
            return None

        return temp

    @is_paused.setter
    def is_paused(self, value: 'bool'):
        self.wrapped.IsPaused = bool(value) if value else False

    @property
    def is_remoting(self) -> 'bool':
        """bool: 'IsRemoting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IsRemoting

        if temp is None:
            return None

        return temp

    @property
    def active_design(self) -> '_1956.Design':
        """Design: 'ActiveDesign' is the original name of this property."""

        temp = self.wrapped.ActiveDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @active_design.setter
    def active_design(self, value: '_1956.Design'):
        value = value.wrapped if value else None
        self.wrapped.ActiveDesign = value

    @property
    def color_of_new_problem_node_group(self) -> 'Color':
        """Color: 'ColorOfNewProblemNodeGroup' is the original name of this property."""

        temp = self.wrapped.ColorOfNewProblemNodeGroup

        if temp is None:
            return None

        value = conversion.pn_to_mp_color(temp)
        return value

    @color_of_new_problem_node_group.setter
    def color_of_new_problem_node_group(self, value: 'Color'):
        value = value if value else None
        value = conversion.mp_to_pn_color(value)
        self.wrapped.ColorOfNewProblemNodeGroup = value

    @property
    def geometry_modeller_process_id(self) -> 'int':
        """int: 'GeometryModellerProcessID' is the original name of this property."""

        temp = self.wrapped.GeometryModellerProcessID

        if temp is None:
            return None

        return temp

    @geometry_modeller_process_id.setter
    def geometry_modeller_process_id(self, value: 'int'):
        self.wrapped.GeometryModellerProcessID = int(value) if value else 0

    @property
    def is_connected_to_geometry_modeller(self) -> 'bool':
        """bool: 'IsConnectedToGeometryModeller' is the original name of this property."""

        temp = self.wrapped.IsConnectedToGeometryModeller

        if temp is None:
            return None

        return temp

    @is_connected_to_geometry_modeller.setter
    def is_connected_to_geometry_modeller(self, value: 'bool'):
        self.wrapped.IsConnectedToGeometryModeller = bool(value) if value else False

    @property
    def name_of_new_problem_node_group(self) -> 'str':
        """str: 'NameOfNewProblemNodeGroup' is the original name of this property."""

        temp = self.wrapped.NameOfNewProblemNodeGroup

        if temp is None:
            return None

        return temp

    @name_of_new_problem_node_group.setter
    def name_of_new_problem_node_group(self, value: 'str'):
        self.wrapped.NameOfNewProblemNodeGroup = str(value) if value else ''

    @property
    def open_designs(self) -> 'List[_1956.Design]':
        """List[Design]: 'OpenDesigns' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OpenDesigns

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def operation_mode(self) -> '_1569.OperationMode':
        """OperationMode: 'OperationMode' is the original name of this property."""

        temp = self.wrapped.OperationMode

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1569.OperationMode)(value) if value is not None else None

    @operation_mode.setter
    def operation_mode(self, value: '_1569.OperationMode'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OperationMode = value

    @property
    def positions_of_problem_node_group(self) -> 'List[Vector3D]':
        """List[Vector3D]: 'PositionsOfProblemNodeGroup' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PositionsOfProblemNodeGroup

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def process_id(self) -> 'int':
        """int: 'ProcessId' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProcessId

        if temp is None:
            return None

        return temp

    @property
    def restart_geometry_modeller_flag(self) -> 'bool':
        """bool: 'RestartGeometryModellerFlag' is the original name of this property."""

        temp = self.wrapped.RestartGeometryModellerFlag

        if temp is None:
            return None

        return temp

    @restart_geometry_modeller_flag.setter
    def restart_geometry_modeller_flag(self, value: 'bool'):
        self.wrapped.RestartGeometryModellerFlag = bool(value) if value else False

    @property
    def restart_geometry_modeller_save_file(self) -> 'str':
        """str: 'RestartGeometryModellerSaveFile' is the original name of this property."""

        temp = self.wrapped.RestartGeometryModellerSaveFile

        if temp is None:
            return None

        return temp

    @restart_geometry_modeller_save_file.setter
    def restart_geometry_modeller_save_file(self, value: 'str'):
        self.wrapped.RestartGeometryModellerSaveFile = str(value) if value else ''

    @property
    def selected_design_entity(self) -> '_1960.DesignEntity':
        """DesignEntity: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _1960.DesignEntity.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to DesignEntity. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity.setter
    def selected_design_entity(self, value: '_1960.DesignEntity'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_2016.AbstractShaftToMountableComponentConnection':
        """AbstractShaftToMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2016.AbstractShaftToMountableComponentConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection.setter
    def selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection(self, value: '_2016.AbstractShaftToMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_belt_connection(self) -> '_2019.BeltConnection':
        """BeltConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2019.BeltConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BeltConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_belt_connection.setter
    def selected_design_entity_of_type_belt_connection(self, value: '_2019.BeltConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coaxial_connection(self) -> '_2020.CoaxialConnection':
        """CoaxialConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2020.CoaxialConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CoaxialConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_coaxial_connection.setter
    def selected_design_entity_of_type_coaxial_connection(self, value: '_2020.CoaxialConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_connection(self) -> '_2023.Connection':
        """Connection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2023.Connection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Connection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_connection.setter
    def selected_design_entity_of_type_connection(self, value: '_2023.Connection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt_belt_connection(self) -> '_2024.CVTBeltConnection':
        """CVTBeltConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2024.CVTBeltConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVTBeltConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cvt_belt_connection.setter
    def selected_design_entity_of_type_cvt_belt_connection(self, value: '_2024.CVTBeltConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_inter_mountable_component_connection(self) -> '_2032.InterMountableComponentConnection':
        """InterMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2032.InterMountableComponentConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to InterMountableComponentConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_inter_mountable_component_connection.setter
    def selected_design_entity_of_type_inter_mountable_component_connection(self, value: '_2032.InterMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planetary_connection(self) -> '_2038.PlanetaryConnection':
        """PlanetaryConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2038.PlanetaryConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetaryConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_planetary_connection.setter
    def selected_design_entity_of_type_planetary_connection(self, value: '_2038.PlanetaryConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring_connection(self) -> '_2043.RollingRingConnection':
        """RollingRingConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2043.RollingRingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_rolling_ring_connection.setter
    def selected_design_entity_of_type_rolling_ring_connection(self, value: '_2043.RollingRingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft_to_mountable_component_connection(self) -> '_2046.ShaftToMountableComponentConnection':
        """ShaftToMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2046.ShaftToMountableComponentConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ShaftToMountableComponentConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_shaft_to_mountable_component_connection.setter
    def selected_design_entity_of_type_shaft_to_mountable_component_connection(self, value: '_2046.ShaftToMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear_mesh(self) -> '_2050.AGMAGleasonConicalGearMesh':
        """AGMAGleasonConicalGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2050.AGMAGleasonConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_agma_gleason_conical_gear_mesh.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear_mesh(self, value: '_2050.AGMAGleasonConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear_mesh(self) -> '_2052.BevelDifferentialGearMesh':
        """BevelDifferentialGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2052.BevelDifferentialGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_differential_gear_mesh.setter
    def selected_design_entity_of_type_bevel_differential_gear_mesh(self, value: '_2052.BevelDifferentialGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear_mesh(self) -> '_2054.BevelGearMesh':
        """BevelGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2054.BevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_gear_mesh.setter
    def selected_design_entity_of_type_bevel_gear_mesh(self, value: '_2054.BevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear_mesh(self) -> '_2056.ConceptGearMesh':
        """ConceptGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2056.ConceptGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_concept_gear_mesh.setter
    def selected_design_entity_of_type_concept_gear_mesh(self, value: '_2056.ConceptGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear_mesh(self) -> '_2058.ConicalGearMesh':
        """ConicalGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2058.ConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_conical_gear_mesh.setter
    def selected_design_entity_of_type_conical_gear_mesh(self, value: '_2058.ConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear_mesh(self) -> '_2060.CylindricalGearMesh':
        """CylindricalGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2060.CylindricalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cylindrical_gear_mesh.setter
    def selected_design_entity_of_type_cylindrical_gear_mesh(self, value: '_2060.CylindricalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear_mesh(self) -> '_2062.FaceGearMesh':
        """FaceGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2062.FaceGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_face_gear_mesh.setter
    def selected_design_entity_of_type_face_gear_mesh(self, value: '_2062.FaceGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear_mesh(self) -> '_2064.GearMesh':
        """GearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2064.GearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_gear_mesh.setter
    def selected_design_entity_of_type_gear_mesh(self, value: '_2064.GearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear_mesh(self) -> '_2066.HypoidGearMesh':
        """HypoidGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2066.HypoidGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_hypoid_gear_mesh.setter
    def selected_design_entity_of_type_hypoid_gear_mesh(self, value: '_2066.HypoidGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_2069.KlingelnbergCycloPalloidConicalGearMesh':
        """KlingelnbergCycloPalloidConicalGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2069.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self, value: '_2069.KlingelnbergCycloPalloidConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_2070.KlingelnbergCycloPalloidHypoidGearMesh':
        """KlingelnbergCycloPalloidHypoidGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2070.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, value: '_2070.KlingelnbergCycloPalloidHypoidGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2071.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        """KlingelnbergCycloPalloidSpiralBevelGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2071.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, value: '_2071.KlingelnbergCycloPalloidSpiralBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear_mesh(self) -> '_2074.SpiralBevelGearMesh':
        """SpiralBevelGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2074.SpiralBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_spiral_bevel_gear_mesh.setter
    def selected_design_entity_of_type_spiral_bevel_gear_mesh(self, value: '_2074.SpiralBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear_mesh(self) -> '_2076.StraightBevelDiffGearMesh':
        """StraightBevelDiffGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2076.StraightBevelDiffGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_diff_gear_mesh.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear_mesh(self, value: '_2076.StraightBevelDiffGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear_mesh(self) -> '_2078.StraightBevelGearMesh':
        """StraightBevelGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2078.StraightBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_gear_mesh.setter
    def selected_design_entity_of_type_straight_bevel_gear_mesh(self, value: '_2078.StraightBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear_mesh(self) -> '_2080.WormGearMesh':
        """WormGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2080.WormGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_worm_gear_mesh.setter
    def selected_design_entity_of_type_worm_gear_mesh(self, value: '_2080.WormGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear_mesh(self) -> '_2082.ZerolBevelGearMesh':
        """ZerolBevelGearMesh: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2082.ZerolBevelGearMesh.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGearMesh. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_zerol_bevel_gear_mesh.setter
    def selected_design_entity_of_type_zerol_bevel_gear_mesh(self, value: '_2082.ZerolBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2086.CycloidalDiscCentralBearingConnection':
        """CycloidalDiscCentralBearingConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2086.CycloidalDiscCentralBearingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cycloidal_disc_central_bearing_connection.setter
    def selected_design_entity_of_type_cycloidal_disc_central_bearing_connection(self, value: '_2086.CycloidalDiscCentralBearingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2089.CycloidalDiscPlanetaryBearingConnection':
        """CycloidalDiscPlanetaryBearingConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2089.CycloidalDiscPlanetaryBearingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection.setter
    def selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection(self, value: '_2089.CycloidalDiscPlanetaryBearingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_ring_pins_to_disc_connection(self) -> '_2092.RingPinsToDiscConnection':
        """RingPinsToDiscConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2092.RingPinsToDiscConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RingPinsToDiscConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_ring_pins_to_disc_connection.setter
    def selected_design_entity_of_type_ring_pins_to_disc_connection(self, value: '_2092.RingPinsToDiscConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch_connection(self) -> '_2093.ClutchConnection':
        """ClutchConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2093.ClutchConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ClutchConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_clutch_connection.setter
    def selected_design_entity_of_type_clutch_connection(self, value: '_2093.ClutchConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling_connection(self) -> '_2095.ConceptCouplingConnection':
        """ConceptCouplingConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2095.ConceptCouplingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCouplingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_concept_coupling_connection.setter
    def selected_design_entity_of_type_concept_coupling_connection(self, value: '_2095.ConceptCouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling_connection(self) -> '_2097.CouplingConnection':
        """CouplingConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2097.CouplingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CouplingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_coupling_connection.setter
    def selected_design_entity_of_type_coupling_connection(self, value: '_2097.CouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling_connection(self) -> '_2099.PartToPartShearCouplingConnection':
        """PartToPartShearCouplingConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2099.PartToPartShearCouplingConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCouplingConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_part_to_part_shear_coupling_connection.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling_connection(self, value: '_2099.PartToPartShearCouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper_connection(self) -> '_2101.SpringDamperConnection':
        """SpringDamperConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2101.SpringDamperConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamperConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_spring_damper_connection.setter
    def selected_design_entity_of_type_spring_damper_connection(self, value: '_2101.SpringDamperConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_connection(self) -> '_2103.TorqueConverterConnection':
        """TorqueConverterConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2103.TorqueConverterConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_torque_converter_connection.setter
    def selected_design_entity_of_type_torque_converter_connection(self, value: '_2103.TorqueConverterConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_assembly(self) -> '_2185.Assembly':
        """Assembly: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2185.Assembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Assembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_assembly.setter
    def selected_design_entity_of_type_assembly(self, value: '_2185.Assembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_assembly(self) -> '_2186.AbstractAssembly':
        """AbstractAssembly: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2186.AbstractAssembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractAssembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_abstract_assembly.setter
    def selected_design_entity_of_type_abstract_assembly(self, value: '_2186.AbstractAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft(self) -> '_2187.AbstractShaft':
        """AbstractShaft: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2187.AbstractShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_abstract_shaft.setter
    def selected_design_entity_of_type_abstract_shaft(self, value: '_2187.AbstractShaft'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft_or_housing(self) -> '_2188.AbstractShaftOrHousing':
        """AbstractShaftOrHousing: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2188.AbstractShaftOrHousing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaftOrHousing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_abstract_shaft_or_housing.setter
    def selected_design_entity_of_type_abstract_shaft_or_housing(self, value: '_2188.AbstractShaftOrHousing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bearing(self) -> '_2191.Bearing':
        """Bearing: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2191.Bearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Bearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bearing.setter
    def selected_design_entity_of_type_bearing(self, value: '_2191.Bearing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bolt(self) -> '_2193.Bolt':
        """Bolt: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2193.Bolt.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Bolt. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bolt.setter
    def selected_design_entity_of_type_bolt(self, value: '_2193.Bolt'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bolted_joint(self) -> '_2194.BoltedJoint':
        """BoltedJoint: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2194.BoltedJoint.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BoltedJoint. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bolted_joint.setter
    def selected_design_entity_of_type_bolted_joint(self, value: '_2194.BoltedJoint'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_component(self) -> '_2195.Component':
        """Component: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2195.Component.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Component. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_component.setter
    def selected_design_entity_of_type_component(self, value: '_2195.Component'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_connector(self) -> '_2198.Connector':
        """Connector: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2198.Connector.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Connector. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_connector.setter
    def selected_design_entity_of_type_connector(self, value: '_2198.Connector'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_datum(self) -> '_2199.Datum':
        """Datum: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2199.Datum.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Datum. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_datum.setter
    def selected_design_entity_of_type_datum(self, value: '_2199.Datum'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_external_cad_model(self) -> '_2202.ExternalCADModel':
        """ExternalCADModel: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2202.ExternalCADModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ExternalCADModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_external_cad_model.setter
    def selected_design_entity_of_type_external_cad_model(self, value: '_2202.ExternalCADModel'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_fe_part(self) -> '_2203.FEPart':
        """FEPart: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2203.FEPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FEPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_fe_part.setter
    def selected_design_entity_of_type_fe_part(self, value: '_2203.FEPart'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_flexible_pin_assembly(self) -> '_2204.FlexiblePinAssembly':
        """FlexiblePinAssembly: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2204.FlexiblePinAssembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FlexiblePinAssembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_flexible_pin_assembly.setter
    def selected_design_entity_of_type_flexible_pin_assembly(self, value: '_2204.FlexiblePinAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_guide_dxf_model(self) -> '_2205.GuideDxfModel':
        """GuideDxfModel: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2205.GuideDxfModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GuideDxfModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_guide_dxf_model.setter
    def selected_design_entity_of_type_guide_dxf_model(self, value: '_2205.GuideDxfModel'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_mass_disc(self) -> '_2212.MassDisc':
        """MassDisc: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2212.MassDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MassDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_mass_disc.setter
    def selected_design_entity_of_type_mass_disc(self, value: '_2212.MassDisc'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_measurement_component(self) -> '_2213.MeasurementComponent':
        """MeasurementComponent: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2213.MeasurementComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MeasurementComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_measurement_component.setter
    def selected_design_entity_of_type_measurement_component(self, value: '_2213.MeasurementComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_mountable_component(self) -> '_2214.MountableComponent':
        """MountableComponent: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2214.MountableComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MountableComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_mountable_component.setter
    def selected_design_entity_of_type_mountable_component(self, value: '_2214.MountableComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_oil_seal(self) -> '_2216.OilSeal':
        """OilSeal: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2216.OilSeal.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to OilSeal. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_oil_seal.setter
    def selected_design_entity_of_type_oil_seal(self, value: '_2216.OilSeal'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part(self) -> '_2218.Part':
        """Part: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2218.Part.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Part. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_part.setter
    def selected_design_entity_of_type_part(self, value: '_2218.Part'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planet_carrier(self) -> '_2219.PlanetCarrier':
        """PlanetCarrier: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2219.PlanetCarrier.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetCarrier. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_planet_carrier.setter
    def selected_design_entity_of_type_planet_carrier(self, value: '_2219.PlanetCarrier'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_point_load(self) -> '_2221.PointLoad':
        """PointLoad: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2221.PointLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PointLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_point_load.setter
    def selected_design_entity_of_type_point_load(self, value: '_2221.PointLoad'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_power_load(self) -> '_2222.PowerLoad':
        """PowerLoad: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2222.PowerLoad.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PowerLoad. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_power_load.setter
    def selected_design_entity_of_type_power_load(self, value: '_2222.PowerLoad'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_root_assembly(self) -> '_2224.RootAssembly':
        """RootAssembly: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2224.RootAssembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RootAssembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_root_assembly.setter
    def selected_design_entity_of_type_root_assembly(self, value: '_2224.RootAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_specialised_assembly(self) -> '_2226.SpecialisedAssembly':
        """SpecialisedAssembly: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2226.SpecialisedAssembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpecialisedAssembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_specialised_assembly.setter
    def selected_design_entity_of_type_specialised_assembly(self, value: '_2226.SpecialisedAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_unbalanced_mass(self) -> '_2227.UnbalancedMass':
        """UnbalancedMass: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2227.UnbalancedMass.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to UnbalancedMass. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_unbalanced_mass.setter
    def selected_design_entity_of_type_unbalanced_mass(self, value: '_2227.UnbalancedMass'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_virtual_component(self) -> '_2229.VirtualComponent':
        """VirtualComponent: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2229.VirtualComponent.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to VirtualComponent. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_virtual_component.setter
    def selected_design_entity_of_type_virtual_component(self, value: '_2229.VirtualComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft(self) -> '_2232.Shaft':
        """Shaft: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2232.Shaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Shaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_shaft.setter
    def selected_design_entity_of_type_shaft(self, value: '_2232.Shaft'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear(self) -> '_2262.AGMAGleasonConicalGear':
        """AGMAGleasonConicalGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2262.AGMAGleasonConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_agma_gleason_conical_gear.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear(self, value: '_2262.AGMAGleasonConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear_set(self) -> '_2263.AGMAGleasonConicalGearSet':
        """AGMAGleasonConicalGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2263.AGMAGleasonConicalGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_agma_gleason_conical_gear_set.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear_set(self, value: '_2263.AGMAGleasonConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear(self) -> '_2264.BevelDifferentialGear':
        """BevelDifferentialGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2264.BevelDifferentialGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_differential_gear.setter
    def selected_design_entity_of_type_bevel_differential_gear(self, value: '_2264.BevelDifferentialGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear_set(self) -> '_2265.BevelDifferentialGearSet':
        """BevelDifferentialGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2265.BevelDifferentialGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_differential_gear_set.setter
    def selected_design_entity_of_type_bevel_differential_gear_set(self, value: '_2265.BevelDifferentialGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_planet_gear(self) -> '_2266.BevelDifferentialPlanetGear':
        """BevelDifferentialPlanetGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2266.BevelDifferentialPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_differential_planet_gear.setter
    def selected_design_entity_of_type_bevel_differential_planet_gear(self, value: '_2266.BevelDifferentialPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_sun_gear(self) -> '_2267.BevelDifferentialSunGear':
        """BevelDifferentialSunGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2267.BevelDifferentialSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_differential_sun_gear.setter
    def selected_design_entity_of_type_bevel_differential_sun_gear(self, value: '_2267.BevelDifferentialSunGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear(self) -> '_2268.BevelGear':
        """BevelGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2268.BevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_gear.setter
    def selected_design_entity_of_type_bevel_gear(self, value: '_2268.BevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear_set(self) -> '_2269.BevelGearSet':
        """BevelGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2269.BevelGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_bevel_gear_set.setter
    def selected_design_entity_of_type_bevel_gear_set(self, value: '_2269.BevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear(self) -> '_2270.ConceptGear':
        """ConceptGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2270.ConceptGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_concept_gear.setter
    def selected_design_entity_of_type_concept_gear(self, value: '_2270.ConceptGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear_set(self) -> '_2271.ConceptGearSet':
        """ConceptGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2271.ConceptGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_concept_gear_set.setter
    def selected_design_entity_of_type_concept_gear_set(self, value: '_2271.ConceptGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear(self) -> '_2272.ConicalGear':
        """ConicalGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2272.ConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_conical_gear.setter
    def selected_design_entity_of_type_conical_gear(self, value: '_2272.ConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear_set(self) -> '_2273.ConicalGearSet':
        """ConicalGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2273.ConicalGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_conical_gear_set.setter
    def selected_design_entity_of_type_conical_gear_set(self, value: '_2273.ConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear(self) -> '_2274.CylindricalGear':
        """CylindricalGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2274.CylindricalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cylindrical_gear.setter
    def selected_design_entity_of_type_cylindrical_gear(self, value: '_2274.CylindricalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear_set(self) -> '_2275.CylindricalGearSet':
        """CylindricalGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2275.CylindricalGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cylindrical_gear_set.setter
    def selected_design_entity_of_type_cylindrical_gear_set(self, value: '_2275.CylindricalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_planet_gear(self) -> '_2276.CylindricalPlanetGear':
        """CylindricalPlanetGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2276.CylindricalPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cylindrical_planet_gear.setter
    def selected_design_entity_of_type_cylindrical_planet_gear(self, value: '_2276.CylindricalPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear(self) -> '_2277.FaceGear':
        """FaceGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2277.FaceGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_face_gear.setter
    def selected_design_entity_of_type_face_gear(self, value: '_2277.FaceGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear_set(self) -> '_2278.FaceGearSet':
        """FaceGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2278.FaceGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_face_gear_set.setter
    def selected_design_entity_of_type_face_gear_set(self, value: '_2278.FaceGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear(self) -> '_2279.Gear':
        """Gear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2279.Gear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Gear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_gear.setter
    def selected_design_entity_of_type_gear(self, value: '_2279.Gear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear_set(self) -> '_2281.GearSet':
        """GearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2281.GearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_gear_set.setter
    def selected_design_entity_of_type_gear_set(self, value: '_2281.GearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear(self) -> '_2283.HypoidGear':
        """HypoidGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2283.HypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_hypoid_gear.setter
    def selected_design_entity_of_type_hypoid_gear(self, value: '_2283.HypoidGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear_set(self) -> '_2284.HypoidGearSet':
        """HypoidGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2284.HypoidGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_hypoid_gear_set.setter
    def selected_design_entity_of_type_hypoid_gear_set(self, value: '_2284.HypoidGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2285.KlingelnbergCycloPalloidConicalGear':
        """KlingelnbergCycloPalloidConicalGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2285.KlingelnbergCycloPalloidConicalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear(self, value: '_2285.KlingelnbergCycloPalloidConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2286.KlingelnbergCycloPalloidConicalGearSet':
        """KlingelnbergCycloPalloidConicalGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2286.KlingelnbergCycloPalloidConicalGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self, value: '_2286.KlingelnbergCycloPalloidConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2287.KlingelnbergCycloPalloidHypoidGear':
        """KlingelnbergCycloPalloidHypoidGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2287.KlingelnbergCycloPalloidHypoidGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self, value: '_2287.KlingelnbergCycloPalloidHypoidGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2288.KlingelnbergCycloPalloidHypoidGearSet':
        """KlingelnbergCycloPalloidHypoidGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2288.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self, value: '_2288.KlingelnbergCycloPalloidHypoidGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2289.KlingelnbergCycloPalloidSpiralBevelGear':
        """KlingelnbergCycloPalloidSpiralBevelGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2289.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, value: '_2289.KlingelnbergCycloPalloidSpiralBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2290.KlingelnbergCycloPalloidSpiralBevelGearSet':
        """KlingelnbergCycloPalloidSpiralBevelGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2290.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, value: '_2290.KlingelnbergCycloPalloidSpiralBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planetary_gear_set(self) -> '_2291.PlanetaryGearSet':
        """PlanetaryGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2291.PlanetaryGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetaryGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_planetary_gear_set.setter
    def selected_design_entity_of_type_planetary_gear_set(self, value: '_2291.PlanetaryGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear(self) -> '_2292.SpiralBevelGear':
        """SpiralBevelGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2292.SpiralBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_spiral_bevel_gear.setter
    def selected_design_entity_of_type_spiral_bevel_gear(self, value: '_2292.SpiralBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear_set(self) -> '_2293.SpiralBevelGearSet':
        """SpiralBevelGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2293.SpiralBevelGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_spiral_bevel_gear_set.setter
    def selected_design_entity_of_type_spiral_bevel_gear_set(self, value: '_2293.SpiralBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear(self) -> '_2294.StraightBevelDiffGear':
        """StraightBevelDiffGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2294.StraightBevelDiffGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_diff_gear.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear(self, value: '_2294.StraightBevelDiffGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear_set(self) -> '_2295.StraightBevelDiffGearSet':
        """StraightBevelDiffGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2295.StraightBevelDiffGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_diff_gear_set.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear_set(self, value: '_2295.StraightBevelDiffGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear(self) -> '_2296.StraightBevelGear':
        """StraightBevelGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2296.StraightBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_gear.setter
    def selected_design_entity_of_type_straight_bevel_gear(self, value: '_2296.StraightBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear_set(self) -> '_2297.StraightBevelGearSet':
        """StraightBevelGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2297.StraightBevelGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_gear_set.setter
    def selected_design_entity_of_type_straight_bevel_gear_set(self, value: '_2297.StraightBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_planet_gear(self) -> '_2298.StraightBevelPlanetGear':
        """StraightBevelPlanetGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2298.StraightBevelPlanetGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelPlanetGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_planet_gear.setter
    def selected_design_entity_of_type_straight_bevel_planet_gear(self, value: '_2298.StraightBevelPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_sun_gear(self) -> '_2299.StraightBevelSunGear':
        """StraightBevelSunGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2299.StraightBevelSunGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelSunGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_straight_bevel_sun_gear.setter
    def selected_design_entity_of_type_straight_bevel_sun_gear(self, value: '_2299.StraightBevelSunGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear(self) -> '_2300.WormGear':
        """WormGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2300.WormGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_worm_gear.setter
    def selected_design_entity_of_type_worm_gear(self, value: '_2300.WormGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear_set(self) -> '_2301.WormGearSet':
        """WormGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2301.WormGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_worm_gear_set.setter
    def selected_design_entity_of_type_worm_gear_set(self, value: '_2301.WormGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear(self) -> '_2302.ZerolBevelGear':
        """ZerolBevelGear: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2302.ZerolBevelGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_zerol_bevel_gear.setter
    def selected_design_entity_of_type_zerol_bevel_gear(self, value: '_2302.ZerolBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear_set(self) -> '_2303.ZerolBevelGearSet':
        """ZerolBevelGearSet: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2303.ZerolBevelGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_zerol_bevel_gear_set.setter
    def selected_design_entity_of_type_zerol_bevel_gear_set(self, value: '_2303.ZerolBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_assembly(self) -> '_2317.CycloidalAssembly':
        """CycloidalAssembly: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2317.CycloidalAssembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalAssembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cycloidal_assembly.setter
    def selected_design_entity_of_type_cycloidal_assembly(self, value: '_2317.CycloidalAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc(self) -> '_2318.CycloidalDisc':
        """CycloidalDisc: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2318.CycloidalDisc.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDisc. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cycloidal_disc.setter
    def selected_design_entity_of_type_cycloidal_disc(self, value: '_2318.CycloidalDisc'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_ring_pins(self) -> '_2319.RingPins':
        """RingPins: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2319.RingPins.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RingPins. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_ring_pins.setter
    def selected_design_entity_of_type_ring_pins(self, value: '_2319.RingPins'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_belt_drive(self) -> '_2325.BeltDrive':
        """BeltDrive: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2325.BeltDrive.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BeltDrive. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_belt_drive.setter
    def selected_design_entity_of_type_belt_drive(self, value: '_2325.BeltDrive'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch(self) -> '_2327.Clutch':
        """Clutch: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2327.Clutch.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Clutch. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_clutch.setter
    def selected_design_entity_of_type_clutch(self, value: '_2327.Clutch'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch_half(self) -> '_2328.ClutchHalf':
        """ClutchHalf: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2328.ClutchHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ClutchHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_clutch_half.setter
    def selected_design_entity_of_type_clutch_half(self, value: '_2328.ClutchHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling(self) -> '_2330.ConceptCoupling':
        """ConceptCoupling: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2330.ConceptCoupling.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCoupling. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_concept_coupling.setter
    def selected_design_entity_of_type_concept_coupling(self, value: '_2330.ConceptCoupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling_half(self) -> '_2331.ConceptCouplingHalf':
        """ConceptCouplingHalf: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2331.ConceptCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_concept_coupling_half.setter
    def selected_design_entity_of_type_concept_coupling_half(self, value: '_2331.ConceptCouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling(self) -> '_2332.Coupling':
        """Coupling: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2332.Coupling.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Coupling. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_coupling.setter
    def selected_design_entity_of_type_coupling(self, value: '_2332.Coupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling_half(self) -> '_2333.CouplingHalf':
        """CouplingHalf: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2333.CouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_coupling_half.setter
    def selected_design_entity_of_type_coupling_half(self, value: '_2333.CouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt(self) -> '_2335.CVT':
        """CVT: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2335.CVT.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVT. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cvt.setter
    def selected_design_entity_of_type_cvt(self, value: '_2335.CVT'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt_pulley(self) -> '_2336.CVTPulley':
        """CVTPulley: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2336.CVTPulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVTPulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_cvt_pulley.setter
    def selected_design_entity_of_type_cvt_pulley(self, value: '_2336.CVTPulley'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling(self) -> '_2337.PartToPartShearCoupling':
        """PartToPartShearCoupling: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2337.PartToPartShearCoupling.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCoupling. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_part_to_part_shear_coupling.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling(self, value: '_2337.PartToPartShearCoupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling_half(self) -> '_2338.PartToPartShearCouplingHalf':
        """PartToPartShearCouplingHalf: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2338.PartToPartShearCouplingHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCouplingHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_part_to_part_shear_coupling_half.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling_half(self, value: '_2338.PartToPartShearCouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_pulley(self) -> '_2339.Pulley':
        """Pulley: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2339.Pulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Pulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_pulley.setter
    def selected_design_entity_of_type_pulley(self, value: '_2339.Pulley'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring(self) -> '_2345.RollingRing':
        """RollingRing: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2345.RollingRing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_rolling_ring.setter
    def selected_design_entity_of_type_rolling_ring(self, value: '_2345.RollingRing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring_assembly(self) -> '_2346.RollingRingAssembly':
        """RollingRingAssembly: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2346.RollingRingAssembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRingAssembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_rolling_ring_assembly.setter
    def selected_design_entity_of_type_rolling_ring_assembly(self, value: '_2346.RollingRingAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft_hub_connection(self) -> '_2347.ShaftHubConnection':
        """ShaftHubConnection: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2347.ShaftHubConnection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ShaftHubConnection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_shaft_hub_connection.setter
    def selected_design_entity_of_type_shaft_hub_connection(self, value: '_2347.ShaftHubConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper(self) -> '_2349.SpringDamper':
        """SpringDamper: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2349.SpringDamper.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamper. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_spring_damper.setter
    def selected_design_entity_of_type_spring_damper(self, value: '_2349.SpringDamper'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper_half(self) -> '_2350.SpringDamperHalf':
        """SpringDamperHalf: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2350.SpringDamperHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamperHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_spring_damper_half.setter
    def selected_design_entity_of_type_spring_damper_half(self, value: '_2350.SpringDamperHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser(self) -> '_2351.Synchroniser':
        """Synchroniser: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2351.Synchroniser.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Synchroniser. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_synchroniser.setter
    def selected_design_entity_of_type_synchroniser(self, value: '_2351.Synchroniser'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_half(self) -> '_2353.SynchroniserHalf':
        """SynchroniserHalf: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2353.SynchroniserHalf.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserHalf. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_synchroniser_half.setter
    def selected_design_entity_of_type_synchroniser_half(self, value: '_2353.SynchroniserHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_part(self) -> '_2354.SynchroniserPart':
        """SynchroniserPart: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2354.SynchroniserPart.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserPart. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_synchroniser_part.setter
    def selected_design_entity_of_type_synchroniser_part(self, value: '_2354.SynchroniserPart'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_sleeve(self) -> '_2355.SynchroniserSleeve':
        """SynchroniserSleeve: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2355.SynchroniserSleeve.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserSleeve. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_synchroniser_sleeve.setter
    def selected_design_entity_of_type_synchroniser_sleeve(self, value: '_2355.SynchroniserSleeve'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter(self) -> '_2356.TorqueConverter':
        """TorqueConverter: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2356.TorqueConverter.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverter. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_torque_converter.setter
    def selected_design_entity_of_type_torque_converter(self, value: '_2356.TorqueConverter'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_pump(self) -> '_2357.TorqueConverterPump':
        """TorqueConverterPump: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2357.TorqueConverterPump.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterPump. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_torque_converter_pump.setter
    def selected_design_entity_of_type_torque_converter_pump(self, value: '_2357.TorqueConverterPump'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_turbine(self) -> '_2359.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'SelectedDesignEntity' is the original name of this property."""

        temp = self.wrapped.SelectedDesignEntity

        if temp is None:
            return None

        if _2359.TorqueConverterTurbine.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterTurbine. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @selected_design_entity_of_type_torque_converter_turbine.setter
    def selected_design_entity_of_type_torque_converter_turbine(self, value: '_2359.TorqueConverterTurbine'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def report_names(self) -> 'List[str]':
        """List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReportNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)
        return value

    @staticmethod
    def get_mastagui(process_id: 'int') -> 'MASTAGUI':
        """ 'GetMASTAGUI' is the original name of this method.

        Args:
            process_id (int)

        Returns:
            mastapy.system_model_gui.MASTAGUI
        """

        process_id = int(process_id)
        method_result = MASTAGUI.TYPE.GetMASTAGUI(process_id if process_id else 0)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def pause(self):
        """ 'Pause' is the original name of this method."""

        self.wrapped.Pause()

    def resume(self):
        """ 'Resume' is the original name of this method."""

        self.wrapped.Resume()

    def start_remoting(self):
        """ 'StartRemoting' is the original name of this method."""

        self.wrapped.StartRemoting()

    def stop_remoting(self):
        """ 'StopRemoting' is the original name of this method."""

        self.wrapped.StopRemoting()

    def add_fe_substructure_from_data(self, vertices_and_facets: '_1318.FacetedBody', dimensions: 'Dict[str, _150.GeometryModellerDimension]', moniker: 'str'):
        """ 'AddFESubstructureFromData' is the original name of this method.

        Args:
            vertices_and_facets (mastapy.math_utility.FacetedBody)
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension])
            moniker (str)
        """

        moniker = str(moniker)
        self.wrapped.AddFESubstructureFromData(vertices_and_facets.wrapped if vertices_and_facets else None, dimensions, moniker if moniker else '')

    def add_fe_substructure_from_file(self, length_scale: 'float', stl_file_name: 'str', dimensions: 'Dict[str, _150.GeometryModellerDimension]'):
        """ 'AddFESubstructureFromFile' is the original name of this method.

        Args:
            length_scale (float)
            stl_file_name (str)
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension])
        """

        length_scale = float(length_scale)
        stl_file_name = str(stl_file_name)
        self.wrapped.AddFESubstructureFromFile(length_scale if length_scale else 0.0, stl_file_name if stl_file_name else '', dimensions)

    def add_line_from_geometry_modeller(self, circles_on_axis: '_1299.CirclesOnAxis'):
        """ 'AddLineFromGeometryModeller' is the original name of this method.

        Args:
            circles_on_axis (mastapy.math_utility.CirclesOnAxis)
        """

        self.wrapped.AddLineFromGeometryModeller(circles_on_axis.wrapped if circles_on_axis else None)

    def circle_pairs_from_geometry_modeller(self, preselection_circles: '_1299.CirclesOnAxis', selected_circles: 'List[_1299.CirclesOnAxis]'):
        """ 'CirclePairsFromGeometryModeller' is the original name of this method.

        Args:
            preselection_circles (mastapy.math_utility.CirclesOnAxis)
            selected_circles (List[mastapy.math_utility.CirclesOnAxis])
        """

        selected_circles = conversion.mp_to_pn_objects_in_list(selected_circles)
        self.wrapped.CirclePairsFromGeometryModeller(preselection_circles.wrapped if preselection_circles else None, selected_circles)

    def create_geometry_modeller_dimension(self) -> '_150.GeometryModellerDimension':
        """ 'CreateGeometryModellerDimension' is the original name of this method.

        Returns:
            mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension
        """

        method_result = self.wrapped.CreateGeometryModellerDimension()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def create_new_circles_on_axis(self) -> '_1299.CirclesOnAxis':
        """ 'CreateNewCirclesOnAxis' is the original name of this method.

        Returns:
            mastapy.math_utility.CirclesOnAxis
        """

        method_result = self.wrapped.CreateNewCirclesOnAxis()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def create_new_faceted_body(self) -> '_1318.FacetedBody':
        """ 'CreateNewFacetedBody' is the original name of this method.

        Returns:
            mastapy.math_utility.FacetedBody
        """

        method_result = self.wrapped.CreateNewFacetedBody()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def flag_message_received(self):
        """ 'FlagMessageReceived' is the original name of this method."""

        self.wrapped.FlagMessageReceived()

    def geometry_modeller_document_loaded(self):
        """ 'GeometryModellerDocumentLoaded' is the original name of this method."""

        self.wrapped.GeometryModellerDocumentLoaded()

    def move_selected_component(self, origin: 'Vector3D', axis: 'Vector3D'):
        """ 'MoveSelectedComponent' is the original name of this method.

        Args:
            origin (Vector3D)
            axis (Vector3D)
        """

        origin = conversion.mp_to_pn_vector3d(origin)
        axis = conversion.mp_to_pn_vector3d(axis)
        self.wrapped.MoveSelectedComponent(origin, axis)

    def new_dimensions(self, dimensions: 'Dict[str, _150.GeometryModellerDimension]'):
        """ 'NewDimensions' is the original name of this method.

        Args:
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension])
        """

        self.wrapped.NewDimensions(dimensions)

    def new_mesh_data(self, vertices_and_facets: '_1318.FacetedBody'):
        """ 'NewMeshData' is the original name of this method.

        Args:
            vertices_and_facets (mastapy.math_utility.FacetedBody)
        """

        self.wrapped.NewMeshData.Overloads[_FACETED_BODY](vertices_and_facets.wrapped if vertices_and_facets else None)

    def new_mesh_data_from_file(self, stl_file_name: 'str'):
        """ 'NewMeshData' is the original name of this method.

        Args:
            stl_file_name (str)
        """

        stl_file_name = str(stl_file_name)
        self.wrapped.NewMeshData.Overloads[_STRING](stl_file_name if stl_file_name else '')

    def open_design_in_new_tab(self, design: '_1956.Design'):
        """ 'OpenDesignInNewTab' is the original name of this method.

        Args:
            design (mastapy.system_model.Design)
        """

        self.wrapped.OpenDesignInNewTab(design.wrapped if design else None)

    def run_command(self, command: 'str'):
        """ 'RunCommand' is the original name of this method.

        Args:
            command (str)
        """

        command = str(command)
        self.wrapped.RunCommand(command if command else '')

    def select_tab(self, tab_text: 'str'):
        """ 'SelectTab' is the original name of this method.

        Args:
            tab_text (str)
        """

        tab_text = str(tab_text)
        self.wrapped.SelectTab(tab_text if tab_text else '')

    def set_error(self, error: 'str'):
        """ 'SetError' is the original name of this method.

        Args:
            error (str)
        """

        error = str(error)
        self.wrapped.SetError(error if error else '')

    def show_boxes(self, small_box: 'List[Vector3D]', big_box: 'List[Vector3D]'):
        """ 'ShowBoxes' is the original name of this method.

        Args:
            small_box (List[Vector3D])
            big_box (List[Vector3D])
        """

        small_box = conversion.mp_to_pn_objects_in_list(small_box)
        big_box = conversion.mp_to_pn_objects_in_list(big_box)
        self.wrapped.ShowBoxes(small_box, big_box)

    def output_default_report_to(self, file_path: 'str'):
        """ 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else '')

    def get_default_report_with_encoded_images(self) -> 'str':
        """ 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        """ 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else '')

    def output_active_report_as_text_to(self, file_path: 'str'):
        """ 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else '')

    def get_active_report_with_encoded_images(self) -> 'str':
        """ 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else '', file_path if file_path else '')

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        """ 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        """

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else '')
        return method_result
