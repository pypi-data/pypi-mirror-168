"""_6628.py

HarmonicLoadDataJMAGImport
"""


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6623, _6605
from mastapy._internal.python_net import python_net_import

_HARMONIC_LOAD_DATA_JMAG_IMPORT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HarmonicLoadDataJMAGImport')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicLoadDataJMAGImport',)


class HarmonicLoadDataJMAGImport(_6623.HarmonicLoadDataCSVImport['_6605.ElectricMachineHarmonicLoadJMAGImportOptions']):
    """HarmonicLoadDataJMAGImport

    This is a mastapy class.
    """

    TYPE = _HARMONIC_LOAD_DATA_JMAG_IMPORT

    def __init__(self, instance_to_wrap: 'HarmonicLoadDataJMAGImport.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def select_jmag_file(self):
        """ 'SelectJMAGFile' is the original name of this method."""

        self.wrapped.SelectJMAGFile()
