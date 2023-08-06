"""_2635.py

CVTBeltConnectionCompoundSystemDeflection
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2476
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2604
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CVTBeltConnectionCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionCompoundSystemDeflection',)


class CVTBeltConnectionCompoundSystemDeflection(_2604.BeltConnectionCompoundSystemDeflection):
    """CVTBeltConnectionCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CVT_BELT_CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def belt_safety_factor_for_clamping_force(self) -> 'float':
        """float: 'BeltSafetyFactorForClampingForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BeltSafetyFactorForClampingForce

        if temp is None:
            return None

        return temp

    @property
    def connection_analysis_cases_ready(self) -> 'List[_2476.CVTBeltConnectionSystemDeflection]':
        """List[CVTBeltConnectionSystemDeflection]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_2476.CVTBeltConnectionSystemDeflection]':
        """List[CVTBeltConnectionSystemDeflection]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
