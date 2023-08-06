#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : input
# @Date : 2021-12-30-21-15
# @Project: content-service-chat-assistant

from typing import Optional
from .components import LayoutBlockAttributeConstructor
from .exception import BlockTypeError
from .components import block_element as BlockElements


def input_element_checker(value: object):
    _class_name = value.__class__.__name__
    deny_list = (
        BlockElements.OverflowMenuElement,
        BlockElements.ButtonElement
    )
    if hasattr(BlockElements, _class_name) is False or isinstance(value, deny_list):
        raise BlockTypeError(f"The type for the element in this field support all block element class(except button & overflow), now got invalid class {_class_name}")


class InputBlock:
    """
    A block that collects information from users - it can hold:

    - a plain-text input element
    - a checkbox element
    - a radio button element
    - a select menu element
    - a multi-select menu element
    - a datepicker.
    """
    def __init__(self,
                 label: str,
                 element: object,
                 dispatch_action: Optional[bool] = None,
                 block_id: Optional[str] = None,
                 hint: Optional[str] = None,
                 optional: Optional[bool] = None):
        """A block that collects information from users

        Args:
            label (str): A label that appears above an input element in the form of a text object
            element (class): An plain-text input element, a checkbox element, a radio button element, a select menu element, a multi-select menu element, or a datepicker.
            dispatch_action (bool): A boolean that indicates whether or not the use of elements in this block should dispatch a block_actions payload
            block_id (str): A string acting as a unique identifier for a block
            hint (str): An optional hint that appears below an input element in a lighter grey
            optional (bool): A boolean that indicates whether the input element may be empty when a user submits the modal
        """
        self.type = "input"
        self.edit_label(label)
        self.edit_element(element)
        if dispatch_action is not None:
            self.edit_dispatch_action(dispatch_action)
        if block_id is not None:
            self.edit_block_id(block_id)
        if hint is not None:
            self.edit_hint(hint)
        if optional is not None:
            self.edit_optional(optional)

    def edit_element(self, element: object):
        input_element_checker(element)
        setattr(self, 'element', element)

    def edit_hint(self, hint: str):
        constructor = LayoutBlockAttributeConstructor(self)
        constructor.edit_input_block_hint(hint)

    def edit_label(self, label: str):
        constructor = LayoutBlockAttributeConstructor(self, label_max=2000)
        constructor.edit_label(label)

    def edit_block_id(self, block_id: str):
        constructor = LayoutBlockAttributeConstructor(self)
        constructor.edit_block_id(block_id)

    def edit_dispatch_action(self, dispatch_action: bool):
        constructor = LayoutBlockAttributeConstructor(self)
        constructor.edit_input_block_dispatch_action(dispatch_action)

    def edit_optional(self, optional: bool):
        constructor = LayoutBlockAttributeConstructor(self)
        constructor.edit_input_block_optional(optional)
