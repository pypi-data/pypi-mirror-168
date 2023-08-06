#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : block_element
# @Date : 2021-12-29-22-06
# @Project: content-service-chat-assistant

import re
from .composition_block import (
    Optional,
    List,
    Any,
    TextObject,
    ConfirmationDialogObject,
    OptionGroupObject,
    OptionObject,
    FilterObject,
    DispatchActionConfigurationObject,
    BlockAttributesCheckers,
    BlockAttributesConstructor
)
from .style import ColorScheme
from ..exception import BlockValueError


class BlockElementAttributeCheckers(BlockAttributesCheckers):
    def action_id_checker(self, value: str):
        self.string_length_checker("action_id", value, 255)

    def confirm_check(self, confirm: Any):
        self.type_checker("confirm", confirm, ConfirmationDialogObject)

    def focus_on_load_checker(self, focus_on_load: Any):
        self.type_checker("focus_on_load", focus_on_load, bool)

    def max_selected_items_checker(self, max_selected_items: Any):
        self.type_checker("max_selected_items", max_selected_items, int)

    @staticmethod
    def date_checker(name: str, date: str):
        _compile = re.compile("^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$")
        if _compile.search(date) is None:
            raise BlockValueError(
                f"The date format of {name} in this filed invalid, should be in the format YYYY-MM-DD")

    @staticmethod
    def time_checker(name: str, date: str):
        _compile = re.compile("^[0-2][0-9]:[0-5][0-9]$")
        if _compile.search(date) is None:
            raise BlockValueError(f"The time format of {name} in this filed invalid, should be in the format HH:mm")

    def placeholder_checker(self, value: str):
        self.string_length_checker("placeholder", value, 150)

    def filter_object_check(self, value: Any):
        self.type_checker("filter", value, FilterObject)

    def dispatch_action_config_check(self, value: Any):
        self.type_checker("dispatch_action_config", value, DispatchActionConfigurationObject)


