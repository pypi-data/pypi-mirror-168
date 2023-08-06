"""_2636.py

CVTCompoundSystemDeflection
"""


from typing import List

from mastapy.system_model.analyses_and_results.system_deflections import _2478
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2605
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CVTCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundSystemDeflection',)


class CVTCompoundSystemDeflection(_2605.BeltDriveCompoundSystemDeflection):
    """CVTCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CVT_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'CVTCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2478.CVTSystemDeflection]':
        """List[CVTSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2478.CVTSystemDeflection]':
        """List[CVTSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
