#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : context_block
# @Date : 2021-12-31-09-44
# @Project: content-service-chat-assistant


from typing import Optional
from .components import (
    Formatter,
    ImageElement,
    TextObject,
    LayoutBlockAttributesCheckers,
    LayoutBlockAttributeConstructor
)


class ContextBlock:
    def __init__(self, block_id: Optional[str] = None):
        self.type = "context"
        if block_id is not None:
            self.edit_block_id(block_id)

    def edit_block_id(self, block_id):
        constructor = LayoutBlockAttributeConstructor(self)
        constructor.edit_block_id(block_id)

    def _fetch_or_create_elements_attribute(self):
        field_key = "elements"
        if hasattr(self, field_key) is False:
            setattr(self, field_key, [])
        field_value: list = getattr(self, field_key)

        checker = LayoutBlockAttributesCheckers()
        max_elements = 10
        checker.list_length_checker("elements", field_value, max_elements - 1)
        return field_value

    def add_text_element(self, text: str, formatter: Optional[Formatter] = None):
        """An array of text objects

        - Maximum number of items is 10.

        Args:
            text (str): The text for the block
            formatter (class): The formatting to use for this text object. Can be one of plain_text mrkdwn

        """
        field_value: list = self._fetch_or_create_elements_attribute()
        text_obj = TextObject(text=text, formatter=formatter, emoji=True)
        field_value.append(text_obj)

    def add_image_element(self, image_url: str, alt_text: str):
        """An array of image elements and text objects

        - Maximum number of items is 10.

        Args:
            image_url (str): The URL of the image to be displayed.
            alt_text (str):	A plain-text summary of the image. This should not contain any markup.

        """
        field_value: list = self._fetch_or_create_elements_attribute()
        image_obj = ImageElement(image_url=image_url, alt_text=alt_text)
        field_value.append(image_obj)
