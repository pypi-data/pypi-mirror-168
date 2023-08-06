"""_1839.py

DynamicAxialLoadCarryingCapacity
"""


from mastapy.bearings.bearing_results.rolling.skf_module import _1852, _1855
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_DYNAMIC_AXIAL_LOAD_CARRYING_CAPACITY = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'DynamicAxialLoadCarryingCapacity')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicAxialLoadCarryingCapacity',)


class DynamicAxialLoadCarryingCapacity(_1855.SKFCalculationResult):
    """DynamicAxialLoadCarryingCapacity

    This is a mastapy class.
    """

    TYPE = _DYNAMIC_AXIAL_LOAD_CARRYING_CAPACITY

    def __init__(self, instance_to_wrap: 'DynamicAxialLoadCarryingCapacity.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def permissible_axial_load(self) -> '_1852.PermissibleAxialLoad':
        """PermissibleAxialLoad: 'PermissibleAxialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleAxialLoad

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
