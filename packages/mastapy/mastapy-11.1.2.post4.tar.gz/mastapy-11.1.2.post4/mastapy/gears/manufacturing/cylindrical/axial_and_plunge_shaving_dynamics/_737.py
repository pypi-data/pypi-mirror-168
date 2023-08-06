"""_737.py

ShavingDynamicsViewModelBase
"""


from mastapy.gears.manufacturing.cylindrical import _594
from mastapy._internal.python_net import python_net_import

_SHAVING_DYNAMICS_VIEW_MODEL_BASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ShavingDynamicsViewModelBase')


__docformat__ = 'restructuredtext en'
__all__ = ('ShavingDynamicsViewModelBase',)


class ShavingDynamicsViewModelBase(_594.GearManufacturingConfigurationViewModel):
    """ShavingDynamicsViewModelBase

    This is a mastapy class.
    """

    TYPE = _SHAVING_DYNAMICS_VIEW_MODEL_BASE

    def __init__(self, instance_to_wrap: 'ShavingDynamicsViewModelBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
