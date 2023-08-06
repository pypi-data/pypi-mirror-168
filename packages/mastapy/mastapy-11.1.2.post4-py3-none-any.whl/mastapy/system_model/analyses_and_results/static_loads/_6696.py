"""_6696.py

SynchroniserLoadCase
"""


from mastapy.system_model.part_model.couplings import _2351
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6679
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SynchroniserLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserLoadCase',)


class SynchroniserLoadCase(_6679.SpecialisedAssemblyLoadCase):
    """SynchroniserLoadCase

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_LOAD_CASE

    def __init__(self, instance_to_wrap: 'SynchroniserLoadCase.TYPE'):
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
