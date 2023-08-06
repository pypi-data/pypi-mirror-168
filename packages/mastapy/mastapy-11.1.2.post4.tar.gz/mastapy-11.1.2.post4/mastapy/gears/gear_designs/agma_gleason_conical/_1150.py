"""_1150.py

AGMAGleasonConicalMeshedGearDesign
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.conical import _1113
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_MESHED_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.AGMAGleasonConical', 'AGMAGleasonConicalMeshedGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalMeshedGearDesign',)


class AGMAGleasonConicalMeshedGearDesign(_1113.ConicalMeshedGearDesign):
    """AGMAGleasonConicalMeshedGearDesign

    This is a mastapy class.
    """

    TYPE = _AGMA_GLEASON_CONICAL_MESHED_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalMeshedGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mean_normal_topland(self) -> 'float':
        """float: 'MeanNormalTopland' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanNormalTopland

        if temp is None:
            return None

        return temp

    @property
    def minimum_topland_to_module_factor(self) -> 'float':
        """float: 'MinimumToplandToModuleFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumToplandToModuleFactor

        if temp is None:
            return None

        return temp

    @property
    def required_mean_normal_topland(self) -> 'float':
        """float: 'RequiredMeanNormalTopland' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RequiredMeanNormalTopland

        if temp is None:
            return None

        return temp
