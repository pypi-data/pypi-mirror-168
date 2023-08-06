"""_6558.py

ClutchLoadCase
"""


from mastapy.system_model.part_model.couplings import _2327
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6576
from mastapy._internal.python_net import python_net_import

_CLUTCH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ClutchLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchLoadCase',)


class ClutchLoadCase(_6576.CouplingLoadCase):
    """ClutchLoadCase

    This is a mastapy class.
    """

    TYPE = _CLUTCH_LOAD_CASE

    def __init__(self, instance_to_wrap: 'ClutchLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2327.Clutch':
        """Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
