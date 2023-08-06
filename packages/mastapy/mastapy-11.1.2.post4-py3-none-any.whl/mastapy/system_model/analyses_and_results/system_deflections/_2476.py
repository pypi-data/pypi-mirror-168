"""_2476.py

CVTBeltConnectionSystemDeflection
"""


from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import _2024
from mastapy.system_model.analyses_and_results.power_flows import _3814
from mastapy.system_model.analyses_and_results.system_deflections import _2443
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CVTBeltConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionSystemDeflection',)


class CVTBeltConnectionSystemDeflection(_2443.BeltConnectionSystemDeflection):
    """CVTBeltConnectionSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CVT_BELT_CONNECTION_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def belt_clamping_force_safety_factor(self) -> 'float':
        """float: 'BeltClampingForceSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BeltClampingForceSafetyFactor

        if temp is None:
            return None

        return temp

    @property
    def minimum_required_clamping_force(self) -> 'float':
        """float: 'MinimumRequiredClampingForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumRequiredClampingForce

        if temp is None:
            return None

        return temp

    @property
    def pump_efficiency(self) -> 'float':
        """float: 'PumpEfficiency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PumpEfficiency

        if temp is None:
            return None

        return temp

    @property
    def total_efficiency(self) -> 'float':
        """float: 'TotalEfficiency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalEfficiency

        if temp is None:
            return None

        return temp

    @property
    def variator_efficiency(self) -> 'float':
        """float: 'VariatorEfficiency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VariatorEfficiency

        if temp is None:
            return None

        return temp

    @property
    def connection_design(self) -> '_2024.CVTBeltConnection':
        """CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results(self) -> '_3814.CVTBeltConnectionPowerFlow':
        """CVTBeltConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
