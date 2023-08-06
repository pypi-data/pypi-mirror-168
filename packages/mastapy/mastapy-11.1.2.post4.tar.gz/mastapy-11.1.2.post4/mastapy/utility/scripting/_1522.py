"""_1522.py

UserDefinedPropertyKey
"""


from mastapy.utility.databases import _1602
from mastapy._internal.python_net import python_net_import

_USER_DEFINED_PROPERTY_KEY = python_net_import('SMT.MastaAPI.Utility.Scripting', 'UserDefinedPropertyKey')


__docformat__ = 'restructuredtext en'
__all__ = ('UserDefinedPropertyKey',)


class UserDefinedPropertyKey(_1602.DatabaseKey):
    """UserDefinedPropertyKey

    This is a mastapy class.
    """

    TYPE = _USER_DEFINED_PROPERTY_KEY

    def __init__(self, instance_to_wrap: 'UserDefinedPropertyKey.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
