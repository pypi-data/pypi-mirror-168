"""_1705.py

BearingStiffnessMatrixReporter
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results import _1728
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BEARING_STIFFNESS_MATRIX_REPORTER = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'BearingStiffnessMatrixReporter')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingStiffnessMatrixReporter',)


class BearingStiffnessMatrixReporter(_0.APIBase):
    """BearingStiffnessMatrixReporter

    This is a mastapy class.
    """

    TYPE = _BEARING_STIFFNESS_MATRIX_REPORTER

    def __init__(self, instance_to_wrap: 'BearingStiffnessMatrixReporter.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_stiffness(self) -> 'float':
        """float: 'AxialStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialStiffness

        if temp is None:
            return None

        return temp

    @property
    def maximum_radial_stiffness(self) -> 'float':
        """float: 'MaximumRadialStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumRadialStiffness

        if temp is None:
            return None

        return temp

    @property
    def maximum_tilt_stiffness(self) -> 'float':
        """float: 'MaximumTiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumTiltStiffness

        if temp is None:
            return None

        return temp

    @property
    def minimum_radial_stiffness(self) -> 'float':
        """float: 'MinimumRadialStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumRadialStiffness

        if temp is None:
            return None

        return temp

    @property
    def minimum_tilt_stiffness(self) -> 'float':
        """float: 'MinimumTiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumTiltStiffness

        if temp is None:
            return None

        return temp

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @property
    def radial_stiffness_variation(self) -> 'float':
        """float: 'RadialStiffnessVariation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialStiffnessVariation

        if temp is None:
            return None

        return temp

    @property
    def stiffness_xx(self) -> 'float':
        """float: 'StiffnessXX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessXX

        if temp is None:
            return None

        return temp

    @property
    def stiffness_xy(self) -> 'float':
        """float: 'StiffnessXY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessXY

        if temp is None:
            return None

        return temp

    @property
    def stiffness_xz(self) -> 'float':
        """float: 'StiffnessXZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessXZ

        if temp is None:
            return None

        return temp

    @property
    def stiffness_x_theta_x(self) -> 'float':
        """float: 'StiffnessXThetaX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessXThetaX

        if temp is None:
            return None

        return temp

    @property
    def stiffness_x_theta_y(self) -> 'float':
        """float: 'StiffnessXThetaY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessXThetaY

        if temp is None:
            return None

        return temp

    @property
    def stiffness_x_theta_z(self) -> 'float':
        """float: 'StiffnessXThetaZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessXThetaZ

        if temp is None:
            return None

        return temp

    @property
    def stiffness_yx(self) -> 'float':
        """float: 'StiffnessYX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessYX

        if temp is None:
            return None

        return temp

    @property
    def stiffness_yy(self) -> 'float':
        """float: 'StiffnessYY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessYY

        if temp is None:
            return None

        return temp

    @property
    def stiffness_yz(self) -> 'float':
        """float: 'StiffnessYZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessYZ

        if temp is None:
            return None

        return temp

    @property
    def stiffness_y_theta_x(self) -> 'float':
        """float: 'StiffnessYThetaX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessYThetaX

        if temp is None:
            return None

        return temp

    @property
    def stiffness_y_theta_y(self) -> 'float':
        """float: 'StiffnessYThetaY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessYThetaY

        if temp is None:
            return None

        return temp

    @property
    def stiffness_y_theta_z(self) -> 'float':
        """float: 'StiffnessYThetaZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessYThetaZ

        if temp is None:
            return None

        return temp

    @property
    def stiffness_zx(self) -> 'float':
        """float: 'StiffnessZX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessZX

        if temp is None:
            return None

        return temp

    @property
    def stiffness_zy(self) -> 'float':
        """float: 'StiffnessZY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessZY

        if temp is None:
            return None

        return temp

    @property
    def stiffness_zz(self) -> 'float':
        """float: 'StiffnessZZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessZZ

        if temp is None:
            return None

        return temp

    @property
    def stiffness_z_theta_x(self) -> 'float':
        """float: 'StiffnessZThetaX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessZThetaX

        if temp is None:
            return None

        return temp

    @property
    def stiffness_z_theta_y(self) -> 'float':
        """float: 'StiffnessZThetaY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessZThetaY

        if temp is None:
            return None

        return temp

    @property
    def stiffness_z_theta_z(self) -> 'float':
        """float: 'StiffnessZThetaZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessZThetaZ

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_xx(self) -> 'float':
        """float: 'StiffnessThetaXX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaXX

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_xy(self) -> 'float':
        """float: 'StiffnessThetaXY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaXY

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_xz(self) -> 'float':
        """float: 'StiffnessThetaXZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaXZ

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_x_theta_x(self) -> 'float':
        """float: 'StiffnessThetaXThetaX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaXThetaX

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_x_theta_y(self) -> 'float':
        """float: 'StiffnessThetaXThetaY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaXThetaY

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_x_theta_z(self) -> 'float':
        """float: 'StiffnessThetaXThetaZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaXThetaZ

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_yx(self) -> 'float':
        """float: 'StiffnessThetaYX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaYX

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_yy(self) -> 'float':
        """float: 'StiffnessThetaYY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaYY

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_yz(self) -> 'float':
        """float: 'StiffnessThetaYZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaYZ

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_y_theta_x(self) -> 'float':
        """float: 'StiffnessThetaYThetaX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaYThetaX

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_y_theta_y(self) -> 'float':
        """float: 'StiffnessThetaYThetaY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaYThetaY

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_y_theta_z(self) -> 'float':
        """float: 'StiffnessThetaYThetaZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaYThetaZ

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_zx(self) -> 'float':
        """float: 'StiffnessThetaZX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaZX

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_zy(self) -> 'float':
        """float: 'StiffnessThetaZY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaZY

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_zz(self) -> 'float':
        """float: 'StiffnessThetaZZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaZZ

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_z_theta_x(self) -> 'float':
        """float: 'StiffnessThetaZThetaX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaZThetaX

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_z_theta_y(self) -> 'float':
        """float: 'StiffnessThetaZThetaY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaZThetaY

        if temp is None:
            return None

        return temp

    @property
    def stiffness_theta_z_theta_z(self) -> 'float':
        """float: 'StiffnessThetaZThetaZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StiffnessThetaZThetaZ

        if temp is None:
            return None

        return temp

    @property
    def tilt_stiffness_variation(self) -> 'float':
        """float: 'TiltStiffnessVariation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TiltStiffnessVariation

        if temp is None:
            return None

        return temp

    @property
    def torsional_stiffness(self) -> 'float':
        """float: 'TorsionalStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorsionalStiffness

        if temp is None:
            return None

        return temp

    @property
    def rows(self) -> 'List[_1728.StiffnessRow]':
        """List[StiffnessRow]: 'Rows' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rows

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
