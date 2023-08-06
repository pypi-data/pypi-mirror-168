"""_1953.py

ConceptAxialClearanceBearing
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.bearing_designs.concept import _1952, _1954
from mastapy._internal.python_net import python_net_import

_CONCEPT_AXIAL_CLEARANCE_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Concept', 'ConceptAxialClearanceBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptAxialClearanceBearing',)


class ConceptAxialClearanceBearing(_1954.ConceptClearanceBearing):
    """ConceptAxialClearanceBearing

    This is a mastapy class.
    """

    TYPE = _CONCEPT_AXIAL_CLEARANCE_BEARING

    def __init__(self, instance_to_wrap: 'ConceptAxialClearanceBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bore(self) -> 'float':
        """float: 'Bore' is the original name of this property."""

        temp = self.wrapped.Bore

        if temp is None:
            return None

        return temp

    @bore.setter
    def bore(self, value: 'float'):
        self.wrapped.Bore = float(value) if value else 0.0

    @property
    def node_position(self) -> '_1952.BearingNodePosition':
        """BearingNodePosition: 'NodePosition' is the original name of this property."""

        temp = self.wrapped.NodePosition

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1952.BearingNodePosition)(value) if value is not None else None

    @node_position.setter
    def node_position(self, value: '_1952.BearingNodePosition'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.NodePosition = value

    @property
    def outer_diameter(self) -> 'float':
        """float: 'OuterDiameter' is the original name of this property."""

        temp = self.wrapped.OuterDiameter

        if temp is None:
            return None

        return temp

    @outer_diameter.setter
    def outer_diameter(self, value: 'float'):
        self.wrapped.OuterDiameter = float(value) if value else 0.0

    @property
    def thickness(self) -> 'float':
        """float: 'Thickness' is the original name of this property."""

        temp = self.wrapped.Thickness

        if temp is None:
            return None

        return temp

    @thickness.setter
    def thickness(self, value: 'float'):
        self.wrapped.Thickness = float(value) if value else 0.0

    @property
    def x_stiffness(self) -> 'float':
        """float: 'XStiffness' is the original name of this property."""

        temp = self.wrapped.XStiffness

        if temp is None:
            return None

        return temp

    @x_stiffness.setter
    def x_stiffness(self, value: 'float'):
        self.wrapped.XStiffness = float(value) if value else 0.0

    @property
    def x_stiffness_applied_only_when_contacting(self) -> 'bool':
        """bool: 'XStiffnessAppliedOnlyWhenContacting' is the original name of this property."""

        temp = self.wrapped.XStiffnessAppliedOnlyWhenContacting

        if temp is None:
            return None

        return temp

    @x_stiffness_applied_only_when_contacting.setter
    def x_stiffness_applied_only_when_contacting(self, value: 'bool'):
        self.wrapped.XStiffnessAppliedOnlyWhenContacting = bool(value) if value else False

    @property
    def y_stiffness(self) -> 'float':
        """float: 'YStiffness' is the original name of this property."""

        temp = self.wrapped.YStiffness

        if temp is None:
            return None

        return temp

    @y_stiffness.setter
    def y_stiffness(self, value: 'float'):
        self.wrapped.YStiffness = float(value) if value else 0.0

    @property
    def y_stiffness_applied_only_when_contacting(self) -> 'bool':
        """bool: 'YStiffnessAppliedOnlyWhenContacting' is the original name of this property."""

        temp = self.wrapped.YStiffnessAppliedOnlyWhenContacting

        if temp is None:
            return None

        return temp

    @y_stiffness_applied_only_when_contacting.setter
    def y_stiffness_applied_only_when_contacting(self, value: 'bool'):
        self.wrapped.YStiffnessAppliedOnlyWhenContacting = bool(value) if value else False
