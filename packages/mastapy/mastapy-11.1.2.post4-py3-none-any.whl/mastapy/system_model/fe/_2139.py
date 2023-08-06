"""_2139.py

FESubstructureWithBatchOptions
"""


from mastapy._internal import constructor
from mastapy.system_model.fe import _2133
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FE_SUBSTRUCTURE_WITH_BATCH_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.FE', 'FESubstructureWithBatchOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('FESubstructureWithBatchOptions',)


class FESubstructureWithBatchOptions(_0.APIBase):
    """FESubstructureWithBatchOptions

    This is a mastapy class.
    """

    TYPE = _FE_SUBSTRUCTURE_WITH_BATCH_OPTIONS

    def __init__(self, instance_to_wrap: 'FESubstructureWithBatchOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def fe_substructure(self) -> 'str':
        """str: 'FESubstructure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FESubstructure

        if temp is None:
            return None

        return temp

    @property
    def load_mesh_and_vectors(self) -> 'bool':
        """bool: 'LoadMeshAndVectors' is the original name of this property."""

        temp = self.wrapped.LoadMeshAndVectors

        if temp is None:
            return None

        return temp

    @load_mesh_and_vectors.setter
    def load_mesh_and_vectors(self, value: 'bool'):
        self.wrapped.LoadMeshAndVectors = bool(value) if value else False

    @property
    def load_mesh(self) -> 'bool':
        """bool: 'LoadMesh' is the original name of this property."""

        temp = self.wrapped.LoadMesh

        if temp is None:
            return None

        return temp

    @load_mesh.setter
    def load_mesh(self, value: 'bool'):
        self.wrapped.LoadMesh = bool(value) if value else False

    @property
    def load_vectors(self) -> 'bool':
        """bool: 'LoadVectors' is the original name of this property."""

        temp = self.wrapped.LoadVectors

        if temp is None:
            return None

        return temp

    @load_vectors.setter
    def load_vectors(self, value: 'bool'):
        self.wrapped.LoadVectors = bool(value) if value else False

    @property
    def run_condensation(self) -> 'bool':
        """bool: 'RunCondensation' is the original name of this property."""

        temp = self.wrapped.RunCondensation

        if temp is None:
            return None

        return temp

    @run_condensation.setter
    def run_condensation(self, value: 'bool'):
        self.wrapped.RunCondensation = bool(value) if value else False

    @property
    def unload_mesh(self) -> 'bool':
        """bool: 'UnloadMesh' is the original name of this property."""

        temp = self.wrapped.UnloadMesh

        if temp is None:
            return None

        return temp

    @unload_mesh.setter
    def unload_mesh(self, value: 'bool'):
        self.wrapped.UnloadMesh = bool(value) if value else False

    @property
    def unload_vectors(self) -> 'bool':
        """bool: 'UnloadVectors' is the original name of this property."""

        temp = self.wrapped.UnloadVectors

        if temp is None:
            return None

        return temp

    @unload_vectors.setter
    def unload_vectors(self, value: 'bool'):
        self.wrapped.UnloadVectors = bool(value) if value else False

    @property
    def fe(self) -> '_2133.FESubstructure':
        """FESubstructure: 'FE' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FE

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
