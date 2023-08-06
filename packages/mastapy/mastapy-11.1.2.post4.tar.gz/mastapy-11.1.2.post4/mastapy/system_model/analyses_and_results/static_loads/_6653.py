"""_6653.py

OilSealLoadCase
"""


from mastapy.system_model.part_model import _2216
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6573
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'OilSealLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealLoadCase',)


class OilSealLoadCase(_6573.ConnectorLoadCase):
    """OilSealLoadCase

    This is a mastapy class.
    """

    TYPE = _OIL_SEAL_LOAD_CASE

    def __init__(self, instance_to_wrap: 'OilSealLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2216.OilSeal':
        """OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
