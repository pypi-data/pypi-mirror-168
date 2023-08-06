"""_2364.py

BearingDetailConfiguration
"""


from mastapy.system_model.part_model.configurations import _2366, _2365
from mastapy.system_model.part_model import _2191
from mastapy.bearings.bearing_designs import _1888
from mastapy._internal.python_net import python_net_import

_BEARING_DETAIL_CONFIGURATION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'BearingDetailConfiguration')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingDetailConfiguration',)


class BearingDetailConfiguration(_2366.PartDetailConfiguration['_2365.BearingDetailSelection', '_2191.Bearing', '_1888.BearingDesign']):
    """BearingDetailConfiguration

    This is a mastapy class.
    """

    TYPE = _BEARING_DETAIL_CONFIGURATION

    def __init__(self, instance_to_wrap: 'BearingDetailConfiguration.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
