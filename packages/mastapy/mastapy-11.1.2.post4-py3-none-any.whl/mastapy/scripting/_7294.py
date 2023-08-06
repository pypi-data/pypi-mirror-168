"""_7294.py

ScriptingCommand
"""


from mastapy._internal import constructor
from mastapy import _7279
from mastapy._internal.python_net import python_net_import

_SCRIPTING_COMMAND = python_net_import('SMT.MastaAPIUtility.Scripting', 'ScriptingCommand')


__docformat__ = 'restructuredtext en'
__all__ = ('ScriptingCommand',)


class ScriptingCommand(_7279.MarshalByRefObjectPermanent):
    """ScriptingCommand

    This is a mastapy class.
    """

    TYPE = _SCRIPTING_COMMAND

    def __init__(self, instance_to_wrap: 'ScriptingCommand.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def execute(self):
        """ 'Execute' is the original name of this method."""

        self.wrapped.Execute()
