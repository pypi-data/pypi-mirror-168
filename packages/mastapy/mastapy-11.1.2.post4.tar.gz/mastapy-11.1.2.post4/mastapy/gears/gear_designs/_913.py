"""_913.py

GearSetDesign
"""


from typing import List, Optional

from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import
from mastapy.gears.fe_model import _1154
from mastapy.gears.fe_model.cylindrical import _1157
from mastapy._internal.cast_exception import CastException
from mastapy.gears.fe_model.conical import _1160
from mastapy.gears import _300
from mastapy.gears.gear_designs import _910, _911

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'GearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetDesign',)


class GearSetDesign(_911.GearDesignComponent):
    """GearSetDesign

    This is a mastapy class.
    """

    TYPE = _GEAR_SET_DESIGN

    def __init__(self, instance_to_wrap: 'GearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_contact_ratio_rating_for_nvh(self) -> 'float':
        """float: 'AxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialContactRatioRatingForNVH

        if temp is None:
            return None

        return temp

    @property
    def fe_model(self) -> 'str':
        """str: 'FEModel' is the original name of this property."""

        temp = self.wrapped.FEModel.SelectedItemName

        if temp is None:
            return None

        return temp

    @fe_model.setter
    def fe_model(self, value: 'str'):
        self.wrapped.FEModel.SetSelectedItem(str(value) if value else '')

    @property
    def gear_set_drawing(self) -> 'Image':
        """Image: 'GearSetDrawing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSetDrawing

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def largest_mesh_ratio(self) -> 'float':
        """float: 'LargestMeshRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LargestMeshRatio

        if temp is None:
            return None

        return temp

    @property
    def largest_number_of_teeth(self) -> 'int':
        """int: 'LargestNumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LargestNumberOfTeeth

        if temp is None:
            return None

        return temp

    @property
    def long_name(self) -> 'str':
        """str: 'LongName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LongName

        if temp is None:
            return None

        return temp

    @property
    def mass(self) -> 'float':
        """float: 'Mass' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Mass

        if temp is None:
            return None

        return temp

    @property
    def name_including_tooth_numbers(self) -> 'str':
        """str: 'NameIncludingToothNumbers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NameIncludingToothNumbers

        if temp is None:
            return None

        return temp

    @property
    def required_safety_factor_for_bending(self) -> 'float':
        """float: 'RequiredSafetyFactorForBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RequiredSafetyFactorForBending

        if temp is None:
            return None

        return temp

    @property
    def required_safety_factor_for_contact(self) -> 'float':
        """float: 'RequiredSafetyFactorForContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RequiredSafetyFactorForContact

        if temp is None:
            return None

        return temp

    @property
    def required_safety_factor_for_static_bending(self) -> 'float':
        """float: 'RequiredSafetyFactorForStaticBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RequiredSafetyFactorForStaticBending

        if temp is None:
            return None

        return temp

    @property
    def required_safety_factor_for_static_contact(self) -> 'float':
        """float: 'RequiredSafetyFactorForStaticContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RequiredSafetyFactorForStaticContact

        if temp is None:
            return None

        return temp

    @property
    def smallest_number_of_teeth(self) -> 'int':
        """int: 'SmallestNumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SmallestNumberOfTeeth

        if temp is None:
            return None

        return temp

    @property
    def transverse_contact_ratio_rating_for_nvh(self) -> 'float':
        """float: 'TransverseContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseContactRatioRatingForNVH

        if temp is None:
            return None

        return temp

    @property
    def transverse_and_axial_contact_ratio_rating_for_nvh(self) -> 'float':
        """float: 'TransverseAndAxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseAndAxialContactRatioRatingForNVH

        if temp is None:
            return None

        return temp

    @property
    def active_ltcafe_model(self) -> '_1154.GearSetFEModel':
        """GearSetFEModel: 'ActiveLTCAFEModel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveLTCAFEModel

        if temp is None:
            return None

        if _1154.GearSetFEModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_ltcafe_model to GearSetFEModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_ltcafe_model_of_type_cylindrical_gear_set_fe_model(self) -> '_1157.CylindricalGearSetFEModel':
        """CylindricalGearSetFEModel: 'ActiveLTCAFEModel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveLTCAFEModel

        if temp is None:
            return None

        if _1157.CylindricalGearSetFEModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_ltcafe_model to CylindricalGearSetFEModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_ltcafe_model_of_type_conical_set_fe_model(self) -> '_1160.ConicalSetFEModel':
        """ConicalSetFEModel: 'ActiveLTCAFEModel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveLTCAFEModel

        if temp is None:
            return None

        if _1160.ConicalSetFEModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_ltcafe_model to ConicalSetFEModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tifffe_model(self) -> '_1154.GearSetFEModel':
        """GearSetFEModel: 'TIFFFEModel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TIFFFEModel

        if temp is None:
            return None

        if _1154.GearSetFEModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast tifffe_model to GearSetFEModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tifffe_model_of_type_cylindrical_gear_set_fe_model(self) -> '_1157.CylindricalGearSetFEModel':
        """CylindricalGearSetFEModel: 'TIFFFEModel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TIFFFEModel

        if temp is None:
            return None

        if _1157.CylindricalGearSetFEModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast tifffe_model to CylindricalGearSetFEModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tifffe_model_of_type_conical_set_fe_model(self) -> '_1160.ConicalSetFEModel':
        """ConicalSetFEModel: 'TIFFFEModel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TIFFFEModel

        if temp is None:
            return None

        if _1160.ConicalSetFEModel.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast tifffe_model to ConicalSetFEModel. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def transmission_properties_gears(self) -> '_300.GearSetDesignGroup':
        """GearSetDesignGroup: 'TransmissionPropertiesGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransmissionPropertiesGears

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gears(self) -> 'List[_910.GearDesign]':
        """List[GearDesign]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Gears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def ltcafe_models(self) -> 'List[_1154.GearSetFEModel]':
        """List[GearSetFEModel]: 'LTCAFEModels' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LTCAFEModels

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def create_new_fe_model(self):
        """ 'CreateNewFEModel' is the original name of this method."""

        self.wrapped.CreateNewFEModel()

    def create_new_tifffe_model(self):
        """ 'CreateNewTIFFFEModel' is the original name of this method."""

        self.wrapped.CreateNewTIFFFEModel()

    def copy(self, include_fe: Optional['bool'] = False) -> 'GearSetDesign':
        """ 'Copy' is the original name of this method.

        Args:
            include_fe (bool, optional)

        Returns:
            mastapy.gears.gear_designs.GearSetDesign
        """

        include_fe = bool(include_fe)
        method_result = self.wrapped.Copy(include_fe if include_fe else False)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
