#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : action_block
# @Date : 2021-12-31-10-17
# @Project: content-service-chat-assistant

from typing import Optional
from .components import LayoutBlockAttributeConstructor, LayoutBlockAttributesCheckers
from .exception import BlockTypeError
from .components import block_element as BlockElements


def action_elements_checker(value: object):
    _class_name = value.__class__.__name__
    deny_list = (
        BlockElements.CheckBoxElement,
        BlockElements.ImageElement,
        BlockElements.TimePickerElement,
        BlockElements.PlainTextInputElement,
        BlockElements.RadioButtonGroupElement,
        BlockElements.PublicChannelListMultiSelectMenuElement,
        BlockElements.ConversationsListMultiSelectMenuElement,
        BlockElements.UserListMultiSelectMenuElement,
        BlockElements.ExternalDataSourceMultiSelectMenuElement,
        BlockElements.StaticMultiSelectMenuElement
    )
    if hasattr(BlockElements, _class_name) is False or isinstance(value, deny_list):
        raise BlockTypeError(f"The type for the element in this field support buttons, select menus, "
                             f"overflow menus, or date pickers, now got invalid class {_class_name}")


class ActionBlock:
    def __init__(self, block_id: Optional[str] = None):
        self.type = "actions"
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
        max_elements = 5
        checker.list_length_checker("elements", field_value, max_elements - 1)
        return field_value

    def add_element(self, block_element: object):
        """Add new element

        Args:
            block_element (class): An array of interactive element objects - buttons, select menus, overflow menus, or date pickers
        """
        checker = LayoutBlockAttributesCheckers()
        max_elements = 5
        elements_list = self._fetch_or_create_elements_attribute()
        checker.list_length_checker("elements", elements_list, max_elements - 1)
        action_elements_checker(block_element)
        elements_list.append(block_element)

