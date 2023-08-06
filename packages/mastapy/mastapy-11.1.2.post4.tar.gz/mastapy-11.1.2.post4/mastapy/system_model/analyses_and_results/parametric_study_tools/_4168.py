"""_4168.py

SynchroniserParametricStudyTool
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2351
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6696
from mastapy.system_model.analyses_and_results.system_deflections import _2568
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4152
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'SynchroniserParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserParametricStudyTool',)


class SynchroniserParametricStudyTool(_4152.SpecialisedAssemblyParametricStudyTool):
    """SynchroniserParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'SynchroniserParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2351.Synchroniser':
        """Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6696.SynchroniserLoadCase':
        """SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2568.SynchroniserSystemDeflection]':
        """List[SynchroniserSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblySystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
