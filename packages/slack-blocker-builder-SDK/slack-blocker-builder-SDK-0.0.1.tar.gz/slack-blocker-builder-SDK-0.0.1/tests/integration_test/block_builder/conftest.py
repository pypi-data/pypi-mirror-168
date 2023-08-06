#-*- coding: utf-8 -*-
# @Filename : conftest
# @Date : 2022-03-08-14-08
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

