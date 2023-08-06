"""_908.py

DesignConstraintCollectionDatabase
"""


from mastapy.utility.databases import _1604
from mastapy.gears.gear_designs import _909
from mastapy._internal.python_net import python_net_import

_DESIGN_CONSTRAINT_COLLECTION_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'DesignConstraintCollectionDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignConstraintCollectionDatabase',)


class DesignConstraintCollectionDatabase(_1604.NamedDatabase['_909.DesignConstraintsCollection']):
    """DesignConstraintCollectionDatabase

    This is a mastapy class.
    """

    TYPE = _DESIGN_CONSTRAINT_COLLECTION_DATABASE

    def __init__(self, instance_to_wrap: 'DesignConstraintCollectionDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
