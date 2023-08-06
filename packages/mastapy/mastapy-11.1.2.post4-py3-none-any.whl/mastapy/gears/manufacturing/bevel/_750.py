"""_750.py

ConicalMeshManufacturingAnalysis
"""


from typing import List

from mastapy.gears.load_case.conical import _853
from mastapy._internal import constructor, conversion
from mastapy.gears.load_case.bevel import _858
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel import _761, _745
from mastapy.gears.analysis import _1175
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_MANUFACTURING_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalMeshManufacturingAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshManufacturingAnalysis',)


class ConicalMeshManufacturingAnalysis(_1175.GearMeshImplementationAnalysis):
    """ConicalMeshManufacturingAnalysis

    This is a mastapy class.
    """

    TYPE = _CONICAL_MESH_MANUFACTURING_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConicalMeshManufacturingAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def conical_mesh_load_case(self) -> '_853.ConicalMeshLoadCase':
        """ConicalMeshLoadCase: 'ConicalMeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConicalMeshLoadCase

        if temp is None:
            return None

        if _853.ConicalMeshLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast conical_mesh_load_case to ConicalMeshLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tca(self) -> '_761.EaseOffBasedTCA':
        """EaseOffBasedTCA: 'TCA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TCA

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def meshed_gears(self) -> 'List[_745.ConicalMeshedGearManufacturingAnalysis]':
        """List[ConicalMeshedGearManufacturingAnalysis]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshedGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
