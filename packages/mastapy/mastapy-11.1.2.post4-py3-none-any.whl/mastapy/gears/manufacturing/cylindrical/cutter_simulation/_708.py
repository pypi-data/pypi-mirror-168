"""_708.py

ManufacturingProcessControls
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MANUFACTURING_PROCESS_CONTROLS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'ManufacturingProcessControls')


__docformat__ = 'restructuredtext en'
__all__ = ('ManufacturingProcessControls',)


class ManufacturingProcessControls(_0.APIBase):
    """ManufacturingProcessControls

    This is a mastapy class.
    """

    TYPE = _MANUFACTURING_PROCESS_CONTROLS

    def __init__(self, instance_to_wrap: 'ManufacturingProcessControls.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def tooth_thickness_specification_compliance_checked(self) -> 'bool':
        """bool: 'ToothThicknessSpecificationComplianceChecked' is the original name of this property."""

        temp = self.wrapped.ToothThicknessSpecificationComplianceChecked

        if temp is None:
            return None

        return temp

    @tooth_thickness_specification_compliance_checked.setter
    def tooth_thickness_specification_compliance_checked(self, value: 'bool'):
        self.wrapped.ToothThicknessSpecificationComplianceChecked = bool(value) if value else False
