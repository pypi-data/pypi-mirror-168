"""_7298.py

LicenceServerDetails
"""


from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_LICENCE_SERVER_DETAILS = python_net_import('SMT.MastaAPIUtility.Licensing', 'LicenceServerDetails')


__docformat__ = 'restructuredtext en'
__all__ = ('LicenceServerDetails',)


class LicenceServerDetails:
    """LicenceServerDetails

    This is a mastapy class.
    """

    TYPE = _LICENCE_SERVER_DETAILS

    def __init__(self, instance_to_wrap: 'LicenceServerDetails.TYPE' = None):
        self.wrapped = instance_to_wrap if instance_to_wrap else LicenceServerDetails.TYPE()
        self._freeze()

    __frozen = False

    def __setattr__(self, attr, value):
        prop = getattr(self.__class__, attr, None)
        if isinstance(prop, property):
            prop.fset(self, value)
        else:
            if self.__frozen and attr not in self.__dict__:
                raise AttributeError((
                    'Attempted to set unknown '
                    'attribute: \'{}\''.format(attr))) from None

            super().__setattr__(attr, value)

    def __delattr__(self, name):
        raise AttributeError(
            'Cannot delete the attributes of a mastapy object.') from None

    def _freeze(self):
        self.__frozen = True

    @property
    def ip(self) -> 'str':
        """str: 'Ip' is the original name of this property."""

        temp = self.wrapped.Ip

        if temp is None:
            return None

        return temp

    @ip.setter
    def ip(self, value: 'str'):
        self.wrapped.Ip = str(value) if value else ''

    @property
    def port(self) -> 'int':
        """int: 'Port' is the original name of this property."""

        temp = self.wrapped.Port

        if temp is None:
            return None

        return temp

    @port.setter
    def port(self, value: 'int'):
        self.wrapped.Port = int(value) if value else 0

    @property
    def web_port(self) -> 'int':
        """int: 'WebPort' is the original name of this property."""

        temp = self.wrapped.WebPort

        if temp is None:
            return None

        return temp

    @web_port.setter
    def web_port(self, value: 'int'):
        self.wrapped.WebPort = int(value) if value else 0

    @property
    def licence_groups_ip(self) -> 'str':
        """str: 'LicenceGroupsIp' is the original name of this property."""

        temp = self.wrapped.LicenceGroupsIp

        if temp is None:
            return None

        return temp

    @licence_groups_ip.setter
    def licence_groups_ip(self, value: 'str'):
        self.wrapped.LicenceGroupsIp = str(value) if value else ''

    @property
    def licence_groups_port(self) -> 'int':
        """int: 'LicenceGroupsPort' is the original name of this property."""

        temp = self.wrapped.LicenceGroupsPort

        if temp is None:
            return None

        return temp

    @licence_groups_port.setter
    def licence_groups_port(self, value: 'int'):
        self.wrapped.LicenceGroupsPort = int(value) if value else 0

    def has_ip(self) -> 'bool':
        """ 'HasIp' is the original name of this method.

        Returns:
            bool
        """

        method_result = self.wrapped.HasIp()
        return method_result

    def has_port(self) -> 'bool':
        """ 'HasPort' is the original name of this method.

        Returns:
            bool
        """

        method_result = self.wrapped.HasPort()
        return method_result

    def has_web_port(self) -> 'bool':
        """ 'HasWebPort' is the original name of this method.

        Returns:
            bool
        """

        method_result = self.wrapped.HasWebPort()
        return method_result

    def has_licence_groups_ip(self) -> 'bool':
        """ 'HasLicenceGroupsIp' is the original name of this method.

        Returns:
            bool
        """

        method_result = self.wrapped.HasLicenceGroupsIp()
        return method_result

    def has_licence_groups_port(self) -> 'bool':
        """ 'HasLicenceGroupsPort' is the original name of this method.

        Returns:
            bool
        """

        method_result = self.wrapped.HasLicenceGroupsPort()
        return method_result