class BlockElementAttributeConstructor(BlockAttributesConstructor):
    def __init__(self, block_obj: object, **kwargs):
        super().__init__(block_obj, **kwargs)
        self._checker = BlockElementAttributeCheckers()

    def edit_action_id(self, action_id: str):
        self._checker.action_id_checker(action_id)
        self._set_attribute("action_id", action_id)

    def edit_confirm(self, confirm: ConfirmationDialogObject):
        self._checker.confirm_check(confirm)
        self._set_attribute("confirm", confirm)

    def edit_placeholder(self, placeholder: str):
        self._checker.placeholder_checker(placeholder)
        self._set_attribute("placeholder", TextObject(placeholder))

    def edit_initial_date(self, initial_date: str):
        self._checker.date_checker("initial_date", initial_date)
        self._set_attribute("initial_date", initial_date)

    def edit_focus_on_load(self, focus_on_load: bool):
        self._checker.focus_on_load_checker(focus_on_load)
        self._set_attribute("focus_on_load", focus_on_load)

    def edit_image_url(self, image_url: str):
        self._checker.string_length_checker("image_url", image_url, 3000)
        self._set_attribute("image_url", image_url)

    def edit_alt_text(self, alt_text: str):
        self._checker.string_length_checker("alt_text", alt_text, 2000)
        self._set_attribute("alt_text", alt_text)

    def edit_option_groups(self, option_groups: list):
        self._checker.option_groups_checker("option_groups", option_groups, 100)
        self._set_attribute("option_groups", option_groups)

    def edit_initial_option(self, initial_option: OptionObject):
        self._checker.option_obj_checker(initial_option)
        self._set_attribute("initial_option", initial_option)

    def edit_initial_options(self, initial_options: List[OptionObject]):
        self._checker.options_list_checker("initial_options",
                                           initial_options,
                                           self._kwargs.get("initial_options_max", 100))
        self._set_attribute("initial_options", initial_options)

    def edit_max_selected_items(self, max_selected_items: int):
        self._checker.max_selected_items_checker(max_selected_items)
        self._set_attribute("max_selected_items", max_selected_items)

    def edit_min_query_length(self, min_query_length: int):
        self._checker.type_checker("min_query_length", min_query_length, int)
        self._set_attribute("min_query_length", min_query_length)

    def edit_initial_user(self, initial_user: str):
        self._checker.string_length_checker("initial_user", initial_user, 100)
        self._set_attribute("initial_user", initial_user)

    def edit_initial_users(self, initial_users: list):
        self._checker.list_string_checker("initial_users", initial_users, 100)
        self._set_attribute("initial_users", initial_users)

    def edit_initial_conversation(self, initial_conversation: str):
        self._checker.string_length_checker("initial_conversation", initial_conversation, 100)
        self._set_attribute("initial_conversation", initial_conversation)

    def edit_initial_conversations(self, initial_conversations: list):
        self._checker.list_string_checker("initial_conversations", initial_conversations, 100)
        self._set_attribute("initial_conversations", initial_conversations)

    def edit_initial_channel(self, initial_channel: str):
        self._checker.string_length_checker("initial_channel", initial_channel, 100)
        self._set_attribute("initial_channel", initial_channel)

    def edit_initial_channels(self, initial_channels: list):
        self._checker.list_string_checker("initial_channels", initial_channels, 100)
        self._set_attribute("initial_channels", initial_channels)

    def edit_initial_value(self, initial_value: str):
        self._checker.string_length_checker("initial_value", initial_value, 1000)
        self._set_attribute("initial_value", initial_value)

    def edit_multiline(self, multiline: bool):
        self._checker.type_checker("multiline", multiline, bool)
        self._set_attribute("multiline", multiline)

    def edit_min_length(self, min_length: int):
        self._checker.type_checker("min_length", min_length, int)
        self._set_attribute("min_length", min_length)

    def edit_max_length(self, max_length: int):
        self._checker.type_checker("max_length", max_length, int)
        self._set_attribute("max_length", max_length)

    def edit_dispatch_action_config(self, dispatch_action_config: DispatchActionConfigurationObject):
        self._checker.dispatch_action_config_check(dispatch_action_config)
        self._set_attribute("dispatch_action_config", dispatch_action_config)

    def edit_default_to_current_conversation(self, default_to_current_conversation: bool):
        self._checker.type_checker("default_to_current_conversation",
                                   default_to_current_conversation,
                                   bool)
        self._set_attribute("default_to_current_conversation", default_to_current_conversation)

    def edit_filter(self, filter: FilterObject):
        self._checker.filter_object_check(filter)
        self._set_attribute("filter", filter)

    def edit_response_url_enabled(self, response_url_enabled: bool):
        self._checker.type_checker("response_url_enabled", response_url_enabled, bool)
        self._set_attribute("response_url_enabled", response_url_enabled)

    def edit_initial_time(self, initial_time: str):
        self._checker.time_checker("initial_time", initial_time)
        self._set_attribute("initial_time", initial_time)


class ButtonElement:
    def __init__(self,
                 text: str,
                 action_id: Optional[str] = None,
                 url: Optional[str] = None,
                 value: Optional[str] = None,
                 style: ColorScheme = None,
                 confirm: Optional[ConfirmationDialogObject] = None):
        """An interactive component that inserts a button

        Works with block types: Section Actions

        Args:
            text (str): A text object that defines the button's text
            action_id (str): An identifier for this action
            url (str): A URL to load in the user's browser when the button is clicked
            value (str): The value to send along with the interaction payload
            style (class): Decorates buttons with alternative visual color schemes
            confirm (class): A confirm object that defines an optional confirmation dialog after the button is clicked
        """
        self.type = "button"
        constructor = BlockElementAttributeConstructor(self, text_max=75, value_max=2000)
        constructor.edit_text(text, emoji=True)
        if action_id is not None:
            constructor.edit_action_id(action_id)
        if url is not None:
            constructor.edit_url(url)
        if value is not None:
            constructor.edit_value(value)
        if style is not None:
            constructor.edit_style(style)
        if confirm is not None:
            constructor.edit_confirm(confirm)


