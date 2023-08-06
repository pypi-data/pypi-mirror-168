"""_866.py

CylindricalGearTwoDimensionalFEAnalysis
"""


from mastapy._internal import constructor
from mastapy.nodal_analysis.dev_tools_analyses import _165
from mastapy.gears.gear_two_d_fe_analysis import _867
from mastapy.nodal_analysis.states import _120
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_TWO_DIMENSIONAL_FE_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.GearTwoDFEAnalysis', 'CylindricalGearTwoDimensionalFEAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearTwoDimensionalFEAnalysis',)


class CylindricalGearTwoDimensionalFEAnalysis(_0.APIBase):
    """CylindricalGearTwoDimensionalFEAnalysis

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_TWO_DIMENSIONAL_FE_ANALYSIS

    def __init__(self, instance_to_wrap: 'CylindricalGearTwoDimensionalFEAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_stress_states(self) -> 'int':
        """int: 'NumberOfStressStates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfStressStates

        if temp is None:
            return None

        return temp

    @property
    def fe_model(self) -> '_165.FEModel':
        """FEModel: 'FEModel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEModel

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def findley_critical_plane_analysis(self) -> '_867.FindleyCriticalPlaneAnalysis':
        """FindleyCriticalPlaneAnalysis: 'FindleyCriticalPlaneAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FindleyCriticalPlaneAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def get_stress_states(self, index: 'int') -> '_120.NodeVectorState':
        """ 'GetStressStates' is the original name of this method.

        Args:
            index (int)

        Returns:
            mastapy.nodal_analysis.states.NodeVectorState
        """

        index = int(index)
        method_result = self.wrapped.GetStressStates(index if index else 0)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def perform(self):
        """ 'Perform' is the original name of this method."""

        self.wrapped.Perform()
