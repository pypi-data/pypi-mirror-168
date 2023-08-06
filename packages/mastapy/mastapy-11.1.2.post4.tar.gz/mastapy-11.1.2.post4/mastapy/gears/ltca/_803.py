"""_803.py

GearFilletNodeStressResults
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_FILLET_NODE_STRESS_RESULTS = python_net_import('SMT.MastaAPI.Gears.LTCA', 'GearFilletNodeStressResults')


__docformat__ = 'restructuredtext en'
__all__ = ('GearFilletNodeStressResults',)


class GearFilletNodeStressResults(_0.APIBase):
    """GearFilletNodeStressResults

    This is a mastapy class.
    """

    TYPE = _GEAR_FILLET_NODE_STRESS_RESULTS

    def __init__(self, instance_to_wrap: 'GearFilletNodeStressResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def fillet_column_index(self) -> 'int':
        """int: 'FilletColumnIndex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FilletColumnIndex

        if temp is None:
            return None

        return temp

    @property
    def fillet_row_index(self) -> 'int':
        """int: 'FilletRowIndex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FilletRowIndex

        if temp is None:
            return None

        return temp

    @property
    def first_principal_stress(self) -> 'float':
        """float: 'FirstPrincipalStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FirstPrincipalStress

        if temp is None:
            return None

        return temp

    @property
    def maximum_tensile_principal_stress(self) -> 'float':
        """float: 'MaximumTensilePrincipalStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumTensilePrincipalStress

        if temp is None:
            return None

        return temp

    @property
    def second_principal_stress(self) -> 'float':
        """float: 'SecondPrincipalStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SecondPrincipalStress

        if temp is None:
            return None

        return temp

    @property
    def stress_intensity(self) -> 'float':
        """float: 'StressIntensity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressIntensity

        if temp is None:
            return None

        return temp

    @property
    def third_principal_stress(self) -> 'float':
        """float: 'ThirdPrincipalStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThirdPrincipalStress

        if temp is None:
            return None

        return temp

    @property
    def von_mises_stress(self) -> 'float':
        """float: 'VonMisesStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VonMisesStress

        if temp is None:
            return None

        return temp

    @property
    def x_component(self) -> 'float':
        """float: 'XComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.XComponent

        if temp is None:
            return None

        return temp

    @property
    def xy_shear_stress(self) -> 'float':
        """float: 'XYShearStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.XYShearStress

        if temp is None:
            return None

        return temp

    @property
    def xz_shear_stress(self) -> 'float':
        """float: 'XZShearStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.XZShearStress

        if temp is None:
            return None

        return temp

    @property
    def y_component(self) -> 'float':
        """float: 'YComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.YComponent

        if temp is None:
            return None

        return temp

    @property
    def yz_shear_stress(self) -> 'float':
        """float: 'YZShearStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.YZShearStress

        if temp is None:
            return None

        return temp

    @property
    def z_component(self) -> 'float':
        """float: 'ZComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZComponent

        if temp is None:
            return None

        return temp