class CheckBoxElement:
    def __init__(self,
                 options: List[OptionObject],
                 action_id: Optional[str] = None,
                 initial_options: Optional[List[OptionObject]] = None,
                 confirm: Optional[ConfirmationDialogObject] = None,
                 focus_on_load: Optional[bool] = None):
        """A checkbox group that allows a user to choose multiple items from a list of possible options.

        Works with block types: Section Actions Input

        Args:
            action_id (str): An identifier for the action triggered when the checkbox group is changed
            options (list): An array of option objects.
                            A maximum of 10 options are allowed
            initial_options (list): An array of option objects that exactly matches one or more of the options within options
            confirm (class): A confirm object that defines an optional confirmation dialog that appears after clicking one of the checkboxes in this element.
            focus_on_load (bool): Indicates whether the element will be set to auto focus within the view object
        """
        self.type = "checkboxes"
        constructor = BlockElementAttributeConstructor(self, options_max=10, initial_options_max=10)
        constructor.edit_options(options)
        if action_id is not None:
            constructor.edit_action_id(action_id)
        if initial_options is not None:
            constructor.edit_initial_options(initial_options)
        if confirm is not None:
            constructor.edit_confirm(confirm)
        if focus_on_load is not None:
            constructor.edit_focus_on_load(focus_on_load)


class DatePickerElement:
    def __init__(self,
                 action_id: Optional[str] = None,
                 placeholder: Optional[str] = None,
                 initial_date: Optional[str] = None,
                 confirm: Optional[ConfirmationDialogObject] = None,
                 focus_on_load: Optional[bool] = None):
        """An element which lets users easily select a date from a calendar style UI

        Works with block types: Section Actions Input

        Args:
            action_id (str): An identifier for the action triggered when a menu option is selected
            placeholder (str): 	A plain_text only text that defines the placeholder text shown on the datepicker
            initial_date (str): The initial date that is selected when the element is loaded.
                                This should be in the format YYYY-MM-DD.
            confirm (class): A confirm object that defines an optional confirmation dialog that appears after a date is selected.
            focus_on_load (bool): Indicates whether the element will be set to auto focus within the view object.
        """
        self.type = "datepicker"
        constructor = BlockElementAttributeConstructor(self)
        if action_id is not None:
            constructor.edit_action_id(action_id)
        if placeholder is not None:
            constructor.edit_placeholder(placeholder)
        if initial_date is not None:
            constructor.edit_initial_date(initial_date)
        if confirm is not None:
            constructor.edit_confirm(confirm)
        if focus_on_load is not None:
            constructor.edit_focus_on_load(focus_on_load)


class ImageElement:
    def __init__(self, image_url: str, alt_text: str):
        """An element to insert an image as part of a larger block of content

        Works with block types: Section Context

        Args:
            image_url (str): The URL of the image to be displayed.
            alt_text (str):	A plain-text summary of the image. This should not contain any markup.
        """
        self.type = "image"
        constructor = BlockElementAttributeConstructor(self)
        constructor.edit_image_url(image_url)
        constructor.edit_alt_text(alt_text)


class StaticSelectMenuElement:
    def __init__(self,
                 placeholder: str,
                 action_id: Optional[str] = None,
                 options: Optional[List[OptionObject]] = None,
                 option_groups: Optional[List[OptionGroupObject]] = None,
                 initial_option: Optional[OptionObject] = None,
                 confirm: Optional[ConfirmationDialogObject] = None,
                 focus_on_load: Optional[bool] = None):
        """This is the simplest form of select menu, with a static list of options passed in when defining the element.

        Works with block types: Section Input

        Args:
            placeholder (str): A plain_text only text that defines the placeholder text shown on the menu
            action_id (str): An identifier for the action triggered when a menu option is selecte
            options (list): An array of option objects. Maximum number of options is 100.
                            If option_groups is specified, this field should not be.
            option_groups (list): An array of option group objects. Maximum number of option groups is 100.
                                  If options is specified, this field should not be.
            initial_option (object): An array of option objects that exactly match one or more of the options within options or option_groups
            confirm (class): A confirm object that defines an optional confirmation dialog that appears before the multi-select choices are submitted.
            focus_on_load (bool): Indicates whether the element will be set to auto focus within the view object
        """
        self.type = "static_select"
        constructor = BlockElementAttributeConstructor(self)
        constructor.edit_placeholder(placeholder)
        if action_id is not None:
            constructor.edit_action_id(action_id)
        if options is None and option_groups is None:
            raise BlockValueError(f"[{self.type}]Must fill up one of options/option_groups")
        if options is not None and option_groups is not None:
            raise BlockValueError(f"[{self.type}]Only select one of options/option_groups")
        if options is not None:
            constructor.edit_options(options)
        if option_groups is not None:
            constructor.edit_option_groups(option_groups)
        if initial_option is not None:
            constructor.edit_initial_option(initial_option)
        if confirm is not None:
            constructor.edit_confirm(confirm)
        if focus_on_load is not None:
            constructor.edit_focus_on_load(focus_on_load)


