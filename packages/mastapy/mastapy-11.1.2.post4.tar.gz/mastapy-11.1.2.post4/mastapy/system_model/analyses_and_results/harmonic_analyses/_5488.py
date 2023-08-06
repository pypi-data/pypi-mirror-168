"""_5488.py

GearMeshMisalignmentExcitationDetail
"""


from mastapy.system_model.analyses_and_results.harmonic_analyses import _5486
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_MISALIGNMENT_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'GearMeshMisalignmentExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshMisalignmentExcitationDetail',)


class GearMeshMisalignmentExcitationDetail(_5486.GearMeshExcitationDetail):
    """GearMeshMisalignmentExcitationDetail

    This is a mastapy class.
    """

    TYPE = _GEAR_MESH_MISALIGNMENT_EXCITATION_DETAIL

    def __init__(self, instance_to_wrap: 'GearMeshMisalignmentExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
