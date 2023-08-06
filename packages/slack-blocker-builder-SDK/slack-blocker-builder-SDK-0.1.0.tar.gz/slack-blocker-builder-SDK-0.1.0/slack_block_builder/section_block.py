#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : section
# @Date : 2021-12-30-20-00
# @Project: content-service-chat-assistant

from typing import Optional
from .exception import BlockTypeError
from .components import Formatter, TextObject, LayoutBlockAttributeConstructor, LayoutBlockAttributesCheckers
from .components import block_element as BlockElements


def section_accessory_element_type_checker(value: object):
    _class_name = value.__class__.__name__
    allow_list = (
        BlockElements.ButtonElement,
        BlockElements.OverflowMenuElement,
        BlockElements.DatePickerElement,
        BlockElements.CheckBoxElement,
        BlockElements.ImageElement,
        BlockElements.TimePickerElement,
        BlockElements.PlainTextInputElement,
        BlockElements.RadioButtonGroupElement,
        BlockElements.PublicChannelListSelectMenuElement,
        BlockElements.PublicChannelListMultiSelectMenuElement,
        BlockElements.ConversationsListSelectMenuElement,
        BlockElements.ConversationsListMultiSelectMenuElement,
        BlockElements.UserListSelectMenuElement,
        BlockElements.UserListMultiSelectMenuElement,
        BlockElements.ExternalDataSourceSelectMenuElement,
        BlockElements.ExternalDataSourceMultiSelectMenuElement,
        BlockElements.StaticSelectMenuElement,
        BlockElements.StaticMultiSelectMenuElement
    )
    if hasattr(BlockElements, _class_name) is False or isinstance(value, allow_list) is False:
        raise BlockTypeError(f"The type for the accessory in this field support all block element class, "
                             f"now got invalid class {_class_name}")


class SectionBlock:
    def __init__(self,
                 text: Optional[str] = None,
                 text_formatter: Optional[Formatter] = None,
                 block_id: Optional[str] = None):
        """A section is one of the most flexible blocks available - it can be used as a simple text block,
           in combination with text fields, or side-by-side with any of the available block elements.

        Args:
            text (str): The text for the block, in the form of a text
            text_formatter (class): Text formatter
            block_id (str): A string acting as a unique identifier for a block
        """
        self.type = "section"
        if text is not None:
            self.edit_text(text, text_formatter)
        if block_id is not None:
            self.edit_block_id(block_id)

    def edit_text(self, text: str, formatter: Optional[Formatter] = None, emoji: Optional[bool] = None):
        constructor = LayoutBlockAttributeConstructor(self, text_max=2000)
        constructor.edit_text(text=text, formatter=formatter, emoji=emoji)

    def edit_block_id(self, block_id):
        constructor = LayoutBlockAttributeConstructor(self)
        constructor.edit_block_id(block_id)

    def add_field(self, text: str, formatter: Optional[Formatter] = None):
        """Add new text objects to field array
        Any text objects included with fields will be rendered in a compact format that allows for 2 columns of side-by-side text

        - Maximum number of items is 10.
        - Maximum length for the text in each item is 2000 characters

        Args:
            text (str): The text for the block
            formatter (class): The formatting to use for this text object. Can be one of plain_text mrkdwn

        """
        _checker = LayoutBlockAttributesCheckers()
        _checker.string_length_checker("text", text, 2000)
        if formatter is not None:
            _checker.format_checker(formatter)
        field_key = "fields"
        if hasattr(self, field_key) is False:
            setattr(self, field_key, [])
        field_value: list = getattr(self, field_key)
        _checker.list_length_checker(field_key, field_value, 10 - 1)
        text_obj = TextObject(text=text, formatter=formatter)
        field_value.append(text_obj)

    def edit_accessory(self, block_element: object):
        """Edit section's accessory

        Args:
            block_element (class): one of the available element objects
        """
        section_accessory_element_type_checker(block_element)
        setattr(self, "accessory", block_element)




