"""_6603.py

ElectricMachineHarmonicLoadFluxImportOptions
"""


from mastapy.system_model.analyses_and_results.static_loads import _6604
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_HARMONIC_LOAD_FLUX_IMPORT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ElectricMachineHarmonicLoadFluxImportOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineHarmonicLoadFluxImportOptions',)


class ElectricMachineHarmonicLoadFluxImportOptions(_6604.ElectricMachineHarmonicLoadImportOptionsBase):
    """ElectricMachineHarmonicLoadFluxImportOptions

    This is a mastapy class.
    """

    TYPE = _ELECTRIC_MACHINE_HARMONIC_LOAD_FLUX_IMPORT_OPTIONS

    def __init__(self, instance_to_wrap: 'ElectricMachineHarmonicLoadFluxImportOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
