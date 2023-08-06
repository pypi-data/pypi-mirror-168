"""_1156.py

CylindricalGearMeshFEModel
"""


from typing import List

from mastapy.gears.fe_model import _1151, _1152
from mastapy.gears import _298
from mastapy._internal import conversion, constructor
from mastapy.gears.ltca import _801
from mastapy import _7285
from mastapy._internal.python_net import python_net_import

_GEAR_FE_MODEL = python_net_import('SMT.MastaAPI.Gears.FEModel', 'GearFEModel')
_GEAR_FLANKS = python_net_import('SMT.MastaAPI.Gears', 'GearFlanks')
_TASK_PROGRESS = python_net_import('SMT.MastaAPIUtility', 'TaskProgress')
_CYLINDRICAL_GEAR_MESH_FE_MODEL = python_net_import('SMT.MastaAPI.Gears.FEModel.Cylindrical', 'CylindricalGearMeshFEModel')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshFEModel',)


class CylindricalGearMeshFEModel(_1152.GearMeshFEModel):
    """CylindricalGearMeshFEModel

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MESH_FE_MODEL

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshFEModel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def stiffness_wrt_contacts_for(self, gear: '_1151.GearFEModel', flank: '_298.GearFlanks') -> 'List[_801.GearContactStiffness]':
        """ 'StiffnessWrtContactsFor' is the original name of this method.

        Args:
            gear (mastapy.gears.fe_model.GearFEModel)
            flank (mastapy.gears.GearFlanks)

        Returns:
            List[mastapy.gears.ltca.GearContactStiffness]
        """

        flank = conversion.mp_to_pn_enum(flank)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.StiffnessWrtContactsFor.Overloads[_GEAR_FE_MODEL, _GEAR_FLANKS](gear.wrapped if gear else None, flank))

    def stiffness_wrt_contacts_for_with_progress(self, gear: '_1151.GearFEModel', flank: '_298.GearFlanks', progress: '_7285.TaskProgress') -> 'List[_801.GearContactStiffness]':
        """ 'StiffnessWrtContactsFor' is the original name of this method.

        Args:
            gear (mastapy.gears.fe_model.GearFEModel)
            flank (mastapy.gears.GearFlanks)
            progress (mastapy.TaskProgress)

        Returns:
            List[mastapy.gears.ltca.GearContactStiffness]
        """

        flank = conversion.mp_to_pn_enum(flank)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.StiffnessWrtContactsFor.Overloads[_GEAR_FE_MODEL, _GEAR_FLANKS, _TASK_PROGRESS](gear.wrapped if gear else None, flank, progress.wrapped if progress else None))
