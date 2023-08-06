"""_513.py

ConicalRateableMesh
"""


from mastapy.gears.rating import _339
from mastapy._internal.python_net import python_net_import

_CONICAL_RATEABLE_MESH = python_net_import('SMT.MastaAPI.Gears.Rating.Conical', 'ConicalRateableMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalRateableMesh',)


class ConicalRateableMesh(_339.RateableMesh):
    """ConicalRateableMesh

    This is a mastapy class.
    """

    TYPE = _CONICAL_RATEABLE_MESH

    def __init__(self, instance_to_wrap: 'ConicalRateableMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
