"""_303.py

GearSetOptimisationResults
"""


from typing import List
from datetime import datetime

from mastapy._internal import constructor, conversion
from mastapy.gears import _302
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_SET_OPTIMISATION_RESULTS = python_net_import('SMT.MastaAPI.Gears', 'GearSetOptimisationResults')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetOptimisationResults',)


class GearSetOptimisationResults(_0.APIBase):
    """GearSetOptimisationResults

    This is a mastapy class.
    """

    TYPE = _GEAR_SET_OPTIMISATION_RESULTS

    def __init__(self, instance_to_wrap: 'GearSetOptimisationResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property."""

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else ''

    @property
    def optimiser_settings_report_table(self) -> 'str':
        """str: 'OptimiserSettingsReportTable' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OptimiserSettingsReportTable

        if temp is None:
            return None

        return temp

    @property
    def report(self) -> 'str':
        """str: 'Report' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Report

        if temp is None:
            return None

        return temp

    @property
    def results(self) -> 'List[_302.GearSetOptimisationResult]':
        """List[GearSetOptimisationResult]: 'Results' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Results

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def run_time(self) -> 'datetime':
        """datetime: 'RunTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RunTime

        if temp is None:
            return None

        value = conversion.pn_to_mp_datetime(temp)
        return value

    def delete_all_results(self):
        """ 'DeleteAllResults' is the original name of this method."""

        self.wrapped.DeleteAllResults()
