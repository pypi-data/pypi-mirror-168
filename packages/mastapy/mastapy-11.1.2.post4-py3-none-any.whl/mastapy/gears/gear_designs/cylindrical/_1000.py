"""_1000.py

CylindricalMeshLinearBacklashSpecification
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _1044, _962
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MESH_LINEAR_BACKLASH_SPECIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalMeshLinearBacklashSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalMeshLinearBacklashSpecification',)


class CylindricalMeshLinearBacklashSpecification(_1044.TolerancedValueSpecification['_962.BacklashSpecification']):
    """CylindricalMeshLinearBacklashSpecification

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_MESH_LINEAR_BACKLASH_SPECIFICATION

    def __init__(self, instance_to_wrap: 'CylindricalMeshLinearBacklashSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def measurement_type(self) -> 'str':
        """str: 'MeasurementType' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeasurementType

        if temp is None:
            return None

        return temp
