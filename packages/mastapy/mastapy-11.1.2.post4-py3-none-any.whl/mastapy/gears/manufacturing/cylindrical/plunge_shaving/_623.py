"""_623.py

VirtualPlungeShaverOutputs
"""


from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.cutters import _681, _676
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _617
from mastapy._internal.python_net import python_net_import

_VIRTUAL_PLUNGE_SHAVER_OUTPUTS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'VirtualPlungeShaverOutputs')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualPlungeShaverOutputs',)


class VirtualPlungeShaverOutputs(_617.PlungeShaverOutputs):
    """VirtualPlungeShaverOutputs

    This is a mastapy class.
    """

    TYPE = _VIRTUAL_PLUNGE_SHAVER_OUTPUTS

    def __init__(self, instance_to_wrap: 'VirtualPlungeShaverOutputs.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def lead_modification_on_conjugate_shaver_chart_left_flank(self) -> 'Image':
        """Image: 'LeadModificationOnConjugateShaverChartLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeadModificationOnConjugateShaverChartLeftFlank

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def lead_modification_on_conjugate_shaver_chart_right_flank(self) -> 'Image':
        """Image: 'LeadModificationOnConjugateShaverChartRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeadModificationOnConjugateShaverChartRightFlank

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def shaver(self) -> '_681.CylindricalGearShaver':
        """CylindricalGearShaver: 'Shaver' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shaver

        if temp is None:
            return None

        if _681.CylindricalGearShaver.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast shaver to CylindricalGearShaver. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
