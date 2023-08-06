#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : test_components__block_elements
# @Date : 2022-01-27-17-20
# @Project: content-service-chat-assistant

import pytest
from unittest import mock
from slack_block_builder.components.block_element import *
from slack_block_builder.exception import *


class TestBlockElementAttributeCheckers:
    @pytest.fixture(scope="function")
    def obj_instance(self):
        return BlockElementAttributeCheckers()

    @mock.patch.object(BlockElementAttributeCheckers, "string_length_checker")
    def test__ut__action_id_checker(self, mock_string_length_checker, obj_instance):
        action_id = "213fu"
        obj_instance.action_id_checker(action_id)
        mock_string_length_checker.assert_called_once_with("action_id", action_id, 255)

    @pytest.mark.parametrize("generate_str", [256], indirect=True)
    def test__ut__action_id_checker__out_of_range(self, generate_str, obj_instance):
        with pytest.raises(BlockElementOutOfRangeError):
            obj_instance.action_id_checker(generate_str)

    @pytest.mark.parametrize("generate_str", [255], indirect=True)
    def test__ut__action_id_checker(self, generate_str, obj_instance):
        obj_instance.action_id_checker(generate_str)

    @mock.patch.object(BlockElementAttributeCheckers, "type_checker")
    def test__ut__focus_on_load_checker(self, mock_type_checker, obj_instance):
        input_value = "confirm class simulator"
        obj_instance.confirm_check(input_value)
        mock_type_checker.assert_called_once_with("confirm", input_value, ConfirmationDialogObject)

    @mock.patch.object(BlockElementAttributeCheckers, "type_checker")
    def test__ut__confirm_check(self, mock_type_checker, obj_instance):
        input_value = False
        obj_instance.focus_on_load_checker(input_value)
        mock_type_checker.assert_called_once_with("focus_on_load", input_value, bool)

    @mock.patch.object(BlockElementAttributeCheckers, "type_checker")
    def test__ut__confirm_check(self, mock_type_checker, obj_instance):
        input_value = 1
        obj_instance.max_selected_items_checker(input_value)
        mock_type_checker.assert_called_once_with("max_selected_items", input_value, int)

    def test__ut__confirm_check__type_errot(self, obj_instance):
        with pytest.raises(BlockTypeError):
            obj_instance.confirm_check(ColorScheme)

    def test__ut__confirm_check(self, obj_instance):
        confirm = ConfirmationDialogObject(
            title="title 1",
            text="body message",
            confirm="confirm",
            deny="deny"
        )
        obj_instance.confirm_check(confirm)

    def test__ut__date_checker__type_error(self, obj_instance):
        _date = "21/Jan/2019"
        with pytest.raises(BlockValueError):
            obj_instance.date_checker("date", _date)

    def test__ut__date_checker(self, obj_instance):
        _date = "2020-01-30"
        obj_instance.date_checker("date", _date)

    def test__ut__time_checker__type_error(self, obj_instance):
        _time = "25:40"
        with pytest.raises(BlockValueError):
            obj_instance.time_checker("time", _time)

    def test__ut__time_checker__type_error(self, obj_instance):
        _time = "12:40"
        obj_instance.time_checker("time", _time)

    @mock.patch.object(BlockElementAttributeCheckers, "string_length_checker")
    def test__ut__placeholder(self, mock_string_length_checker, obj_instance):
        placeholder = "dwjjiiu"
        obj_instance.placeholder_checker(placeholder)
        mock_string_length_checker("placeholder", placeholder, 150)

    @pytest.mark.parametrize("generate_str", [151], indirect=True)
    def test__ut__placeholder_checker__out_of_range(self, generate_str, obj_instance):
        with pytest.raises(BlockElementOutOfRangeError):
            obj_instance.placeholder_checker(generate_str)

    @pytest.mark.parametrize("generate_str", [150], indirect=True)
    def test__ut__placeholder_checker(self, generate_str, obj_instance):
        obj_instance.placeholder_checker(generate_str)

    @mock.patch.object(BlockElementAttributeCheckers, "type_checker")
    def test__ut__filter_object_check(self, mock_type_checker, obj_instance):
        input_value = "confirm class simulator"
        obj_instance.filter_object_check(input_value)
        mock_type_checker.assert_called_once_with("filter", input_value, FilterObject)

    @mock.patch.object(BlockElementAttributeCheckers, "type_checker")
    def test__ut__dispatch_action_config_check(self, mock_type_checker, obj_instance):
        input_value = "confirm class simulator"
        obj_instance.dispatch_action_config_check(input_value)
        mock_type_checker.assert_called_once_with("dispatch_action_config", input_value, DispatchActionConfigurationObject)


