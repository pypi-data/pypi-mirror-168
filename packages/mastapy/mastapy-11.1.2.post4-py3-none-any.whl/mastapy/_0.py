"""_0.py

APIBase
"""


from typing import TypeVar
from sys import modules

from mastapy._internal import constructor
from mastapy import _7279
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_API_BASE = python_net_import('SMT.MastaAPI', 'APIBase')


__docformat__ = 'restructuredtext en'
__all__ = ('APIBase',)


class APIBase(_7279.MarshalByRefObjectPermanent):
    """APIBase

    This is a mastapy class.
    """

    TYPE = _API_BASE

    def __init__(self, instance_to_wrap: 'APIBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def disconnect_from_masta(self):
        """ 'DisconnectFromMASTA' is the original name of this method."""

        self.wrapped.DisconnectFromMASTA()

    def is_instance_of_wrapped_type(self, type_: 'type') -> 'bool':
        """ 'IsInstanceOfWrappedType' is the original name of this method.

        Args:
            type_ (type)

        Returns:
            bool
        """

        method_result = self.wrapped.IsInstanceOfWrappedType(type_)
        return method_result

    T_get_property = TypeVar('T_get_property')

    def get_property(self, name: 'str') -> 'T_get_property':
        """ 'GetProperty' is the original name of this method.

        Args:
            name (str)

        Returns:
            T_get_property
        """

        name = str(name)
        method_result = self.wrapped.GetProperty(name if name else '')
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def set_property(self, name: 'str', value: 'object'):
        """ 'SetProperty' is the original name of this method.

        Args:
            name (str)
            value (object)
        """

        name = str(name)
        self.wrapped.SetProperty(name if name else '', value)

    def is_valid(self, property_name: 'str') -> 'bool':
        """ 'IsValid' is the original name of this method.

        Args:
            property_name (str)

        Returns:
            bool
        """

        property_name = str(property_name)
        method_result = self.wrapped.IsValid(property_name if property_name else '')
        return method_result

    def is_read_only(self, property_name: 'str') -> 'bool':
        """ 'IsReadOnly' is the original name of this method.

        Args:
            property_name (str)

        Returns:
            bool
        """

        property_name = str(property_name)
        method_result = self.wrapped.IsReadOnly(property_name if property_name else '')
        return method_result

    def documentation_url(self) -> 'str':
        """ 'DocumentationUrl' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.DocumentationUrl()
        return method_result

    def to_string(self) -> 'str':
        """ 'ToString' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.ToString()
        return method_result

    def __hash__(self) -> 'int':
        """ 'GetHashCode' is the original name of this method.

        Returns:
            int
        """

        method_result = self.wrapped.GetHashCode()
        return method_result

    def __eq__(self, other: 'APIBase') -> 'bool':
        """ 'op_Equality' is the original name of this method.

        Args:
            other (mastapy.APIBase)

        Returns:
            bool
        """

        method_result = self.wrapped.op_Equality(self.wrapped, other.wrapped if other else None)
        return method_result

    def __ne__(self, other: 'APIBase') -> 'bool':
        """ 'op_Inequality' is the original name of this method.

        Args:
            other (mastapy.APIBase)

        Returns:
            bool
        """

        method_result = self.wrapped.op_Inequality(self.wrapped, other.wrapped if other else None)
        return method_result

    def __str__(self):
        return self.wrapped.ToString()

    def __repr__(self):
        type_name = self.wrapped.GetType().Name
        part_name = self.unique_name if hasattr(self, 'unique_name') else str(self)
        return f'<{type_name} : {part_name}>'

    def is_of_type(self, type_) -> bool:
        """ Method for checking if a mastapy object can be cast to another type.

        Note:
            This method follows all standard casting rules from other languages.

        Args:
            type_: The type to check.

        Returns:
            bool
        """

        a = type(self.wrapped)
        b = getattr(modules[type_.__module__], type_.__name__).TYPE

        return b in a.__mro__

    def cast_or_none(self, type_):
        """ Method for casting one mastapy object to another.

        Note:
            This method follows all standard casting rules from other languages.
            This method will return None if the cast fails.

        Args:
            type_: The type to cast to.
        """

        if not self.is_of_type(type_):
            return None

        return type_(self.wrapped)

    def cast(self, type_):
        """ Method for casting one mastapy object to another.

        Note:
            This method follows all standard casting rules from other languages.
            This method will raise a CastException if the cast fails.

        Args:
            type_: The type to cast to.
        """

        if not self.is_of_type(type_):
            raise CastException('Could not cast {} to type {}. Is it a mastapy type?'.format(type(self), type_))

        return type_(self.wrapped)
