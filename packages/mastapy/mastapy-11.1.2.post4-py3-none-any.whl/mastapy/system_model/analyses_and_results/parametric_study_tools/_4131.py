"""_4131.py

ParametricStudyToolStepResult
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PARAMETRIC_STUDY_TOOL_STEP_RESULT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ParametricStudyToolStepResult')


__docformat__ = 'restructuredtext en'
__all__ = ('ParametricStudyToolStepResult',)


class ParametricStudyToolStepResult(_0.APIBase):
    """ParametricStudyToolStepResult

    This is a mastapy class.
    """

    TYPE = _PARAMETRIC_STUDY_TOOL_STEP_RESULT

    def __init__(self, instance_to_wrap: 'ParametricStudyToolStepResult.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def failure_message(self) -> 'str':
        """str: 'FailureMessage' is the original name of this property."""

        temp = self.wrapped.FailureMessage

        if temp is None:
            return None

        return temp

    @failure_message.setter
    def failure_message(self, value: 'str'):
        self.wrapped.FailureMessage = str(value) if value else ''

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property."""

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else ''

    @property
    def successful(self) -> 'bool':
        """bool: 'Successful' is the original name of this property."""

        temp = self.wrapped.Successful

        if temp is None:
            return None

        return temp

    @successful.setter
    def successful(self, value: 'bool'):
        self.wrapped.Successful = bool(value) if value else False
