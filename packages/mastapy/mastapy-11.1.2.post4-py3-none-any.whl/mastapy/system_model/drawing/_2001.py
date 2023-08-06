"""_2001.py

ModalAnalysisViewable
"""


from mastapy.system_model.analyses_and_results.dynamic_analyses import _6054
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses import _4392
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5493
from mastapy.system_model.drawing import _1998
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS_VIEWABLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'ModalAnalysisViewable')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysisViewable',)


class ModalAnalysisViewable(_1998.DynamicAnalysisViewable):
    """ModalAnalysisViewable

    This is a mastapy class.
    """

    TYPE = _MODAL_ANALYSIS_VIEWABLE

    def __init__(self, instance_to_wrap: 'ModalAnalysisViewable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def dynamic_analysis_draw_style(self) -> '_6054.DynamicAnalysisDrawStyle':
        """DynamicAnalysisDrawStyle: 'DynamicAnalysisDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicAnalysisDrawStyle

        if temp is None:
            return None

        if _6054.DynamicAnalysisDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast dynamic_analysis_draw_style to DynamicAnalysisDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def dynamic_analysis_draw_style_of_type_modal_analysis_draw_style(self) -> '_4392.ModalAnalysisDrawStyle':
        """ModalAnalysisDrawStyle: 'DynamicAnalysisDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicAnalysisDrawStyle

        if temp is None:
            return None

        if _4392.ModalAnalysisDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast dynamic_analysis_draw_style to ModalAnalysisDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def dynamic_analysis_draw_style_of_type_harmonic_analysis_draw_style(self) -> '_5493.HarmonicAnalysisDrawStyle':
        """HarmonicAnalysisDrawStyle: 'DynamicAnalysisDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicAnalysisDrawStyle

        if temp is None:
            return None

        if _5493.HarmonicAnalysisDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast dynamic_analysis_draw_style to HarmonicAnalysisDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
