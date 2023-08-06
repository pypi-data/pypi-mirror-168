#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : test_components__composition_block
# @Date : 2022-01-26-15-15
# @Project: content-service-chat-assistant
import pytest
from unittest import mock

from slack_block_builder.components.composition_block import *
from slack_block_builder.exception import *


class TestBlockAttributesCheckers:
    @pytest.fixture(scope="function")
    def obj_instance(self):
        return BlockAttributesCheckers()

    def test__ut__max_length_checker(self):
        _name = "test"
        _value = "1234567890"
        _length = 20
        BlockAttributesCheckers.max_length_checker(_name, _value, _length)

    def test__ut__max_length_checker__out_of_range(self):
        _name = "test"
        _value = "1234567890"
        _length = 5
        with pytest.raises(BlockElementOutOfRangeError):
            BlockAttributesCheckers.max_length_checker(_name, _value, _length)

    def test__ut__min_length_checker(self):
        _name = "test"
        _value = "1234567890"
        _length = 5
        BlockAttributesCheckers.min_length_checker(_name, _value, _length)

    def test__ut__min_length_checker__min(self):
        _name = "test"
        _value = "1234567890"
        _length = 20
        with pytest.raises(BlockMinimumOneElementError):
            BlockAttributesCheckers.min_length_checker(_name, _value, _length)

    def test__ut__type_checker(self):
        _name = "test"
        _value = "1234567890"
        _type = str
        BlockAttributesCheckers.type_checker(_name, _value, _type)

    def test__ut__type_checker__object(self):
        _name = "test"
        _value = TextObject(text="testing")
        _type = TextObject
        BlockAttributesCheckers.type_checker(_name, _value, _type)

    def test__ut__type_checker__type_error(self):
        _name = "test"
        _value = 2133
        _type = str
        with pytest.raises(BlockTypeError):
            BlockAttributesCheckers.type_checker(_name, _value, _type)

    @mock.patch.object(BlockAttributesCheckers, "max_length_checker")
    @mock.patch.object(BlockAttributesCheckers, "min_length_checker")
    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    def test__ut__string_length_checker(self,
                                        mock_type_checker,
                                        mock_min_length_checker,
                                        mock_max_length_checker,
                                        obj_instance):
        name = "Title"
        value = "value 1"
        maximum = 100
        minimum = 10
        obj_instance.string_length_checker(name, value, maximum, minimum)
        mock_type_checker.assert_called_once_with(name, value, str)
        mock_max_length_checker.assert_called_once_with(name, value, maximum)
        mock_min_length_checker.assert_called_once_with(name, value, minimum)

    @mock.patch.object(BlockAttributesCheckers, "max_length_checker")
    @mock.patch.object(BlockAttributesCheckers, "min_length_checker")
    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    def test__ut__list_length_checker(self,
                                      mock_type_checker,
                                      mock_min_length_checker,
                                      mock_max_length_checker,
                                      obj_instance):
        name = "Title"
        value = [1, 2, 3, 5]
        maximum = 100
        minimum = 10
        obj_instance.list_length_checker(name, value, maximum, minimum)
        mock_type_checker.assert_called_once_with(name, value, list)
        mock_max_length_checker.assert_called_once_with(name, value, maximum)
        mock_min_length_checker.assert_called_once_with(name, value, minimum)

    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    def test__ut__style_checker(self, mock_type_checker, obj_instance):
        _style = ColorScheme.Primary
        obj_instance.style_checker(_style)
        mock_type_checker.assert_called_once_with("style", _style, ColorScheme)

    def test__ut__style_checker__type_error(self, obj_instance):
        with pytest.raises(BlockTypeError):
            obj_instance.style_checker("dww")
        with pytest.raises(BlockTypeError):
            obj_instance.style_checker(1233)
        with pytest.raises(BlockTypeError):
            obj_instance.style_checker({})
        with pytest.raises(BlockTypeError):
            obj_instance.style_checker(Formatter.PlainText)

    def test__ut__style_checker(self, obj_instance):
        obj_instance.style_checker(ColorScheme.Primary)

    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    def test__ut__format_checker(self, mock_type_checker, obj_instance):
        _format = Formatter.MarkDown
        obj_instance.format_checker(_format)
        mock_type_checker.assert_called_once_with("formatter", _format, Formatter)

    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    def test__ut__option_obj_checker(self, mock_type_checker, obj_instance):
        _option = "option class"
        obj_instance.option_obj_checker(_option)
        mock_type_checker.assert_called_once_with("option", _option, OptionObject)

    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    def test__ut__option_group_obj_checker(self, mock_type_checker, obj_instance):
        _option_group = "option group class"
        obj_instance.option_group_obj_checker(_option_group)
        mock_type_checker.assert_called_once_with("option_group", _option_group, OptionGroupObject)

    @mock.patch.object(BlockAttributesCheckers, "list_length_checker")
    @mock.patch.object(BlockAttributesCheckers, "option_obj_checker")
    def test__ut__options_list_checker(self, mock_option_obj_checker, mock_list_length_checker, obj_instance):
        _name = "options"
        _options = [1, 2, 3, 4, 5]
        _maximum = 100
        _minimum = 10
        obj_instance.options_list_checker(name=_name, options=_options, maximum=_maximum, minimum=_minimum)
        mock_list_length_checker.assert_called_once_with(_name, _options, _maximum, _minimum)
        for element in _options:
            mock_option_obj_checker.assert_any_call(element)

    def test__it__options_list_checker(self, obj_instance):
        optional_1 = OptionObject(text="optional 1", value="value-1")
        optional_2 = OptionObject(text="optional 2", value="value-2")

        _name = "optional list"
        _values = [optional_1, optional_2]
        _min = 1
        _max = 5
        obj_instance.options_list_checker(_name, _values, _max, _min)

    def test__it__options_list_checker__min_error(self, obj_instance):
        _name = "optional list"
        _values = []
        _min = 1
        _max = 5
        with pytest.raises(BlockMinimumOneElementError):
            obj_instance.options_list_checker(_name, _values, _max, _min)

    def test__it__options_list_checker__max_error(self, obj_instance):
        optional_1 = OptionObject(text="optional 1", value="value-1")
        optional_2 = OptionObject(text="optional 2", value="value-2")

        _name = "optional list"
        _values = [optional_1, optional_2, optional_2]
        _min = 1
        _max = 2
        with pytest.raises(BlockElementOutOfRangeError):
            obj_instance.options_list_checker(_name, _values, _max, _min)

    def test__it__options_list_checker__optional_type_error(self, obj_instance):
        optional_1 = OptionObject(text="optional 1", value="value-1")
        optional_2 = OptionObject(text="optional 2", value="value-2")
        optional_3 = TextObject(text="text 1")

        _name = "optional list"
        _values = [optional_1, optional_2, optional_3]
        _min = 1
        _max = 5
        with pytest.raises(BlockTypeError):
            obj_instance.options_list_checker(_name, _values, _max, _min)

    @mock.patch.object(BlockAttributesCheckers, "list_length_checker")
    @mock.patch.object(BlockAttributesCheckers, "option_group_obj_checker")
    def test__ut__option_groups_checker(self, mock_option_group_obj_checker, mock_list_length_checker, obj_instance):
        _name = "options"
        _option_groups = [1, 2, 3, 4, 5]
        _maximum = 100
        obj_instance.option_groups_checker(_name, _option_groups, _maximum)
        mock_list_length_checker.assert_called_once_with(_name, _option_groups, _maximum, 1)
        for element in _option_groups:
            mock_option_group_obj_checker.assert_any_call(element)

    def test__it__option_groups_checker(self, obj_instance):
        optional_1 = OptionObject(text="optional 1", value="value-1")
        optional_2 = OptionObject(text="optional 2", value="value-2")
        optional_group_1 = OptionGroupObject(label="class 1", options=[optional_1, optional_1])
        optional_group_2 = OptionGroupObject(label="class 2", options=[optional_2, optional_2])
        _name = "optional group list"
        _values = [optional_group_1, optional_group_2]
        obj_instance.option_groups_checker(_name, _values, 100)

    def test__it__option_groups_checker__min_error(self, obj_instance):
        _name = "optional group list"
        _values = []
        _max = 100
        with pytest.raises(BlockMinimumOneElementError):
            obj_instance.option_groups_checker(_name, _values, _max)

    def test__it__option_groups_checker__max_error(self, obj_instance):
        optional_1 = OptionObject(text="optional 1", value="value-1")
        optional_2 = OptionObject(text="optional 2", value="value-2")
        optional_group_1 = OptionGroupObject(label="class 1", options=[optional_1, optional_1])
        optional_group_2 = OptionGroupObject(label="class 2", options=[optional_2, optional_2])
        _name = "optional group list"
        _values = [optional_group_1, optional_group_2, optional_group_1]
        _max = 2

        with pytest.raises(BlockElementOutOfRangeError):
            obj_instance.option_groups_checker(_name, _values, _max)

    def test__it__option_groups_checker(self, obj_instance):
        optional_1 = OptionObject(text="optional 1", value="value-1")
        optional_2 = OptionObject(text="optional 2", value="value-2")
        optional_group_1 = OptionGroupObject(label="class 1", options=[optional_1, optional_1])
        optional_group_2 = OptionGroupObject(label="class 2", options=[optional_2, optional_2])
        _name = "optional group list"
        _values = [optional_group_1, optional_group_2, "str"]
        _max = 5
        with pytest.raises(BlockTypeError):
            obj_instance.option_groups_checker(_name, _values, _max)

    @mock.patch.object(BlockAttributesCheckers, "min_length_checker")
    @mock.patch.object(BlockAttributesCheckers, "max_length_checker")
    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    def test__ut__list_string_checker(self, mock_type_checker, mock_max_length_checker, mock_min_length_checker,
                                      obj_instance):
        _name = "options"
        _option_groups = ["1", "2", "3"]
        obj_instance.list_string_checker(_name, _option_groups)
        mock_type_checker.assert_any_call(_name, _option_groups, list)
        mock_max_length_checker.assert_not_called()
        mock_min_length_checker.assert_not_called()
        for element in _option_groups:
            mock_type_checker.assert_any_call(f"{_name}-element", element, str)

    @mock.patch.object(BlockAttributesCheckers, "min_length_checker")
    @mock.patch.object(BlockAttributesCheckers, "max_length_checker")
    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    def test__ut__list_string_checker__max_limited(self, mock_type_checker, mock_max_length_checker,
                                                   mock_min_length_checker, obj_instance):
        _name = "options"
        _option_groups = ["1", "2", "3"]
        _maximum = 100
        obj_instance.list_string_checker(_name, _option_groups, _maximum)
        mock_type_checker.assert_any_call(_name, _option_groups, list)
        mock_max_length_checker.assert_called_once_with(_name, _option_groups, _maximum)
        mock_min_length_checker.assert_not_called()
        for element in _option_groups:
            mock_type_checker.assert_any_call(f"{_name}-element", element, str)

    @mock.patch.object(BlockAttributesCheckers, "min_length_checker")
    @mock.patch.object(BlockAttributesCheckers, "max_length_checker")
    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    def test__ut__list_string_checker__max_limited__min_limited(self, mock_type_checker, mock_max_length_checker,
                                                                mock_min_length_checker, obj_instance):
        _name = "options"
        _option_groups = ["1", "2", "3"]
        _maximum = 100
        _minimum = 10
        obj_instance.list_string_checker(_name, _option_groups, _maximum, _minimum)
        mock_type_checker.assert_any_call(_name, _option_groups, list)
        mock_max_length_checker.assert_called_once_with(_name, _option_groups, _maximum)
        mock_min_length_checker.assert_called_once_with(_name, _option_groups, _minimum)
        for element in _option_groups:
            mock_type_checker.assert_any_call(f"{_name}-element", element, str)


