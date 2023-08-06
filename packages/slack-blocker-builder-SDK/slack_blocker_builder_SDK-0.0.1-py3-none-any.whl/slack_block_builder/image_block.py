#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : image_block
# @Date : 2021-12-30-21-46
# @Project: content-service-chat-assistant

from typing import Optional
from .components import ImageElement, LayoutBlockAttributeConstructor


class ImageBlock(ImageElement):
    def __init__(self,
                 image_url: str,
                 alt_text: str,
                 title: Optional[str] = None,
                 block_id: Optional[str] = None):
        super().__init__(image_url=image_url, alt_text=alt_text)
        self.type = "image"
        if title is not None:
            self.edit_title(title)
        if block_id is not None:
            self.edit_block_id(block_id)

    def edit_title(self, title: str):
        constructor = LayoutBlockAttributeConstructor(self, title_max=2000)
        constructor.edit_title(title)

    def edit_block_id(self, block_id: str):
        constructor = LayoutBlockAttributeConstructor(self)
        constructor.edit_block_id(block_id)

