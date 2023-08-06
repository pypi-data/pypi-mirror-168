"""_1273.py

BoltedJointMaterialDatabase
"""


from typing import Generic, TypeVar

from mastapy.utility.databases import _1604
from mastapy.bolts import _1272
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Bolts', 'BoltedJointMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointMaterialDatabase',)


T = TypeVar('T', bound='_1272.BoltedJointMaterial')


class BoltedJointMaterialDatabase(_1604.NamedDatabase['T'], Generic[T]):
    """BoltedJointMaterialDatabase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _BOLTED_JOINT_MATERIAL_DATABASE

    def __init__(self, instance_to_wrap: 'BoltedJointMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
