#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : header_block
# @Date : 2021-12-31-09-25
# @Project: content-service-chat-assistant


from typing import Optional
from .components import LayoutBlockAttributeConstructor


class HeaderBlock:
    def __init__(self, text: str, block_id: Optional[str] = None):
        self.type = 'header'
        self.edit_text(text)
        if block_id is not None:
            self.edit_block_id(block_id)

    def edit_text(self, text: str):
        constructor = LayoutBlockAttributeConstructor(self, text_max=150)
        constructor.edit_text(text)

    def edit_block_id(self, block_id):
        constructor = LayoutBlockAttributeConstructor(self)
        constructor.edit_block_id(block_id)