class StaticMultiSelectMenuElement(StaticSelectMenuElement):
    def __init__(self,
                 placeholder: str,
                 action_id: Optional[str] = None,
                 options: Optional[List[OptionObject]] = None,
                 option_groups: Optional[List[OptionGroupObject]] = None,
                 initial_options: Optional[List[OptionObject]] = None,
                 confirm: Optional[ConfirmationDialogObject] = None,
                 max_selected_items: Optional[int] = None,
                 focus_on_load: Optional[bool] = None):
        """This is the simplest form of select menu, with a static list of options passed in when defining the element.

        Works with block types: Section Input

        Args:
            placeholder (str): A plain_text only text that defines the placeholder text shown on the menu
            action_id (str): An identifier for the action triggered when a menu option is selecte
            options (list): An array of option objects. Maximum number of options is 100.
                            If option_groups is specified, this field should not be.
            option_groups (list): An array of option group objects. Maximum number of option groups is 100.
                                  If options is specified, this field should not be.
            initial_options (list): An array of option objects that exactly match one or more of the options within options or option_groups
            confirm (class): A confirm object that defines an optional confirmation dialog that appears before the multi-select choices are submitted.
            max_selected_items (int): Specifies the maximum number of items that can be selected in the menu. Minimum number is 1.
            focus_on_load (bool): Indicates whether the element will be set to auto focus within the view object
        """
        super().__init__(placeholder=placeholder,
                         action_id=action_id,
                         options=options,
                         option_groups=option_groups,
                         initial_option=None,
                         confirm=confirm,
                         focus_on_load=focus_on_load)
        self.type = "multi_static_select"
        constructor = BlockElementAttributeConstructor(self)
        if initial_options is not None:
            constructor.edit_initial_options(initial_options)
        if max_selected_items is not None:
            constructor.edit_max_selected_items(max_selected_items)


class ExternalDataSourceSelectMenuElement:
    def __init__(self,
                 placeholder: str,
                 action_id: Optional[str] = None,
                 min_query_length: int = None,
                 initial_option: Optional[OptionObject] = None,
                 confirm: Optional[ConfirmationDialogObject] = None,
                 focus_on_load: Optional[bool] = None):
        """This menu will load its options from an external data source, allowing for a dynamic list of options.

        Works with block types: Section Input

        Args:
            placeholder (str): A plain_text only text that defines the placeholder text shown on the menu
            action_id (str): An identifier for the action triggered when a menu option is selecte
            min_query_length (int): When the typeahead field is used, a request will be sent on every character change
            initial_option (list): An array of option objects that exactly match one or more of the options
            confirm (class): A confirm object that defines an optional confirmation dialog that appears before the multi-select choices are submitted.
            focus_on_load (bool): Indicates whether the element will be set to auto focus within the view object
        """
        self.type = "external_select"
        constructor = BlockElementAttributeConstructor(self)
        constructor.edit_placeholder(placeholder)
        if action_id is not None:
            constructor.edit_action_id(action_id)
        if min_query_length is not None:
            constructor.edit_min_query_length(min_query_length)
        if initial_option is not None:
            constructor.edit_initial_option(initial_option)
        if confirm is not None:
            constructor.edit_confirm(confirm)
        if focus_on_load is not None:
            constructor.edit_focus_on_load(focus_on_load)


