"""_2169.py

ElectricMachineStatorFELink
"""


from mastapy.system_model.fe import _2125
from mastapy._internal import constructor
from mastapy.system_model.fe.links import _2175
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_STATOR_FE_LINK = python_net_import('SMT.MastaAPI.SystemModel.FE.Links', 'ElectricMachineStatorFELink')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineStatorFELink',)


class ElectricMachineStatorFELink(_2175.MultiNodeFELink):
    """ElectricMachineStatorFELink

    This is a mastapy class.
    """

    TYPE = _ELECTRIC_MACHINE_STATOR_FE_LINK

    def __init__(self, instance_to_wrap: 'ElectricMachineStatorFELink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def electric_machine_dynamic_load_data(self) -> '_2125.ElectricMachineDynamicLoadData':
        """ElectricMachineDynamicLoadData: 'ElectricMachineDynamicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElectricMachineDynamicLoadData

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
