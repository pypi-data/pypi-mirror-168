"""_1276.py

BoltMaterial
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bolts import _1291, _1272
from mastapy._internal.python_net import python_net_import

_BOLT_MATERIAL = python_net_import('SMT.MastaAPI.Bolts', 'BoltMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltMaterial',)


class BoltMaterial(_1272.BoltedJointMaterial):
    """BoltMaterial

    This is a mastapy class.
    """

    TYPE = _BOLT_MATERIAL

    def __init__(self, instance_to_wrap: 'BoltMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def minimum_tensile_strength(self) -> 'float':
        """float: 'MinimumTensileStrength' is the original name of this property."""

        temp = self.wrapped.MinimumTensileStrength

        if temp is None:
            return None

        return temp

    @minimum_tensile_strength.setter
    def minimum_tensile_strength(self, value: 'float'):
        self.wrapped.MinimumTensileStrength = float(value) if value else 0.0

    @property
    def proof_stress(self) -> 'float':
        """float: 'ProofStress' is the original name of this property."""

        temp = self.wrapped.ProofStress

        if temp is None:
            return None

        return temp

    @proof_stress.setter
    def proof_stress(self, value: 'float'):
        self.wrapped.ProofStress = float(value) if value else 0.0

    @property
    def shearing_strength(self) -> 'float':
        """float: 'ShearingStrength' is the original name of this property."""

        temp = self.wrapped.ShearingStrength

        if temp is None:
            return None

        return temp

    @shearing_strength.setter
    def shearing_strength(self, value: 'float'):
        self.wrapped.ShearingStrength = float(value) if value else 0.0

    @property
    def strength_grade(self) -> '_1291.StrengthGrades':
        """StrengthGrades: 'StrengthGrade' is the original name of this property."""

        temp = self.wrapped.StrengthGrade

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1291.StrengthGrades)(value) if value is not None else None

    @strength_grade.setter
    def strength_grade(self, value: '_1291.StrengthGrades'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.StrengthGrade = value