class ExternalDataSourceMultiSelectMenuElement(ExternalDataSourceSelectMenuElement):
    def __init__(self,
                 placeholder: str,
                 action_id: Optional[str] = None,
                 min_query_length: int = None,
                 initial_options: Optional[List[OptionObject]] = None,
                 confirm: Optional[ConfirmationDialogObject] = None,
                 max_selected_items: Optional[int] = None,
                 focus_on_load: Optional[bool] = None):
        """This menu will load its options from an external data source, allowing for a dynamic list of options.

        Works with block types: Section Input

        Args:
            placeholder (str): A plain_text only text that defines the placeholder text shown on the menu
            action_id (str): An identifier for the action triggered when a menu option is selecte
            min_query_length (int): When the typeahead field is used, a request will be sent on every character change
            initial_options (list): An array of option objects that exactly match one or more of the options
            confirm (class): A confirm object that defines an optional confirmation dialog that appears before the multi-select choices are submitted.
            max_selected_items (int): Specifies the maximum number of items that can be selected in the menu. Minimum number is 1.
            focus_on_load (bool): Indicates whether the element will be set to auto focus within the view object
        """
        super().__init__(placeholder=placeholder,
                         action_id=action_id,
                         min_query_length=min_query_length,
                         initial_option=None,
                         confirm=confirm,
                         focus_on_load=focus_on_load)
        self.type = "multi_external_select"
        constructor = BlockElementAttributeConstructor(self)
        if initial_options is not None:
            constructor.edit_initial_options(initial_options)
        if max_selected_items is not None:
            constructor.edit_max_selected_items(max_selected_items)


class UserListSelectMenuElement:
    def __init__(self,
                 placeholder: str,
                 action_id: Optional[str] = None,
                 initial_user: Optional[str] = None,
                 confirm: Optional[ConfirmationDialogObject] = None,
                 focus_on_load: Optional[bool] = None):
        """This menu will load its options from an external data source, allowing for a dynamic list of options.

        Works with block types: Section Input

        Args:
            placeholder (str): A plain_text only text that defines the placeholder text shown on the menu
            action_id (str): An identifier for the action triggered when a menu option is selecte
            initial_user (str): An array of user IDs of any valid users to be pre-selected when the menu loads.
            confirm (class): A confirm object that defines an optional confirmation dialog that appears before the multi-select choices are submitted.
            focus_on_load (bool): Indicates whether the element will be set to auto focus within the view object
        """
        self.type = "users_select"
        constructor = BlockElementAttributeConstructor(self)
        constructor.edit_placeholder(placeholder)
        if action_id is not None:
            constructor.edit_action_id(action_id)
        if initial_user is not None:
            constructor.edit_initial_user(initial_user)
        if confirm is not None:
            constructor.edit_confirm(confirm)
        if focus_on_load is not None:
            constructor.edit_focus_on_load(focus_on_load)


class UserListMultiSelectMenuElement(UserListSelectMenuElement):
    def __init__(self,
                 placeholder: str,
                 action_id: Optional[str] = None,
                 initial_users: Optional[List[str]] = None,
                 confirm: Optional[ConfirmationDialogObject] = None,
                 max_selected_items: Optional[int] = None,
                 focus_on_load: Optional[bool] = None):
        """This menu will load its options from an external data source, allowing for a dynamic list of options.

        Works with block types: Section Input

        Args:
            placeholder (str): A plain_text only text that defines the placeholder text shown on the menu
            action_id (str): An identifier for the action triggered when a menu option is selecte
            initial_users (list): An array of user IDs of any valid users to be pre-selected when the menu loads.
            confirm (class): A confirm object that defines an optional confirmation dialog that appears before the multi-select choices are submitted.
            max_selected_items (int): Specifies the maximum number of items that can be selected in the menu. Minimum number is 1.
            focus_on_load (bool): Indicates whether the element will be set to auto focus within the view object
        """
        super().__init__(placeholder=placeholder,
                         action_id=action_id,
                         initial_user=None,
                         confirm=confirm,
                         focus_on_load=focus_on_load)
        self.type = "multi_users_select"
        constructor = BlockElementAttributeConstructor(self)
        if initial_users is not None:
            constructor.edit_initial_users(initial_users)
        if max_selected_items is not None:
            constructor.edit_max_selected_items(max_selected_items)