class TestBlockElementAttributeConstructor:
    @pytest.fixture(scope="function")
    def empty_instance(self):
        class Empty(object):
            pass

        return Empty()

    @pytest.fixture(scope="function")
    def obj_instance(self, empty_instance):
        return BlockElementAttributeConstructor(empty_instance)

    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    @mock.patch.object(BlockElementAttributeCheckers, "action_id_checker")
    def test__ut__edit_action_id(self, mock_action_id_checker, mock_set_attribute, obj_instance):
        action_id = "1112222"
        obj_instance.edit_action_id(action_id)
        mock_action_id_checker.assert_called_once_with(action_id)
        mock_set_attribute("action_id", action_id)

    def test__it__edit_action_id(self, obj_instance):
        assert getattr(obj_instance, "action_id", None) is None
        action_id = "1112222"
        obj_instance.edit_action_id(action_id)
        assert obj_instance._object.action_id == action_id

    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    @mock.patch.object(BlockElementAttributeCheckers, "confirm_check")
    def test__ut__edit_confirm(self, mock_confirm_check, mock_set_attribute, obj_instance, generate_confirm_obj):
        obj_instance.edit_confirm(generate_confirm_obj)
        mock_confirm_check.assert_called_once_with(generate_confirm_obj)
        mock_set_attribute("confirm", generate_confirm_obj)

    def test__it__edit_confirm(self, obj_instance, generate_confirm_obj):
        obj_instance.edit_confirm(generate_confirm_obj)
        assert obj_instance._object.confirm is generate_confirm_obj

    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    @mock.patch.object(BlockElementAttributeCheckers, "placeholder_checker")
    def test__ut__edit_placeholder(self, mock_placeholder_checker, mock_set_attribute, obj_instance):
        with mock.patch("slack_block_builder.components.composition_block.TextObject") as MockTextObject:
            text = "placeholder text"
            obj_instance.edit_placeholder(text)
            mock_placeholder_checker(text)
            mock_set_attribute("placeholder", MockTextObject(text))

    def test__it__edit_placeholder(self, obj_instance):
        text = "placeholder text"
        obj_instance.edit_placeholder(text)
        assert isinstance(obj_instance._object.placeholder, TextObject)
        assert obj_instance._object.placeholder.text == text

    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    @mock.patch.object(BlockElementAttributeCheckers, "date_checker")
    def test__ut__edit_initial_date(self, mock_date_checker, mock_set_attribute, obj_instance):
        date = "1999/Jan/01"
        obj_instance.edit_initial_date(date)
        mock_date_checker.assert_called_once_with("initial_date", date)
        mock_set_attribute.assert_called_once_with("initial_date", date)

    def test__it__edit_initial_date(self, obj_instance):
        date = "1999-01-01"
        obj_instance.edit_initial_date(date)
        assert obj_instance._object.initial_date == date

    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    @mock.patch.object(BlockElementAttributeCheckers, "focus_on_load_checker")
    def test__ut__edit_focus_on_load(self, mock_focus_on_load_checker, mock_set_attribute, obj_instance):
        focus_on_load = False
        obj_instance.edit_focus_on_load(focus_on_load)
        mock_focus_on_load_checker.assert_called_once_with(focus_on_load)
        mock_set_attribute("focus_on_load", focus_on_load)

    def test__ut__edit_focus_on_load(self, obj_instance):
        focus_on_load = False
        obj_instance.edit_focus_on_load(focus_on_load)
        assert obj_instance._object.focus_on_load is focus_on_load

    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    @mock.patch.object(BlockElementAttributeCheckers, "string_length_checker")
    def test__ut__edit_image_url(self, mock_string_length_checker, mock_set_attribute, obj_instance):
        _url = "https://sap.com"
        obj_instance.edit_image_url(_url)
        mock_string_length_checker("image_url", _url, 3000)
        mock_set_attribute("image_url", _url)

    def test__it__edit_image_url(self, obj_instance):
        _url = "https://sap.com"
        obj_instance.edit_image_url(_url)
        assert obj_instance._object.image_url == _url

    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    @mock.patch.object(BlockElementAttributeCheckers, "string_length_checker")
    def test__ut__edit_alt_text(self, mock_string_length_checker, mock_set_attribute, obj_instance):
        _text = "https://sap.com loading"
        obj_instance.edit_alt_text(_text)
        mock_string_length_checker("alt_text", _text, 2000)
        mock_set_attribute("alt_text", _text)

    def test__it__edit_alt_text(self, obj_instance):
        _text = "https://sap.com loading"
        obj_instance.edit_alt_text(_text)
        assert obj_instance._object.alt_text == _text

    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    @mock.patch.object(BlockElementAttributeCheckers, "option_groups_checker")
    def test__ut__edit_option_groups(self, mock_option_groups_checker, mock_set_attribute, obj_instance):
        option_groups = "Option Groups"
        obj_instance.edit_option_groups(option_groups)
        mock_option_groups_checker("option_groups", option_groups)
        mock_set_attribute("option_groups", option_groups)

    @pytest.mark.parametrize("generate_optional_object", [20], indirect=True)
    def test__it__edit_option_groups(self, obj_instance, generate_optional_object):
        option_groups = [OptionGroupObject(label="test", options=generate_optional_object)]
        obj_instance.edit_option_groups(option_groups)
        assert obj_instance._object.option_groups is option_groups

    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    @mock.patch.object(BlockElementAttributeCheckers, "option_obj_checker")
    def test__ut__edit_initial_option(self, mock_option_obj_checker, mock_set_attribute, obj_instance):
        option_groups = "Option"
        obj_instance.edit_initial_option(option_groups)
        mock_option_obj_checker(option_groups)
        mock_set_attribute("initial_option", option_groups)

    @pytest.mark.parametrize("generate_optional_object", [20], indirect=True)
    def test__it__edit_initial_option(self, obj_instance, generate_optional_object):
        obj_instance.edit_initial_option(generate_optional_object[0])
        assert obj_instance._object.initial_option is generate_optional_object[0]

    @mock.patch.object(BlockElementAttributeCheckers, "options_list_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_initial_options(self, mock_set_attribute, mock_options_list_checker, obj_instance):
        _options = "list options"
        obj_instance.edit_initial_options(_options)
        mock_options_list_checker.assert_called_once_with("initial_options", _options, 100)
        mock_set_attribute.assert_called_once_with("initial_options", _options)

    @pytest.mark.parametrize("generate_optional_object", [20], indirect=True)
    def test__it__edit_initial_options(self, obj_instance, generate_optional_object):
        obj_instance.edit_initial_options(generate_optional_object)
        obj_instance._object.initial_options is generate_optional_object

    @mock.patch.object(BlockElementAttributeCheckers, "max_selected_items_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_max_selected_items(self, mock_set_attribute, mock_max_selected_items_checker, obj_instance):
        max_selected_items = 1000
        obj_instance.edit_max_selected_items(max_selected_items)
        mock_max_selected_items_checker.assert_called_once_with(max_selected_items)
        mock_set_attribute.assert_called_once_with("max_selected_items", max_selected_items)

    def test__it__edit_max_selected_items(self, obj_instance):
        max_selected_items = 1000
        obj_instance.edit_max_selected_items(max_selected_items)
        assert obj_instance._object.max_selected_items == max_selected_items

    @mock.patch.object(BlockElementAttributeCheckers, "type_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_min_query_length(self, mock_set_attribute, mock_type_checker, obj_instance):
        min_query = 100
        obj_instance.edit_min_query_length(min_query)
        mock_type_checker("min_query_length", min_query)
        mock_set_attribute("min_query_length", min_query)

    def test__ut__edit_min_query_length(self, obj_instance):
        min_query = 100
        obj_instance.edit_min_query_length(min_query)
        assert obj_instance._object.min_query_length == min_query

    @mock.patch.object(BlockElementAttributeCheckers, "string_length_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_initial_user(self, mock_set_attribute, mock_string_length_checker, obj_instance):
        string_list = ["1", "2"]
        obj_instance.edit_initial_user(string_list)
        mock_string_length_checker.assert_called_once_with("initial_user", string_list, 100)
        mock_set_attribute.assert_called_once_with("initial_user", string_list)

    def test__it__edit_initial_user(self, obj_instance):
        _string = "1"
        obj_instance.edit_initial_user(_string)
        assert obj_instance._object.initial_user is _string

    @mock.patch.object(BlockElementAttributeCheckers, "list_string_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_initial_users(self, mock_set_attribute, mock_list_string_checker, obj_instance):
        string_list = ["1", "2"]
        obj_instance.edit_initial_users(string_list)
        mock_list_string_checker.assert_called_once_with("initial_users", string_list, 100)
        mock_set_attribute("initial_users", string_list)

    def test__it__edit_initial_users(self, obj_instance):
        string_list = ["1", "2"]
        obj_instance.edit_initial_users(string_list)
        assert obj_instance._object.initial_users is string_list

    @mock.patch.object(BlockElementAttributeCheckers, "string_length_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_initial_conversation(self, mock_set_attribute, mock_string_length_checker, obj_instance):
        conversation = "text"
        obj_instance.edit_initial_conversation(conversation)
        mock_string_length_checker.assert_called_once_with("initial_conversation", conversation, 100)
        mock_set_attribute("initial_conversation", conversation)

    def test__it__edit_initial_conversation(self, obj_instance):
        conversation = "text"
        obj_instance.edit_initial_conversation(conversation)
        assert obj_instance._object.initial_conversation == conversation

    @mock.patch.object(BlockElementAttributeCheckers, "list_string_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_initial_conversations(self, mock_set_attribute, mock_list_string_checker, obj_instance):
        conversations = ["1", "2"]
        obj_instance.edit_initial_conversations(conversations)
        mock_list_string_checker("initial_conversations", conversations, 100)
        mock_set_attribute("initial_conversations", conversations)

    def test__it__edit_initial_conversations(self, obj_instance):
        conversations = ["1", "2"]
        obj_instance.edit_initial_conversations(conversations)
        assert obj_instance._object.initial_conversations is conversations

    @mock.patch.object(BlockElementAttributeCheckers, "string_length_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_initial_channel(self, mock_set_attribute, mock_string_length_checker, obj_instance):
        channel = "text"
        obj_instance.edit_initial_channel(channel)
        mock_string_length_checker.assert_called_once_with("initial_channel", channel, 100)
        mock_set_attribute.assert_called_once_with("initial_channel", channel)

    def test__it__edit_initial_channel(self, obj_instance):
        channel = "text"
        obj_instance.edit_initial_channel(channel)
        assert obj_instance._object.initial_channel == channel

    @mock.patch.object(BlockElementAttributeCheckers, "list_string_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_initial_channels(self, mock_set_attribute, mock_list_string_checker, obj_instance):
        channels = ["1", "2"]
        obj_instance.edit_initial_channels(channels)
        mock_list_string_checker("initial_channels", channels, 100)
        mock_set_attribute("initial_channels", channels)

    def test__it__edit_initial_channels(self, obj_instance):
        channels = ["1", "2"]
        obj_instance.edit_initial_channels(channels)
        assert obj_instance._object.initial_channels == channels

    @mock.patch.object(BlockElementAttributeCheckers, "string_length_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_initial_value(self, mock_set_attribute, mock_string_length_checker, obj_instance):
        value = "new value"
        obj_instance.edit_initial_value(value)
        mock_string_length_checker.assert_called_once_with("initial_value", value, 1000)
        mock_set_attribute.assert_called_once_with("initial_value", value)

    def test__it__edit_initial_value(self, obj_instance):
        value = "new value"
        obj_instance.edit_initial_value(value)
        assert obj_instance._object.initial_value == value

    @mock.patch.object(BlockElementAttributeCheckers, "type_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_multiline(self, mock_set_attribute, mock_type_checker, obj_instance):
        multiline = False
        obj_instance.edit_multiline(multiline)
        mock_type_checker("multiline", multiline, bool)
        mock_set_attribute("multiline", multiline)

    def test__ut__edit_multiline(self, obj_instance):
        multiline = False
        obj_instance.edit_multiline(multiline)
        assert obj_instance._object.multiline is multiline

    @mock.patch.object(BlockElementAttributeCheckers, "type_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_min_length(self, mock_set_attribute, mock_type_checker, obj_instance):
        _length = 1
        obj_instance.edit_min_length(_length)
        mock_type_checker.assert_called_once_with("min_length", _length, int)
        mock_set_attribute.assert_called_once_with("min_length", _length)

    def test__it__edit_min_length(self, obj_instance):
        _length = 1
        obj_instance.edit_min_length(_length)
        assert obj_instance._object.min_length == _length

    @mock.patch.object(BlockElementAttributeCheckers, "type_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_max_length(self, mock_set_attribute, mock_type_checker, obj_instance):
        _length = 1
        obj_instance.edit_max_length(_length)
        mock_type_checker.assert_called_once_with("max_length", _length, int)
        mock_set_attribute.assert_called_once_with("max_length", _length)

    def test__it__edit_max_length(self, obj_instance):
        _length = 1
        obj_instance.edit_max_length(_length)
        assert obj_instance._object.max_length == _length

    @mock.patch.object(BlockElementAttributeCheckers, "dispatch_action_config_check")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_dispatch_action_config(self, mock_set_attribute, mock_dispatch_action_config_check, obj_instance):
        dispatch = "dispatch class"
        obj_instance.edit_dispatch_action_config(dispatch)
        mock_dispatch_action_config_check.assert_called_once_with(dispatch)
        mock_set_attribute("dispatch_action_config", dispatch)

    def test__it__edit_dispatch_action_config(self, obj_instance):
        dispatch = DispatchActionConfigurationObject(["1", "2"])
        obj_instance.edit_dispatch_action_config(dispatch)
        assert obj_instance._object.dispatch_action_config == dispatch

    @mock.patch.object(BlockElementAttributeCheckers, "type_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_default_to_current_conversation(self, mock_set_attribute, mock_type_checker, obj_instance):
        default_to_current_conversation = False
        obj_instance.edit_default_to_current_conversation(default_to_current_conversation)
        mock_type_checker.assert_called_once_with("default_to_current_conversation", default_to_current_conversation, bool)
        mock_set_attribute("default_to_current_conversation", default_to_current_conversation)

    def test__it__edit_default_to_current_conversation(self, obj_instance):
        default_to_current_conversation = False
        obj_instance.edit_default_to_current_conversation(default_to_current_conversation)
        assert obj_instance._object.default_to_current_conversation is default_to_current_conversation

    @mock.patch.object(BlockElementAttributeCheckers, "filter_object_check")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_filter(self, mock_set_attribute, mock_filter_object_check, obj_instance):
        _filter = "filter class"
        obj_instance.edit_filter(_filter)
        mock_filter_object_check.assert_called_once_with(_filter)
        mock_set_attribute.assert_called_once_with("filter", _filter)

    def test__it__edit_filter(self, obj_instance):
        _filter = FilterObject()
        obj_instance.edit_filter(_filter)
        assert obj_instance._object.filter is _filter

    @mock.patch.object(BlockElementAttributeCheckers, "type_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_response_url_enabled(self, mock_set_attribute, mock_type_checker, obj_instance):
        response_url_enabled = True
        obj_instance.edit_response_url_enabled(response_url_enabled)
        mock_type_checker.assert_called_once_with("response_url_enabled", response_url_enabled, bool)
        mock_set_attribute.assert_called_once_with("response_url_enabled", response_url_enabled)

    def test__it__edit_response_url_enabled(self, obj_instance):
        response_url_enabled = True
        obj_instance.edit_response_url_enabled(response_url_enabled)
        assert obj_instance._object.response_url_enabled is response_url_enabled

    @mock.patch.object(BlockElementAttributeCheckers, "time_checker")
    @mock.patch.object(BlockElementAttributeConstructor, "_set_attribute")
    def test__ut__edit_initial_time(self, mock_time_checker, mock_set_attribute, obj_instance):
        initial_time = "17:00"
        obj_instance.edit_initial_time(initial_time)
        mock_time_checker.assert_called_once_with("initial_time", initial_time)
        mock_set_attribute.assert_called_once_with("initial_time", initial_time)


class TestButtonElement:
    def test__ut__text__type(self):
        button = ButtonElement(text="hello")
        assert button.type == "button"

    @pytest.mark.parametrize("generate_str", [76], indirect=True)
    def test__ut__text__out_of_range(self, generate_str):
        with pytest.raises(BlockElementOutOfRangeError):
            ButtonElement(text=generate_str)

    @pytest.mark.parametrize("generate_str", [75], indirect=True)
    def test__ut__text(self, generate_str):
        button = ButtonElement(text=generate_str)
        assert button.text.text == generate_str
        assert button.text.emoji is True

    @pytest.mark.parametrize("generate_str", [256], indirect=True)
    def test__ut__action_id__out_of_range(self, generate_str):
        with pytest.raises(BlockElementOutOfRangeError):
            ButtonElement(text="hello", action_id=generate_str)

    @pytest.mark.parametrize("generate_str", [255], indirect=True)
    def test__ut__action_id(self, generate_str):
        button = ButtonElement(text="hello", action_id=generate_str)
        assert button.action_id == generate_str

    @pytest.mark.parametrize("generate_str", [3001], indirect=True)
    def test__ut__url__out_of_range(self, generate_str):
        with pytest.raises(BlockElementOutOfRangeError):
            ButtonElement(text="hello", url=generate_str)

    @pytest.mark.parametrize("generate_str", [3000], indirect=True)
    def test__ut__url(self, generate_str):
        button = ButtonElement(text="hello", url=generate_str)
        assert button.url == generate_str

    @pytest.mark.parametrize("generate_str", [2001], indirect=True)
    def test__ut__value__out_of_range(self, generate_str):
        with pytest.raises(BlockElementOutOfRangeError):
            ButtonElement(text="hello", value=generate_str)

    @pytest.mark.parametrize("generate_str", [2000], indirect=True)
    def test__ut__value(self, generate_str):
        button = ButtonElement(text="hello", value=generate_str)
        assert button.value == generate_str

    def test__ut__style__type_error(self):
        with pytest.raises(BlockTypeError):
            ButtonElement(text="hello", style="primary")

    def test__ut__style(self):
        _color = ColorScheme.Primary
        button = ButtonElement(text="hello", style=_color)
        assert button.style == _color.value

    def test__ut__confirm__type_error(self):
        with pytest.raises(BlockTypeError):
            ButtonElement(text="hello", confirm=ColorScheme)

    def test__ut__confirm(self, generate_confirm_obj):
        button = ButtonElement(text="hello", confirm=generate_confirm_obj)
        assert button.confirm.text.text == generate_confirm_obj.text.text


class TestCheckBoxElement:
    @pytest.mark.parametrize("generate_optional_object", [3], indirect=True)
    def test__ut__type_check(self, generate_optional_object):
        _object = CheckBoxElement(
            options=generate_optional_object
        )
        assert _object.type == "checkboxes"

    @pytest.mark.parametrize("generate_optional_object", [10], indirect=True)
    def test__it__options(self, generate_optional_object):
        _object = CheckBoxElement(options=generate_optional_object)
        assert _object.options is generate_optional_object

    @pytest.mark.parametrize("generate_optional_object", [11], indirect=True)
    def test__it__max_options_10(self, generate_optional_object):
        with pytest.raises(BlockElementOutOfRangeError):
            CheckBoxElement(options=generate_optional_object)

    @pytest.mark.parametrize("generate_optional_object", [10], indirect=True)
    def test__it__max_initial_options_10(self, generate_optional_object):
        _object = CheckBoxElement(
            options=generate_optional_object[:5],
            initial_options=generate_optional_object
        )
        assert _object.initial_options is generate_optional_object

    @pytest.mark.parametrize("generate_optional_object", [11], indirect=True)
    def test__it__max_initial_options_10(self, generate_optional_object):
        with pytest.raises(BlockElementOutOfRangeError):
            CheckBoxElement(
                options=generate_optional_object[:5],
                initial_options=generate_optional_object
            )

    @pytest.mark.parametrize("generate_str", [10], indirect=True)
    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__action_id(self, generate_str, generate_optional_object):
        _object = CheckBoxElement(
            options=generate_optional_object,
            action_id=generate_str
        )
        assert _object.action_id == generate_str

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__confirm(self, generate_optional_object, generate_confirm_obj):
        _object = CheckBoxElement(
            options=generate_optional_object,
            confirm=generate_confirm_obj
        )
        assert _object.confirm is generate_confirm_obj

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__focus_on_load(self, generate_optional_object):
        _object = CheckBoxElement(
            options=generate_optional_object,
            focus_on_load=True
        )
        assert _object.focus_on_load is True
        

class TestDatePickerElement:
    def test__ut__type(self):
        _object = DatePickerElement()
        assert _object.type == "datepicker"

    @pytest.mark.parametrize("generate_str", [10], indirect=True)
    def test__it__action_id(self, generate_str):
        _object = DatePickerElement(action_id=generate_str)
        assert _object.action_id == generate_str

    @pytest.mark.parametrize("generate_str", [10], indirect=True)
    def test__it__placeholder(self, generate_str):
        _object = DatePickerElement(placeholder=generate_str)
        assert _object.placeholder.text == generate_str

    def test__it__initial_date(self):
        initial_date = "2019-01-10"
        _object = DatePickerElement(initial_date=initial_date)
        assert _object.initial_date == initial_date

    def test__it__confirm(self, generate_confirm_obj):
        _object = DatePickerElement(confirm=generate_confirm_obj)
        assert _object.confirm is generate_confirm_obj

    def test__it__focus_on_load(self):
        _object = DatePickerElement(focus_on_load=True)
        assert _object.focus_on_load is True


class TestImageElement:
    def test__ut__type(self):
        url = "https://test.me"
        text = "test"
        _object = ImageElement(url, text)
        assert _object.type == "image"

    def test__it__image_url(self):
        url = "https://test.me"
        text = "test"
        _object = ImageElement(url, text)
        assert _object.image_url == url

    def test__it__alt_text(self):
        url = "https://test.me"
        text = "test"
        _object = ImageElement(url, text)
        assert _object.alt_text == text


class TestStaticSelectMenuElement:
    @pytest.mark.parametrize("generate_optional_object", [3], indirect=True)
    def test__ut__type(self, generate_optional_object):
        placeholder = "test"
        _object = StaticSelectMenuElement(placeholder=placeholder, options=generate_optional_object)
        assert _object.type == "static_select"

    @pytest.mark.parametrize("generate_optional_object", [3], indirect=True)
    def test__it__placeholder(self, generate_optional_object):
        placeholder = "test"
        _object = StaticSelectMenuElement(placeholder=placeholder, options=generate_optional_object)
        assert _object.placeholder.text == placeholder

    @pytest.mark.parametrize("generate_optional_object", [3], indirect=True)
    def test__it__action_id(self, generate_optional_object):
        placeholder = "test"
        action_id = "action11122"
        _object = StaticSelectMenuElement(placeholder=placeholder, options=generate_optional_object,
                                          action_id=action_id)
        assert _object.action_id == action_id

    @pytest.mark.parametrize("generate_optional_object", [3], indirect=True)
    def test__it__options(self, generate_optional_object):
        placeholder = "test"
        _object = StaticSelectMenuElement(placeholder=placeholder, options=generate_optional_object)
        assert _object.options is generate_optional_object

    @pytest.mark.parametrize("generate_optional_object", [3], indirect=True)
    def test__it__initial_option(self, generate_optional_object):
        placeholder = "test"
        initial_option = generate_optional_object[0]
        _object = StaticSelectMenuElement(placeholder=placeholder, options=generate_optional_object,
                                          initial_option=initial_option)
        assert _object.initial_option is generate_optional_object[0]

    @pytest.mark.parametrize("generate_option_groups_object", [3], indirect=True)
    def test__it__option_groups(self, generate_option_groups_object):
        placeholder = "test"
        _object = StaticSelectMenuElement(placeholder=placeholder, option_groups=generate_option_groups_object)
        assert _object.option_groups is generate_option_groups_object

    @pytest.mark.parametrize("generate_optional_object", [3], indirect=True)
    @pytest.mark.parametrize("generate_option_groups_object", [3], indirect=True)
    def test__it__conflict_error(self, generate_optional_object, generate_option_groups_object):
        placeholder = "test"
        with pytest.raises(BlockValueError):
            _object = StaticSelectMenuElement(placeholder=placeholder, options=generate_optional_object,
                                              option_groups=generate_option_groups_object)

    def test__it__options_null_error(self):
        placeholder = "test"
        with pytest.raises(BlockValueError):
            _object = StaticSelectMenuElement(placeholder=placeholder)

    @pytest.mark.parametrize("generate_option_groups_object", [3], indirect=True)
    def test__it__confirm(self, generate_option_groups_object, generate_confirm_obj):
        placeholder = "test"
        _object = StaticSelectMenuElement(placeholder=placeholder, option_groups=generate_option_groups_object,
                                          confirm=generate_confirm_obj)
        assert _object.confirm is generate_confirm_obj

    @pytest.mark.parametrize("generate_option_groups_object", [3], indirect=True)
    def test__it__focus_on_load(self, generate_option_groups_object):
        focus_on_load = True
        placeholder = "test"
        _object = StaticSelectMenuElement(placeholder=placeholder, option_groups=generate_option_groups_object,
                                          focus_on_load=focus_on_load)
        assert _object.focus_on_load is focus_on_load


class TestStaticMultiSelectMenuElement:
    @pytest.mark.parametrize("generate_optional_object", [3], indirect=True)
    def test__ut__type(self, generate_optional_object):
        placeholder = "test"
        _object = StaticMultiSelectMenuElement(placeholder=placeholder, options=generate_optional_object)
        assert _object.type == "multi_static_select"

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__initial_options(self, generate_optional_object):
        placeholder = "test"
        initial_options = generate_optional_object[:3]

        _object = StaticMultiSelectMenuElement(placeholder=placeholder, options=generate_optional_object,
                                               initial_options=initial_options)
        assert _object.initial_options is initial_options

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__max_selected_items(self, generate_optional_object):
        placeholder = "test"
        max_selected_items = 10

        _object = StaticMultiSelectMenuElement(placeholder=placeholder, options=generate_optional_object,
                                               max_selected_items=max_selected_items)
        assert _object.max_selected_items == max_selected_items


class TestExternalDataSourceSelectMenuElement:
    def test__ut__type(self):
        placeholder = "test"
        _object = ExternalDataSourceSelectMenuElement(placeholder=placeholder)
        assert _object.type == "external_select"

    def test__it__placeholder(self):
        placeholder = "test"
        _object = ExternalDataSourceSelectMenuElement(placeholder=placeholder)
        assert _object.placeholder.text == placeholder

    def test__it__action_id(self):
        placeholder = "test"
        action_id = "action11222"
        _object = ExternalDataSourceSelectMenuElement(placeholder=placeholder,
                                                      action_id=action_id)
        assert _object.action_id == action_id

    def test__it__min_query_length(self):
        placeholder = "test"
        min_query_length = 1
        _object = ExternalDataSourceSelectMenuElement(placeholder=placeholder,
                                                      min_query_length=min_query_length)
        assert _object.min_query_length == min_query_length

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__initial_option(self, generate_optional_object):
        placeholder = "test"
        initial_option = generate_optional_object[0]
        _object = ExternalDataSourceSelectMenuElement(placeholder=placeholder,
                                                      initial_option=initial_option)
        assert _object.initial_option is initial_option

    @pytest.mark.parametrize("generate_option_groups_object", [3], indirect=True)
    def test__it__confirm(self, generate_option_groups_object, generate_confirm_obj):
        placeholder = "test"
        _object = ExternalDataSourceSelectMenuElement(placeholder=placeholder,
                                                      confirm=generate_confirm_obj)
        assert _object.confirm is generate_confirm_obj

    @pytest.mark.parametrize("generate_option_groups_object", [3], indirect=True)
    def test__it__focus_on_load(self, generate_option_groups_object):
        focus_on_load = True
        placeholder = "test"
        _object = ExternalDataSourceSelectMenuElement(placeholder=placeholder,
                                                      focus_on_load=focus_on_load)
        assert _object.focus_on_load is focus_on_load


class TestExternalDataSourceMultiSelectMenuElement:
    def test__ut__type(self):
        placeholder = "test"
        _object = ExternalDataSourceMultiSelectMenuElement(placeholder=placeholder)
        assert _object.type == "multi_external_select"

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__initial_options(self, generate_optional_object):
        placeholder = "test"
        initial_options = generate_optional_object[:3]

        _object = ExternalDataSourceMultiSelectMenuElement(placeholder=placeholder,
                                                           initial_options=initial_options)
        assert _object.initial_options is initial_options

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__max_selected_items(self, generate_optional_object):
        placeholder = "test"
        max_selected_items = 10

        _object = ExternalDataSourceMultiSelectMenuElement(placeholder=placeholder,
                                                           max_selected_items=max_selected_items)
        assert _object.max_selected_items == max_selected_items


class TestUserListSelectMenuElement:
    def test__ut__type(self):
        placeholder = "test"
        _object = UserListSelectMenuElement(placeholder=placeholder)
        assert _object.type == "users_select"

    def test__it__placeholder(self):
        placeholder = "test"
        _object = UserListSelectMenuElement(placeholder=placeholder)
        assert _object.placeholder.text == placeholder

    def test__it__action_id(self):
        placeholder = "test"
        action_id = "action1122"
        _object = UserListSelectMenuElement(placeholder=placeholder, action_id=action_id)
        assert _object.action_id == action_id

    def test__it__initial_user(self):
        placeholder = "test"
        initial_user = "user#1"
        _object = UserListSelectMenuElement(placeholder=placeholder, initial_user=initial_user)
        assert _object.initial_user == initial_user

    def test__it__confirm(self, generate_confirm_obj):
        placeholder = "test"
        _object = UserListSelectMenuElement(placeholder=placeholder,
                                            confirm=generate_confirm_obj)
        assert _object.confirm is generate_confirm_obj

    def test__it__focus_on_load(self):
        focus_on_load = True
        placeholder = "test"
        _object = UserListSelectMenuElement(placeholder=placeholder,
                                            focus_on_load=focus_on_load)
        assert _object.focus_on_load is focus_on_load


class TestUserListMultiSelectMenuElement:
    def test__ut__type(self):
        placeholder = "test"
        _object = UserListMultiSelectMenuElement(placeholder=placeholder)
        assert _object.type == "multi_users_select"

    def test__it__initial_users(self):
        placeholder = "test"
        initial_users = ["user#1", "user#2"]
        _object = UserListMultiSelectMenuElement(placeholder=placeholder, initial_users=initial_users)
        assert _object.initial_users == initial_users

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__max_selected_items(self, generate_optional_object):
        placeholder = "test"
        max_selected_items = 10

        _object = UserListMultiSelectMenuElement(placeholder=placeholder,
                                                 max_selected_items=max_selected_items)
        assert _object.max_selected_items == max_selected_items


class TestConversationsListSelectMenuElement:
    def test__ut__type(self):
        placeholder = "test"
        _object = ConversationsListSelectMenuElement(placeholder=placeholder)
        assert _object.type == "conversations_select"

    def test__it__placeholder(self):
        placeholder = "test"
        _object = ConversationsListSelectMenuElement(placeholder=placeholder)
        assert _object.placeholder.text == placeholder

    def test__it__action_id(self):
        placeholder = "test"
        action_id = "action1122"
        _object = ConversationsListSelectMenuElement(placeholder=placeholder, action_id=action_id)
        assert _object.action_id == action_id

    def test__it__initial_conversation(self):
        placeholder = "test"
        initial_conversation = "conversation#1"
        _object = ConversationsListSelectMenuElement(placeholder=placeholder, initial_conversation=initial_conversation)
        assert _object.initial_conversation == initial_conversation

    def test__it__default_to_current_conversation(self):
        placeholder = "test"
        default_to_current_conversation = True
        _object = ConversationsListSelectMenuElement(placeholder=placeholder,
                                                     default_to_current_conversation=default_to_current_conversation)
        assert _object.default_to_current_conversation == default_to_current_conversation

    def test__it__confirm(self, generate_confirm_obj):
        placeholder = "test"
        _object = ConversationsListSelectMenuElement(placeholder=placeholder,
                                                     confirm=generate_confirm_obj)
        assert _object.confirm is generate_confirm_obj

    def test__it__filter(self):
        placeholder = "test"
        _filter = FilterObject()
        _object = ConversationsListSelectMenuElement(placeholder=placeholder,
                                                     filter=_filter)
        assert _object.filter is _filter

    def test__it__response_url_enabled(self):
        placeholder = "test"
        response_url_enabled = True
        _object = ConversationsListSelectMenuElement(placeholder=placeholder,
                                                     response_url_enabled=response_url_enabled)
        assert _object.response_url_enabled == response_url_enabled

    def test__it__focus_on_load(self):
        focus_on_load = True
        placeholder = "test"
        _object = ConversationsListSelectMenuElement(placeholder=placeholder,
                                                     focus_on_load=focus_on_load)
        assert _object.focus_on_load is focus_on_load


class TestConversationsListMultiSelectMenuElement:
    def test__ut__type(self):
        placeholder = "test"
        _object = ConversationsListMultiSelectMenuElement(placeholder=placeholder)
        assert _object.type == "multi_conversations_select"

    def test__it__initial_conversations(self):
        placeholder = "test"
        initial_conversations = ["onversation#1", "conversation#2"]
        _object = ConversationsListMultiSelectMenuElement(placeholder=placeholder,
                                                          initial_conversations=initial_conversations)
        assert _object.initial_conversations == initial_conversations

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__max_selected_items(self, generate_optional_object):
        placeholder = "test"
        max_selected_items = 10

        _object = ConversationsListMultiSelectMenuElement(placeholder=placeholder,
                                                          max_selected_items=max_selected_items)
        assert _object.max_selected_items == max_selected_items


class TestPublicChannelListSelectMenuElement:
    def test__ut__type(self):
        placeholder = "test"
        _object = PublicChannelListSelectMenuElement(placeholder=placeholder)
        assert _object.type == "channels_select"

    def test__it__placeholder(self):
        placeholder = "test"
        _object = PublicChannelListSelectMenuElement(placeholder=placeholder)
        assert _object.placeholder.text == placeholder

    def test__it__action_id(self):
        placeholder = "test"
        action_id = "action1122"
        _object = PublicChannelListSelectMenuElement(placeholder=placeholder, action_id=action_id)
        assert _object.action_id == action_id

    def test__it__initial_channel(self):
        placeholder = "test"
        initial_channel = "channel#1"
        _object = PublicChannelListSelectMenuElement(placeholder=placeholder, initial_channel=initial_channel)
        assert _object.initial_channel == initial_channel

    def test__it__confirm(self, generate_confirm_obj):
        placeholder = "test"
        _object = PublicChannelListSelectMenuElement(placeholder=placeholder,
                                                     confirm=generate_confirm_obj)
        assert _object.confirm is generate_confirm_obj

    def test__it__response_url_enabled(self):
        placeholder = "test"
        response_url_enabled = True
        _object = PublicChannelListSelectMenuElement(placeholder=placeholder,
                                                     response_url_enabled=response_url_enabled)
        assert _object.response_url_enabled == response_url_enabled

    def test__it__focus_on_load(self):
        focus_on_load = True
        placeholder = "test"
        _object = PublicChannelListSelectMenuElement(placeholder=placeholder,
                                            focus_on_load=focus_on_load)
        assert _object.focus_on_load is focus_on_load


class TestPublicChannelListMultiSelectMenuElement:
    def test__ut__type(self):
        placeholder = "test"
        _object = PublicChannelListMultiSelectMenuElement(placeholder=placeholder)
        assert _object.type == "multi_channels_select"

    def test__it__initial_channels(self):
        placeholder = "test"
        initial_channels = ["channel#1", "channel#2"]
        _object = PublicChannelListMultiSelectMenuElement(placeholder=placeholder,
                                                          initial_channels=initial_channels)
        assert _object.initial_channels == initial_channels

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__max_selected_items(self, generate_optional_object):
        placeholder = "test"
        max_selected_items = 10

        _object = PublicChannelListMultiSelectMenuElement(placeholder=placeholder,
                                                          max_selected_items=max_selected_items)
        assert _object.max_selected_items == max_selected_items


class TestOverflowMenuElement:
    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__ut__type(self, generate_optional_object):
        _object = OverflowMenuElement(options=generate_optional_object)
        assert _object.type == "overflow"

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__options(self, generate_optional_object):
        _object = OverflowMenuElement(options=generate_optional_object)
        assert _object.options is generate_optional_object

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__options(self, generate_optional_object):
        action_id = "action1234"
        _object = OverflowMenuElement(options=generate_optional_object,
                                      action_id=action_id)
        assert _object.action_id is action_id

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__confirm(self, generate_confirm_obj, generate_optional_object):
        _object = OverflowMenuElement(options=generate_optional_object,
                                      confirm=generate_confirm_obj)
        assert _object.confirm is generate_confirm_obj


class TestPlainTextInputElement:
    def test__ut__type(self):
        _object = PlainTextInputElement()
        assert _object.type == "plain_text_input"

    def test__it__action_id(self):
        action_id = "action1233"
        _object = PlainTextInputElement(action_id=action_id)
        assert _object.action_id == action_id

    def test__it__placeholder(self):
        placeholder = "action1233"
        _object = PlainTextInputElement(placeholder=placeholder)
        assert _object.placeholder.text == placeholder

    def test__it__initial_value(self):
        initial_value = "initial_value"
        _object = PlainTextInputElement(initial_value=initial_value)
        assert _object.initial_value == initial_value

    def test__it__multiline(self):
        multiline = True
        _object = PlainTextInputElement(multiline=multiline)
        assert _object.multiline is multiline

    def test__it__min_length(self):
        min_length = 10
        _object = PlainTextInputElement(min_length=min_length)
        assert _object.min_length == min_length

    def test__it__max_length(self):
        max_length = 10
        _object = PlainTextInputElement(max_length=max_length)
        assert _object.max_length == max_length

    def test__it__dispatch_action_config(self):
        dispatch_action_config = DispatchActionConfigurationObject(trigger_actions_on=["1", "2"])
        _object = PlainTextInputElement(dispatch_action_config=dispatch_action_config)
        assert _object.dispatch_action_config is dispatch_action_config

    def test__it__focus_on_load(self):
        focus_on_load = False
        _object = PlainTextInputElement(focus_on_load=focus_on_load)
        assert _object.focus_on_load is focus_on_load


class TestRadioButtonGroupElement:
    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__ut__type(self, generate_optional_object):
        _object = RadioButtonGroupElement(options=generate_optional_object)
        assert _object.type == "radio_buttons"

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__action_id(self, generate_optional_object):
        action_id = "action1231212"
        _object = RadioButtonGroupElement(options=generate_optional_object,
                                          action_id=action_id)
        assert _object.action_id == action_id

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__action_id(self, generate_optional_object):
        initial_option= generate_optional_object[0]
        _object = RadioButtonGroupElement(options=generate_optional_object,
                                          initial_option=initial_option)
        assert _object.initial_option is initial_option

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__confirm(self, generate_confirm_obj, generate_optional_object):
        _object = RadioButtonGroupElement(options=generate_optional_object,
                                          confirm=generate_confirm_obj)
        assert _object.confirm is generate_confirm_obj

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__focus_on_load(self, generate_confirm_obj, generate_optional_object):
        focus_on_load = True
        _object = RadioButtonGroupElement(options=generate_optional_object,
                                          focus_on_load=focus_on_load)
        assert _object.focus_on_load is focus_on_load


class TestTimePickerElement:
    def test__ut__type(self):
        _object = TimePickerElement()
        assert _object.type == "timepicker"

    def test__it__action_id(self):
        action_id = "action123331"
        _object = TimePickerElement(action_id=action_id)
        assert _object.action_id == action_id

    def test__it__placeholder(self):
        placeholder = "action123331"
        _object = TimePickerElement(placeholder=placeholder)
        assert _object.placeholder.text == placeholder

    def test__it__initial_time(self):
        initial_time = "09:01"
        _object = TimePickerElement(initial_time=initial_time)
        assert _object.initial_time == initial_time

    def test__it__confirm(self, generate_confirm_obj):
        _object = TimePickerElement(confirm=generate_confirm_obj)
        assert _object.confirm is generate_confirm_obj

    def test__it__focus_on_load(self):
        focus_on_load = False
        _object = TimePickerElement(focus_on_load=focus_on_load)
        assert _object.focus_on_load is focus_on_load


