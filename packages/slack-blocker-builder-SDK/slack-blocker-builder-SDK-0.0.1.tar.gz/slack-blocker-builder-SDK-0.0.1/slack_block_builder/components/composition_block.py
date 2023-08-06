#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : text
# @Date : 2021-12-29-20-52
# @Project: content-service-chat-assistant
from .formatter import Formatter
from .style import ColorScheme
from typing import Optional, List, Any
from ..exception import (
    BlockElementOutOfRangeError,
    BlockTypeError,
    BlockMinimumOneElementError
)


class BlockAttributesCheckers:
    @staticmethod
    def max_length_checker(name: str, value: str, length: int):
        if len(value) > length:
            raise BlockElementOutOfRangeError(
                f"Maximum length for the {name} in this field is {str(length)} characters.")

    @staticmethod
    def min_length_checker(name: str, value: str, length: int):
        if len(value) < length:
            raise BlockMinimumOneElementError(
                f"Minimum length for the {name} in this field at least has {str(length)} item/characters")

    @staticmethod
    def type_checker(name: str, value: Any, expected_type: object):
        if not isinstance(value, expected_type):
            element_type_name = expected_type.__class__.__name__
            raise BlockTypeError(f"Type of {name} in this field should be {element_type_name}, got {type(value)}")

    def string_length_checker(self, name: str, value: str, maximum: int, minimum: int = 0):
        self.type_checker(name, value, str)
        self.max_length_checker(name, value, maximum)
        self.min_length_checker(name, value, minimum)

    def list_length_checker(self, name: str, value: list, maximum: int, minimum: int = 0):
        self.type_checker(name, value, list)
        self.max_length_checker(name, value, maximum)
        self.min_length_checker(name, value, minimum)

    def style_checker(self, style: Any):
        self.type_checker("style", style, ColorScheme)

    def format_checker(self, formatter: Any):
        self.type_checker("formatter", formatter, Formatter)

    def option_obj_checker(self, option: Any):
        self.type_checker("option", option, OptionObject)

    def option_group_obj_checker(self, option_group: Any):
        self.type_checker("option_group", option_group, OptionGroupObject)

    def options_list_checker(self, name: str, options: list, maximum: int = 50, minimum: int = 1):
        self.list_length_checker(name, options, maximum, minimum)
        for index, option in enumerate(options):
            try:
                self.option_obj_checker(option)
            except BlockTypeError as error:
                raise BlockTypeError(f"index {index} of options type invalid") from error

    def option_groups_checker(self, name: str, option_groups: list, maximum: int = 100):
        self.list_length_checker(name, option_groups, maximum, 1)
        for index, group in enumerate(option_groups):
            try:
                self.option_group_obj_checker(group)
            except BlockTypeError as error:
                raise BlockTypeError(f"index {index} of option groups type invalid") from error

    def list_string_checker(self, name: str, str_list: list, maximum: int = None, minimum: int = None):
        self.type_checker(name, str_list, list)
        if maximum is not None:
            self.max_length_checker(name, str_list, maximum)
        if minimum is not None:
            self.min_length_checker(name, str_list, minimum)
        for index, element in enumerate(str_list):
            try:
                self.type_checker(f"{name}-element", element, str)
            except BlockTypeError as error:
                raise BlockTypeError(f"index {index} of option groups type invalid") from error


