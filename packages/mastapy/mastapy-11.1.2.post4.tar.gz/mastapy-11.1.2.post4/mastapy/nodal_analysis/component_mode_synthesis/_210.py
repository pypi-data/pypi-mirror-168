"""_210.py

ModalCMSResults
"""


from mastapy._internal import constructor
from mastapy.nodal_analysis.component_mode_synthesis import _211
from mastapy._internal.python_net import python_net_import

_MODAL_CMS_RESULTS = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'ModalCMSResults')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalCMSResults',)


class ModalCMSResults(_211.RealCMSResults):
    """ModalCMSResults

    This is a mastapy class.
    """

    TYPE = _MODAL_CMS_RESULTS

    def __init__(self, instance_to_wrap: 'ModalCMSResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def calculate_results(self) -> 'bool':
        """bool: 'CalculateResults' is the original name of this property."""

        temp = self.wrapped.CalculateResults

        if temp is None:
            return None

        return temp

    @calculate_results.setter
    def calculate_results(self, value: 'bool'):
        self.wrapped.CalculateResults = bool(value) if value else False

    @property
    def frequency(self) -> 'float':
        """float: 'Frequency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Frequency

        if temp is None:
            return None

        return temp

    @property
    def mode_id(self) -> 'int':
        """int: 'ModeID' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModeID

        if temp is None:
            return None

        return temp

    def calculate_strain_and_kinetic_energy(self):
        """ 'CalculateStrainAndKineticEnergy' is the original name of this method."""

        self.wrapped.CalculateStrainAndKineticEnergy()
