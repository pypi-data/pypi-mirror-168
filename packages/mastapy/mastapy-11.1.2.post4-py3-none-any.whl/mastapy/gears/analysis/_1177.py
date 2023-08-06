"""_1177.py

GearMeshImplementationDetail
"""


from mastapy.gears.analysis import _1174
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_IMPLEMENTATION_DETAIL = python_net_import('SMT.MastaAPI.Gears.Analysis', 'GearMeshImplementationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshImplementationDetail',)


class GearMeshImplementationDetail(_1174.GearMeshDesignAnalysis):
    """GearMeshImplementationDetail

    This is a mastapy class.
    """

    TYPE = _GEAR_MESH_IMPLEMENTATION_DETAIL

    def __init__(self, instance_to_wrap: 'GearMeshImplementationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
