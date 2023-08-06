"""_914.py

SelectedDesignConstraintsCollection
"""


from mastapy._internal.python_net import python_net_import
from mastapy._internal import constructor
from mastapy.gears.gear_designs import _909
from mastapy.utility import _1395

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_SELECTED_DESIGN_CONSTRAINTS_COLLECTION = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'SelectedDesignConstraintsCollection')


__docformat__ = 'restructuredtext en'
__all__ = ('SelectedDesignConstraintsCollection',)


class SelectedDesignConstraintsCollection(_1395.PerMachineSettings):
    """SelectedDesignConstraintsCollection

    This is a mastapy class.
    """

    TYPE = _SELECTED_DESIGN_CONSTRAINTS_COLLECTION

    def __init__(self, instance_to_wrap: 'SelectedDesignConstraintsCollection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def design_constraints_database(self) -> 'str':
        """str: 'DesignConstraintsDatabase' is the original name of this property."""

        temp = self.wrapped.DesignConstraintsDatabase.SelectedItemName

        if temp is None:
            return None

        return temp

    @design_constraints_database.setter
    def design_constraints_database(self, value: 'str'):
        self.wrapped.DesignConstraintsDatabase.SetSelectedItem(str(value) if value else '')

    @property
    def design_constraints(self) -> '_909.DesignConstraintsCollection':
        """DesignConstraintsCollection: 'DesignConstraints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DesignConstraints

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
