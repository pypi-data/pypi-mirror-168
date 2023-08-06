"""_2193.py

Bolt
"""


from mastapy.system_model.part_model import _2194, _2195
from mastapy._internal import constructor
from mastapy.bolts import _1288
from mastapy._internal.python_net import python_net_import

_BOLT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bolt')


__docformat__ = 'restructuredtext en'
__all__ = ('Bolt',)


class Bolt(_2195.Component):
    """Bolt

    This is a mastapy class.
    """

    TYPE = _BOLT

    def __init__(self, instance_to_wrap: 'Bolt.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bolted_joint(self) -> '_2194.BoltedJoint':
        """BoltedJoint: 'BoltedJoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BoltedJoint

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def loaded_bolt(self) -> '_1288.LoadedBolt':
        """LoadedBolt: 'LoadedBolt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBolt

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
