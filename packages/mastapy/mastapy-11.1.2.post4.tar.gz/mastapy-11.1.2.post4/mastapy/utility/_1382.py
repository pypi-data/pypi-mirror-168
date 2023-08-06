"""_1382.py

Command
"""


from mastapy._internal import constructor
from mastapy import _7279
from mastapy._internal.python_net import python_net_import

_COMMAND = python_net_import('SMT.MastaAPI.Utility', 'Command')


__docformat__ = 'restructuredtext en'
__all__ = ('Command',)


class Command(_7279.MarshalByRefObjectPermanent):
    """Command

    This is a mastapy class.
    """

    TYPE = _COMMAND

    def __init__(self, instance_to_wrap: 'Command.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def run(self):
        """ 'Run' is the original name of this method."""

        self.wrapped.Run()
