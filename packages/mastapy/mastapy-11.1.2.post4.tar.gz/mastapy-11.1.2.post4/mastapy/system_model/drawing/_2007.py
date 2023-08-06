"""_2007.py

ShaftDeflectionDrawingNodeItem
"""


from mastapy._internal import constructor
from mastapy.math_utility.measured_vectors import _1367
from mastapy.system_model.analyses_and_results.system_deflections import _2547
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHAFT_DEFLECTION_DRAWING_NODE_ITEM = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'ShaftDeflectionDrawingNodeItem')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftDeflectionDrawingNodeItem',)


class ShaftDeflectionDrawingNodeItem(_0.APIBase):
    """ShaftDeflectionDrawingNodeItem

    This is a mastapy class.
    """

    TYPE = _SHAFT_DEFLECTION_DRAWING_NODE_ITEM

    def __init__(self, instance_to_wrap: 'ShaftDeflectionDrawingNodeItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_deflection(self) -> 'float':
        """float: 'AxialDeflection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialDeflection

        if temp is None:
            return None

        return temp

    @property
    def offset(self) -> 'float':
        """float: 'Offset' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Offset

        if temp is None:
            return None

        return temp

    @property
    def radial_deflection(self) -> 'float':
        """float: 'RadialDeflection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialDeflection

        if temp is None:
            return None

        return temp

    @property
    def node_detail(self) -> '_1367.ForceAndDisplacementResults':
        """ForceAndDisplacementResults: 'NodeDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NodeDetail

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def section_to_the_left_side(self) -> '_2547.ShaftSectionSystemDeflection':
        """ShaftSectionSystemDeflection: 'SectionToTheLeftSide' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SectionToTheLeftSide

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def section_to_the_right_side(self) -> '_2547.ShaftSectionSystemDeflection':
        """ShaftSectionSystemDeflection: 'SectionToTheRightSide' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SectionToTheRightSide

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
