"""_923.py

WormWheelDesign
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.worm import _920
from mastapy._internal.python_net import python_net_import

_WORM_WHEEL_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Worm', 'WormWheelDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('WormWheelDesign',)


class WormWheelDesign(_920.WormGearDesign):
    """WormWheelDesign

    This is a mastapy class.
    """

    TYPE = _WORM_WHEEL_DESIGN

    def __init__(self, instance_to_wrap: 'WormWheelDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def addendum(self) -> 'float':
        """float: 'Addendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Addendum

        if temp is None:
            return None

        return temp

    @property
    def dedendum(self) -> 'float':
        """float: 'Dedendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Dedendum

        if temp is None:
            return None

        return temp

    @property
    def face_width(self) -> 'float':
        """float: 'FaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceWidth

        if temp is None:
            return None

        return temp

    @property
    def mean_diameter(self) -> 'float':
        """float: 'MeanDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanDiameter

        if temp is None:
            return None

        return temp

    @property
    def mean_helix_angle(self) -> 'float':
        """float: 'MeanHelixAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanHelixAngle

        if temp is None:
            return None

        return temp

    @property
    def outer_diameter(self) -> 'float':
        """float: 'OuterDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterDiameter

        if temp is None:
            return None

        return temp

    @property
    def reference_diameter(self) -> 'float':
        """float: 'ReferenceDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReferenceDiameter

        if temp is None:
            return None

        return temp

    @property
    def reference_helix_angle(self) -> 'float':
        """float: 'ReferenceHelixAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReferenceHelixAngle

        if temp is None:
            return None

        return temp

    @property
    def root_diameter(self) -> 'float':
        """float: 'RootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootDiameter

        if temp is None:
            return None

        return temp

    @property
    def throat_radius(self) -> 'float':
        """float: 'ThroatRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThroatRadius

        if temp is None:
            return None

        return temp

    @property
    def throat_tip_diameter(self) -> 'float':
        """float: 'ThroatTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThroatTipDiameter

        if temp is None:
            return None

        return temp

    @property
    def whole_depth(self) -> 'float':
        """float: 'WholeDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WholeDepth

        if temp is None:
            return None

        return temp

    @property
    def working_pitch_diameter(self) -> 'float':
        """float: 'WorkingPitchDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkingPitchDiameter

        if temp is None:
            return None

        return temp
