"""_7278.py

ConsoleProgress
"""


from typing import Optional

from mastapy._internal import constructor
from mastapy import _7285
from mastapy._internal.python_net import python_net_import

_CONSOLE_PROGRESS = python_net_import('SMT.MastaAPIUtility', 'ConsoleProgress')


__docformat__ = 'restructuredtext en'
__all__ = ('ConsoleProgress',)


class ConsoleProgress(_7285.TaskProgress):
    """ConsoleProgress

    This is a mastapy class.
    """

    TYPE = _CONSOLE_PROGRESS

    def __init__(self, instance_to_wrap: 'ConsoleProgress.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def id(self) -> 'int':
        """int: 'Id' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Id

        if temp is None:
            return None

        return temp

    def add_error(self, error: 'str'):
        """ 'AddError' is the original name of this method.

        Args:
            error (str)
        """

        error = str(error)
        self.wrapped.AddError(error if error else '')

    def complete(self):
        """ 'Complete' is the original name of this method."""

        self.wrapped.Complete()

    def update_status(self, new_status: 'str'):
        """ 'UpdateStatus' is the original name of this method.

        Args:
            new_status (str)
        """

        new_status = str(new_status)
        self.wrapped.UpdateStatus(new_status if new_status else '')

    def increment_progress(self, inc: Optional['int'] = 1):
        """ 'IncrementProgress' is the original name of this method.

        Args:
            inc (int, optional)
        """

        inc = int(inc)
        self.wrapped.IncrementProgress(inc if inc else 0)