class TestBlockAttributesConstructor:
    @pytest.fixture(scope="function")
    def empty_instance(self):
        class Empty(object):
            pass

        return Empty()

    @pytest.fixture(scope="function")
    def block_attr_constructor_instance(self, empty_instance):
        return BlockAttributesConstructor(empty_instance)

    def test__ut__attributes(self, empty_instance):
        block_attr = BlockAttributesConstructor(empty_instance)
        assert block_attr._object == empty_instance
        assert isinstance(block_attr._checker, BlockAttributesCheckers)
        assert block_attr._kwargs == {}

    def test__ut__attributes__1(self, empty_instance):
        block_attr = BlockAttributesConstructor(empty_instance, options_max=10)
        assert block_attr._object == empty_instance
        assert isinstance(block_attr._checker, BlockAttributesCheckers)
        assert block_attr._kwargs.get("options_max") == 10

    def test__ut__set_attributes(self, block_attr_constructor_instance):
        _name = "Name"
        _value = "value 1"
        block_attr_constructor_instance._set_attribute(_name, _value)
        assert getattr(block_attr_constructor_instance._object, _name, None) == _value

    def test__ut__set_attributes__with_instance(self, block_attr_constructor_instance, empty_instance):
        _name = "Name"
        _value = "value 1"

        class TestingInstance:
            pass

        _testing = TestingInstance()
        block_attr_constructor_instance._set_attribute(_name, _value, instance=_testing)
        assert getattr(block_attr_constructor_instance._object, _name, None) is None
        assert getattr(_testing, _name, None) == _value

    def test__ut__del_attributes(self, block_attr_constructor_instance):
        block_attr_constructor_instance._object.name = "1"
        assert getattr(block_attr_constructor_instance._object, "name", None) == "1"
        block_attr_constructor_instance._del_attribute("name")
        assert getattr(block_attr_constructor_instance._object, "name", None) is None

    def test__ut__del_attributes__with_instance(self, block_attr_constructor_instance, empty_instance):
        class TestingInstance:
            def __init__(self):
                self.name = "1"
                self.value = "2"

        _testing = TestingInstance()
        block_attr_constructor_instance._del_attribute("name", _testing)
        assert getattr(_testing, "name", None) is None

    def test__ut__get_attributes(self, block_attr_constructor_instance):
        assert block_attr_constructor_instance._get_attribute("name") is None

    def test__ut__get_attributes_1(self, block_attr_constructor_instance):
        block_attr_constructor_instance._object.name = "111"
        assert block_attr_constructor_instance._get_attribute("name") == "111"

    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_textobj_text(self, mock_set_attribute, mock_type_checker, block_attr_constructor_instance):
        _text = "testing"
        block_attr_constructor_instance.edit_textobj_text(_text)
        mock_type_checker.assert_called_once_with("text", _text, str)
        mock_set_attribute("text", _text)

    def test__it__edit_textobj_text__errors(self, block_attr_constructor_instance):
        with pytest.raises(BlockTypeError):
            block_attr_constructor_instance.edit_textobj_text(1)
        with pytest.raises(BlockTypeError):
            block_attr_constructor_instance.edit_textobj_text([])
        with pytest.raises(BlockTypeError):
            block_attr_constructor_instance.edit_textobj_text({})

    @pytest.mark.parametrize("generate_str", [10000], indirect=True)
    def test__it__edit_textobj_text__errors(self, block_attr_constructor_instance, generate_str):
        block_attr_constructor_instance.edit_textobj_text(generate_str)
        assert block_attr_constructor_instance._object.text == generate_str

    @mock.patch.object(BlockAttributesCheckers, "format_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    @mock.patch.object(BlockAttributesConstructor, "_get_attribute")
    @mock.patch.object(BlockAttributesConstructor, "_del_attribute")
    def test__ut__edit_textobj_formatter(self, mock_del_attribute, mock_get_attribute, mock_set_attribute, mock_format_checker, block_attr_constructor_instance):
        _format = Formatter.PlainText
        mock_get_attribute.return_value = None
        block_attr_constructor_instance.edit_textobj_formatter(_format)
        mock_format_checker.assert_called_once_with(_format)
        mock_set_attribute("type", _format.value)
        mock_get_attribute.assert_called_once_with("verbatim")
        mock_del_attribute.assert_not_called()

    @mock.patch.object(BlockAttributesCheckers, "format_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    @mock.patch.object(BlockAttributesConstructor, "_get_attribute")
    @mock.patch.object(BlockAttributesConstructor, "_del_attribute")
    def test__ut__edit_textobj_formatter_1(self, mock_del_attribute, mock_get_attribute, mock_set_attribute, mock_format_checker, block_attr_constructor_instance):
        _format = Formatter.MarkDown
        mock_get_attribute.return_value = None
        block_attr_constructor_instance.edit_textobj_formatter(_format)
        mock_format_checker.assert_called_once_with(_format)
        mock_set_attribute("type", _format.value)
        mock_get_attribute.assert_called_once_with("emoji")
        mock_del_attribute.assert_not_called()

    @mock.patch.object(BlockAttributesCheckers, "format_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    @mock.patch.object(BlockAttributesConstructor, "_get_attribute")
    @mock.patch.object(BlockAttributesConstructor, "_del_attribute")
    def test__ut__edit_textobj_formatter_3(self, mock_del_attribute, mock_get_attribute, mock_set_attribute, mock_format_checker, block_attr_constructor_instance):
        _format = Formatter.PlainText
        mock_get_attribute.return_value = True
        block_attr_constructor_instance.edit_textobj_formatter(_format)
        mock_format_checker.assert_called_once_with(_format)
        mock_set_attribute("type", _format.value)
        mock_get_attribute.assert_called_once_with("verbatim")
        mock_del_attribute.assert_called_once_with("verbatim")

    @mock.patch.object(BlockAttributesCheckers, "format_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    @mock.patch.object(BlockAttributesConstructor, "_get_attribute")
    @mock.patch.object(BlockAttributesConstructor, "_del_attribute")
    def test__ut__edit_textobj_formatter_4(self, mock_del_attribute, mock_get_attribute, mock_set_attribute, mock_format_checker, block_attr_constructor_instance):
        _format = Formatter.MarkDown
        mock_get_attribute.return_value = True
        block_attr_constructor_instance.edit_textobj_formatter(_format)
        mock_format_checker.assert_called_once_with(_format)
        mock_set_attribute("type", _format.value)
        mock_get_attribute.assert_called_once_with("emoji")
        mock_del_attribute.assert_called_once_with("emoji")

    def test__it__edit_textobj_formatter(self, block_attr_constructor_instance):
        _format = Formatter.PlainText
        block_attr_constructor_instance.edit_textobj_formatter(_format)
        assert block_attr_constructor_instance._object.type == _format.value

    def test__it__edit_textobj_formatter__emoji_del(self, block_attr_constructor_instance):
        block_attr_constructor_instance._object.emoji = True
        _format = Formatter.MarkDown
        block_attr_constructor_instance.edit_textobj_formatter(_format)
        assert block_attr_constructor_instance._object.type == _format.value
        assert getattr(block_attr_constructor_instance._object, "emoji", None) is None

    def test__it__edit_textobj_formatter__verbatim_del(self, block_attr_constructor_instance):
        block_attr_constructor_instance._object.verbatim = True
        _format = Formatter.PlainText
        block_attr_constructor_instance.edit_textobj_formatter(_format)
        assert block_attr_constructor_instance._object.type == _format.value
        assert getattr(block_attr_constructor_instance._object, "verbatim", None) is None

    def test__it__edit_textobj_formatter__errors(self, block_attr_constructor_instance):
        with pytest.raises(BlockTypeError):
            block_attr_constructor_instance.edit_textobj_formatter(ColorScheme.Primary)
        with pytest.raises(BlockTypeError):
            block_attr_constructor_instance.edit_textobj_formatter("primary")
        with pytest.raises(BlockTypeError):
            block_attr_constructor_instance.edit_textobj_formatter(["primary"])

    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_textobj_emoji(self, mock_set_attribute, mock_type_checker, block_attr_constructor_instance):
        block_attr_constructor_instance._object.type = Formatter.PlainText.value
        emoji = True
        block_attr_constructor_instance.edit_textobj_emoji(emoji)
        mock_type_checker.assert_called_once_with("emoji", emoji, bool)
        mock_set_attribute.assert_called_once_with("emoji", emoji)

    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_textobj_emoji__non_plain_type(self, mock_set_attribute, mock_type_checker, block_attr_constructor_instance):
        block_attr_constructor_instance._object.type = Formatter.MarkDown.value
        emoji = True
        block_attr_constructor_instance.edit_textobj_emoji(emoji)
        mock_type_checker.assert_not_called()
        mock_set_attribute.assert_not_called()

    def test__it__edit_textobj_emoji(self, block_attr_constructor_instance):
        block_attr_constructor_instance._object.type = Formatter.PlainText.value
        emoji = True
        assert getattr(block_attr_constructor_instance._object, "emoji", None) is None
        block_attr_constructor_instance.edit_textobj_emoji(emoji)
        assert getattr(block_attr_constructor_instance._object, "emoji", None) == emoji

    def test__it__edit_textobj_emoji_1(self, block_attr_constructor_instance):
        block_attr_constructor_instance._object.type = Formatter.MarkDown.value
        emoji = True
        assert getattr(block_attr_constructor_instance._object, "emoji", None) is None
        block_attr_constructor_instance.edit_textobj_emoji(emoji)
        assert getattr(block_attr_constructor_instance._object, "emoji", None) is None

    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_textobj_verbatim(self, mock_set_attribute, mock_type_checker, block_attr_constructor_instance):
        block_attr_constructor_instance._object.type = Formatter.MarkDown.value
        verbatim = True
        block_attr_constructor_instance.edit_textobj_verbatim(verbatim)
        mock_type_checker.assert_called_once_with("verbatim", verbatim, bool)
        mock_set_attribute.assert_called_once_with("verbatim", verbatim)

    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_textobj_verbatim_1(self, mock_set_attribute, mock_type_checker, block_attr_constructor_instance):
        block_attr_constructor_instance._object.type = Formatter.PlainText.value
        verbatim = True
        block_attr_constructor_instance.edit_textobj_verbatim(verbatim)
        mock_type_checker.assert_not_called()
        mock_set_attribute.assert_not_called()

    def test__it__edit_textobj_verbatim(self, block_attr_constructor_instance):
        block_attr_constructor_instance._object.type = Formatter.MarkDown.value
        verbatim = True
        assert getattr(block_attr_constructor_instance._object, "verbatim", None) is None
        block_attr_constructor_instance.edit_textobj_verbatim(verbatim)
        assert getattr(block_attr_constructor_instance._object, "verbatim", None) == verbatim

    def test__it__edit_textobj_verbatim(self, block_attr_constructor_instance):
        block_attr_constructor_instance._object.type = Formatter.PlainText.value
        verbatim = True
        assert getattr(block_attr_constructor_instance._object, "verbatim", None) is None
        block_attr_constructor_instance.edit_textobj_verbatim(verbatim)
        assert getattr(block_attr_constructor_instance._object, "verbatim", None) is None

    @mock.patch.object(BlockAttributesCheckers, "string_length_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_title(self, mock_set_attributes, mock_string_length_checker, block_attr_constructor_instance):
        text = "d2dwad"
        with mock.patch("slack_block_builder.components.composition_block.TextObject") as MockTextObject:
            block_attr_constructor_instance.edit_title(text)
            mock_string_length_checker.assert_called_once_with("title", text, 100)
            mock_set_attributes.assert_any_call("title", MockTextObject(text))

    @pytest.mark.parametrize("generate_str", [101], indirect=True)
    def test__it__edit_title__errors(self, block_attr_constructor_instance, generate_str):
        with pytest.raises(BlockTypeError):
            block_attr_constructor_instance.edit_title(1)
        with pytest.raises(BlockTypeError):
            block_attr_constructor_instance.edit_title([])
        with pytest.raises(BlockTypeError):
            block_attr_constructor_instance.edit_title({})

    @pytest.mark.parametrize("generate_str", [100], indirect=True)
    def test__it__edit_title__errors(self, block_attr_constructor_instance, generate_str):
        block_attr_constructor_instance.edit_title(generate_str)
        assert isinstance(block_attr_constructor_instance._object.title, TextObject)
        assert block_attr_constructor_instance._object.title.text == generate_str
        assert block_attr_constructor_instance._object.title.type == Formatter.PlainText.value

    @mock.patch.object(BlockAttributesCheckers, "format_checker")
    @mock.patch.object(BlockAttributesCheckers, "string_length_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_text(self, mock_set_attributes, mock_string_length_checker, mock_format_checker, block_attr_constructor_instance):
        text = "d2dwad"
        block_attr_constructor_instance.edit_text(text)
        mock_format_checker.assert_any_call(Formatter.PlainText)
        mock_string_length_checker.assert_called_once_with("text", text, 300)
        mock_set_attributes("text", TextObject(text, formatter=Formatter.PlainText))

    @mock.patch.object(BlockAttributesCheckers, "format_checker")
    @mock.patch.object(BlockAttributesCheckers, "string_length_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_text__with_format(self, mock_set_attributes, mock_string_length_checker, mock_format_checker, block_attr_constructor_instance):
        text = "d2dwad"
        _format = Formatter.MarkDown
        block_attr_constructor_instance.edit_text(text, _format)
        mock_format_checker.assert_any_call(Formatter.MarkDown)
        mock_string_length_checker.assert_called_once_with("text", text, 300)
        mock_set_attributes("text", TextObject(text, formatter=Formatter.MarkDown))

    @mock.patch.object(BlockAttributesCheckers, "format_checker")
    @mock.patch.object(BlockAttributesCheckers, "string_length_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_text__change_max_lim(self, mock_set_attributes, mock_string_length_checker, mock_format_checker, block_attr_constructor_instance):
        max_lim = 400
        block_attr_constructor_instance._kwargs["text_max"] = max_lim
        text = "d2dwad"
        _format = Formatter.MarkDown
        block_attr_constructor_instance.edit_text(text, _format)
        mock_format_checker.assert_any_call(Formatter.MarkDown)
        mock_string_length_checker.assert_called_once_with("text", text, max_lim)
        mock_set_attributes("text", TextObject(text, formatter=Formatter.MarkDown))

    def test__it__edit_text(self, block_attr_constructor_instance):
        text = "new test string"
        block_attr_constructor_instance.edit_text(text)
        assert block_attr_constructor_instance._object.text.text == text
        assert block_attr_constructor_instance._object.text.type == Formatter.PlainText.value
        assert getattr(block_attr_constructor_instance._object.text, "emoji", None) is None

    def test__it__edit_text__none_formatter(self, block_attr_constructor_instance):
        text = "new test string"
        block_attr_constructor_instance.edit_text(text, formatter=None)
        assert block_attr_constructor_instance._object.text.text == text
        assert block_attr_constructor_instance._object.text.type == Formatter.PlainText.value
        assert getattr(block_attr_constructor_instance._object.text, "emoji", None) is None

    def test__it__edit_text__with_emoji(self, block_attr_constructor_instance):
        text = "new test string"
        block_attr_constructor_instance.edit_text(text, emoji=True)
        assert block_attr_constructor_instance._object.text.text == text
        assert block_attr_constructor_instance._object.text.type == Formatter.PlainText.value
        assert block_attr_constructor_instance._object.text.emoji is True

    def test__it__edit_text__errors(self, block_attr_constructor_instance):
        text = TextObject("new")
        with pytest.raises(BlockTypeError):
            block_attr_constructor_instance.edit_text(text)

    @mock.patch.object(BlockAttributesCheckers, "string_length_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_confirm(self, mock_set_attribute, mock_string_length_checker, block_attr_constructor_instance):
        confirm = "Confirm"
        block_attr_constructor_instance.edit_confirm(confirm)
        mock_string_length_checker("confirm", confirm, 30)
        mock_set_attribute("confirm", TextObject(confirm, formatter=Formatter.PlainText))

    @mock.patch.object(BlockAttributesCheckers, "string_length_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_deny(self, mock_set_attribute, mock_string_length_checker, block_attr_constructor_instance):
        deny = "Deny"
        block_attr_constructor_instance.edit_deny(deny)
        mock_string_length_checker("deny", deny, 30)
        mock_set_attribute("deny", TextObject(deny, formatter=Formatter.PlainText))

    @mock.patch.object(BlockAttributesCheckers, "style_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_style(self, mock_set_attribute, mock_style_checker, block_attr_constructor_instance):
        style = ColorScheme.Primary
        block_attr_constructor_instance.edit_style(style)
        mock_style_checker(style)
        mock_set_attribute("style", style.value)

    @mock.patch.object(BlockAttributesCheckers, "string_length_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_value(self, mock_set_attribute, mock_string_length_checker, block_attr_constructor_instance):
        value = "Value"
        block_attr_constructor_instance.edit_value(value)
        mock_string_length_checker("value", value, 75)
        mock_set_attribute("value", value)

    @mock.patch.object(BlockAttributesCheckers, "string_length_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_description(self, mock_set_attribute, mock_string_length_checker, block_attr_constructor_instance):
        description = "description"
        block_attr_constructor_instance.edit_description(description)
        mock_string_length_checker("description", description, 75)
        mock_set_attribute("description", TextObject(description))

    @mock.patch.object(BlockAttributesCheckers, "string_length_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_url(self, mock_set_attribute, mock_string_length_checker, block_attr_constructor_instance):
        url = "https://my.testing.net"
        block_attr_constructor_instance.edit_url(url)
        mock_string_length_checker("url", url, 3000)
        mock_set_attribute("url", url)

    @mock.patch.object(BlockAttributesCheckers, "string_length_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_label(self, mock_set_attribute, mock_string_length_checker, block_attr_constructor_instance):
        label = "new label"
        block_attr_constructor_instance.edit_label(label)
        mock_string_length_checker("label", label, 75)
        mock_set_attribute("label", label)

    @mock.patch.object(BlockAttributesCheckers, "string_length_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_label__label_max(self, mock_set_attribute, mock_string_length_checker, block_attr_constructor_instance):
        label = "new label"
        block_attr_constructor_instance._kwargs['label_max'] = 2000
        block_attr_constructor_instance.edit_label(label)
        mock_string_length_checker("label", label, 2000)
        mock_set_attribute("label", label)

    @mock.patch.object(BlockAttributesCheckers, "options_list_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_options(self, mock_set_attribute, mock_options_list_checker, block_attr_constructor_instance):
        options = [mock.Mock(), mock.Mock()]
        block_attr_constructor_instance.edit_options(options)
        mock_options_list_checker("options", options, 100)
        mock_set_attribute("options", options)

    @mock.patch.object(BlockAttributesCheckers, "options_list_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_options__change_max_lim(self, mock_set_attribute, mock_options_list_checker, block_attr_constructor_instance):
        max_lim = 200
        block_attr_constructor_instance._kwargs['options_max'] = 200
        options = [mock.Mock(), mock.Mock()]
        block_attr_constructor_instance.edit_options(options)
        mock_options_list_checker("options", options, max_lim)
        mock_set_attribute("options", options)

    @mock.patch.object(BlockAttributesCheckers, "list_string_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_include(self, mock_set_attribute, mock_list_string_checker, block_attr_constructor_instance):
        includes = ["string1", "string2"]
        block_attr_constructor_instance.edit_include(includes)
        mock_list_string_checker("includes", includes)
        mock_set_attribute("includes", includes)

    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_exclude_external_shared_channels(self, mock_set_attribute, mock_type_checker, block_attr_constructor_instance):
        exclude_external_shared_channels = True
        block_attr_constructor_instance.edit_exclude_external_shared_channels(exclude_external_shared_channels)
        mock_type_checker("exclude_external_shared_channels", exclude_external_shared_channels, bool)
        mock_set_attribute("exclude_external_shared_channels", exclude_external_shared_channels)

    @mock.patch.object(BlockAttributesCheckers, "type_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_exclude_bot_users(self, mock_set_attribute, mock_type_checker, block_attr_constructor_instance):
        exclude_bot_users = True
        block_attr_constructor_instance.edit_exclude_bot_users(exclude_bot_users)
        mock_type_checker("exclude_bot_users", exclude_bot_users, bool)
        mock_set_attribute("exclude_bot_users", exclude_bot_users)

    @mock.patch.object(BlockAttributesCheckers, "list_string_checker")
    @mock.patch.object(BlockAttributesConstructor, "_set_attribute")
    def test__ut__edit_trigger_actions_on(self, mock_set_attribute, mock_list_string_checker, block_attr_constructor_instance):
        trigger_actions_on = ["string1", "string2"]
        block_attr_constructor_instance.edit_trigger_actions_on(trigger_actions_on)
        mock_list_string_checker("trigger_actions_on", trigger_actions_on)
        mock_set_attribute("trigger_actions_on", trigger_actions_on)


class TestTextObject:
    def test__ut__text(self):
        _text = "New"
        text_obj = TextObject(text=_text)
        assert text_obj.text == _text
        assert text_obj.type == Formatter.PlainText.value

    def test__ut__markdown_format(self):
        _text = "New"
        _format = Formatter.MarkDown
        text_obj = TextObject(text=_text, formatter=_format)
        assert text_obj.text == _text
        assert text_obj.type == _format.value

    def test__ut__emoji_not_support_on_markdown(self):
        _text = "New"
        _format = Formatter.MarkDown
        text_obj = TextObject(text=_text, formatter=_format)
        assert text_obj.text == _text
        assert text_obj.type == _format.value
        assert getattr(text_obj, "emoji", None) is None

    def test__ut__verbatim(self):
        _text = "New"
        _format = Formatter.MarkDown
        text_obj = TextObject(text=_text, formatter=_format, emoji=True, verbatim=True)
        assert text_obj.text == _text
        assert text_obj.type == _format.value
        assert getattr(text_obj, "emoji", None) is None
        assert text_obj.verbatim is True

    def test__ut__emoji_on_plain_text(self):
        _text = "New"
        _format = Formatter.PlainText
        text_obj = TextObject(text=_text, formatter=_format, emoji=True)
        assert text_obj.text == _text
        assert text_obj.type == _format.value
        assert getattr(text_obj, "emoji", None) is True

    def test__ut__no_verbatim_on_plain_text(self):
        _text = "New"
        _format = Formatter.PlainText
        text_obj = TextObject(text=_text, formatter=_format, emoji=True, verbatim=True)
        assert text_obj.text == _text
        assert text_obj.type == _format.value
        assert getattr(text_obj, "emoji", None) is True
        assert getattr(text_obj, "verbatim", None) is None


class TestConfirmationDialogObject:
    @pytest.mark.parametrize("generate_str", [101], indirect=True)
    def test__ut__title_len_error(self, generate_str):
        _title = generate_str
        _text = "xxxx"
        _confirm = "confirm"
        _deny = "deny"
        with pytest.raises(BlockElementOutOfRangeError):
            ConfirmationDialogObject(title=_title,
                                     text=_text,
                                     confirm=_confirm,
                                     deny=_deny)

    @pytest.mark.parametrize("generate_str", [100], indirect=True)
    def test__ut__title(self, generate_str):
        _title = generate_str
        _text = "xxxx"
        _confirm = "confirm"
        _deny = "deny"
        ConfirmationDialogObject(title=_title,
                                 text=_text,
                                 confirm=_confirm,
                                 deny=_deny)

    @pytest.mark.parametrize("generate_str", [301], indirect=True)
    def test__ut__text_len_error(self, generate_str):
        _title = "xxxxxxx"
        _text = generate_str
        _confirm = "confirm"
        _deny = "deny"
        with pytest.raises(BlockElementOutOfRangeError):
            ConfirmationDialogObject(title=_title,
                                     text=_text,
                                     confirm=_confirm,
                                     deny=_deny)

    @pytest.mark.parametrize("generate_str", [300], indirect=True)
    def test__ut__text(self, generate_str):
        _title = "xxxxxxx"
        _text = generate_str
        _confirm = "confirm"
        _deny = "deny"
        ConfirmationDialogObject(title=_title,
                                 text=_text,
                                 confirm=_confirm,
                                 deny=_deny)

    @pytest.mark.parametrize("generate_str", [31], indirect=True)
    def test__ut__confirm_len_error(self, generate_str):
        _title = "xxxxxxx"
        _text = "texting"
        _confirm = generate_str
        _deny = "deny"
        with pytest.raises(BlockElementOutOfRangeError):
            ConfirmationDialogObject(title=_title,
                                     text=_text,
                                     confirm=_confirm,
                                     deny=_deny)

    @pytest.mark.parametrize("generate_str", [30], indirect=True)
    def test__ut__confirm(self, generate_str):
        _title = "xxxxxxx"
        _text = "texting"
        _confirm = generate_str
        _deny = "deny"
        ConfirmationDialogObject(title=_title,
                                 text=_text,
                                 confirm=_confirm,
                                 deny=_deny)

    @pytest.mark.parametrize("generate_str", [31], indirect=True)
    def test__ut__deny_len_error(self, generate_str):
        _title = "xxxxxxx"
        _text = "texting"
        _confirm = "confirm"
        _deny = generate_str
        with pytest.raises(BlockElementOutOfRangeError):
            ConfirmationDialogObject(title=_title,
                                     text=_text,
                                     confirm=_confirm,
                                     deny=_deny)

    @pytest.mark.parametrize("generate_str", [30], indirect=True)
    def test__ut__deny(self, generate_str):
        _title = "xxxxxxx"
        _text = "texting"
        _confirm = "confirm"
        _deny = generate_str
        ConfirmationDialogObject(title=_title,
                                 text=_text,
                                 confirm=_confirm,
                                 deny=_deny)

    def test__ut__style(self):
        _title = "xxxxxxx"
        _text = "texting"
        _confirm = "confirm"
        _deny = "deny"
        ConfirmationDialogObject(title=_title,
                                 text=_text,
                                 confirm=_confirm,
                                 deny=_deny,
                                 style=ColorScheme.Danger)

    def test__ut__style_error(self):
        _title = "xxxxxxx"
        _text = "texting"
        _confirm = "confirm"
        _deny = "deny"
        with pytest.raises(BlockTypeError):
            ConfirmationDialogObject(title=_title,
                                     text=_text,
                                     confirm=_confirm,
                                     deny=_deny,
                                     style="danger")

    def test__ut__attrs(self):
        _title = "xxxxxxx"
        _text = "texting"
        _text_format = Formatter.MarkDown
        _confirm = "confirm"
        _deny = "deny"
        _style = ColorScheme.Primary
        confirm_block = ConfirmationDialogObject(title=_title,
                                                 text=_text,
                                                 text_format=_text_format,
                                                 confirm=_confirm,
                                                 deny=_deny,
                                                 style=_style)
        assert confirm_block.title.text == _title
        assert confirm_block.text.text == _text
        assert confirm_block.text.type == _text_format.value
        assert confirm_block.confirm.text == _confirm
        assert confirm_block.deny.text == _deny
        assert confirm_block.style == _style.value


class TestOptionObject:
    @pytest.mark.parametrize("generate_str", [76], indirect=True)
    def test__ut__out_of_range_text(self, generate_str):
        text = generate_str
        value = "value-1"
        with pytest.raises(BlockElementOutOfRangeError):
            OptionObject(text, value)

    @pytest.mark.parametrize("generate_str", [75], indirect=True)
    def test__ut__text(self, generate_str):
        text = generate_str
        value = "value-1"
        option_obj = OptionObject(text, value)
        assert option_obj.text.text == text
        assert option_obj.text.type == Formatter.PlainText.value

    @pytest.mark.parametrize("generate_str", [75], indirect=True)
    def test__ut__text_formatter(self, generate_str):
        text = generate_str
        value = "value-1"
        formatter = Formatter.MarkDown
        option_obj = OptionObject(text, value, text_format=formatter)
        assert option_obj.text.text == text
        assert option_obj.text.type == Formatter.MarkDown.value

    @pytest.mark.parametrize("generate_str", [76], indirect=True)
    def test__ut__out_of_range_value(self, generate_str):
        text = "texting"
        value = generate_str
        with pytest.raises(BlockElementOutOfRangeError):
            OptionObject(text, value)

    @pytest.mark.parametrize("generate_str", [75], indirect=True)
    def test__ut__value(self, generate_str):
        text = "texting"
        value = generate_str
        option_obj = OptionObject(text, value)
        assert option_obj.value == value

    @pytest.mark.parametrize("generate_str", [76], indirect=True)
    def test__ut__out_of_range_description(self, generate_str):
        text = "texting"
        value = "value-1"
        description = generate_str
        with pytest.raises(BlockElementOutOfRangeError):
            OptionObject(text, value, description=description)

    @pytest.mark.parametrize("generate_str", [75], indirect=True)
    def test__ut__description(self, generate_str):
        text = "texting"
        value = generate_str
        description = generate_str
        option_obj = OptionObject(text, value, description=description)
        assert option_obj.description.text == description
        assert option_obj.description.type == Formatter.PlainText.value

    @pytest.mark.parametrize("generate_str", [3001], indirect=True)
    def test__ut__out_of_range_url(self, generate_str):
        text = "texting"
        value = "value-1"
        url = generate_str
        with pytest.raises(BlockElementOutOfRangeError):
            OptionObject(text, value, url=url)

    @pytest.mark.parametrize("generate_str", [3000], indirect=True)
    def test__ut__url(self, generate_str):
        text = "texting"
        value = "value-1"
        url = generate_str
        option_obj = OptionObject(text, value, url=url)
        assert option_obj.url == url


class TestOptionGroupObject:
    @pytest.mark.parametrize("generate_str", [76], indirect=True)
    def test__ut__out_of_range_label(self, generate_str):
        label = generate_str
        option_1 = OptionObject(text="option 1", value="value-1")
        option_2 = OptionObject(text="option 2", value="value-2")
        with pytest.raises(BlockElementOutOfRangeError):
            OptionGroupObject(label, [option_1, option_2])

    @pytest.mark.parametrize("generate_str", [75], indirect=True)
    def test__ut__label(self, generate_str):
        label = generate_str
        option_1 = OptionObject(text="option 1", value="value-1")
        option_2 = OptionObject(text="option 2", value="value-2")
        option_group = OptionGroupObject(label, [option_1, option_2])
        option_group.label.text == label

    @pytest.mark.parametrize("generate_optional_object", [101], indirect=True)
    def test__ut__out_of_range__options(self, generate_optional_object):
        label = "option groups"
        options = generate_optional_object
        with pytest.raises(BlockElementOutOfRangeError):
            OptionGroupObject(label, options)

    @pytest.mark.parametrize("generate_optional_object", [100], indirect=True)
    def test__ut__options(self, generate_optional_object):
        label = "option groups"
        options = generate_optional_object
        optional_group = OptionGroupObject(label, options)
        assert len(optional_group.options) == len(options)
        for option in optional_group.options:
            assert isinstance(option, OptionObject)


class TestFilterObject:
    def test__ut__include_type_error(self):
        include = {}
        with pytest.raises(BlockTypeError):
            FilterObject(include=include)

    def test__ut__include(self):
        include = ["master", "master2"]
        filter_obj = FilterObject(include=include)
        assert filter_obj.include == include

    def test__ut__exclude_external_shared_channels_type_error(self):
        with pytest.raises(BlockTypeError):
            FilterObject(exclude_external_shared_channels="x")

    def test__ut__exclude_external_shared_channels(self):
        filter_obj = FilterObject(exclude_external_shared_channels=True)
        assert filter_obj.exclude_external_shared_channels is True

    def test__ut__exclude_exclude_bot_users_type_error(self):
        with pytest.raises(BlockTypeError):
            FilterObject(exclude_bot_users="x")


class TestDispatchActionConfigurationObject:
    def test__ut__trigger_actions_on_type_error(self):
        with pytest.raises(BlockTypeError):
            DispatchActionConfigurationObject({})
            DispatchActionConfigurationObject("dww")

    def test__ut__trigger_action_on_type(self):
        trigger = ["action"]
        dispatch = DispatchActionConfigurationObject(trigger)
        assert dispatch.trigger_actions_on == trigger
