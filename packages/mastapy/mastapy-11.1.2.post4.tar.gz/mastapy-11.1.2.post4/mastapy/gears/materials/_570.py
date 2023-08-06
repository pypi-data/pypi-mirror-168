"""_570.py

PlasticSNCurve
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.materials import _262, _259, _260
from mastapy.gears.materials import _569
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PLASTIC_SN_CURVE = python_net_import('SMT.MastaAPI.Gears.Materials', 'PlasticSNCurve')


__docformat__ = 'restructuredtext en'
__all__ = ('PlasticSNCurve',)


class PlasticSNCurve(_0.APIBase):
    """PlasticSNCurve

    This is a mastapy class.
    """

    TYPE = _PLASTIC_SN_CURVE

    def __init__(self, instance_to_wrap: 'PlasticSNCurve.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def allowable_stress_number_bending(self) -> 'float':
        """float: 'AllowableStressNumberBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableStressNumberBending

        if temp is None:
            return None

        return temp

    @property
    def allowable_stress_number_contact(self) -> 'float':
        """float: 'AllowableStressNumberContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableStressNumberContact

        if temp is None:
            return None

        return temp

    @property
    def flank_temperature(self) -> 'float':
        """float: 'FlankTemperature' is the original name of this property."""

        temp = self.wrapped.FlankTemperature

        if temp is None:
            return None

        return temp

    @flank_temperature.setter
    def flank_temperature(self, value: 'float'):
        self.wrapped.FlankTemperature = float(value) if value else 0.0

    @property
    def life_cycles(self) -> 'float':
        """float: 'LifeCycles' is the original name of this property."""

        temp = self.wrapped.LifeCycles

        if temp is None:
            return None

        return temp

    @life_cycles.setter
    def life_cycles(self, value: 'float'):
        self.wrapped.LifeCycles = float(value) if value else 0.0

    @property
    def lubricant(self) -> '_262.VDI2736LubricantType':
        """VDI2736LubricantType: 'Lubricant' is the original name of this property."""

        temp = self.wrapped.Lubricant

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_262.VDI2736LubricantType)(value) if value is not None else None

    @lubricant.setter
    def lubricant(self, value: '_262.VDI2736LubricantType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Lubricant = value

    @property
    def nominal_stress_number_bending(self) -> 'float':
        """float: 'NominalStressNumberBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalStressNumberBending

        if temp is None:
            return None

        return temp

    @property
    def note_1(self) -> 'str':
        """str: 'Note1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Note1

        if temp is None:
            return None

        return temp

    @property
    def note_2(self) -> 'str':
        """str: 'Note2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Note2

        if temp is None:
            return None

        return temp

    @property
    def number_of_rows_in_the_bending_sn_table(self) -> 'int':
        """int: 'NumberOfRowsInTheBendingSNTable' is the original name of this property."""

        temp = self.wrapped.NumberOfRowsInTheBendingSNTable

        if temp is None:
            return None

        return temp

    @number_of_rows_in_the_bending_sn_table.setter
    def number_of_rows_in_the_bending_sn_table(self, value: 'int'):
        self.wrapped.NumberOfRowsInTheBendingSNTable = int(value) if value else 0

    @property
    def number_of_rows_in_the_contact_sn_table(self) -> 'int':
        """int: 'NumberOfRowsInTheContactSNTable' is the original name of this property."""

        temp = self.wrapped.NumberOfRowsInTheContactSNTable

        if temp is None:
            return None

        return temp

    @number_of_rows_in_the_contact_sn_table.setter
    def number_of_rows_in_the_contact_sn_table(self, value: 'int'):
        self.wrapped.NumberOfRowsInTheContactSNTable = int(value) if value else 0

    @property
    def root_temperature(self) -> 'float':
        """float: 'RootTemperature' is the original name of this property."""

        temp = self.wrapped.RootTemperature

        if temp is None:
            return None

        return temp

    @root_temperature.setter
    def root_temperature(self, value: 'float'):
        self.wrapped.RootTemperature = float(value) if value else 0.0

    @property
    def material(self) -> '_569.PlasticCylindricalGearMaterial':
        """PlasticCylindricalGearMaterial: 'Material' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Material

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bending_stress_cycle_data_for_damage_tables(self) -> 'List[_259.StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial]':
        """List[StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial]: 'BendingStressCycleDataForDamageTables' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BendingStressCycleDataForDamageTables

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bending_stress_cycle_data(self) -> 'List[_259.StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial]':
        """List[StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial]: 'BendingStressCycleData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BendingStressCycleData

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def contact_stress_cycle_data_for_damage_tables(self) -> 'List[_260.StressCyclesDataForTheContactSNCurveOfAPlasticMaterial]':
        """List[StressCyclesDataForTheContactSNCurveOfAPlasticMaterial]: 'ContactStressCycleDataForDamageTables' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStressCycleDataForDamageTables

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def contact_stress_cycle_data(self) -> 'List[_260.StressCyclesDataForTheContactSNCurveOfAPlasticMaterial]':
        """List[StressCyclesDataForTheContactSNCurveOfAPlasticMaterial]: 'ContactStressCycleData' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStressCycleData

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def report_names(self) -> 'List[str]':
        """List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReportNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)
        return value

    def output_default_report_to(self, file_path: 'str'):
        """ 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else '')

    def get_default_report_with_encoded_images(self) -> 'str':
        """ 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        """ 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else '')

    def output_active_report_as_text_to(self, file_path: 'str'):
        """ 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else '')

    def get_active_report_with_encoded_images(self) -> 'str':
        """ 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else '', file_path if file_path else '')

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        """ 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        """

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else '')
        return method_result
