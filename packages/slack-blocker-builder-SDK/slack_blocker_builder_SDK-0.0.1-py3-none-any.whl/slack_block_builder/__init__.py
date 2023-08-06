#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : __init__.py
# @Date : 2021-12-29-18-13
# @Project: content-service-chat-assistant
import json
from typing import Optional
from .components.composition_block import (
    max_length_checker,
    type_checker,
)
from .components import *
from .section_block import SectionBlock
from .action_block import ActionBlock
from .context_block import ContextBlock
from .divider_block import DividerHeader
from .header_block import HeaderBlock
from .image_block import ImageBlock
from .input_block import InputBlock
from .body_parser import (
    ActionBodyParser,
    CommandBodyParser,
    EventBodyParser,
    ViewSubmissionBodyParser,
    auto_parser
)
from .utils import obj2dict


class BlockBuilder:
    def __init__(self):
        self.blocks = []

    def to_dict(self) -> dict:
        return obj2dict(self)

    def to_json(self) -> str:
        json_object = json.dumps(self.to_dict(), indent=4)
        return json_object

    def add_section_block(self,
                          text: Optional[str] = None,
                          text_formatter: Optional[Formatter] = Formatter.PlainText,
                          block_id: Optional[str] = None):
        _section_block = SectionBlock(text=text,
                                      text_formatter=text_formatter,
                                      block_id=block_id)
        self.blocks.append(_section_block)
        return _section_block

    def add_action_block(self, block_id: Optional[str] = None):
        _action_block = ActionBlock(block_id=block_id)
        self.blocks.append(_action_block)
        return _action_block

    def add_context_block(self, block_id: Optional[str] = None):
        _context_block = ContextBlock(block_id=block_id)
        self.blocks.append(_context_block)
        return _context_block

    def add_divider_block(self, block_id: Optional[str] = None):
        _divider_block = DividerHeader(block_id=block_id)
        self.blocks.append(_divider_block)
        return _divider_block

    def add_header_block(self, text: str, block_id: Optional[str] = None):
        _header_block = HeaderBlock(text=text, block_id=block_id)
        self.blocks.append(_header_block)
        return _header_block

    def add_image_block(self,
                        image_url: str,
                        alt_text: str,
                        title: Optional[str] = None,
                        block_id: Optional[str] = None):
        _image_block = ImageBlock(image_url=image_url,
                                  alt_text=alt_text,
                                  title=title,
                                  block_id=block_id)
        self.blocks.append(_image_block)
        return _image_block

    def add_input_block(self,
                        label: str,
                        element: object,
                        dispatch_action: Optional[bool] = None,
                        block_id: Optional[str] = None,
                        hint: Optional[str] = None,
                        optional: Optional[bool] = None):
        _input_block = InputBlock(label=label,
                                  element=element,
                                  dispatch_action=dispatch_action,
                                  block_id=block_id,
                                  hint=hint,
                                  optional=optional)
        self.blocks.append(_input_block)
        return _input_block


class ModalBuilder(BlockBuilder):
    def __init__(self,
                 title: str,
                 submit: str,
                 close: str,
                 callback_id: Optional[str] = None):

        self.type = "modal"
        self.edit_title(title)
        self.edit_submit(submit)
        self.edit_close(close)
        if callback_id is not None:
            self.edit_callback_id(callback_id)
        super().__init__()

    def edit_title(self, title):
        _checker = LayoutBlockAttributesCheckers()
        _checker.string_length_checker("title", title, 24)
        setattr(self, "title", TextObject(text=title, formatter=Formatter.PlainText, emoji=True))

    def edit_submit(self, submit):
        _checker = LayoutBlockAttributesCheckers()
        _checker.string_length_checker("submit", submit, 24)
        setattr(self, "submit", TextObject(text=submit, formatter=Formatter.PlainText, emoji=True))

    def edit_close(self, close):
        _checker = LayoutBlockAttributesCheckers()
        _checker.string_length_checker("close", close, 24)
        setattr(self, "close", TextObject(text=close, formatter=Formatter.PlainText, emoji=True))

    def edit_private_metadata(self, private_metadata: str):
        _checker = LayoutBlockAttributesCheckers()
        _checker.string_length_checker("private_metadata", private_metadata, 3000)
        setattr(self, "private_metadata", private_metadata)

    def edit_callback_id(self, callback_id: str):
        _checker = LayoutBlockAttributesCheckers()
        _checker.string_length_checker("callback_id", callback_id, 3000)
        setattr(self, "callback_id", callback_id)

    def edit_notify_on_close(self, notify_on_close: bool):
        _checker = LayoutBlockAttributesCheckers()
        _checker.type_checker("notify_on_close", notify_on_close, bool)
        setattr(self, "notify_on_close", notify_on_close)


class AppHomeBuilder(BlockBuilder):
    def __init__(self):
        super().__init__()
        self.type = "home"


__all__ = (
    "BlockBuilder",
    "ModalBuilder",
    "AppHomeBuilder",
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
    "auto_parser",
    "ActionBodyParser",
    "CommandBodyParser",
    "EventBodyParser",
    "ViewSubmissionBodyParser"
)