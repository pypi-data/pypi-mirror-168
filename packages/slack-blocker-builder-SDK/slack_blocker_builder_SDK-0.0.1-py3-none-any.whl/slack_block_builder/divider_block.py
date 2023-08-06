#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : divider_block
# @Date : 2021-12-31-09-36
# @Project: content-service-chat-assistant

from typing import Optional
from .components import LayoutBlockAttributeConstructor


class DividerHeader:
    def __init__(self, block_id: Optional[str] = None):
        self.type = "divider"
        if block_id is not None:
            self.edit_block_id(block_id)

    def edit_block_id(self, block_id):
        constructor = LayoutBlockAttributeConstructor(self)
        constructor.edit_block_id(block_id)
