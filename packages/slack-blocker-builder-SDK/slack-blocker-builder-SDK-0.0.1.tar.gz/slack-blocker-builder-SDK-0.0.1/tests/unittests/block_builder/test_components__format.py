#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : test_compoents__format
# @Date : 2022-01-27-16-06
# @Project: content-service-chat-assistant

import pytest
from slack_block_builder.components.formatter import Formatter


class TestFormatter:
    @pytest.mark.parametrize("formatter", [("PlainText", "plain_text"), ('MarkDown', "mrkdwn")])
    def test__ut__formatter(self, formatter):
        _formatter = getattr(Formatter, formatter[0])
        assert _formatter.value == formatter[1]
