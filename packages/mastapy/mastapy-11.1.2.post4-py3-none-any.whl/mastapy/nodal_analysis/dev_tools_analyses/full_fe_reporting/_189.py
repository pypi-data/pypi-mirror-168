"""_189.py

ElementPropertiesInterface
"""


from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import _187
from mastapy._internal.python_net import python_net_import

_ELEMENT_PROPERTIES_INTERFACE = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'ElementPropertiesInterface')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementPropertiesInterface',)


class ElementPropertiesInterface(_187.ElementPropertiesBase):
    """ElementPropertiesInterface

    This is a mastapy class.
    """

    TYPE = _ELEMENT_PROPERTIES_INTERFACE

    def __init__(self, instance_to_wrap: 'ElementPropertiesInterface.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
