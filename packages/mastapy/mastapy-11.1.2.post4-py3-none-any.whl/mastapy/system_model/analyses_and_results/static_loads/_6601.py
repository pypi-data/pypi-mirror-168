"""_6601.py

ElectricMachineHarmonicLoadDataFromMotorPackages
"""


from typing import Generic, TypeVar

from mastapy.system_model.analyses_and_results.static_loads import _6596, _6604
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_MOTOR_PACKAGES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ElectricMachineHarmonicLoadDataFromMotorPackages')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineHarmonicLoadDataFromMotorPackages',)


T = TypeVar('T', bound='_6604.ElectricMachineHarmonicLoadImportOptionsBase')


class ElectricMachineHarmonicLoadDataFromMotorPackages(_6596.ElectricMachineHarmonicLoadData, Generic[T]):
    """ElectricMachineHarmonicLoadDataFromMotorPackages

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_MOTOR_PACKAGES

    def __init__(self, instance_to_wrap: 'ElectricMachineHarmonicLoadDataFromMotorPackages.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
