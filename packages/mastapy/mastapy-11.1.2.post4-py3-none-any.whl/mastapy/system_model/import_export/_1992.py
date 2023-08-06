"""_1992.py

GeometryExportOptions
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEOMETRY_EXPORT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.ImportExport', 'GeometryExportOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('GeometryExportOptions',)


class GeometryExportOptions(_0.APIBase):
    """GeometryExportOptions

    This is a mastapy class.
    """

    TYPE = _GEOMETRY_EXPORT_OPTIONS

    def __init__(self, instance_to_wrap: 'GeometryExportOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def create_solid(self) -> 'bool':
        """bool: 'CreateSolid' is the original name of this property."""

        temp = self.wrapped.CreateSolid

        if temp is None:
            return None

        return temp

    @create_solid.setter
    def create_solid(self, value: 'bool'):
        self.wrapped.CreateSolid = bool(value) if value else False

    @property
    def draw_fillets(self) -> 'bool':
        """bool: 'DrawFillets' is the original name of this property."""

        temp = self.wrapped.DrawFillets

        if temp is None:
            return None

        return temp

    @draw_fillets.setter
    def draw_fillets(self, value: 'bool'):
        self.wrapped.DrawFillets = bool(value) if value else False

    @property
    def draw_gear_teeth(self) -> 'bool':
        """bool: 'DrawGearTeeth' is the original name of this property."""

        temp = self.wrapped.DrawGearTeeth

        if temp is None:
            return None

        return temp

    @draw_gear_teeth.setter
    def draw_gear_teeth(self, value: 'bool'):
        self.wrapped.DrawGearTeeth = bool(value) if value else False

    @property
    def draw_to_tip_diameter(self) -> 'bool':
        """bool: 'DrawToTipDiameter' is the original name of this property."""

        temp = self.wrapped.DrawToTipDiameter

        if temp is None:
            return None

        return temp

    @draw_to_tip_diameter.setter
    def draw_to_tip_diameter(self, value: 'bool'):
        self.wrapped.DrawToTipDiameter = bool(value) if value else False

    @property
    def number_of_points_per_cycloidal_disc_half_lobe(self) -> 'int':
        """int: 'NumberOfPointsPerCycloidalDiscHalfLobe' is the original name of this property."""

        temp = self.wrapped.NumberOfPointsPerCycloidalDiscHalfLobe

        if temp is None:
            return None

        return temp

    @number_of_points_per_cycloidal_disc_half_lobe.setter
    def number_of_points_per_cycloidal_disc_half_lobe(self, value: 'int'):
        self.wrapped.NumberOfPointsPerCycloidalDiscHalfLobe = int(value) if value else 0

    def export_to_stp(self, file_name: 'str'):
        """ 'ExportToSTP' is the original name of this method.

        Args:
            file_name (str)
        """

        file_name = str(file_name)
        self.wrapped.ExportToSTP(file_name if file_name else '')

    def to_stl_code(self) -> 'str':
        """ 'ToSTLCode' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.ToSTLCode()
        return method_result
