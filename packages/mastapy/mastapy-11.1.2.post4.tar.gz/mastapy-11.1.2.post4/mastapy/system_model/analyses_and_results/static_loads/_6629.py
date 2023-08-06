"""_6629.py

HarmonicLoadDataMotorCADImport
"""


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6627, _6606
from mastapy._internal.python_net import python_net_import

_HARMONIC_LOAD_DATA_MOTOR_CAD_IMPORT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HarmonicLoadDataMotorCADImport')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicLoadDataMotorCADImport',)


class HarmonicLoadDataMotorCADImport(_6627.HarmonicLoadDataImportFromMotorPackages['_6606.ElectricMachineHarmonicLoadMotorCADImportOptions']):
    """HarmonicLoadDataMotorCADImport

    This is a mastapy class.
    """

    TYPE = _HARMONIC_LOAD_DATA_MOTOR_CAD_IMPORT

    def __init__(self, instance_to_wrap: 'HarmonicLoadDataMotorCADImport.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def derive_rotor_forces_from_stator_loads(self) -> 'bool':
        """bool: 'DeriveRotorForcesFromStatorLoads' is the original name of this property."""

        temp = self.wrapped.DeriveRotorForcesFromStatorLoads

        if temp is None:
            return None

        return temp

    @derive_rotor_forces_from_stator_loads.setter
    def derive_rotor_forces_from_stator_loads(self, value: 'bool'):
        self.wrapped.DeriveRotorForcesFromStatorLoads = bool(value) if value else False

    def select_motor_cad_file(self):
        """ 'SelectMotorCADFile' is the original name of this method."""

        self.wrapped.SelectMotorCADFile()