class ConversationsListSelectMenuElement:
    def __init__(self,
                 placeholder: str,
                 action_id: Optional[str] = None,
                 initial_conversation: Optional[str] = None,
                 default_to_current_conversation: Optional[bool] = None,
                 confirm: Optional[ConfirmationDialogObject] = None,
                 filter: Optional[FilterObject] = None,
                 response_url_enabled: Optional[bool] = None,
                 focus_on_load: Optional[bool] = None):
        """This menu will load its options from an external data source, allowing for a dynamic list of options.

        Works with block types: Section Input

        Args:
            placeholder (str): A plain_text only text that defines the placeholder text shown on the menu
            action_id (str): An identifier for the action triggered when a menu option is selecte
            initial_conversation (list): An array of one or more IDs of any valid conversations to be pre-selected when the menu loads
            default_to_current_conversation (bool): Pre-populates the select menu with the conversation that the user was viewing when they opened the modal, if available
            confirm (class): A confirm object that defines an optional confirmation dialog that appears before the multi-select choices are submitted.
            filter (class): A filter object that reduces the list of available conversations using the specified criteria
            response_url_enabled (bool): When set to true, the view_submission payload from the menu's parent view will contain a response_url
                                         This field only works with menus in input blocks in modals.
            focus_on_load (bool): Indicates whether the element will be set to auto focus within the view object
        """
        self.type = "conversations_select"
        constructor = BlockElementAttributeConstructor(self)
        constructor.edit_placeholder(placeholder)
        if action_id is not None:
            constructor.edit_action_id(action_id)
        if initial_conversation is not None:
            constructor.edit_initial_conversation(initial_conversation)
        if default_to_current_conversation is not None:
            constructor.edit_default_to_current_conversation(default_to_current_conversation)
        if confirm is not None:
            constructor.edit_confirm(confirm)
        if filter is not None:
            constructor.edit_filter(filter)
        if response_url_enabled is not None:
            constructor.edit_response_url_enabled(response_url_enabled)
        if focus_on_load is not None:
            constructor.edit_focus_on_load(focus_on_load)


class ConversationsListMultiSelectMenuElement(ConversationsListSelectMenuElement):
    def __init__(self,
                 placeholder: str,
                 action_id: Optional[str] = None,
                 initial_conversations: Optional[List[str]] = None,
                 default_to_current_conversation: Optional[bool] = None,
                 confirm: Optional[ConfirmationDialogObject] = None,
                 max_selected_items: Optional[int] = None,
                 filter: Optional[FilterObject] = None,
                 focus_on_load: Optional[bool] = None):
        """This menu will load its options from an external data source, allowing for a dynamic list of options.

        Works with block types: Section Input

        Args:
            placeholder (str): A plain_text only text that defines the placeholder text shown on the menu
            action_id (str): An identifier for the action triggered when a menu option is selecte
            initial_conversations (list): An array of one or more IDs of any valid conversations to be pre-selected when the menu loads
            default_to_current_conversation (bool): Pre-populates the select menu with the conversation that the user was viewing when they opened the modal, if available
            confirm (class): A confirm object that defines an optional confirmation dialog that appears before the multi-select choices are submitted.
            max_selected_items (int): Specifies the maximum number of items that can be selected in the menu. Minimum number is 1.
            filter (class): A filter object that reduces the list of available conversations using the specified criteria
            focus_on_load (bool): Indicates whether the element will be set to auto focus within the view object
        """
        super().__init__(placeholder=placeholder,
                         action_id=action_id,
                         initial_conversation=None,
                         default_to_current_conversation=default_to_current_conversation,
                         confirm=confirm,
                         filter=filter,
                         focus_on_load=focus_on_load
                         )
        self.type = "multi_conversations_select"
        constructor = BlockElementAttributeConstructor(self)
        if initial_conversations is not None:
            constructor.edit_initial_conversations(initial_conversations)
        if max_selected_items is not None:
            constructor.edit_max_selected_items(max_selected_items)


