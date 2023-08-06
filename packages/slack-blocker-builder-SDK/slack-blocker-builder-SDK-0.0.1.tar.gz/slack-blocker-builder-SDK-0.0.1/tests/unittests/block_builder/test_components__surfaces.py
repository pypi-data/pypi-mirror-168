#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : test_components__surfaces
# @Date : 2022-01-27-16-08
# @Project: content-service-chat-assistant

import pytest
from slack_block_builder.components.surface import SurfaceBlocks


class TestFormatter:
    @pytest.mark.parametrize("surface", [
        ("message", "Message"),
        ('home_tabs', "Home Tabs"),
        ("modals", "Modals")
    ])
    def test__ut__surface(self, surface):
        _surface = getattr(SurfaceBlocks, surface[0])
        assert _surface.value == surface[1]
