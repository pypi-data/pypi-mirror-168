"""_3550.py

CVTStabilityAnalysis
"""


from mastapy.system_model.part_model.couplings import _2335
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.stability_analyses import _3517
from mastapy._internal.python_net import python_net_import

_CVT_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'CVTStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTStabilityAnalysis',)


class CVTStabilityAnalysis(_3517.BeltDriveStabilityAnalysis):
    """CVTStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _CVT_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'CVTStabilityAnalysis.TYPE'):
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
