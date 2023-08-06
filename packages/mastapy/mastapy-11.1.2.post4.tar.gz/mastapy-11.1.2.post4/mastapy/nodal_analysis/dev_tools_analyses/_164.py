"""_164.py

FEEntityGroupInt
"""


from mastapy.nodal_analysis.dev_tools_analyses import _163
from mastapy._internal.python_net import python_net_import

_FE_ENTITY_GROUP_INT = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses', 'FEEntityGroupInt')


__docformat__ = 'restructuredtext en'
__all__ = ('FEEntityGroupInt',)


class FEEntityGroupInt(_163.FEEntityGroup['int']):
    """FEEntityGroupInt

    This is a mastapy class.
    """

    TYPE = _FE_ENTITY_GROUP_INT

    def __init__(self, instance_to_wrap: 'FEEntityGroupInt.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
