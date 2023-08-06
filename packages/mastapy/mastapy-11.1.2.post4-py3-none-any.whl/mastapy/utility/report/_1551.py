"""_1551.py

CustomReportNamedItem
"""


from mastapy.utility.report import _1550
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_NAMED_ITEM = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportNamedItem')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportNamedItem',)


class CustomReportNamedItem(_1550.CustomReportNameableItem):
    """CustomReportNamedItem

    This is a mastapy class.
    """

    TYPE = _CUSTOM_REPORT_NAMED_ITEM

    def __init__(self, instance_to_wrap: 'CustomReportNamedItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
