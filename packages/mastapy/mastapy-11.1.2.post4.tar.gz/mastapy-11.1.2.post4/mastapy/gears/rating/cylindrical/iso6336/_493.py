"""_493.py

ToothFlankFractureAnalysisContactPointMethodA
"""


from mastapy._internal import constructor
from mastapy.gears.rating.cylindrical.iso6336 import _492
from mastapy._internal.python_net import python_net_import

_TOOTH_FLANK_FRACTURE_ANALYSIS_CONTACT_POINT_METHOD_A = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'ToothFlankFractureAnalysisContactPointMethodA')


__docformat__ = 'restructuredtext en'
__all__ = ('ToothFlankFractureAnalysisContactPointMethodA',)


class ToothFlankFractureAnalysisContactPointMethodA(_492.ToothFlankFractureAnalysisContactPointCommon):
    """ToothFlankFractureAnalysisContactPointMethodA

    This is a mastapy class.
    """

    TYPE = _TOOTH_FLANK_FRACTURE_ANALYSIS_CONTACT_POINT_METHOD_A

    def __init__(self, instance_to_wrap: 'ToothFlankFractureAnalysisContactPointMethodA.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def half_of_hertzian_contact_width(self) -> 'float':
        """float: 'HalfOfHertzianContactWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfOfHertzianContactWidth

        if temp is None:
            return None

        return temp

    @property
    def hertzian_contact_stress(self) -> 'float':
        """float: 'HertzianContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianContactStress

        if temp is None:
            return None

        return temp

    @property
    def local_normal_radius_of_relative_curvature(self) -> 'float':
        """float: 'LocalNormalRadiusOfRelativeCurvature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LocalNormalRadiusOfRelativeCurvature

        if temp is None:
            return None

        return temp
