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


class DiveSettingsMessage(DataMessage):
    ID = 258
    NAME = 'dive_settings'

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
        super().__init__(name=DiveSettingsMessage.NAME,
                         global_id=DiveSettingsMessage.ID,
                         local_id=definition_message.local_id if definition_message else local_id,
                         endian=definition_message.endian if definition_message else endian,
                         definition_message=definition_message,
                         developer_fields=developer_fields,
                         fields=[
                             MessageIndexField(
                                 size=self.__get_field_size(definition_message, MessageIndexField.ID),
                                 growable=definition_message is None),
                             DiveSettingsNameField(
                                 size=self.__get_field_size(definition_message, DiveSettingsNameField.ID),
                                 growable=definition_message is None),
                             DiveSettingsModelField(
                                 size=self.__get_field_size(definition_message, DiveSettingsModelField.ID),
                                 growable=definition_message is None),
                             DiveSettingsGfLowField(
                                 size=self.__get_field_size(definition_message, DiveSettingsGfLowField.ID),
                                 growable=definition_message is None),
                             DiveSettingsGfHighField(
                                 size=self.__get_field_size(definition_message, DiveSettingsGfHighField.ID),
                                 growable=definition_message is None),
                             DiveSettingsWaterTypeField(
                                 size=self.__get_field_size(definition_message, DiveSettingsWaterTypeField.ID),
                                 growable=definition_message is None),
                             DiveSettingsWaterDensityField(
                                 size=self.__get_field_size(definition_message, DiveSettingsWaterDensityField.ID),
                                 growable=definition_message is None),
                             DiveSettingsPo2WarnField(
                                 size=self.__get_field_size(definition_message, DiveSettingsPo2WarnField.ID),
                                 growable=definition_message is None),
                             DiveSettingsPo2CriticalField(
                                 size=self.__get_field_size(definition_message, DiveSettingsPo2CriticalField.ID),
                                 growable=definition_message is None),
                             DiveSettingsPo2DecoField(
                                 size=self.__get_field_size(definition_message, DiveSettingsPo2DecoField.ID),
                                 growable=definition_message is None),
                             DiveSettingsSafetyStopEnabledField(
                                 size=self.__get_field_size(definition_message, DiveSettingsSafetyStopEnabledField.ID),
                                 growable=definition_message is None),
                             DiveSettingsBottomDepthField(
                                 size=self.__get_field_size(definition_message, DiveSettingsBottomDepthField.ID),
                                 growable=definition_message is None),
                             DiveSettingsBottomTimeField(
                                 size=self.__get_field_size(definition_message, DiveSettingsBottomTimeField.ID),
                                 growable=definition_message is None),
                             DiveSettingsApneaCountdownEnabledField(
                                 size=self.__get_field_size(definition_message,
                                                            DiveSettingsApneaCountdownEnabledField.ID),
                                 growable=definition_message is None),
                             DiveSettingsApneaCountdownTimeField(
                                 size=self.__get_field_size(definition_message, DiveSettingsApneaCountdownTimeField.ID),
                                 growable=definition_message is None),
                             DiveSettingsBacklightModeField(
                                 size=self.__get_field_size(definition_message, DiveSettingsBacklightModeField.ID),
                                 growable=definition_message is None),
                             DiveSettingsBacklightBrightnessField(
                                 size=self.__get_field_size(definition_message,
                                                            DiveSettingsBacklightBrightnessField.ID),
                                 growable=definition_message is None),
                             DiveSettingsBacklightTimeoutField(
                                 size=self.__get_field_size(definition_message, DiveSettingsBacklightTimeoutField.ID),
                                 growable=definition_message is None),
                             DiveSettingsRepeatDiveIntervalField(
                                 size=self.__get_field_size(definition_message, DiveSettingsRepeatDiveIntervalField.ID),
                                 growable=definition_message is None),
                             DiveSettingsSafetyStopTimeField(
                                 size=self.__get_field_size(definition_message, DiveSettingsSafetyStopTimeField.ID),
                                 growable=definition_message is None),
                             DiveSettingsHeartRateSourceTypeField(
                                 size=self.__get_field_size(definition_message,
                                                            DiveSettingsHeartRateSourceTypeField.ID),
                                 growable=definition_message is None),
                             DiveSettingsHeartRateSourceField(
                                 size=self.__get_field_size(definition_message, DiveSettingsHeartRateSourceField.ID),
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
    def dive_settings_name(self) -> Optional[str]:
        field = self.get_field(DiveSettingsNameField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @dive_settings_name.setter
    def dive_settings_name(self, value: str):
        field = self.get_field(DiveSettingsNameField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def model(self) -> Optional[TissueModelType]:
        field = self.get_field(DiveSettingsModelField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @model.setter
    def model(self, value: TissueModelType):
        field = self.get_field(DiveSettingsModelField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def gf_low(self) -> Optional[int]:
        field = self.get_field(DiveSettingsGfLowField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @gf_low.setter
    def gf_low(self, value: int):
        field = self.get_field(DiveSettingsGfLowField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def gf_high(self) -> Optional[int]:
        field = self.get_field(DiveSettingsGfHighField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @gf_high.setter
    def gf_high(self, value: int):
        field = self.get_field(DiveSettingsGfHighField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def water_type(self) -> Optional[WaterType]:
        field = self.get_field(DiveSettingsWaterTypeField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @water_type.setter
    def water_type(self, value: WaterType):
        field = self.get_field(DiveSettingsWaterTypeField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def water_density(self) -> Optional[float]:
        field = self.get_field(DiveSettingsWaterDensityField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @water_density.setter
    def water_density(self, value: float):
        field = self.get_field(DiveSettingsWaterDensityField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def po2_warn(self) -> Optional[float]:
        field = self.get_field(DiveSettingsPo2WarnField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @po2_warn.setter
    def po2_warn(self, value: float):
        field = self.get_field(DiveSettingsPo2WarnField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def po2_critical(self) -> Optional[float]:
        field = self.get_field(DiveSettingsPo2CriticalField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @po2_critical.setter
    def po2_critical(self, value: float):
        field = self.get_field(DiveSettingsPo2CriticalField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def po2_deco(self) -> Optional[float]:
        field = self.get_field(DiveSettingsPo2DecoField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @po2_deco.setter
    def po2_deco(self, value: float):
        field = self.get_field(DiveSettingsPo2DecoField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def safety_stop_enabled(self) -> Optional[bool]:
        field = self.get_field(DiveSettingsSafetyStopEnabledField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @safety_stop_enabled.setter
    def safety_stop_enabled(self, value: bool):
        field = self.get_field(DiveSettingsSafetyStopEnabledField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def bottom_depth(self) -> Optional[float]:
        field = self.get_field(DiveSettingsBottomDepthField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @bottom_depth.setter
    def bottom_depth(self, value: float):
        field = self.get_field(DiveSettingsBottomDepthField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def bottom_time(self) -> Optional[int]:
        field = self.get_field(DiveSettingsBottomTimeField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @bottom_time.setter
    def bottom_time(self, value: int):
        field = self.get_field(DiveSettingsBottomTimeField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def apnea_countdown_enabled(self) -> Optional[bool]:
        field = self.get_field(DiveSettingsApneaCountdownEnabledField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @apnea_countdown_enabled.setter
    def apnea_countdown_enabled(self, value: bool):
        field = self.get_field(DiveSettingsApneaCountdownEnabledField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def apnea_countdown_time(self) -> Optional[int]:
        field = self.get_field(DiveSettingsApneaCountdownTimeField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @apnea_countdown_time.setter
    def apnea_countdown_time(self, value: int):
        field = self.get_field(DiveSettingsApneaCountdownTimeField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def backlight_mode(self) -> Optional[DiveBacklightMode]:
        field = self.get_field(DiveSettingsBacklightModeField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @backlight_mode.setter
    def backlight_mode(self, value: DiveBacklightMode):
        field = self.get_field(DiveSettingsBacklightModeField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def backlight_brightness(self) -> Optional[int]:
        field = self.get_field(DiveSettingsBacklightBrightnessField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @backlight_brightness.setter
    def backlight_brightness(self, value: int):
        field = self.get_field(DiveSettingsBacklightBrightnessField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def backlight_timeout(self) -> Optional[int]:
        field = self.get_field(DiveSettingsBacklightTimeoutField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @backlight_timeout.setter
    def backlight_timeout(self, value: int):
        field = self.get_field(DiveSettingsBacklightTimeoutField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def repeat_dive_interval(self) -> Optional[int]:
        field = self.get_field(DiveSettingsRepeatDiveIntervalField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @repeat_dive_interval.setter
    def repeat_dive_interval(self, value: int):
        field = self.get_field(DiveSettingsRepeatDiveIntervalField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def safety_stop_time(self) -> Optional[int]:
        field = self.get_field(DiveSettingsSafetyStopTimeField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @safety_stop_time.setter
    def safety_stop_time(self, value: int):
        field = self.get_field(DiveSettingsSafetyStopTimeField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def heart_rate_source_type(self) -> Optional[SourceType]:
        field = self.get_field(DiveSettingsHeartRateSourceTypeField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @heart_rate_source_type.setter
    def heart_rate_source_type(self, value: SourceType):
        field = self.get_field(DiveSettingsHeartRateSourceTypeField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def heart_rate_source(self) -> Optional[int]:
        field = self.get_field(DiveSettingsHeartRateSourceField.ID)
        if field and field.is_valid():
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @heart_rate_source.setter
    def heart_rate_source(self, value: int):
        field = self.get_field(DiveSettingsHeartRateSourceField.ID)

        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def heart_rate_antplus_device_type(self) -> Optional[int]:
        field = self.get_field(DiveSettingsHeartRateSourceField.ID)
        type_field = self.get_field(DiveSettingsHeartRateSourceTypeField.ID)

        is_sub_field_valid = type_field and type_field.get_value() in [1]
        if field and field.is_valid() and is_sub_field_valid:
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @heart_rate_antplus_device_type.setter
    def heart_rate_antplus_device_type(self, value: int):
        field = self.get_field(DiveSettingsHeartRateSourceField.ID)
        if field:
            if value is None:
                field.clear()
            else:
                sub_field = field.get_valid_sub_field(self.fields)
                field.set_value(0, value, sub_field)

    @property
    def heart_rate_local_device_type(self) -> Optional[int]:
        field = self.get_field(DiveSettingsHeartRateSourceField.ID)
        type_field = self.get_field(DiveSettingsHeartRateSourceTypeField.ID)

        is_sub_field_valid = type_field and type_field.get_value() in [5]
        if field and field.is_valid() and is_sub_field_valid:
            sub_field = field.get_valid_sub_field(self.fields)
            return field.get_value(sub_field=sub_field)
        else:
            return None

    @heart_rate_local_device_type.setter
    def heart_rate_local_device_type(self, value: int):
        field = self.get_field(DiveSettingsHeartRateSourceField.ID)
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


class DiveSettingsNameField(Field):
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


class DiveSettingsModelField(Field):
    ID = 1

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='model',
            field_id=self.ID,
            base_type=BaseType.ENUM,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsGfLowField(Field):
    ID = 2

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='gf_low',
            field_id=self.ID,
            base_type=BaseType.UINT8,
            offset=0,
            scale=1,
            size=size,
            units='percent',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsGfHighField(Field):
    ID = 3

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='gf_high',
            field_id=self.ID,
            base_type=BaseType.UINT8,
            offset=0,
            scale=1,
            size=size,
            units='percent',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsWaterTypeField(Field):
    ID = 4

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='water_type',
            field_id=self.ID,
            base_type=BaseType.ENUM,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsWaterDensityField(Field):
    ID = 5

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='water_density',
            field_id=self.ID,
            base_type=BaseType.FLOAT32,
            offset=0,
            scale=1,
            size=size,
            units='kg/m^3',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsPo2WarnField(Field):
    ID = 6

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='po2_warn',
            field_id=self.ID,
            base_type=BaseType.UINT8,
            offset=0,
            scale=100,
            size=size,
            units='percent',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsPo2CriticalField(Field):
    ID = 7

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='po2_critical',
            field_id=self.ID,
            base_type=BaseType.UINT8,
            offset=0,
            scale=100,
            size=size,
            units='percent',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsPo2DecoField(Field):
    ID = 8

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='po2_deco',
            field_id=self.ID,
            base_type=BaseType.UINT8,
            offset=0,
            scale=100,
            size=size,
            units='percent',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsSafetyStopEnabledField(Field):
    ID = 9

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='safety_stop_enabled',
            field_id=self.ID,
            base_type=BaseType.UINT8,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsBottomDepthField(Field):
    ID = 10

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='bottom_depth',
            field_id=self.ID,
            base_type=BaseType.FLOAT32,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsBottomTimeField(Field):
    ID = 11

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='bottom_time',
            field_id=self.ID,
            base_type=BaseType.UINT32,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsApneaCountdownEnabledField(Field):
    ID = 12

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='apnea_countdown_enabled',
            field_id=self.ID,
            base_type=BaseType.UINT8,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsApneaCountdownTimeField(Field):
    ID = 13

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='apnea_countdown_time',
            field_id=self.ID,
            base_type=BaseType.UINT32,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsBacklightModeField(Field):
    ID = 14

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='backlight_mode',
            field_id=self.ID,
            base_type=BaseType.ENUM,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsBacklightBrightnessField(Field):
    ID = 15

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='backlight_brightness',
            field_id=self.ID,
            base_type=BaseType.UINT8,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsBacklightTimeoutField(Field):
    ID = 16

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='backlight_timeout',
            field_id=self.ID,
            base_type=BaseType.UINT8,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsRepeatDiveIntervalField(Field):
    ID = 17

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='repeat_dive_interval',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=1,
            size=size,
            units='s',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsSafetyStopTimeField(Field):
    ID = 18

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='safety_stop_time',
            field_id=self.ID,
            base_type=BaseType.UINT16,
            offset=0,
            scale=1,
            size=size,
            units='s',
            type_name='',
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsHeartRateSourceTypeField(Field):
    ID = 19

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='heart_rate_source_type',
            field_id=self.ID,
            base_type=BaseType.ENUM,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
            ]
        )


class DiveSettingsHeartRateSourceField(Field):
    ID = 20

    def __init__(self, size: int = 0, growable: bool = True):
        super().__init__(
            name='heart_rate_source',
            field_id=self.ID,
            base_type=BaseType.UINT8,
            offset=0,
            scale=1,
            size=size,
            growable=growable,
            sub_fields=[
                SubField(
                    name='heart_rate_antplus_device_type',
                    base_type=BaseType.UINT8,
                    scale=1,
                    offset=0,
                    reference_map={
                        DiveSettingsHeartRateSourceTypeField.ID: [1]
                    }),
                SubField(
                    name='heart_rate_local_device_type',
                    base_type=BaseType.UINT8,
                    scale=1,
                    offset=0,
                    reference_map={
                        DiveSettingsHeartRateSourceTypeField.ID: [5]
                    })
            ]
        )
