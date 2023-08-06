# -*- coding: utf-8 -*-
# @Filename : conftest
# @Date : 2022-03-09-10-47
# @Project: content-service-chat-assistant

import pytest
import os
import json


@pytest.fixture(scope="function")
def test_data_dir():
    workdir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(workdir, "data")


@pytest.fixture(scope="function")
def load_test_json_data(request, test_data_dir):
    data_name = request.param
    data_path = os.path.join(test_data_dir, data_name)
    with open(data_path, "r") as fb:
        json_data = json.load(fb)
    return json_data


@pytest.fixture(scope="function")
def action_button_data():
    data = {
        "type": "button",
        "block_id": "Jz4NQ",
        "action_id": "21Q",
        "text": {
            "type": "plain_text",
            "text": "Approve",
            "emoji": True
        },
        "value": "click_me_123",
        "style": "primary",
        "action_ts": "1646803670.728532"
    }
    return data


@pytest.fixture(scope="function")
def action_plain_text_input_data():
    data = {
        "type": "plain_text_input",
        "block_id": "OLH",
        "action_id": "plain_text_input-action",
        "value": "212",
        "action_ts": "1646803972.772286"
    }
    return data


@pytest.fixture(scope="function")
def action_checkbox_data():
    data = {
        "type": "checkboxes",
        "block_id": "F2N",
        "action_id": "actionId-0",
        "selected_options": [
            {
                "text": {
                    "type": "plain_text",
                    "text": "*this is plain_text text*",
                    "emoji": True
                },
                "value": "value-1",
                "description": {
                    "type": "plain_text",
                    "text": "*this is plain_text text*",
                    "emoji": True
                }
            },
            {
                "text": {
                    "type": "plain_text",
                    "text": "*this is plain_text text*",
                    "emoji": True
                },
                "value": "value-0",
                "description": {
                    "type": "plain_text",
                    "text": "*this is plain_text text*",
                    "emoji": True
                }
            }
        ],
        "action_ts": "1646804012.621399"
    }
    return data


@pytest.fixture(scope="function")
def action_overflow_data():
    data = {
        "type": "overflow",
        "block_id": "mGK",
        "action_id": "overflow-action",
        "selected_option": {
            "text": {
                "type": "plain_text",
                "text": "*this is plain_text text*",
                "emoji": True
            },
            "value": "value-1"
        },
        "action_ts": "1646804448.785760"
    }
    return data


@pytest.fixture(scope="function")
def action_radio_button_data():
    data = {
        "type": "radio_buttons",
        "block_id": "1JQd",
        "action_id": "actionId-0",
        "selected_option": {
            "text": {
                "type": "plain_text",
                "text": "*this is plain_text text*",
                "emoji": True
            },
            "value": "value-0"
        },
        "action_ts": "1646804507.661191"
    }
    return data


@pytest.fixture(scope="function")
def action_datepicker_data():
    data = {
        "type": "datepicker",
        "block_id": "SI7I",
        "action_id": "actionId-0",
        "selected_date": "1990-04-06",
        "initial_date": "1990-04-28",
        "action_ts": "1646804596.982841"
    }
    return data


@pytest.fixture(scope="function")
def action_timepicker_data():
    data = {
        "type": "timepicker",
        "block_id": "IibT",
        "action_id": "actionId-0",
        "selected_time": "04:00",
        "initial_time": "13:37",
        "action_ts": "1646804660.329374"
    }
    return data


@pytest.fixture(scope="function")
def action_static_select_data():
    data = {
        "type": "static_select",
        "block_id": "PB/Zh",
        "action_id": "actionId-3",
        "selected_option": {
            "text": {
                "type": "plain_text",
                "text": "*this is plain_text text*",
                "emoji": True
            },
            "value": "value-2"
        },
        "placeholder": {
            "type": "plain_text",
            "text": "Select an item",
            "emoji": True
        },
        "action_ts": "1646804693.021166"
    }
    return data


@pytest.fixture(scope="function")
def action_multi_static_select_data():
    data = {
        "type": "multi_static_select",
        "block_id": "VSeb9",
        "action_id": "multi_static_select-action",
        "selected_options": [
            {
                "text": {
                    "type": "plain_text",
                    "text": "*this is plain_text text*",
                    "emoji": True
                },
                "value": "value-2"
            },
            {
                "text": {
                    "type": "plain_text",
                    "text": "*this is plain_text text*",
                    "emoji": True
                },
                "value": "value-1"
            }
        ],
        "placeholder": {
            "type": "plain_text",
            "text": "Select options",
            "emoji": True
        },
        "action_ts": "1646805007.926877"
    }
    return data


@pytest.fixture(scope="function")
def action_users_select_data():
    data = {
        "type": "users_select",
        "block_id": "PB/Zh",
        "action_id": "actionId-2",
        "selected_user": "WBTHD9DCZ",
        "action_ts": "1646804760.094416"
    }
    return data


@pytest.fixture(scope="function")
def action_multi_users_select_data():
    data = {
        "type": "multi_users_select",
        "block_id": "llh5",
        "action_id": "multi_users_select-action",
        "selected_users": [
            "W01AG1MNWHW",
            "WBTHD9DCZ"
        ],
        "action_ts": "1646804949.445608"
    }
    return data


@pytest.fixture(scope="function")
def action_conversations_select_data():
    data = {
        "type": "conversations_select",
        "block_id": "PB/Zh",
        "action_id": "actionId-0",
        "selected_conversation": "CAJ680C03",
        "action_ts": "1646804797.520590"
    }
    return data


@pytest.fixture(scope="function")
def action_multi_conversations_select_data():
    data = {
        "type": "multi_conversations_select",
        "block_id": "gAC",
        "action_id": "multi_conversations_select-action",
        "selected_conversations": [
            "C01ALR6U7EW",
            "CFLE550G3"
        ],
        "action_ts": "1646805073.596717"
    }
    return data


@pytest.fixture(scope="function")
def action_channel_select_data():
    data = {
        "type": "channels_select",
        "block_id": "PB/Zh",
        "action_id": "actionId-1",
        "selected_channel": "CAAJPP7KK",
        "action_ts": "1646804825.629694"
    }
    return data


@pytest.fixture(scope="function")
def action_multi_channel_select_data():
    data = {
        "type": "multi_channels_select",
        "block_id": "jBVn",
        "action_id": "multi_static_select-action",
        "selected_channels": [
            "CFLE550G3",
            "C01ALR6U7EW"
        ],
        "action_ts": "1646805333.701460"
    }
    return data
