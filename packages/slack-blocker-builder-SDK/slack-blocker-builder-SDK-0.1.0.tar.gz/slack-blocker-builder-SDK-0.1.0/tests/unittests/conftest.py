#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : conftest
# @Date : 2022-01-26-17-04
# @Project: content-service-chat-assistant

import pytest
from random import Random
from slack_block_builder import (
    OptionObject,
    ConfirmationDialogObject,
    OptionGroupObject
)


@pytest.fixture(scope='function')
def generate_str(request):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(request.param):
        str += chars[random.randint(0, length)]
    return str


@pytest.fixture(scope='function')
def generate_optional_object(request):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    options = []
    for i in range(request.param):
        text = chars[random.randint(0, length)]
        value = text.upper()
        options.append(OptionObject(text, value))

    return options


@pytest.fixture(scope="function")
def generate_option_groups_object(request):
    option_groups = []
    for ii in range(request.param):
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        random = Random()
        options = []
        for i in range(5):
            text = chars[random.randint(0, length)]
            value = text.upper()
            options.append(OptionObject(text, value))

        text = chars[random.randint(0, length)]
        option_groups.append(OptionGroupObject(label=text, options=options))

    return option_groups


@pytest.fixture(scope="function")
def generate_confirm_obj():
    confirm = ConfirmationDialogObject(
        title="Title",
        text="Testing Confirm Info",
        confirm="Submit",
        deny="Cancel"
    )
    return confirm
