# -*- coding: utf-8 -*-
# @Filename : test_components_layout_attrs
# @Date : 2022-03-08-13-13
# @Project: content-service-chat-assistant


import pytest
from unittest import mock
from slack_block_builder.components import (
    LayoutBlockAttributeConstructor,
    LayoutBlockAttributesCheckers,
    Formatter
)


class TestLayoutBlockAttributesChecker:
    @pytest.fixture(scope="function")
    def obj_instance(self):
        return LayoutBlockAttributesCheckers()

    @mock.patch.object(LayoutBlockAttributesCheckers, "string_length_checker")
    def test__it__block_id_checker(self, mock_string_length_checker, obj_instance):
        block_id = "1231"
        obj_instance.block_id_checker(block_id)
        mock_string_length_checker.assert_called_once_with("block_id", block_id, 255)


class TestLayoutBlockAttributesConstructor:
    @pytest.fixture(scope="function")
    def empty_instance(self):
        class Empty(object):
            pass

        return Empty()

    @pytest.fixture(scope="function")
    def obj_instance(self, empty_instance):
        return LayoutBlockAttributeConstructor(empty_instance)

    def test__ut__attributes(self, obj_instance):
        assert isinstance(obj_instance._checker, LayoutBlockAttributesCheckers)

    @mock.patch.object(LayoutBlockAttributeConstructor, "_set_attribute")
    @mock.patch.object(LayoutBlockAttributesCheckers, "block_id_checker")
    def test__ut__edit_block_id(self, mock_block_id_checker, mock_set_attribute, obj_instance):
        block_id = "112233"
        obj_instance.edit_block_id(block_id)
        mock_block_id_checker.assert_called_once_with(block_id)
        mock_set_attribute.assert_called_once_with("block_id", block_id)

    @mock.patch.object(LayoutBlockAttributeConstructor, "_set_attribute")
    @mock.patch.object(LayoutBlockAttributesCheckers, "string_length_checker")
    def test__ut__edit_input_block_hint(self, mock_string_length_checker, mock_set_attribute, obj_instance):
        _value = "test value"
        with mock.patch("slack_block_builder.components.TextObject") as MockTextObject:
            obj_instance.edit_input_block_hint(_value)
            mock_string_length_checker.assert_called_once_with("hint", _value, 2000)
            mock_set_attribute.assert_called_once_with("hint", MockTextObject(_value))

    @mock.patch.object(LayoutBlockAttributeConstructor, "_set_attribute")
    @mock.patch.object(LayoutBlockAttributesCheckers, "type_checker")
    def test__ut__edit_input_block_dispatch_action(self, mock_type_checker, mock_set_attribute, obj_instance):
        bool_value = True
        obj_instance.edit_input_block_dispatch_action(bool_value)
        mock_type_checker.assert_called_once_with("dispatch_action", bool_value, bool)
        mock_set_attribute.assert_called_once_with("dispatch_action", bool_value)

    @mock.patch.object(LayoutBlockAttributeConstructor, "_set_attribute")
    @mock.patch.object(LayoutBlockAttributesCheckers, "type_checker")
    def test__ut__edit_input_block_optional(self, mock_type_checker, mock_set_attribute, obj_instance):
        bool_value = True
        obj_instance.edit_input_block_optional(bool_value)
        mock_type_checker.assert_called_once_with("optional", bool_value, bool)
        mock_set_attribute.assert_called_once_with("optional", bool_value)
