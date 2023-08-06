#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : __init__.py
# @Date : 2021-12-31-09-54
# @Project: content-service-chat-assistant

from typing import Optional
from .block_element import (
    ButtonElement,
    CheckBoxElement,
    DatePickerElement,
    ImageElement,
    StaticSelectMenuElement,
    StaticMultiSelectMenuElement,
    ExternalDataSourceSelectMenuElement,
    ExternalDataSourceMultiSelectMenuElement,
    UserListMultiSelectMenuElement,
    UserListSelectMenuElement,
    ConversationsListMultiSelectMenuElement,
    ConversationsListSelectMenuElement,
    PublicChannelListSelectMenuElement,
    PublicChannelListMultiSelectMenuElement,
    OverflowMenuElement,
    PlainTextInputElement,
    RadioButtonGroupElement,
    TimePickerElement,
    BlockElementAttributeCheckers,
    BlockElementAttributeConstructor
)
from .composition_block import (
    TextObject,
    ConfirmationDialogObject,
    OptionObject,
    OptionGroupObject,
    FilterObject,
    DispatchActionConfigurationObject,
)
from .formatter import Formatter
from .style import ColorScheme
from .surface import SurfaceBlocks


class LayoutBlockAttributesCheckers(BlockElementAttributeCheckers):
    def block_id_checker(self, block_id: str):
        self.string_length_checker("block_id", block_id, 255)


class LayoutBlockAttributeConstructor(BlockElementAttributeConstructor):
    def __init__(self, block_obj: object, **kwargs):
        super().__init__(block_obj, **kwargs)
        self._checker = LayoutBlockAttributesCheckers()

    def edit_block_id(self, block_id: str):
        self._checker.block_id_checker(block_id)
        self._set_attribute("block_id", block_id)

    def edit_input_block_hint(self, hint: str):
        self._checker.string_length_checker("hint", hint, 2000)
        self._set_attribute("hint", TextObject(hint))

    def edit_input_block_dispatch_action(self, dispatch_action: bool):
        self._checker.type_checker("dispatch_action", dispatch_action, bool)
        self._set_attribute("dispatch_action", dispatch_action)

    def edit_input_block_optional(self, optional: bool):
        self._checker.type_checker("optional", optional, bool)
        self._set_attribute("optional", optional)


__all__ = (
    "ButtonElement",
    "CheckBoxElement",
    "DatePickerElement",
    "ImageElement",
    "StaticSelectMenuElement",
    "StaticMultiSelectMenuElement",
    "ExternalDataSourceSelectMenuElement",
    "ExternalDataSourceMultiSelectMenuElement",
    "UserListMultiSelectMenuElement",
    "UserListSelectMenuElement",
    "ConversationsListMultiSelectMenuElement",
    "ConversationsListSelectMenuElement",
    "PublicChannelListSelectMenuElement",
    "PublicChannelListMultiSelectMenuElement",
    "OverflowMenuElement",
    "PlainTextInputElement",
    "RadioButtonGroupElement",
    "TimePickerElement",
    "TextObject",
    "ConfirmationDialogObject",
    "OptionObject",
    "OptionGroupObject",
    "FilterObject",
    "DispatchActionConfigurationObject",
    "Formatter",
    "ColorScheme",
    "SurfaceBlocks",
    "LayoutBlockAttributesCheckers",
    "LayoutBlockAttributeConstructor"
)