class BlockAttributesConstructor:
    def __init__(self, block_obj: object, **kwargs):
        self._object = block_obj
        self._checker = BlockAttributesCheckers()
        self._kwargs: dict = kwargs

    def _set_attribute(self, name: str, value: Any, instance: Optional[object] = None):
        if instance is None:
            instance = self._object
        setattr(instance, name, value)

    def _del_attribute(self, name: str, instance: Optional[object] = None):
        if instance is None:
            instance = self._object
        delattr(instance, name)

    def _get_attribute(self, name: str, instance: Optional[object] = None) -> Optional[Any]:
        if instance is None:
            instance = self._object
        return getattr(instance, name, None)

    def edit_textobj_text(self, text: str):
        self._checker.type_checker("text", text, str)
        self._set_attribute("text", text)

    def edit_textobj_formatter(self, formatter: Formatter):
        self._checker.format_checker(formatter)
        self._set_attribute("type", formatter.value)
        if formatter == Formatter.MarkDown and self._get_attribute("emoji") is not None:
            self._del_attribute("emoji")
        elif formatter == Formatter.PlainText and self._get_attribute("verbatim") is not None:
            self._del_attribute("verbatim")

    def edit_textobj_emoji(self, emoji: bool):
        if self._object.type == Formatter.PlainText.value:
            self._checker.type_checker("emoji", emoji, bool)
            self._set_attribute("emoji", emoji)

    def edit_textobj_verbatim(self, verbatim: bool):
        if self._object.type == Formatter.MarkDown.value:
            self._checker.type_checker("verbatim", verbatim, bool)
            self._set_attribute("verbatim", verbatim)

    def edit_title(self, title: str):
        self._checker.string_length_checker("title", title, self._kwargs.get("title_max", 100))
        self._set_attribute("title", TextObject(title))

    def edit_text(self, text: str, formatter: Formatter = Formatter.PlainText, emoji: Optional[bool] = None):
        self._checker.string_length_checker("text", text, self._kwargs.get("text_max", 300))
        self._set_attribute("text", TextObject(text, formatter=formatter, emoji=emoji))

    def edit_confirm(self, confirm):
        self._checker.string_length_checker("confirm", confirm, 30)
        self._set_attribute('confirm', TextObject(confirm, formatter=Formatter.PlainText))

    def edit_deny(self, deny):
        self._checker.string_length_checker("deny", deny, 30)
        self._set_attribute('deny', TextObject(deny, formatter=Formatter.PlainText))

    def edit_style(self, style: ColorScheme):
        self._checker.style_checker(style)
        self._set_attribute("style", style.value)

    def edit_value(self, value: str):
        self._checker.string_length_checker("value", value, self._kwargs.get("value_max", 75))
        self._set_attribute("value", value)

    def edit_description(self, description: str):
        self._checker.string_length_checker("description", description, 75)
        self._set_attribute("description", TextObject(description))

    def edit_url(self, url):
        self._checker.string_length_checker("url", url, 3000)
        self._set_attribute("url", url)

    def edit_label(self, label: str):
        self._checker.string_length_checker("label", label, self._kwargs.get("label_max", 75))
        self._set_attribute("label", TextObject(label))

    def edit_options(self, options):
        self._checker.options_list_checker("options",
                                           options,
                                           self._kwargs.get("options_max", 100),
                                           self._kwargs.get("options_min", 1))
        self._set_attribute("options", options)

    def edit_include(self, include: List[str]):
        self._checker.list_string_checker("include", include)
        self._set_attribute("include", include)

    def edit_exclude_external_shared_channels(self, exclude_external_shared_channels: bool):
        self._checker.type_checker("exclude_external_shared_channels", exclude_external_shared_channels, bool)
        self._set_attribute("exclude_external_shared_channels", exclude_external_shared_channels)

    def edit_exclude_bot_users(self, exclude_bot_users: bool):
        self._checker.type_checker("exclude_bot_users", exclude_bot_users, bool)
        self._set_attribute("exclude_bot_users", exclude_bot_users)

    def edit_trigger_actions_on(self, trigger_actions_on: List[str]):
        self._checker.list_string_checker("trigger_actions_on", trigger_actions_on)
        self._set_attribute("trigger_actions_on", trigger_actions_on)


def max_length_checker(name: str, value: str, length: int):
    if len(value) > length:
        raise BlockElementOutOfRangeError(f"Maximum length for the {name} in this field is {str(length)} characters.")


def min_length_checker(name: str, value: str, length: int):
    if len(value) < length:
        raise BlockMinimumOneElementError(f"Minimum length for the {name} in this field at least has {str(length)} item/characters")


def type_checker(name: str, value: Any, expected_type: object):
    if isinstance(value, expected_type) is False:
        element_type_name = expected_type.__class__.__name__
        raise BlockTypeError(f"Type of {name} in this field should be {element_type_name}, got {type(value)}")


def options_list_checker(name: str, options: list, maximum: int = 50, minimum: int = 1):
    max_length_checker(name, options, maximum)
    min_length_checker(name, options, minimum)
    for index, option in enumerate(options):
        try:
            type_checker(name, option, OptionObject)
        except BlockTypeError as error:
            raise BlockTypeError(f"index {index} of options type invalid") from error


def option_groups_checker(name: str, option_groups: list, maximum: int = 100):
    max_length_checker(name, option_groups, maximum)
    min_length_checker(name, option_groups, 1)
    for index, group in enumerate(option_groups):
        try:
            type_checker(name, group, OptionGroupObject)
        except BlockTypeError as error:
            raise BlockTypeError(f"index {index} of option groups type invalid") from error


def url_checker(value: str):
    max_length_checker("url", value, 3000)


def style_checker(style: Any):
    type_checker("style", style, ColorScheme)


