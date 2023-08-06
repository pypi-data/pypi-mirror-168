"""_4077.py

CVTParametricStudyTool
"""


from mastapy.system_model.part_model.couplings import _2335
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4046
from mastapy._internal.python_net import python_net_import

_CVT_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'CVTParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTParametricStudyTool',)


class CVTParametricStudyTool(_4046.BeltDriveParametricStudyTool):
    """CVTParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _CVT_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'CVTParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2335.CVT':
        """CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
