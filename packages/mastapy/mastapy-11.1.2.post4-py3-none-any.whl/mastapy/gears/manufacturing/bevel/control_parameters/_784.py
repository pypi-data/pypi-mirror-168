"""_784.py

ConicalManufacturingSGMControlParameters
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.bevel.control_parameters import _783
from mastapy._internal.python_net import python_net_import

_CONICAL_MANUFACTURING_SGM_CONTROL_PARAMETERS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel.ControlParameters', 'ConicalManufacturingSGMControlParameters')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalManufacturingSGMControlParameters',)


class ConicalManufacturingSGMControlParameters(_783.ConicalGearManufacturingControlParameters):
    """ConicalManufacturingSGMControlParameters

    This is a mastapy class.
    """

    TYPE = _CONICAL_MANUFACTURING_SGM_CONTROL_PARAMETERS

    def __init__(self, instance_to_wrap: 'ConicalManufacturingSGMControlParameters.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def delta_gamma(self) -> 'float':
        """float: 'DeltaGamma' is the original name of this property."""

        temp = self.wrapped.DeltaGamma

        if temp is None:
            return None

        return temp

    @delta_gamma.setter
    def delta_gamma(self, value: 'float'):
        self.wrapped.DeltaGamma = float(value) if value else 0.0

    @property
    def profile_mismatch_factor(self) -> 'float':
        """float: 'ProfileMismatchFactor' is the original name of this property."""

        temp = self.wrapped.ProfileMismatchFactor

        if temp is None:
            return None

        return temp

    @profile_mismatch_factor.setter
    def profile_mismatch_factor(self, value: 'float'):
        self.wrapped.ProfileMismatchFactor = float(value) if value else 0.0

    @property
    def work_head_offset_change(self) -> 'float':
        """float: 'WorkHeadOffsetChange' is the original name of this property."""

        temp = self.wrapped.WorkHeadOffsetChange

        if temp is None:
            return None

        return temp

    @work_head_offset_change.setter
    def work_head_offset_change(self, value: 'float'):
        self.wrapped.WorkHeadOffsetChange = float(value) if value else 0.0