class TextObject:
    def __init__(self,
                 text: str,
                 formatter: Formatter = Formatter.PlainText,
                 emoji: Optional[bool] = None,
                 verbatim: Optional[bool] = None
                 ):
        """An object containing some text

        Args:
            text (str): The text for the block
            formatter (class): The formatting to use for this text object. Can be one of plain_text mrkdwn
            emoji (bool): Indicates whether emojis in a text field should be escaped into the colon emoji format.
                          default: True
            verbatim (bool): When set to false (as is default) URLs will be auto-converted into links.

        Returns:
            dict: text object
        """
        constructor = BlockAttributesConstructor(self)
        constructor.edit_textobj_text(text)
        if formatter is None:
            formatter = Formatter.PlainText
        constructor.edit_textobj_formatter(formatter)
        if emoji is not None:
            constructor.edit_textobj_emoji(emoji)
        if verbatim is not None:
            constructor.edit_textobj_verbatim(verbatim)


class ConfirmationDialogObject:
    def __init__(self,
                 title: str,
                 text: str,
                 confirm: str,
                 deny: str,
                 text_format: Formatter = Formatter.PlainText,
                 style: Optional[ColorScheme] = None):
        """An object that defines a dialog that provides a confirmation step to any interactive element.
        This dialog will ask the user to confirm their action by offering a confirm and deny buttons.

        Args:
            title (str): A plain_text-only text that defines the dialog's title
            text (str): A text that defines the explanatory text that appears in the confirm dialog
            confirm (str): A plain_text-only text to define the text of the button that confirms the action
            deny (str): A plain_text-only text to define the text of the button that cancels the action
            text_format (str): The formatting to use for this text parameter. Can be one of plain_text mrkdwn

        Returns:
            dict: dialog object
        """
        constructor = BlockAttributesConstructor(self)
        constructor.edit_title(title)
        constructor.edit_text(text, text_format)
        constructor.edit_confirm(confirm)
        constructor.edit_deny(deny)
        if style is not None:
            constructor.edit_style(style)


class OptionObject:
    def __init__(self,
                 text: str,
                 value: str,
                 description: Optional[str] = None,
                 url: Optional[str] = None,
                 text_format: Formatter = Formatter.PlainText):
        """An object that represents a single selectable item in
            - select menu
            - multi-select menu
            - checkbox group
            - radio button group
            - overflow menu.

        Args:
            text (str): A text that defines the text shown in the option on the menu.
                        Overflow, select, and multi-select menus can only use plain_text objects,
                        while radio buttons and checkboxes can use mrkdwn text objects.
            value (str): A unique string value that will be passed to your app when this option is chosen
            description (str): A plain_text only text that defines a line of descriptive text shown below the text field beside the radio button
            url (str): A URL to load in the user's browser when the option is clicked
                       The url attribute is only available in overflow menus.

        Returns:
            dict: option object
        """
        constructor = BlockAttributesConstructor(self, text_max=75)
        constructor.edit_text(text, text_format)
        constructor.edit_value(value)
        if description is not None:
            constructor.edit_description(description)
        if url is not None:
            constructor.edit_url(url)


class OptionGroupObject:
    def __init__(self, label: str, options: List[OptionObject]):
        """Provides a way to group options in
            - select menu
            - multi-select menu.

        Args:
            label (str): A plain_text only text that defines the label shown above this group of options
            options (list): An array of option objects that belong to this specific group. Maximum of 100 items.

        Returns:
            dict: option group object
        """
        constructor = BlockAttributesConstructor(self, text_max=75)
        constructor.edit_label(label)
        constructor.edit_options(options)


class FilterObject:
    def __init__(self,
                 include: Optional[List[str]] = None,
                 exclude_external_shared_channels: Optional[bool] = None,
                 exclude_bot_users: Optional[bool] = None):
        """Provides a way to filter the list of options in a conversations select menu or conversations multi-select menu

        Args:
            include (list): Indicates which type of conversations should be included in the list
                            You should provide an array of strings from the following options: im, mpim, private, and public
            exclude_external_shared_channels (bool): Indicates whether to exclude external shared channels from conversation lists
            exclude_bot_users (bool): Indicates whether to exclude bot users from conversation lists
        """
        constructor = BlockAttributesConstructor(self, text_max=75)
        if include is not None:
            constructor.edit_include(include)
        if exclude_external_shared_channels is not None:
            constructor.edit_exclude_external_shared_channels(exclude_external_shared_channels)
        if exclude_bot_users is not None:
            constructor.edit_exclude_external_shared_channels(exclude_bot_users)


class DispatchActionConfigurationObject:
    def __init__(self, trigger_actions_on: List[str]):
        """Determines when a plain-text input element will return a block_actions interaction payload.

        Args:
            trigger_actions_on (list): An array of interaction types that you would like to receive a block_actions payload for.
                                       Should be one or both of:

                                            on_enter_pressed — payload is dispatched when user presses the enter key while the input is in focus.
                                                               Hint text will appear underneath the input explaining to the user to press enter to submit.

                                            on_character_entered — payload is dispatched when a character is entered (or removed) in the input.
        """
        constructor = BlockAttributesConstructor(self, text_max=75)
        constructor.edit_trigger_actions_on(trigger_actions_on)


