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


class SegmentLeaderboardEntryMessage(DataMessage):
    ID = 149
    NAME = 'segment_leaderboard_entry'

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
        super().__init__(name=SegmentLeaderboardEntryMessage.NAME,
                         global_id=SegmentLeaderboardEntryMessage.ID,
                         local_id=definition_message.local_id if definition_message else local_id,
                         endian=definition_message.endian if definition_message else endian,
                         definition_message=definition_message,
                         developer_fields=developer_fields,
                         fields=[
                             MessageIndexField(
                                 size=self.__get_field_size(definition_message, MessageIndexField.ID),
                                 growable=definition_message is None),
                             SegmentLeaderboardEntryNameField(
                                 size=self.__get_field_size(definition_message, SegmentLeaderboardEntryNameField.ID),
                                 growable=definition_message is None),
                             SegmentLeaderboardEntryTypeField(
                                 size=self.__get_field_size(definition_message, SegmentLeaderboardEntryTypeField.ID),
                                 growable=definition_message is None),
                             SegmentLeaderboardEntryGroupPrimaryKeyField(
                                 size=self.__get_field_size(definition_message,
                                                            SegmentLeaderboardEntryGroupPrimaryKeyField.ID),
                                 growable=definition_message is None),
                             SegmentLeaderboardEntryActivityIdField(
                                 size=self.__get_field_size(definition_message,
                                                            SegmentLeaderboardEntryActivityIdField.ID),
                                 growable=definition_message is None),
                             SegmentLeaderboardEntrySegmentTimeField(
                                 size=self.__get_field_size(definition_message,
                                                            SegmentLeaderboardEntrySegmentTimeField.ID),
                                 growable=definition_message is None),
                             SegmentLeaderboardEntryActivityIdStringField(
                                 size=self.__get_field_size(definition_message,
                                                            SegmentLeaderboardEntryActivityIdStringField.ID),
                                 growable=definition_message is None)
                         ])

        self.growable = self.definition_message is None

    @classmethod
    def from_bytes(cls, definition_message: DefinitionMessage, developer_fields: list[DeveloperField],
                   bytes_buffer: bytes, offset: int = 0):
        message = cls(definition_message=definition_message, developer_fields=developer_fields)
        message.read_from_bytes(bytes_buffer, offset)
        return message

    @property
    def message_index(self) -> Optional[int]:
        field = self.get_field(MessageIndexField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @message_index.setter
    def message_index(self, value: int):
        field = self.get_field(MessageIndexField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def segment_leaderboard_entry_name(self) -> Optional[str]:
        field = self.get_field(SegmentLeaderboardEntryNameField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @segment_leaderboard_entry_name.setter
    def segment_leaderboard_entry_name(self, value: str):
        field = self.get_field(SegmentLeaderboardEntryNameField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def type(self) -> Optional[SegmentLeaderboardType]:
        field = self.get_field(SegmentLeaderboardEntryTypeField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @type.setter
    def type(self, value: SegmentLeaderboardType):
        field = self.get_field(SegmentLeaderboardEntryTypeField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def group_primary_key(self) -> Optional[int]:
        field = self.get_field(SegmentLeaderboardEntryGroupPrimaryKeyField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @group_primary_key.setter
    def group_primary_key(self, value: int):
        field = self.get_field(SegmentLeaderboardEntryGroupPrimaryKeyField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def activity_id(self) -> Optional[int]:
        field = self.get_field(SegmentLeaderboardEntryActivityIdField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @activity_id.setter
    def activity_id(self, value: int):
        field = self.get_field(SegmentLeaderboardEntryActivityIdField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def segment_time(self) -> Optional[float]:
        field = self.get_field(SegmentLeaderboardEntrySegmentTimeField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @segment_time.setter
    def segment_time(self, value: float):
        field = self.get_field(SegmentLeaderboardEntrySegmentTimeField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def activity_id_string(self) -> Optional[str]:
        field = self.get_field(SegmentLeaderboardEntryActivityIdStringField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @activity_id_string.setter
    def activity_id_string(self, value: str):
        field = self.get_field(SegmentLeaderboardEntryActivityIdStringField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)


class MessageIndexField(Field):
    ID = 254

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='message_index',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class SegmentLeaderboardEntryNameField(Field):
    ID = 0

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='name',
            field_id=self.ID,
            base_type=BaseType.STRING,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class SegmentLeaderboardEntryTypeField(Field):
    ID = 1

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='type',
            field_id=self.ID,
            base_type=BaseType.ENUM,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class SegmentLeaderboardEntryGroupPrimaryKeyField(Field):
    ID = 2

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='group_primary_key',
            field_id=self.ID,
            base_type=BaseType.UINT32,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class SegmentLeaderboardEntryActivityIdField(Field):
    ID = 3

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='activity_id',
            field_id=self.ID,
            base_type=BaseType.UINT32,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class SegmentLeaderboardEntrySegmentTimeField(Field):
    ID = 4

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='segment_time',
            field_id=self.ID,
            base_type=BaseType.UINT32,
            offset=0,
            scale=1000,
            size=size,
            units='s',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class SegmentLeaderboardEntryActivityIdStringField(Field):
    ID = 5

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='activity_id_string',
            field_id=self.ID,
            base_type=BaseType.STRING,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )
