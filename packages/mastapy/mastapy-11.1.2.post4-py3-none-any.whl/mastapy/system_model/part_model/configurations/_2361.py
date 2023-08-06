"""_2361.py

ActiveFESubstructureSelectionGroup
"""


from mastapy.system_model.part_model.configurations import _2366, _2360
from mastapy.system_model.part_model import _2203
from mastapy.system_model.fe import _2133
from mastapy._internal.python_net import python_net_import

_ACTIVE_FE_SUBSTRUCTURE_SELECTION_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveFESubstructureSelectionGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveFESubstructureSelectionGroup',)


class ActiveFESubstructureSelectionGroup(_2366.PartDetailConfiguration['_2360.ActiveFESubstructureSelection', '_2203.FEPart', '_2133.FESubstructure']):
    """ActiveFESubstructureSelectionGroup

    This is a mastapy class.
    """

    TYPE = _ACTIVE_FE_SUBSTRUCTURE_SELECTION_GROUP

    def __init__(self, instance_to_wrap: 'ActiveFESubstructureSelectionGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
