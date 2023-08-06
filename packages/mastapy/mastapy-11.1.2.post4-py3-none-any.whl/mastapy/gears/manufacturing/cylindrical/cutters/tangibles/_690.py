"""_690.py

CylindricalGearFormedWheelGrinderTangible
"""


from mastapy.gears.manufacturing.cylindrical.cutters import _673
from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _689
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_FORMED_WHEEL_GRINDER_TANGIBLE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters.Tangibles', 'CylindricalGearFormedWheelGrinderTangible')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearFormedWheelGrinderTangible',)


class CylindricalGearFormedWheelGrinderTangible(_689.CutterShapeDefinition):
    """CylindricalGearFormedWheelGrinderTangible

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_FORMED_WHEEL_GRINDER_TANGIBLE

    def __init__(self, instance_to_wrap: 'CylindricalGearFormedWheelGrinderTangible.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def design(self) -> '_673.CylindricalGearFormGrindingWheel':
        """CylindricalGearFormGrindingWheel: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Design

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
