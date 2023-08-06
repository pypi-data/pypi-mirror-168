"""_738.py

AbstractTCA
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.conical import _1114
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ABSTRACT_TCA = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'AbstractTCA')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractTCA',)


class AbstractTCA(_0.APIBase):
    """AbstractTCA

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_TCA

    def __init__(self, instance_to_wrap: 'AbstractTCA.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mean_transmission_error_with_respect_to_wheel(self) -> 'float':
        """float: 'MeanTransmissionErrorWithRespectToWheel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanTransmissionErrorWithRespectToWheel

        if temp is None:
            return None

        return temp

    @property
    def peak_to_peak_transmission_error_with_respect_to_wheel(self) -> 'float':
        """float: 'PeakToPeakTransmissionErrorWithRespectToWheel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeakToPeakTransmissionErrorWithRespectToWheel

        if temp is None:
            return None

        return temp

    @property
    def conical_mesh_misalignments(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'ConicalMeshMisalignments' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConicalMeshMisalignments

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
