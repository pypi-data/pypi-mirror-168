"""_7290.py

SMTBitmap
"""


from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy import _7279
from mastapy._internal.python_net import python_net_import

_SMT_BITMAP = python_net_import('SMT.MastaAPIUtility.Scripting', 'SMTBitmap')


__docformat__ = 'restructuredtext en'
__all__ = ('SMTBitmap',)


class SMTBitmap(_7279.MarshalByRefObjectPermanent):
    """SMTBitmap

    This is a mastapy class.
    """

    TYPE = _SMT_BITMAP

    def __init__(self, instance_to_wrap: 'SMTBitmap.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def to_image(self) -> 'Image':
        """ 'ToImage' is the original name of this method.

        Returns:
            Image
        """

        return conversion.pn_to_mp_image(self.wrapped.ToImage())

    def to_bytes(self) -> 'bytes':
        """ 'ToBytes' is the original name of this method.

        Returns:
            bytes
        """

        return conversion.pn_to_mp_bytes(self.wrapped.ToBytes())
