"""_1993.py

AbstractSystemDeflectionViewable
"""


from mastapy.system_model.drawing import _1996, _2003
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2570
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2834
from mastapy.system_model.analyses_and_results.stability_analyses import _3613
from mastapy.system_model.analyses_and_results.rotor_dynamics import _3768
from mastapy.system_model.analyses_and_results.modal_analyses import _4392
from mastapy.system_model.analyses_and_results.mbd_analyses import _5195
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5493
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6054
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6307
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SYSTEM_DEFLECTION_VIEWABLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'AbstractSystemDeflectionViewable')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractSystemDeflectionViewable',)


class AbstractSystemDeflectionViewable(_2003.PartAnalysisCaseWithContourViewable):
    """AbstractSystemDeflectionViewable

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_SYSTEM_DEFLECTION_VIEWABLE

    def __init__(self, instance_to_wrap: 'AbstractSystemDeflectionViewable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contour_draw_style(self) -> '_1996.ContourDrawStyle':
        """ContourDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContourDrawStyle

        if temp is None:
            return None

        if _1996.ContourDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to ContourDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def contour_draw_style_of_type_system_deflection_draw_style(self) -> '_2570.SystemDeflectionDrawStyle':
        """SystemDeflectionDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContourDrawStyle

        if temp is None:
            return None

        if _2570.SystemDeflectionDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to SystemDeflectionDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def contour_draw_style_of_type_steady_state_synchronous_response_draw_style(self) -> '_2834.SteadyStateSynchronousResponseDrawStyle':
        """SteadyStateSynchronousResponseDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContourDrawStyle

        if temp is None:
            return None

        if _2834.SteadyStateSynchronousResponseDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to SteadyStateSynchronousResponseDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def contour_draw_style_of_type_stability_analysis_draw_style(self) -> '_3613.StabilityAnalysisDrawStyle':
        """StabilityAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContourDrawStyle

        if temp is None:
            return None

        if _3613.StabilityAnalysisDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to StabilityAnalysisDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def contour_draw_style_of_type_rotor_dynamics_draw_style(self) -> '_3768.RotorDynamicsDrawStyle':
        """RotorDynamicsDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContourDrawStyle

        if temp is None:
            return None

        if _3768.RotorDynamicsDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to RotorDynamicsDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def contour_draw_style_of_type_modal_analysis_draw_style(self) -> '_4392.ModalAnalysisDrawStyle':
        """ModalAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContourDrawStyle

        if temp is None:
            return None

        if _4392.ModalAnalysisDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to ModalAnalysisDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def contour_draw_style_of_type_mbd_analysis_draw_style(self) -> '_5195.MBDAnalysisDrawStyle':
        """MBDAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContourDrawStyle

        if temp is None:
            return None

        if _5195.MBDAnalysisDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to MBDAnalysisDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def contour_draw_style_of_type_harmonic_analysis_draw_style(self) -> '_5493.HarmonicAnalysisDrawStyle':
        """HarmonicAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContourDrawStyle

        if temp is None:
            return None

        if _5493.HarmonicAnalysisDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to HarmonicAnalysisDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def contour_draw_style_of_type_dynamic_analysis_draw_style(self) -> '_6054.DynamicAnalysisDrawStyle':
        """DynamicAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContourDrawStyle

        if temp is None:
            return None

        if _6054.DynamicAnalysisDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to DynamicAnalysisDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def contour_draw_style_of_type_critical_speed_analysis_draw_style(self) -> '_6307.CriticalSpeedAnalysisDrawStyle':
        """CriticalSpeedAnalysisDrawStyle: 'ContourDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContourDrawStyle

        if temp is None:
            return None

        if _6307.CriticalSpeedAnalysisDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast contour_draw_style to CriticalSpeedAnalysisDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_draw_style(self) -> '_2570.SystemDeflectionDrawStyle':
        """SystemDeflectionDrawStyle: 'SystemDeflectionDrawStyle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionDrawStyle

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def fe_results(self):
        """ 'FEResults' is the original name of this method."""

        self.wrapped.FEResults()