class PublicChannelListSelectMenuElement:
    def __init__(self,
                 placeholder: str,
                 action_id: Optional[str] = None,
                 initial_channel: Optional[str] = None,
                 confirm: Optional[ConfirmationDialogObject] = None,
                 response_url_enabled: Optional[bool] = None,
                 focus_on_load: Optional[bool] = None):
        """This menu will load its options from an external data source, allowing for a dynamic list of options.

        Works with block types: Section Input

        Args:
            placeholder (str): A plain_text only text that defines the placeholder text shown on the menu
            action_id (str): An identifier for the action triggered when a menu option is selecte
            initial_channel (list): An array of one or more IDs of any valid public channel to be pre-selected when the menu loads
            confirm (class): A confirm object that defines an optional confirmation dialog that appears before the multi-select choices are submitted.
            response_url_enabled (bool): When set to true, the view_submission payload from the menu's parent view will contain a response_url
                                         This field only works with menus in input blocks in modals.
            max_selected_items (int): Specifies the maximum number of items that can be selected in the menu. Minimum number is 1.
            focus_on_load (bool): Indicates whether the element will be set to auto focus within the view object
        """
        self.type = "channels_select"
        constructor = BlockElementAttributeConstructor(self)
        constructor.edit_placeholder(placeholder)
        if action_id is not None:
            constructor.edit_action_id(action_id)
        if initial_channel is not None:
            constructor.edit_initial_channel(initial_channel)
        if confirm is not None:
            constructor.edit_confirm(confirm)
        if response_url_enabled is not None:
            constructor.edit_response_url_enabled(response_url_enabled)
        if focus_on_load is not None:
            constructor.edit_focus_on_load(focus_on_load)


class PublicChannelListMultiSelectMenuElement(PublicChannelListSelectMenuElement):
    def __init__(self,
                 placeholder: str,
                 action_id: Optional[str] = None,
                 initial_channels: Optional[List[str]] = None,
                 confirm: Optional[ConfirmationDialogObject] = None,
                 max_selected_items: Optional[int] = None,
                 focus_on_load: Optional[bool] = None):
        """This menu will load its options from an external data source, allowing for a dynamic list of options.

        Works with block types: Section Input

        Args:
            placeholder (str): A plain_text only text that defines the placeholder text shown on the menu
            action_id (str): An identifier for the action triggered when a menu option is selecte
            initial_channels (list): An array of one or more IDs of any valid public channel to be pre-selected when the menu loads
            confirm (class): A confirm object that defines an optional confirmation dialog that appears before the multi-select choices are submitted.
            max_selected_items (int): Specifies the maximum number of items that can be selected in the menu. Minimum number is 1.
            focus_on_load (bool): Indicates whether the element will be set to auto focus within the view object
        """
        super().__init__(placeholder=placeholder,
                         action_id=action_id,
                         initial_channel=None,
                         confirm=confirm,
                         focus_on_load=focus_on_load)
        self.type = "multi_channels_select"
        constructor = BlockElementAttributeConstructor(self)
        if initial_channels is not None:
            constructor.edit_initial_channels(initial_channels)
        if max_selected_items is not None:
            constructor.edit_max_selected_items(max_selected_items)


class OverflowMenuElement:
    def __init__(self,
                 options: List[OptionObject],
                 action_id: Optional[str] = None,
                 confirm: Optional[ConfirmationDialogObject] = None):
        """This is like a cross between a button and a select menu - when a user clicks on this overflow button,
        they will be presented with a list of options to choose from.

        Works with block types: Section Actions

        Args:
            action_id (str): An identifier for the action triggered when a menu option is selected
            options (list): An array of option objects to display in the menu
                            Maximum number of options is 5, minimum is 2
            confirm (class): A confirm object that defines an optional confirmation dialog that appears after a menu item is selected.
        """
        self.type = "overflow"
        constructor = BlockElementAttributeConstructor(self, options_max=5, options_min=2)
        constructor.edit_options(options)
        if action_id is not None:
            constructor.edit_action_id(action_id)
        if confirm is not None:
            constructor.edit_confirm(confirm)


