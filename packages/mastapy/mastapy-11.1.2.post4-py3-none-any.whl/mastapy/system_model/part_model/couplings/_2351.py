"""_2351.py

Synchroniser
"""


from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.couplings import _2093
from mastapy.system_model.part_model.couplings import _2355, _2353
from mastapy.system_model.part_model import _2226
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Synchroniser')


__docformat__ = 'restructuredtext en'
__all__ = ('Synchroniser',)


class Synchroniser(_2226.SpecialisedAssembly):
    """Synchroniser

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER

    def __init__(self, instance_to_wrap: 'Synchroniser.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def has_left_cone(self) -> 'bool':
        """bool: 'HasLeftCone' is the original name of this property."""

        temp = self.wrapped.HasLeftCone

        if temp is None:
            return None

        return temp

    @has_left_cone.setter
    def has_left_cone(self, value: 'bool'):
        self.wrapped.HasLeftCone = bool(value) if value else False

    @property
    def has_right_cone(self) -> 'bool':
        """bool: 'HasRightCone' is the original name of this property."""

        temp = self.wrapped.HasRightCone

        if temp is None:
            return None

        return temp

    @has_right_cone.setter
    def has_right_cone(self, value: 'bool'):
        self.wrapped.HasRightCone = bool(value) if value else False

    @property
    def clutch_connection_left(self) -> '_2093.ClutchConnection':
        """ClutchConnection: 'ClutchConnectionLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ClutchConnectionLeft

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def clutch_connection_right(self) -> '_2093.ClutchConnection':
        """ClutchConnection: 'ClutchConnectionRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ClutchConnectionRight

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def hub_and_sleeve(self) -> '_2355.SynchroniserSleeve':
        """SynchroniserSleeve: 'HubAndSleeve' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HubAndSleeve

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def left_cone(self) -> '_2353.SynchroniserHalf':
        """SynchroniserHalf: 'LeftCone' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftCone

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def right_cone(self) -> '_2353.SynchroniserHalf':
        """SynchroniserHalf: 'RightCone' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightCone

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
