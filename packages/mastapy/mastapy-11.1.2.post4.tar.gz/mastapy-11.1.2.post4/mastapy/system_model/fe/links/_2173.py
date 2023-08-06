"""_2173.py

MultiAngleConnectionFELink
"""


from mastapy.system_model.fe.links import _2175
from mastapy._internal.python_net import python_net_import

_MULTI_ANGLE_CONNECTION_FE_LINK = python_net_import('SMT.MastaAPI.SystemModel.FE.Links', 'MultiAngleConnectionFELink')


__docformat__ = 'restructuredtext en'
__all__ = ('MultiAngleConnectionFELink',)


class MultiAngleConnectionFELink(_2175.MultiNodeFELink):
    """MultiAngleConnectionFELink

    This is a mastapy class.
    """

    TYPE = _MULTI_ANGLE_CONNECTION_FE_LINK

    def __init__(self, instance_to_wrap: 'MultiAngleConnectionFELink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
