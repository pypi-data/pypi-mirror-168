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


class AviationAttitudeMessage(DataMessage):
    ID = 178
    NAME = 'aviation_attitude'

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
        super().__init__(name=AviationAttitudeMessage.NAME,
                         global_id=AviationAttitudeMessage.ID,
                         local_id=definition_message.local_id if definition_message else local_id,
                         endian=definition_message.endian if definition_message else endian,
                         definition_message=definition_message,
                         developer_fields=developer_fields,
                         fields=[
                             TimestampField(
                                 size=self.__get_field_size(definition_message, TimestampField.ID),
                                 growable=definition_message is None),
                             AviationAttitudeTimestampMsField(
                                 size=self.__get_field_size(definition_message, AviationAttitudeTimestampMsField.ID),
                                 growable=definition_message is None),
                             AviationAttitudeSystemTimeField(
                                 size=self.__get_field_size(definition_message, AviationAttitudeSystemTimeField.ID),
                                 growable=definition_message is None),
                             AviationAttitudePitchField(
                                 size=self.__get_field_size(definition_message, AviationAttitudePitchField.ID),
                                 growable=definition_message is None),
                             AviationAttitudeRollField(
                                 size=self.__get_field_size(definition_message, AviationAttitudeRollField.ID),
                                 growable=definition_message is None),
                             AviationAttitudeAccelLateralField(
                                 size=self.__get_field_size(definition_message, AviationAttitudeAccelLateralField.ID),
                                 growable=definition_message is None),
                             AviationAttitudeAccelNormalField(
                                 size=self.__get_field_size(definition_message, AviationAttitudeAccelNormalField.ID),
                                 growable=definition_message is None),
                             AviationAttitudeTurnRateField(
                                 size=self.__get_field_size(definition_message, AviationAttitudeTurnRateField.ID),
                                 growable=definition_message is None),
                             AviationAttitudeStageField(
                                 size=self.__get_field_size(definition_message, AviationAttitudeStageField.ID),
                                 growable=definition_message is None),
                             AviationAttitudeAttitudeStageCompleteField(
                                 size=self.__get_field_size(definition_message,
                                                            AviationAttitudeAttitudeStageCompleteField.ID),
                                 growable=definition_message is None),
                             AviationAttitudeTrackField(
                                 size=self.__get_field_size(definition_message, AviationAttitudeTrackField.ID),
                                 growable=definition_message is None),
                             AviationAttitudeValidityField(
                                 size=self.__get_field_size(definition_message, AviationAttitudeValidityField.ID),
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
        field = self.get_field(AviationAttitudeTimestampMsField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @timestamp_ms.setter
    def timestamp_ms(self, value: int):
        field = self.get_field(AviationAttitudeTimestampMsField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def system_time(self) -> Optional[int]:
        field = self.get_field(AviationAttitudeSystemTimeField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @system_time.setter
    def system_time(self, value: int):
        field = self.get_field(AviationAttitudeSystemTimeField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def pitch(self) -> Optional[float]:
        field = self.get_field(AviationAttitudePitchField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @pitch.setter
    def pitch(self, value: float):
        field = self.get_field(AviationAttitudePitchField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def roll(self) -> Optional[float]:
        field = self.get_field(AviationAttitudeRollField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @roll.setter
    def roll(self, value: float):
        field = self.get_field(AviationAttitudeRollField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def accel_lateral(self) -> Optional[float]:
        field = self.get_field(AviationAttitudeAccelLateralField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @accel_lateral.setter
    def accel_lateral(self, value: float):
        field = self.get_field(AviationAttitudeAccelLateralField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def accel_normal(self) -> Optional[float]:
        field = self.get_field(AviationAttitudeAccelNormalField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @accel_normal.setter
    def accel_normal(self, value: float):
        field = self.get_field(AviationAttitudeAccelNormalField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def turn_rate(self) -> Optional[float]:
        field = self.get_field(AviationAttitudeTurnRateField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @turn_rate.setter
    def turn_rate(self, value: float):
        field = self.get_field(AviationAttitudeTurnRateField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def stage(self) -> Optional[AttitudeStage]:
        field = self.get_field(AviationAttitudeStageField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @stage.setter
    def stage(self, value: AttitudeStage):
        field = self.get_field(AviationAttitudeStageField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def attitude_stage_complete(self) -> Optional[int]:
        field = self.get_field(AviationAttitudeAttitudeStageCompleteField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @attitude_stage_complete.setter
    def attitude_stage_complete(self, value: int):
        field = self.get_field(AviationAttitudeAttitudeStageCompleteField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def track(self) -> Optional[float]:
        field = self.get_field(AviationAttitudeTrackField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @track.setter
    def track(self, value: float):
        field = self.get_field(AviationAttitudeTrackField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def validity(self) -> Optional[int]:
        field = self.get_field(AviationAttitudeValidityField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @validity.setter
    def validity(self, value: int):
        field = self.get_field(AviationAttitudeValidityField.ID)

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


class AviationAttitudeTimestampMsField(Field):
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


class AviationAttitudeSystemTimeField(Field):
    ID = 1

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='system_time',
            field_id=self.ID,
            base_type=BaseType.UINT32,
            offset=0,
            scale=1,
            size=size,
            units='ms',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class AviationAttitudePitchField(Field):
    ID = 2

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='pitch',
            field_id=self.ID,
            base_type=BaseType.SINT16,
            offset=0,
            scale=10430.38,
            size=size,
            units='radians',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class AviationAttitudeRollField(Field):
    ID = 3

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='roll',
            field_id=self.ID,
            base_type=BaseType.SINT16,
            offset=0,
            scale=10430.38,
            size=size,
            units='radians',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class AviationAttitudeAccelLateralField(Field):
    ID = 4

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='accel_lateral',
            field_id=self.ID,
            base_type=BaseType.SINT16,
            offset=0,
            scale=100,
            size=size,
            units='m/s^2',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class AviationAttitudeAccelNormalField(Field):
    ID = 5

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='accel_normal',
            field_id=self.ID,
            base_type=BaseType.SINT16,
            offset=0,
            scale=100,
            size=size,
            units='m/s^2',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class AviationAttitudeTurnRateField(Field):
    ID = 6

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='turn_rate',
            field_id=self.ID,
            base_type=BaseType.SINT16,
            offset=0,
            scale=1024,
            size=size,
            units='radians/second',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class AviationAttitudeStageField(Field):
    ID = 7

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='stage',
            field_id=self.ID,
            base_type=BaseType.ENUM,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class AviationAttitudeAttitudeStageCompleteField(Field):
    ID = 8

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='attitude_stage_complete',
            field_id=self.ID,
            base_type=BaseType.UINT8,
            offset=0,
            scale=1,
            size=size,
            units='%',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class AviationAttitudeTrackField(Field):
    ID = 9

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='track',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=10430.38,
            size=size,
            units='radians',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class AviationAttitudeValidityField(Field):
    ID = 10

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='validity',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )
