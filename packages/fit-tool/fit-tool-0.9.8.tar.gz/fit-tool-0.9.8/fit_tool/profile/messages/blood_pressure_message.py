# Autogenerated. Do not modify.
#
# Profile: 21.60
from typing import Optional

from fit_tool.base_type import BaseType
from fit_tool.data_message import DataMessage
from fit_tool.definition_message import DefinitionMessage
from fit_tool.developer_field import DeveloperField
from fit_tool.endian import Endian
from fit_tool.field import Field
from fit_tool.sub_field import SubField
from fit_tool.profile.profile_type import *


class BloodPressureMessage(DataMessage):
    ID = 51
    NAME = 'blood_pressure'

    @staticmethod
    def __get_field_size(definition_message: DefinitionMessage, field_id: int) -> int:
        size = 0
        if definition_message:
            field_definition = definition_message.get_field_definition(field_id)
            if field_definition:
                size = field_definition.size

        return size

    def __init__(self, definition_message=None, developer_fields=None, local_id: int = 0,
                 endian: Endian = Endian.LITTLE):
        super().__init__(name=BloodPressureMessage.NAME,
                         global_id=BloodPressureMessage.ID,
                         local_id=definition_message.local_id if definition_message else local_id,
                         endian=definition_message.endian if definition_message else endian,
                         definition_message=definition_message,
                         developer_fields=developer_fields,
                         fields=[
                             TimestampField(
                                 size=self.__get_field_size(definition_message, TimestampField.ID),
                                 growable=definition_message is None),
                             BloodPressureSystolicPressureField(
                                 size=self.__get_field_size(definition_message, BloodPressureSystolicPressureField.ID),
                                 growable=definition_message is None),
                             BloodPressureDiastolicPressureField(
                                 size=self.__get_field_size(definition_message, BloodPressureDiastolicPressureField.ID),
                                 growable=definition_message is None),
                             BloodPressureMeanArterialPressureField(
                                 size=self.__get_field_size(definition_message,
                                                            BloodPressureMeanArterialPressureField.ID),
                                 growable=definition_message is None),
                             BloodPressureMap3SampleMeanField(
                                 size=self.__get_field_size(definition_message, BloodPressureMap3SampleMeanField.ID),
                                 growable=definition_message is None),
                             BloodPressureMapMorningValuesField(
                                 size=self.__get_field_size(definition_message, BloodPressureMapMorningValuesField.ID),
                                 growable=definition_message is None),
                             BloodPressureMapEveningValuesField(
                                 size=self.__get_field_size(definition_message, BloodPressureMapEveningValuesField.ID),
                                 growable=definition_message is None),
                             BloodPressureHeartRateField(
                                 size=self.__get_field_size(definition_message, BloodPressureHeartRateField.ID),
                                 growable=definition_message is None),
                             BloodPressureHeartRateTypeField(
                                 size=self.__get_field_size(definition_message, BloodPressureHeartRateTypeField.ID),
                                 growable=definition_message is None),
                             BloodPressureStatusField(
                                 size=self.__get_field_size(definition_message, BloodPressureStatusField.ID),
                                 growable=definition_message is None),
                             BloodPressureUserProfileIndexField(
                                 size=self.__get_field_size(definition_message, BloodPressureUserProfileIndexField.ID),
                                 growable=definition_message is None)
                         ])

        self.growable = self.definition_message is None

    @classmethod
    def from_bytes(cls, definition_message: DefinitionMessage, developer_fields: list[DeveloperField],
                   bytes_buffer: bytes, offset: int = 0):
        message = cls(definition_message=definition_message, developer_fields=developer_fields)
        message.read_from_bytes(bytes_buffer, offset)
        return message

    # timestamp : milliseconds from January 1st, 1970 at 00:00:00 UTC

    @property
    def timestamp(self) -> Optional[int]:
        field = self.get_field(TimestampField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    # timestamp : milliseconds from January 1st, 1970 at 00:00:00 UTC

    @timestamp.setter
    def timestamp(self, value: int):
        field = self.get_field(TimestampField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def systolic_pressure(self) -> Optional[int]:
        field = self.get_field(BloodPressureSystolicPressureField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @systolic_pressure.setter
    def systolic_pressure(self, value: int):
        field = self.get_field(BloodPressureSystolicPressureField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def diastolic_pressure(self) -> Optional[int]:
        field = self.get_field(BloodPressureDiastolicPressureField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @diastolic_pressure.setter
    def diastolic_pressure(self, value: int):
        field = self.get_field(BloodPressureDiastolicPressureField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def mean_arterial_pressure(self) -> Optional[int]:
        field = self.get_field(BloodPressureMeanArterialPressureField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @mean_arterial_pressure.setter
    def mean_arterial_pressure(self, value: int):
        field = self.get_field(BloodPressureMeanArterialPressureField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def map_3_sample_mean(self) -> Optional[int]:
        field = self.get_field(BloodPressureMap3SampleMeanField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @map_3_sample_mean.setter
    def map_3_sample_mean(self, value: int):
        field = self.get_field(BloodPressureMap3SampleMeanField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def map_morning_values(self) -> Optional[int]:
        field = self.get_field(BloodPressureMapMorningValuesField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @map_morning_values.setter
    def map_morning_values(self, value: int):
        field = self.get_field(BloodPressureMapMorningValuesField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def map_evening_values(self) -> Optional[int]:
        field = self.get_field(BloodPressureMapEveningValuesField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @map_evening_values.setter
    def map_evening_values(self, value: int):
        field = self.get_field(BloodPressureMapEveningValuesField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def heart_rate(self) -> Optional[int]:
        field = self.get_field(BloodPressureHeartRateField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @heart_rate.setter
    def heart_rate(self, value: int):
        field = self.get_field(BloodPressureHeartRateField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def heart_rate_type(self) -> Optional[HrType]:
        field = self.get_field(BloodPressureHeartRateTypeField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @heart_rate_type.setter
    def heart_rate_type(self, value: HrType):
        field = self.get_field(BloodPressureHeartRateTypeField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def status(self) -> Optional[BpStatus]:
        field = self.get_field(BloodPressureStatusField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @status.setter
    def status(self, value: BpStatus):
        field = self.get_field(BloodPressureStatusField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def user_profile_index(self) -> Optional[int]:
        field = self.get_field(BloodPressureUserProfileIndexField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @user_profile_index.setter
    def user_profile_index(self, value: int):
        field = self.get_field(BloodPressureUserProfileIndexField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)


class TimestampField(Field):
    ID = 253

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='timestamp',
            field_id=self.ID,
            base_type=BaseType.UINT32,
            offset=-631065600000,
            scale=0.001,
            size=size,
            units='ms',
            type_name='date_time',
            growable=growable,
            sub_fields=[
            ]
        )


class BloodPressureSystolicPressureField(Field):
    ID = 0

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='systolic_pressure',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=1,
            size=size,
            units='mmHg',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class BloodPressureDiastolicPressureField(Field):
    ID = 1

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='diastolic_pressure',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=1,
            size=size,
            units='mmHg',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class BloodPressureMeanArterialPressureField(Field):
    ID = 2

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='mean_arterial_pressure',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=1,
            size=size,
            units='mmHg',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class BloodPressureMap3SampleMeanField(Field):
    ID = 3

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='map_3_sample_mean',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=1,
            size=size,
            units='mmHg',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class BloodPressureMapMorningValuesField(Field):
    ID = 4

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='map_morning_values',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=1,
            size=size,
            units='mmHg',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class BloodPressureMapEveningValuesField(Field):
    ID = 5

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='map_evening_values',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=1,
            size=size,
            units='mmHg',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class BloodPressureHeartRateField(Field):
    ID = 6

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='heart_rate',
            field_id=self.ID,
            base_type=BaseType.UINT8,
            offset=0,
            scale=1,
            size=size,
            units='bpm',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class BloodPressureHeartRateTypeField(Field):
    ID = 7

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='heart_rate_type',
            field_id=self.ID,
            base_type=BaseType.ENUM,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class BloodPressureStatusField(Field):
    ID = 8

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='status',
            field_id=self.ID,
            base_type=BaseType.ENUM,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class BloodPressureUserProfileIndexField(Field):
    ID = 9

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='user_profile_index',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )
