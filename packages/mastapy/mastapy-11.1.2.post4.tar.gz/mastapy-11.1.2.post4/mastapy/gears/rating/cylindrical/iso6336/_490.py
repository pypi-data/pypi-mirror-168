"""_490.py

ISO6336RateableMesh
"""


from mastapy.gears.rating.cylindrical import _446, _439
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.python_net import python_net_import

_ISO6336_RATEABLE_MESH = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'ISO6336RateableMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO6336RateableMesh',)


class ISO6336RateableMesh(_439.CylindricalRateableMesh):
    """ISO6336RateableMesh

    This is a mastapy class.
    """

    TYPE = _ISO6336_RATEABLE_MESH

    def __init__(self, instance_to_wrap: 'ISO6336RateableMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def misalignment_contact_pattern_enhancement(self) -> '_446.MisalignmentContactPatternEnhancements':
        """MisalignmentContactPatternEnhancements: 'MisalignmentContactPatternEnhancement' is the original name of this property."""

        temp = self.wrapped.MisalignmentContactPatternEnhancement

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_446.MisalignmentContactPatternEnhancements)(value) if value is not None else None

    @misalignment_contact_pattern_enhancement.setter
    def misalignment_contact_pattern_enhancement(self, value: '_446.MisalignmentContactPatternEnhancements'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MisalignmentContactPatternEnhancement = value
