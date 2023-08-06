"""_1883.py

LoadedPlainOilFedJournalBearingRow
"""


from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results.fluid_film import _1881
from mastapy._internal.python_net import python_net_import

_LOADED_PLAIN_OIL_FED_JOURNAL_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.FluidFilm', 'LoadedPlainOilFedJournalBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedPlainOilFedJournalBearingRow',)


class LoadedPlainOilFedJournalBearingRow(_1881.LoadedPlainJournalBearingRow):
    """LoadedPlainOilFedJournalBearingRow

    This is a mastapy class.
    """

    TYPE = _LOADED_PLAIN_OIL_FED_JOURNAL_BEARING_ROW

    def __init__(self, instance_to_wrap: 'LoadedPlainOilFedJournalBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def attitude_correction_factor(self) -> 'float':
        """float: 'AttitudeCorrectionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AttitudeCorrectionFactor

        if temp is None:
            return None

        return temp

    @property
    def load_correction_factor(self) -> 'float':
        """float: 'LoadCorrectionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadCorrectionFactor

        if temp is None:
            return None

        return temp

    @property
    def misalignment_angle(self) -> 'float':
        """float: 'MisalignmentAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentAngle

        if temp is None:
            return None

        return temp

    @property
    def non_dimensional_misalignment(self) -> 'float':
        """float: 'NonDimensionalMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NonDimensionalMisalignment

        if temp is None:
            return None

        return temp

    @property
    def power_correction_factor(self) -> 'float':
        """float: 'PowerCorrectionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerCorrectionFactor

        if temp is None:
            return None

        return temp

    @property
    def pressure_distribution(self) -> 'Image':
        """Image: 'PressureDistribution' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PressureDistribution

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def side_flow_correction_factor(self) -> 'float':
        """float: 'SideFlowCorrectionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SideFlowCorrectionFactor

        if temp is None:
            return None

        return temp
