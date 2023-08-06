"""_585.py

CylindricalManufacturedGearMeshLoadCase
"""


from mastapy.gears.analysis import _1175
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MANUFACTURED_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalManufacturedGearMeshLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalManufacturedGearMeshLoadCase',)


class CylindricalManufacturedGearMeshLoadCase(_1175.GearMeshImplementationAnalysis):
    """CylindricalManufacturedGearMeshLoadCase

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_MANUFACTURED_GEAR_MESH_LOAD_CASE

    def __init__(self, instance_to_wrap: 'CylindricalManufacturedGearMeshLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
