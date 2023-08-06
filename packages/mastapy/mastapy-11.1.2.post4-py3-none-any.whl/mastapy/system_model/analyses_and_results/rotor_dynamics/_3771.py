"""_3771.py

ShaftModalComplexShape
"""


from mastapy.system_model.analyses_and_results.rotor_dynamics import _3769
from mastapy.utility.units_and_measurements.measurements import _1476
from mastapy._internal.python_net import python_net_import

_SHAFT_MODAL_COMPLEX_SHAPE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.RotorDynamics', 'ShaftModalComplexShape')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftModalComplexShape',)


class ShaftModalComplexShape(_3769.ShaftComplexShape['_1476.Number', 'SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements.Number']):
    """ShaftModalComplexShape

    This is a mastapy class.
    """

    TYPE = _SHAFT_MODAL_COMPLEX_SHAPE

    def __init__(self, instance_to_wrap: 'ShaftModalComplexShape.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
