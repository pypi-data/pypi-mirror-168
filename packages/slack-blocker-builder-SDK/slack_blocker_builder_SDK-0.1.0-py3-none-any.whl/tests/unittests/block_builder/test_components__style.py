#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : test_compoents__style
# @Date : 2022-01-27-15-56
# @Project: content-service-chat-assistant

import pytest
from slack_block_builder.components.style import ColorScheme


class TestColorScheme:
    @pytest.mark.parametrize("color", ["Primary", "Default", "Danger"])
    def test__ut__colors(self, color):
        _color = getattr(ColorScheme, color)
        assert _color.value == color.lower()