class PlainTextInputElement:
    def __init__(self,
                 action_id: Optional[str] = None,
                 placeholder: Optional[str] = None,
                 initial_value: Optional[str] = None,
                 multiline: Optional[bool] = None,
                 min_length: Optional[int] = None,
                 max_length: Optional[int] = None,
                 dispatch_action_config: Optional[DispatchActionConfigurationObject] = None,
                 focus_on_load: Optional[bool] = None
                 ):
        self.type = "plain_text_input"
        constructor = BlockElementAttributeConstructor(self)
        if action_id is not None:
            constructor.edit_action_id(action_id)
        if placeholder is not None:
            constructor.edit_placeholder(placeholder)
        if initial_value is not None:
            constructor.edit_initial_value(initial_value)
        if multiline is not None:
            constructor.edit_multiline(multiline)
        if min_length is not None:
            constructor.edit_min_length(min_length)
        if max_length is not None:
            constructor.edit_max_length(max_length)
        if dispatch_action_config is not None:
            constructor.edit_dispatch_action_config(dispatch_action_config)
        if focus_on_load is not None:
            constructor.edit_focus_on_load(focus_on_load)


class RadioButtonGroupElement:
    def __init__(self,
                 options: List[OptionObject],
                 action_id: Optional[str] = None,
                 initial_option: Optional[OptionObject] = None,
                 confirm: Optional[ConfirmationDialogObject] = None,
                 focus_on_load: Optional[bool] = None):
        """A radio button group that allows a user to choose one item from a list of possible option

        Works with block types: Section Actions Input

        Args:
            action_id (str): An identifier for the action triggered when the checkbox group is changed
            options (list): An array of option objects.
                            A maximum of 10 options are allowed
            initial_option (list): An array of option objects that exactly matches one or more of the options within options
            confirm (class): A confirm object that defines an optional confirmation dialog that appears after clicking one of the checkboxes in this element.
            focus_on_load (bool): Indicates whether the element will be set to auto focus within the view object
        """
        self.type = "radio_buttons"
        constructor = BlockElementAttributeConstructor(self, options_max=10)
        self.options = options
        if action_id is not None:
            constructor.edit_action_id(action_id)
        if initial_option is not None:
            constructor.edit_initial_option(initial_option)
        if confirm is not None:
            constructor.edit_confirm(confirm)
        if focus_on_load is not None:
            constructor.edit_focus_on_load(focus_on_load)


class TimePickerElement:
    def __init__(self,
                 action_id: Optional[str] = None,
                 placeholder: Optional[str] = None,
                 initial_time: Optional[str] = None,
                 confirm: Optional[ConfirmationDialogObject] = None,
                 focus_on_load: Optional[bool] = None):
        """An element which allows selection of a time of day.

        Works with block types: Section Actions Input

        Args:
            action_id (str): An identifier for the action triggered when a menu option is selected
            placeholder (str): 	A plain_text only text that defines the placeholder text shown on the datepicker
            initial_time (str): The initial time that is selected when the element is loaded.
                                This should be in the format HH:mm
            confirm (class): A confirm object that defines an optional confirmation dialog that appears after a date is selected.
            focus_on_load (bool): Indicates whether the element will be set to auto focus within the view object.
        """
        self.type = "timepicker"
        constructor = BlockElementAttributeConstructor(self, options_max=10)
        if action_id is not None:
            constructor.edit_action_id(action_id)
        if placeholder is not None:
            constructor.edit_placeholder(placeholder)
        if initial_time is not None:
            constructor.edit_initial_time(initial_time)
        if confirm is not None:
            constructor.edit_confirm(confirm)
        if focus_on_load is not None:
            constructor.edit_focus_on_load(focus_on_load)
