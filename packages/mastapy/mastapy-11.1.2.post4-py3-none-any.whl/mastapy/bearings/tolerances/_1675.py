"""_1675.py

MountingSleeveDiameterDetail
"""


from mastapy.bearings.tolerances import _1672
from mastapy._internal.python_net import python_net_import

_MOUNTING_SLEEVE_DIAMETER_DETAIL = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'MountingSleeveDiameterDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('MountingSleeveDiameterDetail',)


class MountingSleeveDiameterDetail(_1672.InterferenceDetail):
    """MountingSleeveDiameterDetail

    This is a mastapy class.
    """

    TYPE = _MOUNTING_SLEEVE_DIAMETER_DETAIL

    def __init__(self, instance_to_wrap: 'MountingSleeveDiameterDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
