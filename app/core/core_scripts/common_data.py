from typing import List, Tuple

from app.core.core_scripts.choices import Choices


class CommonData:

    @classmethod
    def choice_to_dict(cls, choices: List[Tuple[int, str]]) -> List[dict]:
        choices_list = []
        for choice_key, choice_label in choices:
            choices_list.append({'key': choice_key, 'label': choice_label})
        return choices_list

    COMMON_DATA = {
        'device_type_choices': {
            'data_type': 'choice',
            'data': Choices.DEVICE_TYPE_CHOICES,
        },
        'device_sub_type_choices': {
            'data_type': 'choice',
            'data': Choices.DEVICE_SUB_TYPE_CHOICES,
        },
        'device_address_type_choices': {
            'data_type': 'choice',
            'data': Choices.DEVICE_ADDRESS_TYPE_CHOICES,
        },
        'forecast_units_choices': {
            'data_type': 'choice',
            'data': Choices.FORECAST_UNITS_CHOICES,
        },
    }
