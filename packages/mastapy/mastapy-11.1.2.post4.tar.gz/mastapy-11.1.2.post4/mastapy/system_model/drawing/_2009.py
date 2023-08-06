"""_2009.py

SteadyStateSynchronousResponseViewable
"""


from mastapy.system_model.drawing import _2005
from mastapy._internal.python_net import python_net_import

_STEADY_STATE_SYNCHRONOUS_RESPONSE_VIEWABLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'SteadyStateSynchronousResponseViewable')


__docformat__ = 'restructuredtext en'
__all__ = ('SteadyStateSynchronousResponseViewable',)


class SteadyStateSynchronousResponseViewable(_2005.RotorDynamicsViewable):
    """SteadyStateSynchronousResponseViewable

    This is a mastapy class.
    """

    TYPE = _STEADY_STATE_SYNCHRONOUS_RESPONSE_VIEWABLE

    def __init__(self, instance_to_wrap: 'SteadyStateSynchronousResponseViewable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
