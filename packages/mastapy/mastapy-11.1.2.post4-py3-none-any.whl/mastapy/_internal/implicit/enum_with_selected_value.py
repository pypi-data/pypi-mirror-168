"""enum_with_selected_value.py

Implementations of 'EnumWithSelectedValue' in Python.
As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""


from enum import Enum
from typing import List

from mastapy._internal import (
    mixins, enum_with_selected_value_runtime, constructor, conversion
)
from mastapy.shafts import _33, _42
from mastapy._internal.python_net import python_net_import
from mastapy.nodal_analysis import (
    _68, _87, _74, _83,
    _50
)
from mastapy.nodal_analysis.varying_input_components import _94
from mastapy.fe_tools.enums import _1194
from mastapy.materials import _237, _241, _227
from mastapy.gears import _309, _307, _310
from mastapy.math_utility import (
    _1317, _1298, _1297, _1301,
    _1312, _1313, _1310
)
from mastapy.gears.rating.cylindrical import _448, _449
from mastapy.gears.micro_geometry import (
    _539, _540, _541, _542
)
from mastapy.gears.manufacturing.cylindrical import (
    _589, _590, _593, _575
)
from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _611, _612, _609
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _624
from mastapy.geometry.two_d.curves import _285
from mastapy.gears.gear_designs.cylindrical import _1040, _1011, _1032
from mastapy.gears.gear_designs.conical import _1111, _1112, _1123
from mastapy.gears.gear_set_pareto_optimiser import _869
from mastapy.utility.model_validation import _1571, _1574
from mastapy.gears.ltca import _793
from mastapy.gears.gear_designs.creation_options import _1100
from mastapy.gears.gear_designs.bevel import _1144, _1133
from mastapy.fe_tools.vfx_tools.vfx_enums import _1191, _1192
from mastapy.bearings.tolerances import (
    _1674, _1687, _1667, _1666,
    _1668
)
from mastapy.detailed_rigid_connectors.splines import (
    _1202, _1225, _1211, _1212,
    _1220, _1226, _1203
)
from mastapy.detailed_rigid_connectors.interference_fits import _1256
from mastapy.utility import _1385
from mastapy.utility.report import _1526
from mastapy.bearings import (
    _1656, _1649, _1657, _1637,
    _1638, _1660, _1662, _1644
)
from mastapy.bearings.bearing_results import (
    _1725, _1724, _1726, _1727
)
from mastapy.materials.efficiency import _266, _274
from mastapy.system_model.part_model import _2225
from mastapy.system_model.drawing.options import _2013
from mastapy.utility.enums import _1599, _1600, _1598
from mastapy.system_model.fe import (
    _2117, _2161, _2138, _2114,
    _2148
)
from mastapy.system_model import (
    _1961, _1973, _1968, _1971
)
from mastapy.nodal_analysis.fe_export_utility import _158, _157
from mastapy.system_model.part_model.couplings import _2340, _2343, _2344
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4089
from mastapy.system_model.analyses_and_results.static_loads import (
    _6541, _6630, _6704, _6621,
    _6665, _6705
)
from mastapy.system_model.analyses_and_results.mbd_analyses import (
    _5121, _5173, _5218, _5243
)
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5477, _5495
from mastapy.bearings.bearing_results.rolling import _1734
from mastapy.bearings.bearing_results.rolling.iso_rating_results import _1868
from mastapy.math_utility.hertzian_contact import _1378
from mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition import _6719

_ARRAY = python_net_import('System', 'Array')
_ENUM_WITH_SELECTED_VALUE = python_net_import('SMT.MastaAPI.Utility.Property', 'EnumWithSelectedValue')


__docformat__ = 'restructuredtext en'
__all__ = (
    'EnumWithSelectedValue_ShaftRatingMethod', 'EnumWithSelectedValue_SurfaceFinishes',
    'EnumWithSelectedValue_IntegrationMethod', 'EnumWithSelectedValue_ValueInputOption',
    'EnumWithSelectedValue_SinglePointSelectionMethod', 'EnumWithSelectedValue_ModeInputType',
    'EnumWithSelectedValue_MaterialPropertyClass', 'EnumWithSelectedValue_LubricantDefinition',
    'EnumWithSelectedValue_LubricantViscosityClassISO', 'EnumWithSelectedValue_MicroGeometryModel',
    'EnumWithSelectedValue_ExtrapolationOptions', 'EnumWithSelectedValue_CylindricalGearRatingMethods',
    'EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod', 'EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod',
    'EnumWithSelectedValue_LocationOfEvaluationLowerLimit', 'EnumWithSelectedValue_LocationOfEvaluationUpperLimit',
    'EnumWithSelectedValue_LocationOfRootReliefEvaluation', 'EnumWithSelectedValue_LocationOfTipReliefEvaluation',
    'EnumWithSelectedValue_CylindricalMftFinishingMethods', 'EnumWithSelectedValue_CylindricalMftRoughingMethods',
    'EnumWithSelectedValue_MicroGeometryDefinitionMethod', 'EnumWithSelectedValue_MicroGeometryDefinitionType',
    'EnumWithSelectedValue_ChartType', 'EnumWithSelectedValue_Flank',
    'EnumWithSelectedValue_ActiveProcessMethod', 'EnumWithSelectedValue_CutterFlankSections',
    'EnumWithSelectedValue_BasicCurveTypes', 'EnumWithSelectedValue_ThicknessType',
    'EnumWithSelectedValue_ConicalMachineSettingCalculationMethods', 'EnumWithSelectedValue_ConicalManufactureMethods',
    'EnumWithSelectedValue_CandidateDisplayChoice', 'EnumWithSelectedValue_Severity',
    'EnumWithSelectedValue_GeometrySpecificationType', 'EnumWithSelectedValue_StatusItemSeverity',
    'EnumWithSelectedValue_LubricationMethods', 'EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod',
    'EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods', 'EnumWithSelectedValue_ContactResultType',
    'EnumWithSelectedValue_StressResultsType', 'EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption',
    'EnumWithSelectedValue_ToothThicknessSpecificationMethod', 'EnumWithSelectedValue_LoadDistributionFactorMethods',
    'EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods', 'EnumWithSelectedValue_ProSolveMpcType',
    'EnumWithSelectedValue_ProSolveSolverType', 'EnumWithSelectedValue_ITDesignation',
    'EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption', 'EnumWithSelectedValue_SplineRatingTypes',
    'EnumWithSelectedValue_Modules', 'EnumWithSelectedValue_PressureAngleTypes',
    'EnumWithSelectedValue_SplineFitClassType', 'EnumWithSelectedValue_SplineToleranceClassTypes',
    'EnumWithSelectedValue_Table4JointInterfaceTypes', 'EnumWithSelectedValue_ExecutableDirectoryCopier_Option',
    'EnumWithSelectedValue_CadPageOrientation', 'EnumWithSelectedValue_RollerBearingProfileTypes',
    'EnumWithSelectedValue_FluidFilmTemperatureOptions', 'EnumWithSelectedValue_SupportToleranceLocationDesignation',
    'EnumWithSelectedValue_LoadedBallElementPropertyType', 'EnumWithSelectedValue_RollingBearingArrangement',
    'EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod', 'EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod',
    'EnumWithSelectedValue_RollingBearingRaceType', 'EnumWithSelectedValue_RotationalDirections',
    'EnumWithSelectedValue_BearingEfficiencyRatingMethod', 'EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing',
    'EnumWithSelectedValue_ExcitationAnalysisViewOption', 'EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection',
    'EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection', 'EnumWithSelectedValue_ComponentOrientationOption',
    'EnumWithSelectedValue_Axis', 'EnumWithSelectedValue_AlignmentAxis',
    'EnumWithSelectedValue_DesignEntityId', 'EnumWithSelectedValue_ThermalExpansionOption',
    'EnumWithSelectedValue_FESubstructureType', 'EnumWithSelectedValue_FEExportFormat',
    'EnumWithSelectedValue_ThreeDViewContourOption', 'EnumWithSelectedValue_BoundaryConditionType',
    'EnumWithSelectedValue_BearingNodeOption', 'EnumWithSelectedValue_LinkNodeSource',
    'EnumWithSelectedValue_BearingToleranceClass', 'EnumWithSelectedValue_BearingModel',
    'EnumWithSelectedValue_PreloadType', 'EnumWithSelectedValue_RaceAxialMountingType',
    'EnumWithSelectedValue_RaceRadialMountingType', 'EnumWithSelectedValue_InternalClearanceClass',
    'EnumWithSelectedValue_BearingToleranceDefinitionOptions', 'EnumWithSelectedValue_OilSealLossCalculationMethod',
    'EnumWithSelectedValue_PowerLoadType', 'EnumWithSelectedValue_RigidConnectorStiffnessType',
    'EnumWithSelectedValue_RigidConnectorToothSpacingType', 'EnumWithSelectedValue_RigidConnectorTypes',
    'EnumWithSelectedValue_FitTypes', 'EnumWithSelectedValue_DoeValueSpecificationOption',
    'EnumWithSelectedValue_AnalysisType', 'EnumWithSelectedValue_BarModelExportType',
    'EnumWithSelectedValue_ComplexPartDisplayOption', 'EnumWithSelectedValue_DynamicsResponseScaling',
    'EnumWithSelectedValue_DynamicsResponseType', 'EnumWithSelectedValue_BearingStiffnessModel',
    'EnumWithSelectedValue_GearMeshStiffnessModel', 'EnumWithSelectedValue_ShaftAndHousingFlexibilityOption',
    'EnumWithSelectedValue_ExportOutputType', 'EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput',
    'EnumWithSelectedValue_FrictionModelForGyroscopicMoment', 'EnumWithSelectedValue_MeshStiffnessModel',
    'EnumWithSelectedValue_StressConcentrationMethod', 'EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod',
    'EnumWithSelectedValue_HarmonicLoadDataType', 'EnumWithSelectedValue_TorqueRippleInputType',
    'EnumWithSelectedValue_HarmonicExcitationType', 'EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification',
    'EnumWithSelectedValue_TorqueSpecificationForSystemDeflection', 'EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod',
    'EnumWithSelectedValue_TorqueConverterLockupRule', 'EnumWithSelectedValue_DegreesOfFreedom',
    'EnumWithSelectedValue_DestinationDesignState'
)


class EnumWithSelectedValue_ShaftRatingMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ShaftRatingMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftRatingMethod' types.
    """
    __qualname__ = 'ShaftRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_33.ShaftRatingMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _33.ShaftRatingMethod

    @classmethod
    def implicit_type(cls) -> '_33.ShaftRatingMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _33.ShaftRatingMethod.type_()

    @property
    def selected_value(self) -> '_33.ShaftRatingMethod':
        """ShaftRatingMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_33.ShaftRatingMethod]':
        """List[ShaftRatingMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_SurfaceFinishes(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_SurfaceFinishes

    A specific implementation of 'EnumWithSelectedValue' for 'SurfaceFinishes' types.
    """
    __qualname__ = 'SurfaceFinishes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_42.SurfaceFinishes':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _42.SurfaceFinishes

    @classmethod
    def implicit_type(cls) -> '_42.SurfaceFinishes.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _42.SurfaceFinishes.type_()

    @property
    def selected_value(self) -> '_42.SurfaceFinishes':
        """SurfaceFinishes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_42.SurfaceFinishes]':
        """List[SurfaceFinishes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_IntegrationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_IntegrationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'IntegrationMethod' types.
    """
    __qualname__ = 'IntegrationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_68.IntegrationMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _68.IntegrationMethod

    @classmethod
    def implicit_type(cls) -> '_68.IntegrationMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _68.IntegrationMethod.type_()

    @property
    def selected_value(self) -> '_68.IntegrationMethod':
        """IntegrationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_68.IntegrationMethod]':
        """List[IntegrationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ValueInputOption(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ValueInputOption

    A specific implementation of 'EnumWithSelectedValue' for 'ValueInputOption' types.
    """
    __qualname__ = 'ValueInputOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_87.ValueInputOption':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _87.ValueInputOption

    @classmethod
    def implicit_type(cls) -> '_87.ValueInputOption.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _87.ValueInputOption.type_()

    @property
    def selected_value(self) -> '_87.ValueInputOption':
        """ValueInputOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_87.ValueInputOption]':
        """List[ValueInputOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_SinglePointSelectionMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_SinglePointSelectionMethod

    A specific implementation of 'EnumWithSelectedValue' for 'SinglePointSelectionMethod' types.
    """
    __qualname__ = 'SinglePointSelectionMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_94.SinglePointSelectionMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _94.SinglePointSelectionMethod

    @classmethod
    def implicit_type(cls) -> '_94.SinglePointSelectionMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _94.SinglePointSelectionMethod.type_()

    @property
    def selected_value(self) -> '_94.SinglePointSelectionMethod':
        """SinglePointSelectionMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_94.SinglePointSelectionMethod]':
        """List[SinglePointSelectionMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ModeInputType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ModeInputType

    A specific implementation of 'EnumWithSelectedValue' for 'ModeInputType' types.
    """
    __qualname__ = 'ModeInputType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_74.ModeInputType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _74.ModeInputType

    @classmethod
    def implicit_type(cls) -> '_74.ModeInputType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _74.ModeInputType.type_()

    @property
    def selected_value(self) -> '_74.ModeInputType':
        """ModeInputType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_74.ModeInputType]':
        """List[ModeInputType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_MaterialPropertyClass(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_MaterialPropertyClass

    A specific implementation of 'EnumWithSelectedValue' for 'MaterialPropertyClass' types.
    """
    __qualname__ = 'MaterialPropertyClass'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1194.MaterialPropertyClass':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1194.MaterialPropertyClass

    @classmethod
    def implicit_type(cls) -> '_1194.MaterialPropertyClass.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1194.MaterialPropertyClass.type_()

    @property
    def selected_value(self) -> '_1194.MaterialPropertyClass':
        """MaterialPropertyClass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1194.MaterialPropertyClass]':
        """List[MaterialPropertyClass]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_LubricantDefinition(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_LubricantDefinition

    A specific implementation of 'EnumWithSelectedValue' for 'LubricantDefinition' types.
    """
    __qualname__ = 'LubricantDefinition'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_237.LubricantDefinition':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _237.LubricantDefinition

    @classmethod
    def implicit_type(cls) -> '_237.LubricantDefinition.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _237.LubricantDefinition.type_()

    @property
    def selected_value(self) -> '_237.LubricantDefinition':
        """LubricantDefinition: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_237.LubricantDefinition]':
        """List[LubricantDefinition]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_LubricantViscosityClassISO(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_LubricantViscosityClassISO

    A specific implementation of 'EnumWithSelectedValue' for 'LubricantViscosityClassISO' types.
    """
    __qualname__ = 'LubricantViscosityClassISO'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_241.LubricantViscosityClassISO':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _241.LubricantViscosityClassISO

    @classmethod
    def implicit_type(cls) -> '_241.LubricantViscosityClassISO.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _241.LubricantViscosityClassISO.type_()

    @property
    def selected_value(self) -> '_241.LubricantViscosityClassISO':
        """LubricantViscosityClassISO: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_241.LubricantViscosityClassISO]':
        """List[LubricantViscosityClassISO]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_MicroGeometryModel(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_MicroGeometryModel

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryModel' types.
    """
    __qualname__ = 'MicroGeometryModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_309.MicroGeometryModel':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _309.MicroGeometryModel

    @classmethod
    def implicit_type(cls) -> '_309.MicroGeometryModel.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _309.MicroGeometryModel.type_()

    @property
    def selected_value(self) -> '_309.MicroGeometryModel':
        """MicroGeometryModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_309.MicroGeometryModel]':
        """List[MicroGeometryModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ExtrapolationOptions(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ExtrapolationOptions

    A specific implementation of 'EnumWithSelectedValue' for 'ExtrapolationOptions' types.
    """
    __qualname__ = 'ExtrapolationOptions'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1317.ExtrapolationOptions':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1317.ExtrapolationOptions

    @classmethod
    def implicit_type(cls) -> '_1317.ExtrapolationOptions.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1317.ExtrapolationOptions.type_()

    @property
    def selected_value(self) -> '_1317.ExtrapolationOptions':
        """ExtrapolationOptions: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1317.ExtrapolationOptions]':
        """List[ExtrapolationOptions]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_CylindricalGearRatingMethods(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_CylindricalGearRatingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalGearRatingMethods' types.
    """
    __qualname__ = 'CylindricalGearRatingMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_227.CylindricalGearRatingMethods':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _227.CylindricalGearRatingMethods

    @classmethod
    def implicit_type(cls) -> '_227.CylindricalGearRatingMethods.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _227.CylindricalGearRatingMethods.type_()

    @property
    def selected_value(self) -> '_227.CylindricalGearRatingMethods':
        """CylindricalGearRatingMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_227.CylindricalGearRatingMethods]':
        """List[CylindricalGearRatingMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ScuffingFlashTemperatureRatingMethod' types.
    """
    __qualname__ = 'ScuffingFlashTemperatureRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_448.ScuffingFlashTemperatureRatingMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _448.ScuffingFlashTemperatureRatingMethod

    @classmethod
    def implicit_type(cls) -> '_448.ScuffingFlashTemperatureRatingMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _448.ScuffingFlashTemperatureRatingMethod.type_()

    @property
    def selected_value(self) -> '_448.ScuffingFlashTemperatureRatingMethod':
        """ScuffingFlashTemperatureRatingMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_448.ScuffingFlashTemperatureRatingMethod]':
        """List[ScuffingFlashTemperatureRatingMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ScuffingIntegralTemperatureRatingMethod' types.
    """
    __qualname__ = 'ScuffingIntegralTemperatureRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_449.ScuffingIntegralTemperatureRatingMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _449.ScuffingIntegralTemperatureRatingMethod

    @classmethod
    def implicit_type(cls) -> '_449.ScuffingIntegralTemperatureRatingMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _449.ScuffingIntegralTemperatureRatingMethod.type_()

    @property
    def selected_value(self) -> '_449.ScuffingIntegralTemperatureRatingMethod':
        """ScuffingIntegralTemperatureRatingMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_449.ScuffingIntegralTemperatureRatingMethod]':
        """List[ScuffingIntegralTemperatureRatingMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_LocationOfEvaluationLowerLimit(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_LocationOfEvaluationLowerLimit

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfEvaluationLowerLimit' types.
    """
    __qualname__ = 'LocationOfEvaluationLowerLimit'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_539.LocationOfEvaluationLowerLimit':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _539.LocationOfEvaluationLowerLimit

    @classmethod
    def implicit_type(cls) -> '_539.LocationOfEvaluationLowerLimit.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _539.LocationOfEvaluationLowerLimit.type_()

    @property
    def selected_value(self) -> '_539.LocationOfEvaluationLowerLimit':
        """LocationOfEvaluationLowerLimit: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_539.LocationOfEvaluationLowerLimit]':
        """List[LocationOfEvaluationLowerLimit]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_LocationOfEvaluationUpperLimit(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_LocationOfEvaluationUpperLimit

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfEvaluationUpperLimit' types.
    """
    __qualname__ = 'LocationOfEvaluationUpperLimit'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_540.LocationOfEvaluationUpperLimit':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _540.LocationOfEvaluationUpperLimit

    @classmethod
    def implicit_type(cls) -> '_540.LocationOfEvaluationUpperLimit.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _540.LocationOfEvaluationUpperLimit.type_()

    @property
    def selected_value(self) -> '_540.LocationOfEvaluationUpperLimit':
        """LocationOfEvaluationUpperLimit: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_540.LocationOfEvaluationUpperLimit]':
        """List[LocationOfEvaluationUpperLimit]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_LocationOfRootReliefEvaluation(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_LocationOfRootReliefEvaluation

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfRootReliefEvaluation' types.
    """
    __qualname__ = 'LocationOfRootReliefEvaluation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_541.LocationOfRootReliefEvaluation':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _541.LocationOfRootReliefEvaluation

    @classmethod
    def implicit_type(cls) -> '_541.LocationOfRootReliefEvaluation.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _541.LocationOfRootReliefEvaluation.type_()

    @property
    def selected_value(self) -> '_541.LocationOfRootReliefEvaluation':
        """LocationOfRootReliefEvaluation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_541.LocationOfRootReliefEvaluation]':
        """List[LocationOfRootReliefEvaluation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_LocationOfTipReliefEvaluation(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_LocationOfTipReliefEvaluation

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfTipReliefEvaluation' types.
    """
    __qualname__ = 'LocationOfTipReliefEvaluation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_542.LocationOfTipReliefEvaluation':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _542.LocationOfTipReliefEvaluation

    @classmethod
    def implicit_type(cls) -> '_542.LocationOfTipReliefEvaluation.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _542.LocationOfTipReliefEvaluation.type_()

    @property
    def selected_value(self) -> '_542.LocationOfTipReliefEvaluation':
        """LocationOfTipReliefEvaluation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_542.LocationOfTipReliefEvaluation]':
        """List[LocationOfTipReliefEvaluation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_CylindricalMftFinishingMethods(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_CylindricalMftFinishingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalMftFinishingMethods' types.
    """
    __qualname__ = 'CylindricalMftFinishingMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_589.CylindricalMftFinishingMethods':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _589.CylindricalMftFinishingMethods

    @classmethod
    def implicit_type(cls) -> '_589.CylindricalMftFinishingMethods.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _589.CylindricalMftFinishingMethods.type_()

    @property
    def selected_value(self) -> '_589.CylindricalMftFinishingMethods':
        """CylindricalMftFinishingMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_589.CylindricalMftFinishingMethods]':
        """List[CylindricalMftFinishingMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_CylindricalMftRoughingMethods(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_CylindricalMftRoughingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalMftRoughingMethods' types.
    """
    __qualname__ = 'CylindricalMftRoughingMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_590.CylindricalMftRoughingMethods':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _590.CylindricalMftRoughingMethods

    @classmethod
    def implicit_type(cls) -> '_590.CylindricalMftRoughingMethods.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _590.CylindricalMftRoughingMethods.type_()

    @property
    def selected_value(self) -> '_590.CylindricalMftRoughingMethods':
        """CylindricalMftRoughingMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_590.CylindricalMftRoughingMethods]':
        """List[CylindricalMftRoughingMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_MicroGeometryDefinitionMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_MicroGeometryDefinitionMethod

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryDefinitionMethod' types.
    """
    __qualname__ = 'MicroGeometryDefinitionMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_611.MicroGeometryDefinitionMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _611.MicroGeometryDefinitionMethod

    @classmethod
    def implicit_type(cls) -> '_611.MicroGeometryDefinitionMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _611.MicroGeometryDefinitionMethod.type_()

    @property
    def selected_value(self) -> '_611.MicroGeometryDefinitionMethod':
        """MicroGeometryDefinitionMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_611.MicroGeometryDefinitionMethod]':
        """List[MicroGeometryDefinitionMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_MicroGeometryDefinitionType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_MicroGeometryDefinitionType

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryDefinitionType' types.
    """
    __qualname__ = 'MicroGeometryDefinitionType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_612.MicroGeometryDefinitionType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _612.MicroGeometryDefinitionType

    @classmethod
    def implicit_type(cls) -> '_612.MicroGeometryDefinitionType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _612.MicroGeometryDefinitionType.type_()

    @property
    def selected_value(self) -> '_612.MicroGeometryDefinitionType':
        """MicroGeometryDefinitionType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_612.MicroGeometryDefinitionType]':
        """List[MicroGeometryDefinitionType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ChartType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ChartType

    A specific implementation of 'EnumWithSelectedValue' for 'ChartType' types.
    """
    __qualname__ = 'ChartType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_609.ChartType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _609.ChartType

    @classmethod
    def implicit_type(cls) -> '_609.ChartType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _609.ChartType.type_()

    @property
    def selected_value(self) -> '_609.ChartType':
        """ChartType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_609.ChartType]':
        """List[ChartType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_Flank(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_Flank

    A specific implementation of 'EnumWithSelectedValue' for 'Flank' types.
    """
    __qualname__ = 'Flank'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_593.Flank':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _593.Flank

    @classmethod
    def implicit_type(cls) -> '_593.Flank.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _593.Flank.type_()

    @property
    def selected_value(self) -> '_593.Flank':
        """Flank: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_593.Flank]':
        """List[Flank]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ActiveProcessMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ActiveProcessMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ActiveProcessMethod' types.
    """
    __qualname__ = 'ActiveProcessMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_624.ActiveProcessMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _624.ActiveProcessMethod

    @classmethod
    def implicit_type(cls) -> '_624.ActiveProcessMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _624.ActiveProcessMethod.type_()

    @property
    def selected_value(self) -> '_624.ActiveProcessMethod':
        """ActiveProcessMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_624.ActiveProcessMethod]':
        """List[ActiveProcessMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_CutterFlankSections(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_CutterFlankSections

    A specific implementation of 'EnumWithSelectedValue' for 'CutterFlankSections' types.
    """
    __qualname__ = 'CutterFlankSections'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_575.CutterFlankSections':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _575.CutterFlankSections

    @classmethod
    def implicit_type(cls) -> '_575.CutterFlankSections.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _575.CutterFlankSections.type_()

    @property
    def selected_value(self) -> '_575.CutterFlankSections':
        """CutterFlankSections: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_575.CutterFlankSections]':
        """List[CutterFlankSections]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_BasicCurveTypes(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BasicCurveTypes

    A specific implementation of 'EnumWithSelectedValue' for 'BasicCurveTypes' types.
    """
    __qualname__ = 'BasicCurveTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_285.BasicCurveTypes':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _285.BasicCurveTypes

    @classmethod
    def implicit_type(cls) -> '_285.BasicCurveTypes.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _285.BasicCurveTypes.type_()

    @property
    def selected_value(self) -> '_285.BasicCurveTypes':
        """BasicCurveTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_285.BasicCurveTypes]':
        """List[BasicCurveTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ThicknessType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ThicknessType

    A specific implementation of 'EnumWithSelectedValue' for 'ThicknessType' types.
    """
    __qualname__ = 'ThicknessType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1040.ThicknessType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1040.ThicknessType

    @classmethod
    def implicit_type(cls) -> '_1040.ThicknessType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1040.ThicknessType.type_()

    @property
    def selected_value(self) -> '_1040.ThicknessType':
        """ThicknessType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1040.ThicknessType]':
        """List[ThicknessType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ConicalMachineSettingCalculationMethods(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ConicalMachineSettingCalculationMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ConicalMachineSettingCalculationMethods' types.
    """
    __qualname__ = 'ConicalMachineSettingCalculationMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1111.ConicalMachineSettingCalculationMethods':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1111.ConicalMachineSettingCalculationMethods

    @classmethod
    def implicit_type(cls) -> '_1111.ConicalMachineSettingCalculationMethods.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1111.ConicalMachineSettingCalculationMethods.type_()

    @property
    def selected_value(self) -> '_1111.ConicalMachineSettingCalculationMethods':
        """ConicalMachineSettingCalculationMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1111.ConicalMachineSettingCalculationMethods]':
        """List[ConicalMachineSettingCalculationMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ConicalManufactureMethods(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ConicalManufactureMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ConicalManufactureMethods' types.
    """
    __qualname__ = 'ConicalManufactureMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1112.ConicalManufactureMethods':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1112.ConicalManufactureMethods

    @classmethod
    def implicit_type(cls) -> '_1112.ConicalManufactureMethods.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1112.ConicalManufactureMethods.type_()

    @property
    def selected_value(self) -> '_1112.ConicalManufactureMethods':
        """ConicalManufactureMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1112.ConicalManufactureMethods]':
        """List[ConicalManufactureMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_CandidateDisplayChoice(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_CandidateDisplayChoice

    A specific implementation of 'EnumWithSelectedValue' for 'CandidateDisplayChoice' types.
    """
    __qualname__ = 'CandidateDisplayChoice'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_869.CandidateDisplayChoice':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _869.CandidateDisplayChoice

    @classmethod
    def implicit_type(cls) -> '_869.CandidateDisplayChoice.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _869.CandidateDisplayChoice.type_()

    @property
    def selected_value(self) -> '_869.CandidateDisplayChoice':
        """CandidateDisplayChoice: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_869.CandidateDisplayChoice]':
        """List[CandidateDisplayChoice]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_Severity(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_Severity

    A specific implementation of 'EnumWithSelectedValue' for 'Severity' types.
    """
    __qualname__ = 'Severity'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1571.Severity':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1571.Severity

    @classmethod
    def implicit_type(cls) -> '_1571.Severity.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1571.Severity.type_()

    @property
    def selected_value(self) -> '_1571.Severity':
        """Severity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1571.Severity]':
        """List[Severity]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_GeometrySpecificationType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_GeometrySpecificationType

    A specific implementation of 'EnumWithSelectedValue' for 'GeometrySpecificationType' types.
    """
    __qualname__ = 'GeometrySpecificationType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1011.GeometrySpecificationType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1011.GeometrySpecificationType

    @classmethod
    def implicit_type(cls) -> '_1011.GeometrySpecificationType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1011.GeometrySpecificationType.type_()

    @property
    def selected_value(self) -> '_1011.GeometrySpecificationType':
        """GeometrySpecificationType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1011.GeometrySpecificationType]':
        """List[GeometrySpecificationType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_StatusItemSeverity(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_StatusItemSeverity

    A specific implementation of 'EnumWithSelectedValue' for 'StatusItemSeverity' types.
    """
    __qualname__ = 'StatusItemSeverity'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1574.StatusItemSeverity':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1574.StatusItemSeverity

    @classmethod
    def implicit_type(cls) -> '_1574.StatusItemSeverity.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1574.StatusItemSeverity.type_()

    @property
    def selected_value(self) -> '_1574.StatusItemSeverity':
        """StatusItemSeverity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1574.StatusItemSeverity]':
        """List[StatusItemSeverity]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_LubricationMethods(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_LubricationMethods

    A specific implementation of 'EnumWithSelectedValue' for 'LubricationMethods' types.
    """
    __qualname__ = 'LubricationMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_307.LubricationMethods':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _307.LubricationMethods

    @classmethod
    def implicit_type(cls) -> '_307.LubricationMethods.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _307.LubricationMethods.type_()

    @property
    def selected_value(self) -> '_307.LubricationMethods':
        """LubricationMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_307.LubricationMethods]':
        """List[LubricationMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'MicropittingCoefficientOfFrictionCalculationMethod' types.
    """
    __qualname__ = 'MicropittingCoefficientOfFrictionCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_310.MicropittingCoefficientOfFrictionCalculationMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _310.MicropittingCoefficientOfFrictionCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_310.MicropittingCoefficientOfFrictionCalculationMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _310.MicropittingCoefficientOfFrictionCalculationMethod.type_()

    @property
    def selected_value(self) -> '_310.MicropittingCoefficientOfFrictionCalculationMethod':
        """MicropittingCoefficientOfFrictionCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_310.MicropittingCoefficientOfFrictionCalculationMethod]':
        """List[MicropittingCoefficientOfFrictionCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ScuffingCoefficientOfFrictionMethods' types.
    """
    __qualname__ = 'ScuffingCoefficientOfFrictionMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1032.ScuffingCoefficientOfFrictionMethods':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1032.ScuffingCoefficientOfFrictionMethods

    @classmethod
    def implicit_type(cls) -> '_1032.ScuffingCoefficientOfFrictionMethods.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1032.ScuffingCoefficientOfFrictionMethods.type_()

    @property
    def selected_value(self) -> '_1032.ScuffingCoefficientOfFrictionMethods':
        """ScuffingCoefficientOfFrictionMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1032.ScuffingCoefficientOfFrictionMethods]':
        """List[ScuffingCoefficientOfFrictionMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ContactResultType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ContactResultType

    A specific implementation of 'EnumWithSelectedValue' for 'ContactResultType' types.
    """
    __qualname__ = 'ContactResultType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_793.ContactResultType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _793.ContactResultType

    @classmethod
    def implicit_type(cls) -> '_793.ContactResultType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _793.ContactResultType.type_()

    @property
    def selected_value(self) -> '_793.ContactResultType':
        """ContactResultType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_793.ContactResultType]':
        """List[ContactResultType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_StressResultsType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_StressResultsType

    A specific implementation of 'EnumWithSelectedValue' for 'StressResultsType' types.
    """
    __qualname__ = 'StressResultsType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_83.StressResultsType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _83.StressResultsType

    @classmethod
    def implicit_type(cls) -> '_83.StressResultsType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _83.StressResultsType.type_()

    @property
    def selected_value(self) -> '_83.StressResultsType':
        """StressResultsType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_83.StressResultsType]':
        """List[StressResultsType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalGearPairCreationOptions.DerivedParameterOption' types.
    """
    __qualname__ = 'CylindricalGearPairCreationOptions.DerivedParameterOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1100.CylindricalGearPairCreationOptions.DerivedParameterOption':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1100.CylindricalGearPairCreationOptions.DerivedParameterOption

    @classmethod
    def implicit_type(cls) -> '_1100.CylindricalGearPairCreationOptions.DerivedParameterOption.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1100.CylindricalGearPairCreationOptions.DerivedParameterOption.type_()

    @property
    def selected_value(self) -> '_1100.CylindricalGearPairCreationOptions.DerivedParameterOption':
        """CylindricalGearPairCreationOptions.DerivedParameterOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1100.CylindricalGearPairCreationOptions.DerivedParameterOption]':
        """List[CylindricalGearPairCreationOptions.DerivedParameterOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ToothThicknessSpecificationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ToothThicknessSpecificationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ToothThicknessSpecificationMethod' types.
    """
    __qualname__ = 'ToothThicknessSpecificationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1144.ToothThicknessSpecificationMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1144.ToothThicknessSpecificationMethod

    @classmethod
    def implicit_type(cls) -> '_1144.ToothThicknessSpecificationMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1144.ToothThicknessSpecificationMethod.type_()

    @property
    def selected_value(self) -> '_1144.ToothThicknessSpecificationMethod':
        """ToothThicknessSpecificationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1144.ToothThicknessSpecificationMethod]':
        """List[ToothThicknessSpecificationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_LoadDistributionFactorMethods(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_LoadDistributionFactorMethods

    A specific implementation of 'EnumWithSelectedValue' for 'LoadDistributionFactorMethods' types.
    """
    __qualname__ = 'LoadDistributionFactorMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1123.LoadDistributionFactorMethods':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1123.LoadDistributionFactorMethods

    @classmethod
    def implicit_type(cls) -> '_1123.LoadDistributionFactorMethods.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1123.LoadDistributionFactorMethods.type_()

    @property
    def selected_value(self) -> '_1123.LoadDistributionFactorMethods':
        """LoadDistributionFactorMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1123.LoadDistributionFactorMethods]':
        """List[LoadDistributionFactorMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods

    A specific implementation of 'EnumWithSelectedValue' for 'AGMAGleasonConicalGearGeometryMethods' types.
    """
    __qualname__ = 'AGMAGleasonConicalGearGeometryMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1133.AGMAGleasonConicalGearGeometryMethods':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1133.AGMAGleasonConicalGearGeometryMethods

    @classmethod
    def implicit_type(cls) -> '_1133.AGMAGleasonConicalGearGeometryMethods.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1133.AGMAGleasonConicalGearGeometryMethods.type_()

    @property
    def selected_value(self) -> '_1133.AGMAGleasonConicalGearGeometryMethods':
        """AGMAGleasonConicalGearGeometryMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1133.AGMAGleasonConicalGearGeometryMethods]':
        """List[AGMAGleasonConicalGearGeometryMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ProSolveMpcType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ProSolveMpcType

    A specific implementation of 'EnumWithSelectedValue' for 'ProSolveMpcType' types.
    """
    __qualname__ = 'ProSolveMpcType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1191.ProSolveMpcType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1191.ProSolveMpcType

    @classmethod
    def implicit_type(cls) -> '_1191.ProSolveMpcType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1191.ProSolveMpcType.type_()

    @property
    def selected_value(self) -> '_1191.ProSolveMpcType':
        """ProSolveMpcType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1191.ProSolveMpcType]':
        """List[ProSolveMpcType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ProSolveSolverType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ProSolveSolverType

    A specific implementation of 'EnumWithSelectedValue' for 'ProSolveSolverType' types.
    """
    __qualname__ = 'ProSolveSolverType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1192.ProSolveSolverType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1192.ProSolveSolverType

    @classmethod
    def implicit_type(cls) -> '_1192.ProSolveSolverType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1192.ProSolveSolverType.type_()

    @property
    def selected_value(self) -> '_1192.ProSolveSolverType':
        """ProSolveSolverType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1192.ProSolveSolverType]':
        """List[ProSolveSolverType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ITDesignation(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ITDesignation

    A specific implementation of 'EnumWithSelectedValue' for 'ITDesignation' types.
    """
    __qualname__ = 'ITDesignation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1674.ITDesignation':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1674.ITDesignation

    @classmethod
    def implicit_type(cls) -> '_1674.ITDesignation.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1674.ITDesignation.type_()

    @property
    def selected_value(self) -> '_1674.ITDesignation':
        """ITDesignation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1674.ITDesignation]':
        """List[ITDesignation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption

    A specific implementation of 'EnumWithSelectedValue' for 'DudleyEffectiveLengthApproximationOption' types.
    """
    __qualname__ = 'DudleyEffectiveLengthApproximationOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1202.DudleyEffectiveLengthApproximationOption':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1202.DudleyEffectiveLengthApproximationOption

    @classmethod
    def implicit_type(cls) -> '_1202.DudleyEffectiveLengthApproximationOption.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1202.DudleyEffectiveLengthApproximationOption.type_()

    @property
    def selected_value(self) -> '_1202.DudleyEffectiveLengthApproximationOption':
        """DudleyEffectiveLengthApproximationOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1202.DudleyEffectiveLengthApproximationOption]':
        """List[DudleyEffectiveLengthApproximationOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_SplineRatingTypes(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_SplineRatingTypes

    A specific implementation of 'EnumWithSelectedValue' for 'SplineRatingTypes' types.
    """
    __qualname__ = 'SplineRatingTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1225.SplineRatingTypes':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1225.SplineRatingTypes

    @classmethod
    def implicit_type(cls) -> '_1225.SplineRatingTypes.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1225.SplineRatingTypes.type_()

    @property
    def selected_value(self) -> '_1225.SplineRatingTypes':
        """SplineRatingTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1225.SplineRatingTypes]':
        """List[SplineRatingTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_Modules(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_Modules

    A specific implementation of 'EnumWithSelectedValue' for 'Modules' types.
    """
    __qualname__ = 'Modules'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1211.Modules':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1211.Modules

    @classmethod
    def implicit_type(cls) -> '_1211.Modules.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1211.Modules.type_()

    @property
    def selected_value(self) -> '_1211.Modules':
        """Modules: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1211.Modules]':
        """List[Modules]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_PressureAngleTypes(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_PressureAngleTypes

    A specific implementation of 'EnumWithSelectedValue' for 'PressureAngleTypes' types.
    """
    __qualname__ = 'PressureAngleTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1212.PressureAngleTypes':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1212.PressureAngleTypes

    @classmethod
    def implicit_type(cls) -> '_1212.PressureAngleTypes.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1212.PressureAngleTypes.type_()

    @property
    def selected_value(self) -> '_1212.PressureAngleTypes':
        """PressureAngleTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1212.PressureAngleTypes]':
        """List[PressureAngleTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_SplineFitClassType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_SplineFitClassType

    A specific implementation of 'EnumWithSelectedValue' for 'SplineFitClassType' types.
    """
    __qualname__ = 'SplineFitClassType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1220.SplineFitClassType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1220.SplineFitClassType

    @classmethod
    def implicit_type(cls) -> '_1220.SplineFitClassType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1220.SplineFitClassType.type_()

    @property
    def selected_value(self) -> '_1220.SplineFitClassType':
        """SplineFitClassType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1220.SplineFitClassType]':
        """List[SplineFitClassType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_SplineToleranceClassTypes(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_SplineToleranceClassTypes

    A specific implementation of 'EnumWithSelectedValue' for 'SplineToleranceClassTypes' types.
    """
    __qualname__ = 'SplineToleranceClassTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1226.SplineToleranceClassTypes':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1226.SplineToleranceClassTypes

    @classmethod
    def implicit_type(cls) -> '_1226.SplineToleranceClassTypes.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1226.SplineToleranceClassTypes.type_()

    @property
    def selected_value(self) -> '_1226.SplineToleranceClassTypes':
        """SplineToleranceClassTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1226.SplineToleranceClassTypes]':
        """List[SplineToleranceClassTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_Table4JointInterfaceTypes(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_Table4JointInterfaceTypes

    A specific implementation of 'EnumWithSelectedValue' for 'Table4JointInterfaceTypes' types.
    """
    __qualname__ = 'Table4JointInterfaceTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1256.Table4JointInterfaceTypes':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1256.Table4JointInterfaceTypes

    @classmethod
    def implicit_type(cls) -> '_1256.Table4JointInterfaceTypes.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1256.Table4JointInterfaceTypes.type_()

    @property
    def selected_value(self) -> '_1256.Table4JointInterfaceTypes':
        """Table4JointInterfaceTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1256.Table4JointInterfaceTypes]':
        """List[Table4JointInterfaceTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ExecutableDirectoryCopier_Option(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ExecutableDirectoryCopier_Option

    A specific implementation of 'EnumWithSelectedValue' for 'ExecutableDirectoryCopier.Option' types.
    """
    __qualname__ = 'ExecutableDirectoryCopier.Option'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1385.ExecutableDirectoryCopier.Option':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1385.ExecutableDirectoryCopier.Option

    @classmethod
    def implicit_type(cls) -> '_1385.ExecutableDirectoryCopier.Option.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1385.ExecutableDirectoryCopier.Option.type_()

    @property
    def selected_value(self) -> '_1385.ExecutableDirectoryCopier.Option':
        """ExecutableDirectoryCopier.Option: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1385.ExecutableDirectoryCopier.Option]':
        """List[ExecutableDirectoryCopier.Option]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_CadPageOrientation(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_CadPageOrientation

    A specific implementation of 'EnumWithSelectedValue' for 'CadPageOrientation' types.
    """
    __qualname__ = 'CadPageOrientation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1526.CadPageOrientation':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1526.CadPageOrientation

    @classmethod
    def implicit_type(cls) -> '_1526.CadPageOrientation.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1526.CadPageOrientation.type_()

    @property
    def selected_value(self) -> '_1526.CadPageOrientation':
        """CadPageOrientation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1526.CadPageOrientation]':
        """List[CadPageOrientation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_RollerBearingProfileTypes(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_RollerBearingProfileTypes

    A specific implementation of 'EnumWithSelectedValue' for 'RollerBearingProfileTypes' types.
    """
    __qualname__ = 'RollerBearingProfileTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1656.RollerBearingProfileTypes':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1656.RollerBearingProfileTypes

    @classmethod
    def implicit_type(cls) -> '_1656.RollerBearingProfileTypes.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1656.RollerBearingProfileTypes.type_()

    @property
    def selected_value(self) -> '_1656.RollerBearingProfileTypes':
        """RollerBearingProfileTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1656.RollerBearingProfileTypes]':
        """List[RollerBearingProfileTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_FluidFilmTemperatureOptions(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_FluidFilmTemperatureOptions

    A specific implementation of 'EnumWithSelectedValue' for 'FluidFilmTemperatureOptions' types.
    """
    __qualname__ = 'FluidFilmTemperatureOptions'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1649.FluidFilmTemperatureOptions':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1649.FluidFilmTemperatureOptions

    @classmethod
    def implicit_type(cls) -> '_1649.FluidFilmTemperatureOptions.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1649.FluidFilmTemperatureOptions.type_()

    @property
    def selected_value(self) -> '_1649.FluidFilmTemperatureOptions':
        """FluidFilmTemperatureOptions: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1649.FluidFilmTemperatureOptions]':
        """List[FluidFilmTemperatureOptions]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_SupportToleranceLocationDesignation(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_SupportToleranceLocationDesignation

    A specific implementation of 'EnumWithSelectedValue' for 'SupportToleranceLocationDesignation' types.
    """
    __qualname__ = 'SupportToleranceLocationDesignation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1687.SupportToleranceLocationDesignation':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1687.SupportToleranceLocationDesignation

    @classmethod
    def implicit_type(cls) -> '_1687.SupportToleranceLocationDesignation.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1687.SupportToleranceLocationDesignation.type_()

    @property
    def selected_value(self) -> '_1687.SupportToleranceLocationDesignation':
        """SupportToleranceLocationDesignation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1687.SupportToleranceLocationDesignation]':
        """List[SupportToleranceLocationDesignation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_LoadedBallElementPropertyType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_LoadedBallElementPropertyType

    A specific implementation of 'EnumWithSelectedValue' for 'LoadedBallElementPropertyType' types.
    """
    __qualname__ = 'LoadedBallElementPropertyType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1725.LoadedBallElementPropertyType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1725.LoadedBallElementPropertyType

    @classmethod
    def implicit_type(cls) -> '_1725.LoadedBallElementPropertyType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1725.LoadedBallElementPropertyType.type_()

    @property
    def selected_value(self) -> '_1725.LoadedBallElementPropertyType':
        """LoadedBallElementPropertyType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1725.LoadedBallElementPropertyType]':
        """List[LoadedBallElementPropertyType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_RollingBearingArrangement(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_RollingBearingArrangement

    A specific implementation of 'EnumWithSelectedValue' for 'RollingBearingArrangement' types.
    """
    __qualname__ = 'RollingBearingArrangement'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1657.RollingBearingArrangement':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1657.RollingBearingArrangement

    @classmethod
    def implicit_type(cls) -> '_1657.RollingBearingArrangement.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1657.RollingBearingArrangement.type_()

    @property
    def selected_value(self) -> '_1657.RollingBearingArrangement':
        """RollingBearingArrangement: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1657.RollingBearingArrangement]':
        """List[RollingBearingArrangement]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'BasicDynamicLoadRatingCalculationMethod' types.
    """
    __qualname__ = 'BasicDynamicLoadRatingCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1637.BasicDynamicLoadRatingCalculationMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1637.BasicDynamicLoadRatingCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_1637.BasicDynamicLoadRatingCalculationMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1637.BasicDynamicLoadRatingCalculationMethod.type_()

    @property
    def selected_value(self) -> '_1637.BasicDynamicLoadRatingCalculationMethod':
        """BasicDynamicLoadRatingCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1637.BasicDynamicLoadRatingCalculationMethod]':
        """List[BasicDynamicLoadRatingCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'BasicStaticLoadRatingCalculationMethod' types.
    """
    __qualname__ = 'BasicStaticLoadRatingCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1638.BasicStaticLoadRatingCalculationMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1638.BasicStaticLoadRatingCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_1638.BasicStaticLoadRatingCalculationMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1638.BasicStaticLoadRatingCalculationMethod.type_()

    @property
    def selected_value(self) -> '_1638.BasicStaticLoadRatingCalculationMethod':
        """BasicStaticLoadRatingCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1638.BasicStaticLoadRatingCalculationMethod]':
        """List[BasicStaticLoadRatingCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_RollingBearingRaceType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_RollingBearingRaceType

    A specific implementation of 'EnumWithSelectedValue' for 'RollingBearingRaceType' types.
    """
    __qualname__ = 'RollingBearingRaceType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1660.RollingBearingRaceType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1660.RollingBearingRaceType

    @classmethod
    def implicit_type(cls) -> '_1660.RollingBearingRaceType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1660.RollingBearingRaceType.type_()

    @property
    def selected_value(self) -> '_1660.RollingBearingRaceType':
        """RollingBearingRaceType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1660.RollingBearingRaceType]':
        """List[RollingBearingRaceType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_RotationalDirections(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_RotationalDirections

    A specific implementation of 'EnumWithSelectedValue' for 'RotationalDirections' types.
    """
    __qualname__ = 'RotationalDirections'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1662.RotationalDirections':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1662.RotationalDirections

    @classmethod
    def implicit_type(cls) -> '_1662.RotationalDirections.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1662.RotationalDirections.type_()

    @property
    def selected_value(self) -> '_1662.RotationalDirections':
        """RotationalDirections: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1662.RotationalDirections]':
        """List[RotationalDirections]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_BearingEfficiencyRatingMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BearingEfficiencyRatingMethod

    A specific implementation of 'EnumWithSelectedValue' for 'BearingEfficiencyRatingMethod' types.
    """
    __qualname__ = 'BearingEfficiencyRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_266.BearingEfficiencyRatingMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _266.BearingEfficiencyRatingMethod

    @classmethod
    def implicit_type(cls) -> '_266.BearingEfficiencyRatingMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _266.BearingEfficiencyRatingMethod.type_()

    @property
    def selected_value(self) -> '_266.BearingEfficiencyRatingMethod':
        """BearingEfficiencyRatingMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_266.BearingEfficiencyRatingMethod]':
        """List[BearingEfficiencyRatingMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftDiameterModificationDueToRollingBearingRing' types.
    """
    __qualname__ = 'ShaftDiameterModificationDueToRollingBearingRing'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2225.ShaftDiameterModificationDueToRollingBearingRing':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _2225.ShaftDiameterModificationDueToRollingBearingRing

    @classmethod
    def implicit_type(cls) -> '_2225.ShaftDiameterModificationDueToRollingBearingRing.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _2225.ShaftDiameterModificationDueToRollingBearingRing.type_()

    @property
    def selected_value(self) -> '_2225.ShaftDiameterModificationDueToRollingBearingRing':
        """ShaftDiameterModificationDueToRollingBearingRing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_2225.ShaftDiameterModificationDueToRollingBearingRing]':
        """List[ShaftDiameterModificationDueToRollingBearingRing]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ExcitationAnalysisViewOption(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ExcitationAnalysisViewOption

    A specific implementation of 'EnumWithSelectedValue' for 'ExcitationAnalysisViewOption' types.
    """
    __qualname__ = 'ExcitationAnalysisViewOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2013.ExcitationAnalysisViewOption':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _2013.ExcitationAnalysisViewOption

    @classmethod
    def implicit_type(cls) -> '_2013.ExcitationAnalysisViewOption.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _2013.ExcitationAnalysisViewOption.type_()

    @property
    def selected_value(self) -> '_2013.ExcitationAnalysisViewOption':
        """ExcitationAnalysisViewOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_2013.ExcitationAnalysisViewOption]':
        """List[ExcitationAnalysisViewOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ThreeDViewContourOptionFirstSelection

    A specific implementation of 'EnumWithSelectedValue' for 'ThreeDViewContourOptionFirstSelection' types.
    """
    __qualname__ = 'ThreeDViewContourOptionFirstSelection'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1599.ThreeDViewContourOptionFirstSelection':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1599.ThreeDViewContourOptionFirstSelection

    @classmethod
    def implicit_type(cls) -> '_1599.ThreeDViewContourOptionFirstSelection.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1599.ThreeDViewContourOptionFirstSelection.type_()

    @property
    def selected_value(self) -> '_1599.ThreeDViewContourOptionFirstSelection':
        """ThreeDViewContourOptionFirstSelection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1599.ThreeDViewContourOptionFirstSelection]':
        """List[ThreeDViewContourOptionFirstSelection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection

    A specific implementation of 'EnumWithSelectedValue' for 'ThreeDViewContourOptionSecondSelection' types.
    """
    __qualname__ = 'ThreeDViewContourOptionSecondSelection'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1600.ThreeDViewContourOptionSecondSelection':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1600.ThreeDViewContourOptionSecondSelection

    @classmethod
    def implicit_type(cls) -> '_1600.ThreeDViewContourOptionSecondSelection.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1600.ThreeDViewContourOptionSecondSelection.type_()

    @property
    def selected_value(self) -> '_1600.ThreeDViewContourOptionSecondSelection':
        """ThreeDViewContourOptionSecondSelection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1600.ThreeDViewContourOptionSecondSelection]':
        """List[ThreeDViewContourOptionSecondSelection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ComponentOrientationOption(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ComponentOrientationOption

    A specific implementation of 'EnumWithSelectedValue' for 'ComponentOrientationOption' types.
    """
    __qualname__ = 'ComponentOrientationOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2117.ComponentOrientationOption':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _2117.ComponentOrientationOption

    @classmethod
    def implicit_type(cls) -> '_2117.ComponentOrientationOption.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _2117.ComponentOrientationOption.type_()

    @property
    def selected_value(self) -> '_2117.ComponentOrientationOption':
        """ComponentOrientationOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_2117.ComponentOrientationOption]':
        """List[ComponentOrientationOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_Axis(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_Axis

    A specific implementation of 'EnumWithSelectedValue' for 'Axis' types.
    """
    __qualname__ = 'Axis'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1298.Axis':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1298.Axis

    @classmethod
    def implicit_type(cls) -> '_1298.Axis.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1298.Axis.type_()

    @property
    def selected_value(self) -> '_1298.Axis':
        """Axis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1298.Axis]':
        """List[Axis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_AlignmentAxis(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_AlignmentAxis

    A specific implementation of 'EnumWithSelectedValue' for 'AlignmentAxis' types.
    """
    __qualname__ = 'AlignmentAxis'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1297.AlignmentAxis':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1297.AlignmentAxis

    @classmethod
    def implicit_type(cls) -> '_1297.AlignmentAxis.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1297.AlignmentAxis.type_()

    @property
    def selected_value(self) -> '_1297.AlignmentAxis':
        """AlignmentAxis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1297.AlignmentAxis]':
        """List[AlignmentAxis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_DesignEntityId(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_DesignEntityId

    A specific implementation of 'EnumWithSelectedValue' for 'DesignEntityId' types.
    """
    __qualname__ = 'DesignEntityId'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1961.DesignEntityId':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1961.DesignEntityId

    @classmethod
    def implicit_type(cls) -> '_1961.DesignEntityId.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1961.DesignEntityId.type_()

    @property
    def selected_value(self) -> '_1961.DesignEntityId':
        """DesignEntityId: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1961.DesignEntityId]':
        """List[DesignEntityId]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ThermalExpansionOption(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ThermalExpansionOption

    A specific implementation of 'EnumWithSelectedValue' for 'ThermalExpansionOption' types.
    """
    __qualname__ = 'ThermalExpansionOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2161.ThermalExpansionOption':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _2161.ThermalExpansionOption

    @classmethod
    def implicit_type(cls) -> '_2161.ThermalExpansionOption.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _2161.ThermalExpansionOption.type_()

    @property
    def selected_value(self) -> '_2161.ThermalExpansionOption':
        """ThermalExpansionOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_2161.ThermalExpansionOption]':
        """List[ThermalExpansionOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_FESubstructureType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_FESubstructureType

    A specific implementation of 'EnumWithSelectedValue' for 'FESubstructureType' types.
    """
    __qualname__ = 'FESubstructureType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2138.FESubstructureType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _2138.FESubstructureType

    @classmethod
    def implicit_type(cls) -> '_2138.FESubstructureType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _2138.FESubstructureType.type_()

    @property
    def selected_value(self) -> '_2138.FESubstructureType':
        """FESubstructureType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_2138.FESubstructureType]':
        """List[FESubstructureType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_FEExportFormat(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_FEExportFormat

    A specific implementation of 'EnumWithSelectedValue' for 'FEExportFormat' types.
    """
    __qualname__ = 'FEExportFormat'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_158.FEExportFormat':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _158.FEExportFormat

    @classmethod
    def implicit_type(cls) -> '_158.FEExportFormat.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _158.FEExportFormat.type_()

    @property
    def selected_value(self) -> '_158.FEExportFormat':
        """FEExportFormat: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_158.FEExportFormat]':
        """List[FEExportFormat]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ThreeDViewContourOption(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ThreeDViewContourOption

    A specific implementation of 'EnumWithSelectedValue' for 'ThreeDViewContourOption' types.
    """
    __qualname__ = 'ThreeDViewContourOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1598.ThreeDViewContourOption':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1598.ThreeDViewContourOption

    @classmethod
    def implicit_type(cls) -> '_1598.ThreeDViewContourOption.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1598.ThreeDViewContourOption.type_()

    @property
    def selected_value(self) -> '_1598.ThreeDViewContourOption':
        """ThreeDViewContourOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1598.ThreeDViewContourOption]':
        """List[ThreeDViewContourOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_BoundaryConditionType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BoundaryConditionType

    A specific implementation of 'EnumWithSelectedValue' for 'BoundaryConditionType' types.
    """
    __qualname__ = 'BoundaryConditionType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_157.BoundaryConditionType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _157.BoundaryConditionType

    @classmethod
    def implicit_type(cls) -> '_157.BoundaryConditionType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _157.BoundaryConditionType.type_()

    @property
    def selected_value(self) -> '_157.BoundaryConditionType':
        """BoundaryConditionType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_157.BoundaryConditionType]':
        """List[BoundaryConditionType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_BearingNodeOption(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BearingNodeOption

    A specific implementation of 'EnumWithSelectedValue' for 'BearingNodeOption' types.
    """
    __qualname__ = 'BearingNodeOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2114.BearingNodeOption':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _2114.BearingNodeOption

    @classmethod
    def implicit_type(cls) -> '_2114.BearingNodeOption.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _2114.BearingNodeOption.type_()

    @property
    def selected_value(self) -> '_2114.BearingNodeOption':
        """BearingNodeOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_2114.BearingNodeOption]':
        """List[BearingNodeOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_LinkNodeSource(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_LinkNodeSource

    A specific implementation of 'EnumWithSelectedValue' for 'LinkNodeSource' types.
    """
    __qualname__ = 'LinkNodeSource'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2148.LinkNodeSource':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _2148.LinkNodeSource

    @classmethod
    def implicit_type(cls) -> '_2148.LinkNodeSource.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _2148.LinkNodeSource.type_()

    @property
    def selected_value(self) -> '_2148.LinkNodeSource':
        """LinkNodeSource: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_2148.LinkNodeSource]':
        """List[LinkNodeSource]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_BearingToleranceClass(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BearingToleranceClass

    A specific implementation of 'EnumWithSelectedValue' for 'BearingToleranceClass' types.
    """
    __qualname__ = 'BearingToleranceClass'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1667.BearingToleranceClass':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1667.BearingToleranceClass

    @classmethod
    def implicit_type(cls) -> '_1667.BearingToleranceClass.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1667.BearingToleranceClass.type_()

    @property
    def selected_value(self) -> '_1667.BearingToleranceClass':
        """BearingToleranceClass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1667.BearingToleranceClass]':
        """List[BearingToleranceClass]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_BearingModel(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BearingModel

    A specific implementation of 'EnumWithSelectedValue' for 'BearingModel' types.
    """
    __qualname__ = 'BearingModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1644.BearingModel':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1644.BearingModel

    @classmethod
    def implicit_type(cls) -> '_1644.BearingModel.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1644.BearingModel.type_()

    @property
    def selected_value(self) -> '_1644.BearingModel':
        """BearingModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1644.BearingModel]':
        """List[BearingModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_PreloadType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_PreloadType

    A specific implementation of 'EnumWithSelectedValue' for 'PreloadType' types.
    """
    __qualname__ = 'PreloadType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1724.PreloadType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1724.PreloadType

    @classmethod
    def implicit_type(cls) -> '_1724.PreloadType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1724.PreloadType.type_()

    @property
    def selected_value(self) -> '_1724.PreloadType':
        """PreloadType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1724.PreloadType]':
        """List[PreloadType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_RaceAxialMountingType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_RaceAxialMountingType

    A specific implementation of 'EnumWithSelectedValue' for 'RaceAxialMountingType' types.
    """
    __qualname__ = 'RaceAxialMountingType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1726.RaceAxialMountingType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1726.RaceAxialMountingType

    @classmethod
    def implicit_type(cls) -> '_1726.RaceAxialMountingType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1726.RaceAxialMountingType.type_()

    @property
    def selected_value(self) -> '_1726.RaceAxialMountingType':
        """RaceAxialMountingType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1726.RaceAxialMountingType]':
        """List[RaceAxialMountingType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_RaceRadialMountingType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_RaceRadialMountingType

    A specific implementation of 'EnumWithSelectedValue' for 'RaceRadialMountingType' types.
    """
    __qualname__ = 'RaceRadialMountingType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1727.RaceRadialMountingType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1727.RaceRadialMountingType

    @classmethod
    def implicit_type(cls) -> '_1727.RaceRadialMountingType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1727.RaceRadialMountingType.type_()

    @property
    def selected_value(self) -> '_1727.RaceRadialMountingType':
        """RaceRadialMountingType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1727.RaceRadialMountingType]':
        """List[RaceRadialMountingType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_InternalClearanceClass(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_InternalClearanceClass

    A specific implementation of 'EnumWithSelectedValue' for 'InternalClearanceClass' types.
    """
    __qualname__ = 'InternalClearanceClass'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1666.InternalClearanceClass':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1666.InternalClearanceClass

    @classmethod
    def implicit_type(cls) -> '_1666.InternalClearanceClass.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1666.InternalClearanceClass.type_()

    @property
    def selected_value(self) -> '_1666.InternalClearanceClass':
        """InternalClearanceClass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1666.InternalClearanceClass]':
        """List[InternalClearanceClass]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_BearingToleranceDefinitionOptions(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BearingToleranceDefinitionOptions

    A specific implementation of 'EnumWithSelectedValue' for 'BearingToleranceDefinitionOptions' types.
    """
    __qualname__ = 'BearingToleranceDefinitionOptions'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1668.BearingToleranceDefinitionOptions':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1668.BearingToleranceDefinitionOptions

    @classmethod
    def implicit_type(cls) -> '_1668.BearingToleranceDefinitionOptions.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1668.BearingToleranceDefinitionOptions.type_()

    @property
    def selected_value(self) -> '_1668.BearingToleranceDefinitionOptions':
        """BearingToleranceDefinitionOptions: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1668.BearingToleranceDefinitionOptions]':
        """List[BearingToleranceDefinitionOptions]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_OilSealLossCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_OilSealLossCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'OilSealLossCalculationMethod' types.
    """
    __qualname__ = 'OilSealLossCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_274.OilSealLossCalculationMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _274.OilSealLossCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_274.OilSealLossCalculationMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _274.OilSealLossCalculationMethod.type_()

    @property
    def selected_value(self) -> '_274.OilSealLossCalculationMethod':
        """OilSealLossCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_274.OilSealLossCalculationMethod]':
        """List[OilSealLossCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_PowerLoadType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_PowerLoadType

    A specific implementation of 'EnumWithSelectedValue' for 'PowerLoadType' types.
    """
    __qualname__ = 'PowerLoadType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1973.PowerLoadType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1973.PowerLoadType

    @classmethod
    def implicit_type(cls) -> '_1973.PowerLoadType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1973.PowerLoadType.type_()

    @property
    def selected_value(self) -> '_1973.PowerLoadType':
        """PowerLoadType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1973.PowerLoadType]':
        """List[PowerLoadType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_RigidConnectorStiffnessType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_RigidConnectorStiffnessType

    A specific implementation of 'EnumWithSelectedValue' for 'RigidConnectorStiffnessType' types.
    """
    __qualname__ = 'RigidConnectorStiffnessType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2340.RigidConnectorStiffnessType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _2340.RigidConnectorStiffnessType

    @classmethod
    def implicit_type(cls) -> '_2340.RigidConnectorStiffnessType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _2340.RigidConnectorStiffnessType.type_()

    @property
    def selected_value(self) -> '_2340.RigidConnectorStiffnessType':
        """RigidConnectorStiffnessType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_2340.RigidConnectorStiffnessType]':
        """List[RigidConnectorStiffnessType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_RigidConnectorToothSpacingType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_RigidConnectorToothSpacingType

    A specific implementation of 'EnumWithSelectedValue' for 'RigidConnectorToothSpacingType' types.
    """
    __qualname__ = 'RigidConnectorToothSpacingType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2343.RigidConnectorToothSpacingType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _2343.RigidConnectorToothSpacingType

    @classmethod
    def implicit_type(cls) -> '_2343.RigidConnectorToothSpacingType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _2343.RigidConnectorToothSpacingType.type_()

    @property
    def selected_value(self) -> '_2343.RigidConnectorToothSpacingType':
        """RigidConnectorToothSpacingType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_2343.RigidConnectorToothSpacingType]':
        """List[RigidConnectorToothSpacingType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_RigidConnectorTypes(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_RigidConnectorTypes

    A specific implementation of 'EnumWithSelectedValue' for 'RigidConnectorTypes' types.
    """
    __qualname__ = 'RigidConnectorTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2344.RigidConnectorTypes':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _2344.RigidConnectorTypes

    @classmethod
    def implicit_type(cls) -> '_2344.RigidConnectorTypes.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _2344.RigidConnectorTypes.type_()

    @property
    def selected_value(self) -> '_2344.RigidConnectorTypes':
        """RigidConnectorTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_2344.RigidConnectorTypes]':
        """List[RigidConnectorTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_FitTypes(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_FitTypes

    A specific implementation of 'EnumWithSelectedValue' for 'FitTypes' types.
    """
    __qualname__ = 'FitTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1203.FitTypes':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1203.FitTypes

    @classmethod
    def implicit_type(cls) -> '_1203.FitTypes.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1203.FitTypes.type_()

    @property
    def selected_value(self) -> '_1203.FitTypes':
        """FitTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1203.FitTypes]':
        """List[FitTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_DoeValueSpecificationOption(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_DoeValueSpecificationOption

    A specific implementation of 'EnumWithSelectedValue' for 'DoeValueSpecificationOption' types.
    """
    __qualname__ = 'DoeValueSpecificationOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_4089.DoeValueSpecificationOption':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _4089.DoeValueSpecificationOption

    @classmethod
    def implicit_type(cls) -> '_4089.DoeValueSpecificationOption.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _4089.DoeValueSpecificationOption.type_()

    @property
    def selected_value(self) -> '_4089.DoeValueSpecificationOption':
        """DoeValueSpecificationOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_4089.DoeValueSpecificationOption]':
        """List[DoeValueSpecificationOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_AnalysisType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_AnalysisType

    A specific implementation of 'EnumWithSelectedValue' for 'AnalysisType' types.
    """
    __qualname__ = 'AnalysisType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6541.AnalysisType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _6541.AnalysisType

    @classmethod
    def implicit_type(cls) -> '_6541.AnalysisType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _6541.AnalysisType.type_()

    @property
    def selected_value(self) -> '_6541.AnalysisType':
        """AnalysisType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_6541.AnalysisType]':
        """List[AnalysisType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_BarModelExportType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BarModelExportType

    A specific implementation of 'EnumWithSelectedValue' for 'BarModelExportType' types.
    """
    __qualname__ = 'BarModelExportType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_50.BarModelExportType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _50.BarModelExportType

    @classmethod
    def implicit_type(cls) -> '_50.BarModelExportType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _50.BarModelExportType.type_()

    @property
    def selected_value(self) -> '_50.BarModelExportType':
        """BarModelExportType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_50.BarModelExportType]':
        """List[BarModelExportType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ComplexPartDisplayOption(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ComplexPartDisplayOption

    A specific implementation of 'EnumWithSelectedValue' for 'ComplexPartDisplayOption' types.
    """
    __qualname__ = 'ComplexPartDisplayOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1301.ComplexPartDisplayOption':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1301.ComplexPartDisplayOption

    @classmethod
    def implicit_type(cls) -> '_1301.ComplexPartDisplayOption.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1301.ComplexPartDisplayOption.type_()

    @property
    def selected_value(self) -> '_1301.ComplexPartDisplayOption':
        """ComplexPartDisplayOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1301.ComplexPartDisplayOption]':
        """List[ComplexPartDisplayOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_DynamicsResponseScaling(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_DynamicsResponseScaling

    A specific implementation of 'EnumWithSelectedValue' for 'DynamicsResponseScaling' types.
    """
    __qualname__ = 'DynamicsResponseScaling'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1312.DynamicsResponseScaling':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1312.DynamicsResponseScaling

    @classmethod
    def implicit_type(cls) -> '_1312.DynamicsResponseScaling.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1312.DynamicsResponseScaling.type_()

    @property
    def selected_value(self) -> '_1312.DynamicsResponseScaling':
        """DynamicsResponseScaling: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1312.DynamicsResponseScaling]':
        """List[DynamicsResponseScaling]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_DynamicsResponseType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_DynamicsResponseType

    A specific implementation of 'EnumWithSelectedValue' for 'DynamicsResponseType' types.
    """
    __qualname__ = 'DynamicsResponseType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1313.DynamicsResponseType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1313.DynamicsResponseType

    @classmethod
    def implicit_type(cls) -> '_1313.DynamicsResponseType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1313.DynamicsResponseType.type_()

    @property
    def selected_value(self) -> '_1313.DynamicsResponseType':
        """DynamicsResponseType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1313.DynamicsResponseType]':
        """List[DynamicsResponseType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_BearingStiffnessModel(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BearingStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'BearingStiffnessModel' types.
    """
    __qualname__ = 'BearingStiffnessModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5121.BearingStiffnessModel':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _5121.BearingStiffnessModel

    @classmethod
    def implicit_type(cls) -> '_5121.BearingStiffnessModel.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _5121.BearingStiffnessModel.type_()

    @property
    def selected_value(self) -> '_5121.BearingStiffnessModel':
        """BearingStiffnessModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_5121.BearingStiffnessModel]':
        """List[BearingStiffnessModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_GearMeshStiffnessModel(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_GearMeshStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'GearMeshStiffnessModel' types.
    """
    __qualname__ = 'GearMeshStiffnessModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5173.GearMeshStiffnessModel':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _5173.GearMeshStiffnessModel

    @classmethod
    def implicit_type(cls) -> '_5173.GearMeshStiffnessModel.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _5173.GearMeshStiffnessModel.type_()

    @property
    def selected_value(self) -> '_5173.GearMeshStiffnessModel':
        """GearMeshStiffnessModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_5173.GearMeshStiffnessModel]':
        """List[GearMeshStiffnessModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ShaftAndHousingFlexibilityOption(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ShaftAndHousingFlexibilityOption

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftAndHousingFlexibilityOption' types.
    """
    __qualname__ = 'ShaftAndHousingFlexibilityOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5218.ShaftAndHousingFlexibilityOption':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _5218.ShaftAndHousingFlexibilityOption

    @classmethod
    def implicit_type(cls) -> '_5218.ShaftAndHousingFlexibilityOption.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _5218.ShaftAndHousingFlexibilityOption.type_()

    @property
    def selected_value(self) -> '_5218.ShaftAndHousingFlexibilityOption':
        """ShaftAndHousingFlexibilityOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_5218.ShaftAndHousingFlexibilityOption]':
        """List[ShaftAndHousingFlexibilityOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_ExportOutputType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ExportOutputType

    A specific implementation of 'EnumWithSelectedValue' for 'ExportOutputType' types.
    """
    __qualname__ = 'ExportOutputType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5477.ExportOutputType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _5477.ExportOutputType

    @classmethod
    def implicit_type(cls) -> '_5477.ExportOutputType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _5477.ExportOutputType.type_()

    @property
    def selected_value(self) -> '_5477.ExportOutputType':
        """ExportOutputType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_5477.ExportOutputType]':
        """List[ExportOutputType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput

    A specific implementation of 'EnumWithSelectedValue' for 'HarmonicAnalysisFEExportOptions.ComplexNumberOutput' types.
    """
    __qualname__ = 'HarmonicAnalysisFEExportOptions.ComplexNumberOutput'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5495.HarmonicAnalysisFEExportOptions.ComplexNumberOutput':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _5495.HarmonicAnalysisFEExportOptions.ComplexNumberOutput

    @classmethod
    def implicit_type(cls) -> '_5495.HarmonicAnalysisFEExportOptions.ComplexNumberOutput.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _5495.HarmonicAnalysisFEExportOptions.ComplexNumberOutput.type_()

    @property
    def selected_value(self) -> '_5495.HarmonicAnalysisFEExportOptions.ComplexNumberOutput':
        """HarmonicAnalysisFEExportOptions.ComplexNumberOutput: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_5495.HarmonicAnalysisFEExportOptions.ComplexNumberOutput]':
        """List[HarmonicAnalysisFEExportOptions.ComplexNumberOutput]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_FrictionModelForGyroscopicMoment(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_FrictionModelForGyroscopicMoment

    A specific implementation of 'EnumWithSelectedValue' for 'FrictionModelForGyroscopicMoment' types.
    """
    __qualname__ = 'FrictionModelForGyroscopicMoment'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1734.FrictionModelForGyroscopicMoment':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1734.FrictionModelForGyroscopicMoment

    @classmethod
    def implicit_type(cls) -> '_1734.FrictionModelForGyroscopicMoment.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1734.FrictionModelForGyroscopicMoment.type_()

    @property
    def selected_value(self) -> '_1734.FrictionModelForGyroscopicMoment':
        """FrictionModelForGyroscopicMoment: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1734.FrictionModelForGyroscopicMoment]':
        """List[FrictionModelForGyroscopicMoment]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_MeshStiffnessModel(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_MeshStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'MeshStiffnessModel' types.
    """
    __qualname__ = 'MeshStiffnessModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1968.MeshStiffnessModel':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1968.MeshStiffnessModel

    @classmethod
    def implicit_type(cls) -> '_1968.MeshStiffnessModel.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1968.MeshStiffnessModel.type_()

    @property
    def selected_value(self) -> '_1968.MeshStiffnessModel':
        """MeshStiffnessModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1968.MeshStiffnessModel]':
        """List[MeshStiffnessModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_StressConcentrationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_StressConcentrationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'StressConcentrationMethod' types.
    """
    __qualname__ = 'StressConcentrationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1868.StressConcentrationMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1868.StressConcentrationMethod

    @classmethod
    def implicit_type(cls) -> '_1868.StressConcentrationMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1868.StressConcentrationMethod.type_()

    @property
    def selected_value(self) -> '_1868.StressConcentrationMethod':
        """StressConcentrationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1868.StressConcentrationMethod]':
        """List[StressConcentrationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'HertzianContactDeflectionCalculationMethod' types.
    """
    __qualname__ = 'HertzianContactDeflectionCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1378.HertzianContactDeflectionCalculationMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1378.HertzianContactDeflectionCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_1378.HertzianContactDeflectionCalculationMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1378.HertzianContactDeflectionCalculationMethod.type_()

    @property
    def selected_value(self) -> '_1378.HertzianContactDeflectionCalculationMethod':
        """HertzianContactDeflectionCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1378.HertzianContactDeflectionCalculationMethod]':
        """List[HertzianContactDeflectionCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_HarmonicLoadDataType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_HarmonicLoadDataType

    A specific implementation of 'EnumWithSelectedValue' for 'HarmonicLoadDataType' types.
    """
    __qualname__ = 'HarmonicLoadDataType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6630.HarmonicLoadDataType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _6630.HarmonicLoadDataType

    @classmethod
    def implicit_type(cls) -> '_6630.HarmonicLoadDataType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _6630.HarmonicLoadDataType.type_()

    @property
    def selected_value(self) -> '_6630.HarmonicLoadDataType':
        """HarmonicLoadDataType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_6630.HarmonicLoadDataType]':
        """List[HarmonicLoadDataType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_TorqueRippleInputType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_TorqueRippleInputType

    A specific implementation of 'EnumWithSelectedValue' for 'TorqueRippleInputType' types.
    """
    __qualname__ = 'TorqueRippleInputType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6704.TorqueRippleInputType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _6704.TorqueRippleInputType

    @classmethod
    def implicit_type(cls) -> '_6704.TorqueRippleInputType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _6704.TorqueRippleInputType.type_()

    @property
    def selected_value(self) -> '_6704.TorqueRippleInputType':
        """TorqueRippleInputType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_6704.TorqueRippleInputType]':
        """List[TorqueRippleInputType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_HarmonicExcitationType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_HarmonicExcitationType

    A specific implementation of 'EnumWithSelectedValue' for 'HarmonicExcitationType' types.
    """
    __qualname__ = 'HarmonicExcitationType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6621.HarmonicExcitationType':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _6621.HarmonicExcitationType

    @classmethod
    def implicit_type(cls) -> '_6621.HarmonicExcitationType.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _6621.HarmonicExcitationType.type_()

    @property
    def selected_value(self) -> '_6621.HarmonicExcitationType':
        """HarmonicExcitationType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_6621.HarmonicExcitationType]':
        """List[HarmonicExcitationType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification

    A specific implementation of 'EnumWithSelectedValue' for 'PointLoadLoadCase.ForceSpecification' types.
    """
    __qualname__ = 'PointLoadLoadCase.ForceSpecification'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6665.PointLoadLoadCase.ForceSpecification':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _6665.PointLoadLoadCase.ForceSpecification

    @classmethod
    def implicit_type(cls) -> '_6665.PointLoadLoadCase.ForceSpecification.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _6665.PointLoadLoadCase.ForceSpecification.type_()

    @property
    def selected_value(self) -> '_6665.PointLoadLoadCase.ForceSpecification':
        """PointLoadLoadCase.ForceSpecification: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_6665.PointLoadLoadCase.ForceSpecification]':
        """List[PointLoadLoadCase.ForceSpecification]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_TorqueSpecificationForSystemDeflection(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_TorqueSpecificationForSystemDeflection

    A specific implementation of 'EnumWithSelectedValue' for 'TorqueSpecificationForSystemDeflection' types.
    """
    __qualname__ = 'TorqueSpecificationForSystemDeflection'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6705.TorqueSpecificationForSystemDeflection':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _6705.TorqueSpecificationForSystemDeflection

    @classmethod
    def implicit_type(cls) -> '_6705.TorqueSpecificationForSystemDeflection.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _6705.TorqueSpecificationForSystemDeflection.type_()

    @property
    def selected_value(self) -> '_6705.TorqueSpecificationForSystemDeflection':
        """TorqueSpecificationForSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_6705.TorqueSpecificationForSystemDeflection]':
        """List[TorqueSpecificationForSystemDeflection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'PowerLoadInputTorqueSpecificationMethod' types.
    """
    __qualname__ = 'PowerLoadInputTorqueSpecificationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1971.PowerLoadInputTorqueSpecificationMethod':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1971.PowerLoadInputTorqueSpecificationMethod

    @classmethod
    def implicit_type(cls) -> '_1971.PowerLoadInputTorqueSpecificationMethod.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1971.PowerLoadInputTorqueSpecificationMethod.type_()

    @property
    def selected_value(self) -> '_1971.PowerLoadInputTorqueSpecificationMethod':
        """PowerLoadInputTorqueSpecificationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1971.PowerLoadInputTorqueSpecificationMethod]':
        """List[PowerLoadInputTorqueSpecificationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_TorqueConverterLockupRule(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_TorqueConverterLockupRule

    A specific implementation of 'EnumWithSelectedValue' for 'TorqueConverterLockupRule' types.
    """
    __qualname__ = 'TorqueConverterLockupRule'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5243.TorqueConverterLockupRule':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _5243.TorqueConverterLockupRule

    @classmethod
    def implicit_type(cls) -> '_5243.TorqueConverterLockupRule.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _5243.TorqueConverterLockupRule.type_()

    @property
    def selected_value(self) -> '_5243.TorqueConverterLockupRule':
        """TorqueConverterLockupRule: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_5243.TorqueConverterLockupRule]':
        """List[TorqueConverterLockupRule]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_DegreesOfFreedom(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_DegreesOfFreedom

    A specific implementation of 'EnumWithSelectedValue' for 'DegreesOfFreedom' types.
    """
    __qualname__ = 'DegreesOfFreedom'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1310.DegreesOfFreedom':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _1310.DegreesOfFreedom

    @classmethod
    def implicit_type(cls) -> '_1310.DegreesOfFreedom.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _1310.DegreesOfFreedom.type_()

    @property
    def selected_value(self) -> '_1310.DegreesOfFreedom':
        """DegreesOfFreedom: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_1310.DegreesOfFreedom]':
        """List[DegreesOfFreedom]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None


class EnumWithSelectedValue_DestinationDesignState(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_DestinationDesignState

    A specific implementation of 'EnumWithSelectedValue' for 'DestinationDesignState' types.
    """
    __qualname__ = 'DestinationDesignState'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        """Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6719.DestinationDesignState':
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        """

        return _6719.DestinationDesignState

    @classmethod
    def implicit_type(cls) -> '_6719.DestinationDesignState.type_()':
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        """

        return _6719.DestinationDesignState.type_()

    @property
    def selected_value(self) -> '_6719.DestinationDesignState':
        """DestinationDesignState: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None

    @property
    def available_values(self) -> 'List[_6719.DestinationDesignState]':
        """List[DestinationDesignState]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        return None
