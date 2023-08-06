"""_7262.py

AbstractAnalysisOptions
"""


from typing import Generic, TypeVar

from mastapy import _0
from mastapy.system_model.analyses_and_results.static_loads import _6527
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ANALYSIS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases', 'AbstractAnalysisOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractAnalysisOptions',)


T = TypeVar('T', bound='_6527.LoadCase')


class AbstractAnalysisOptions(_0.APIBase, Generic[T]):
    """AbstractAnalysisOptions

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _ABSTRACT_ANALYSIS_OPTIONS

    def __init__(self, instance_to_wrap: 'AbstractAnalysisOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
