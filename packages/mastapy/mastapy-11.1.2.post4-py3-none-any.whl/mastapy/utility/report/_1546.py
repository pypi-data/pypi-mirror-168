"""_1546.py

CustomReportItemContainerCollectionItem
"""


from mastapy.utility.report import _1543
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_ITEM_CONTAINER_COLLECTION_ITEM = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportItemContainerCollectionItem')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportItemContainerCollectionItem',)


class CustomReportItemContainerCollectionItem(_1543.CustomReportItemContainer):
    """CustomReportItemContainerCollectionItem

    This is a mastapy class.
    """

    TYPE = _CUSTOM_REPORT_ITEM_CONTAINER_COLLECTION_ITEM

    def __init__(self, instance_to_wrap: 'CustomReportItemContainerCollectionItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
