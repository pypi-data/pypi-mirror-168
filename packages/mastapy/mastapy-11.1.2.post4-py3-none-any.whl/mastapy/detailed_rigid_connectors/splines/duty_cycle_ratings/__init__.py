"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1241 import AGMA6123SplineJointDutyCycleRating
    from ._1242 import GBT17855SplineJointDutyCycleRating
    from ._1243 import SAESplineJointDutyCycleRating
