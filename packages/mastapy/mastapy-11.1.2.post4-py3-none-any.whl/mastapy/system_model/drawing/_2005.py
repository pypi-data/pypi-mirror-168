"""_2005.py

RotorDynamicsViewable
"""


from typing import List

from mastapy.system_model.analyses_and_results.rotor_dynamics import _3768
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2834
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.stability_analyses import _3613
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6307
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ROTOR_DYNAMICS_VIEWABLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'RotorDynamicsViewable')


__docformat__ = 'restructuredtext en'
__all__ = ('RotorDynamicsViewable',)


class RotorDynamicsViewable(_0.APIBase):
    """RotorDynamicsViewable

    This is a mastapy class.
    """

    TYPE = _ROTOR_DYNAMICS_VIEWABLE

    def __init__(self, instance_to_wrap: 'RotorDynamicsViewable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rotor_dynamics(self) -> '_3768.RotorDynamicsDrawStyle':
        """RotorDynamicsDrawStyle: 'RotorDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RotorDynamics

        if temp is None:
            return None

        if _3768.RotorDynamicsDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rotor_dynamics to RotorDynamicsDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rotor_dynamics_of_type_steady_state_synchronous_response_draw_style(self) -> '_2834.SteadyStateSynchronousResponseDrawStyle':
        """SteadyStateSynchronousResponseDrawStyle: 'RotorDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RotorDynamics

        if temp is None:
            return None

        if _2834.SteadyStateSynchronousResponseDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rotor_dynamics to SteadyStateSynchronousResponseDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rotor_dynamics_of_type_stability_analysis_draw_style(self) -> '_3613.StabilityAnalysisDrawStyle':
        """StabilityAnalysisDrawStyle: 'RotorDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RotorDynamics

        if temp is None:
            return None

        if _3613.StabilityAnalysisDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rotor_dynamics to StabilityAnalysisDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rotor_dynamics_of_type_critical_speed_analysis_draw_style(self) -> '_6307.CriticalSpeedAnalysisDrawStyle':
        """CriticalSpeedAnalysisDrawStyle: 'RotorDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RotorDynamics

        if temp is None:
            return None

        if _6307.CriticalSpeedAnalysisDrawStyle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast rotor_dynamics to CriticalSpeedAnalysisDrawStyle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def report_names(self) -> 'List[str]':
        """List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReportNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)
        return value

    def output_default_report_to(self, file_path: 'str'):
        """ 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else '')

    def get_default_report_with_encoded_images(self) -> 'str':
        """ 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        """ 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else '')

    def output_active_report_as_text_to(self, file_path: 'str'):
        """ 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else '')

    def get_active_report_with_encoded_images(self) -> 'str':
        """ 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else '', file_path if file_path else '')

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        """ 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        """

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else '')
        return method_result
