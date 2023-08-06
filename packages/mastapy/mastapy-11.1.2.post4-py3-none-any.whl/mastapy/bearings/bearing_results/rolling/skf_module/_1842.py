"""_1842.py

Friction
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.skf_module import _1844, _1843, _1855
from mastapy._internal.python_net import python_net_import

_FRICTION = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'Friction')


__docformat__ = 'restructuredtext en'
__all__ = ('Friction',)


class Friction(_1855.SKFCalculationResult):
    """Friction

    This is a mastapy class.
    """

    TYPE = _FRICTION

    def __init__(self, instance_to_wrap: 'Friction.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def power_loss(self) -> 'float':
        """float: 'PowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerLoss

        if temp is None:
            return None

        return temp

    @property
    def friction_sources(self) -> '_1844.FrictionSources':
        """FrictionSources: 'FrictionSources' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FrictionSources

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def frictional_moment(self) -> '_1843.FrictionalMoment':
        """FrictionalMoment: 'FrictionalMoment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FrictionalMoment

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
