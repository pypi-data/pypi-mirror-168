"""_2136.py

FESubstructureNodeModeShape
"""


from mastapy._internal import constructor
from mastapy.math_utility.measured_vectors import _1371
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FE_SUBSTRUCTURE_NODE_MODE_SHAPE = python_net_import('SMT.MastaAPI.SystemModel.FE', 'FESubstructureNodeModeShape')


__docformat__ = 'restructuredtext en'
__all__ = ('FESubstructureNodeModeShape',)


class FESubstructureNodeModeShape(_0.APIBase):
    """FESubstructureNodeModeShape

    This is a mastapy class.
    """

    TYPE = _FE_SUBSTRUCTURE_NODE_MODE_SHAPE

    def __init__(self, instance_to_wrap: 'FESubstructureNodeModeShape.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mode(self) -> 'int':
        """int: 'Mode' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Mode

        if temp is None:
            return None

        return temp

    @property
    def mode_shape_component_coordinate_system(self) -> '_1371.VectorWithLinearAndAngularComponents':
        """VectorWithLinearAndAngularComponents: 'ModeShapeComponentCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModeShapeComponentCoordinateSystem

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mode_shape_fe_coordinate_system(self) -> '_1371.VectorWithLinearAndAngularComponents':
        """VectorWithLinearAndAngularComponents: 'ModeShapeFECoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModeShapeFECoordinateSystem

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mode_shape_global_cordinate_system(self) -> '_1371.VectorWithLinearAndAngularComponents':
        """VectorWithLinearAndAngularComponents: 'ModeShapeGlobalCordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModeShapeGlobalCordinateSystem

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
