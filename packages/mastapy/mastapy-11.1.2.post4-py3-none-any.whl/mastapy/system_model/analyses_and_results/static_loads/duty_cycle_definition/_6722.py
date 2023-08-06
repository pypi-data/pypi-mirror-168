"""_6722.py

LoadCaseNameOptions
"""


from mastapy.utility_gui import _1622
from mastapy._internal.python_net import python_net_import

_LOAD_CASE_NAME_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition', 'LoadCaseNameOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadCaseNameOptions',)


class LoadCaseNameOptions(_1622.ColumnInputOptions):
    """LoadCaseNameOptions

    This is a mastapy class.
    """

    TYPE = _LOAD_CASE_NAME_OPTIONS

    def __init__(self, instance_to_wrap: 'LoadCaseNameOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
