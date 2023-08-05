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


class ObdiiDataMessage(DataMessage):
    ID = 174
    NAME = 'obdii_data'

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
        super().__init__(name=ObdiiDataMessage.NAME,
                         global_id=ObdiiDataMessage.ID,
                         local_id=definition_message.local_id if definition_message else local_id,
                         endian=definition_message.endian if definition_message else endian,
                         definition_message=definition_message,
                         developer_fields=developer_fields,
                         fields=[
                             TimestampField(
                                 size=self.__get_field_size(definition_message, TimestampField.ID),
                                 growable=definition_message is None),
                             ObdiiDataTimestampMsField(
                                 size=self.__get_field_size(definition_message, ObdiiDataTimestampMsField.ID),
                                 growable=definition_message is None),
                             ObdiiDataTimeOffsetField(
                                 size=self.__get_field_size(definition_message, ObdiiDataTimeOffsetField.ID),
                                 growable=definition_message is None),
                             ObdiiDataPidField(
                                 size=self.__get_field_size(definition_message, ObdiiDataPidField.ID),
                                 growable=definition_message is None),
                             ObdiiDataRawDataField(
                                 size=self.__get_field_size(definition_message, ObdiiDataRawDataField.ID),
                                 growable=definition_message is None),
                             ObdiiDataPidDataSizeField(
                                 size=self.__get_field_size(definition_message, ObdiiDataPidDataSizeField.ID),
                                 growable=definition_message is None),
                             ObdiiDataSystemTimeField(
                                 size=self.__get_field_size(definition_message, ObdiiDataSystemTimeField.ID),
                                 growable=definition_message is None),
                             ObdiiDataStartTimestampField(
                                 size=self.__get_field_size(definition_message, ObdiiDataStartTimestampField.ID),
                                 growable=definition_message is None),
                             ObdiiDataStartTimestampMsField(
                                 size=self.__get_field_size(definition_message, ObdiiDataStartTimestampMsField.ID),
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
    def timestamp_ms(self) -> Optional[int]:
        field = self.get_field(ObdiiDataTimestampMsField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @timestamp_ms.setter
    def timestamp_ms(self, value: int):
        field = self.get_field(ObdiiDataTimestampMsField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def time_offset(self) -> Optional[int]:
        field = self.get_field(ObdiiDataTimeOffsetField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @time_offset.setter
    def time_offset(self, value: int):
        field = self.get_field(ObdiiDataTimeOffsetField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def pid(self) -> Optional[int]:
        field = self.get_field(ObdiiDataPidField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @pid.setter
    def pid(self, value: int):
        field = self.get_field(ObdiiDataPidField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def raw_data(self) -> Optional[int]:
        field = self.get_field(ObdiiDataRawDataField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @raw_data.setter
    def raw_data(self, value: int):
        field = self.get_field(ObdiiDataRawDataField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def pid_data_size(self) -> Optional[int]:
        field = self.get_field(ObdiiDataPidDataSizeField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @pid_data_size.setter
    def pid_data_size(self, value: int):
        field = self.get_field(ObdiiDataPidDataSizeField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def system_time(self) -> Optional[int]:
        field = self.get_field(ObdiiDataSystemTimeField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @system_time.setter
    def system_time(self, value: int):
        field = self.get_field(ObdiiDataSystemTimeField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    # timestamp : milliseconds from January 1st, 1970 at 00:00:00 UTC

    @property
    def start_timestamp(self) -> Optional[int]:
        field = self.get_field(ObdiiDataStartTimestampField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    # timestamp : milliseconds from January 1st, 1970 at 00:00:00 UTC

    @start_timestamp.setter
    def start_timestamp(self, value: int):
        field = self.get_field(ObdiiDataStartTimestampField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def start_timestamp_ms(self) -> Optional[int]:
        field = self.get_field(ObdiiDataStartTimestampMsField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @start_timestamp_ms.setter
    def start_timestamp_ms(self, value: int):
        field = self.get_field(ObdiiDataStartTimestampMsField.ID)

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


class ObdiiDataTimestampMsField(Field):
    ID = 0

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='timestamp_ms',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=1,
            size=size,
            units='ms',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class ObdiiDataTimeOffsetField(Field):
    ID = 1

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='time_offset',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=1,
            size=size,
            units='ms',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class ObdiiDataPidField(Field):
    ID = 2

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='pid',
            field_id=self.ID,
            base_type=BaseType.BYTE,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class ObdiiDataRawDataField(Field):
    ID = 3

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='raw_data',
            field_id=self.ID,
            base_type=BaseType.BYTE,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class ObdiiDataPidDataSizeField(Field):
    ID = 4

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='pid_data_size',
            field_id=self.ID,
            base_type=BaseType.UINT8,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class ObdiiDataSystemTimeField(Field):
    ID = 5

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='system_time',
            field_id=self.ID,
            base_type=BaseType.UINT32,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class ObdiiDataStartTimestampField(Field):
    ID = 6

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='start_timestamp',
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


class ObdiiDataStartTimestampMsField(Field):
    ID = 7

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='start_timestamp_ms',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=1,
            size=size,
            units='ms',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )
