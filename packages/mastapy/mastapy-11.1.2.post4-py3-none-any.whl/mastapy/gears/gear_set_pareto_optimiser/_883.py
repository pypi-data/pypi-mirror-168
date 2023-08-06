"""_883.py

MicroGeometryDesignSpaceSearchCandidate
"""


from mastapy.gears.ltca.cylindrical import _826, _828
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1064
from mastapy.gears.gear_set_pareto_optimiser import _873
from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_DESIGN_SPACE_SEARCH_CANDIDATE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'MicroGeometryDesignSpaceSearchCandidate')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryDesignSpaceSearchCandidate',)


class MicroGeometryDesignSpaceSearchCandidate(_873.DesignSpaceSearchCandidateBase['_826.CylindricalGearSetLoadDistributionAnalysis', 'MicroGeometryDesignSpaceSearchCandidate']):
    """MicroGeometryDesignSpaceSearchCandidate

    This is a mastapy class.
    """

    TYPE = _MICRO_GEOMETRY_DESIGN_SPACE_SEARCH_CANDIDATE

    def __init__(self, instance_to_wrap: 'MicroGeometryDesignSpaceSearchCandidate.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def candidate(self) -> '_826.CylindricalGearSetLoadDistributionAnalysis':
        """CylindricalGearSetLoadDistributionAnalysis: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Candidate

        if temp is None:
            return None

        if _826.CylindricalGearSetLoadDistributionAnalysis.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast candidate to CylindricalGearSetLoadDistributionAnalysis. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def candidate_for_slider(self) -> '_1064.CylindricalGearSetMicroGeometry':
        """CylindricalGearSetMicroGeometry: 'CandidateForSlider' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CandidateForSlider

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def add_design(self):
        """ 'AddDesign' is the original name of this method."""

        self.wrapped.AddDesign()
