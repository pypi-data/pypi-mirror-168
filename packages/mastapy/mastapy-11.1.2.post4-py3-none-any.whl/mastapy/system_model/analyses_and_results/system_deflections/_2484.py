"""_2484.py

CylindricalGearMeshSystemDeflectionTimestep
"""


from typing import List

from mastapy.gears.ltca.cylindrical import _824
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2483
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_SYSTEM_DEFLECTION_TIMESTEP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CylindricalGearMeshSystemDeflectionTimestep')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshSystemDeflectionTimestep',)


class CylindricalGearMeshSystemDeflectionTimestep(_2483.CylindricalGearMeshSystemDeflection):
    """CylindricalGearMeshSystemDeflectionTimestep

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MESH_SYSTEM_DEFLECTION_TIMESTEP

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshSystemDeflectionTimestep.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def loaded_contact_lines(self) -> 'List[_824.CylindricalGearMeshLoadedContactLine]':
        """List[CylindricalGearMeshLoadedContactLine]: 'LoadedContactLines' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedContactLines

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
