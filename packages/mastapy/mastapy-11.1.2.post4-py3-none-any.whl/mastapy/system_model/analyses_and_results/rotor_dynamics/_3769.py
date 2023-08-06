"""_3769.py

ShaftComplexShape
"""


from typing import List, Generic, TypeVar

from mastapy._math.vector_3d import Vector3D
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy.utility.units_and_measurements import _1406
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPLEX_SHAPE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.RotorDynamics', 'ShaftComplexShape')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftComplexShape',)


TLinearMeasurement = TypeVar('TLinearMeasurement', bound='_1406.MeasurementBase')
TAngularMeasurement = TypeVar('TAngularMeasurement', bound='_1406.MeasurementBase')


class ShaftComplexShape(_0.APIBase, Generic[TLinearMeasurement, TAngularMeasurement]):
    """ShaftComplexShape

    This is a mastapy class.

    Generic Types:
        TLinearMeasurement
        TAngularMeasurement
    """

    TYPE = _SHAFT_COMPLEX_SHAPE

    def __init__(self, instance_to_wrap: 'ShaftComplexShape.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angular_imaginary(self) -> 'List[Vector3D]':
        """List[Vector3D]: 'AngularImaginary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularImaginary

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def angular_magnitude(self) -> 'List[Vector3D]':
        """List[Vector3D]: 'AngularMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularMagnitude

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def angular_phase(self) -> 'List[Vector3D]':
        """List[Vector3D]: 'AngularPhase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularPhase

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def angular_real(self) -> 'List[Vector3D]':
        """List[Vector3D]: 'AngularReal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularReal

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def linear_imaginary(self) -> 'List[Vector3D]':
        """List[Vector3D]: 'LinearImaginary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LinearImaginary

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def linear_magnitude(self) -> 'List[Vector3D]':
        """List[Vector3D]: 'LinearMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LinearMagnitude

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def linear_phase(self) -> 'List[Vector3D]':
        """List[Vector3D]: 'LinearPhase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LinearPhase

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def linear_real(self) -> 'List[Vector3D]':
        """List[Vector3D]: 'LinearReal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LinearReal

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
