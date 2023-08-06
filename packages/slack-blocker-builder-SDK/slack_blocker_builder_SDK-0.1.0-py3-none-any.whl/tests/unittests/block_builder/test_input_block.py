# -*- coding: utf-8 -*-
# @Filename : test_input_block
# @Date : 2022-03-07-16-32
# @Project: content-service-chat-assistant


import pytest
from slack_block_builder.input_block import InputBlock, input_element_checker
from slack_block_builder.components import DatePickerElement
import slack_block_builder.components.block_element as BlockElements
from slack_block_builder.exception import BlockTypeError


class TestInputElementsChecker:
    def test__it__input_element_checker__access(self):
        class_instance = BlockElements.PublicChannelListMultiSelectMenuElement("testing")
        input_element_checker(class_instance)

    @pytest.mark.parametrize("generate_optional_object", [5], indirect=True)
    def test__it__input_element_checker__false(self, generate_optional_object):
        class_instance = BlockElements.OverflowMenuElement(generate_optional_object)
        with pytest.raises(BlockTypeError):
            input_element_checker(class_instance)


class TestInputBlock:
    @pytest.fixture(scope="function")
    def date_picker_instance(self):
        return DatePickerElement()

    def test__ut__type(self, date_picker_instance):
        _object = InputBlock(label="test", element=date_picker_instance)
        assert _object.type == "input"

    def test__it__label(self, date_picker_instance):
        _object = InputBlock(label="test", element=date_picker_instance)
        assert _object.label.text == "test"

    def test__it__element(self, date_picker_instance):
        _object = InputBlock(label="test", element=date_picker_instance)
        assert _object.element is date_picker_instance

    def test__it__null_attrs(self, date_picker_instance):
        _object = InputBlock(label="test", element=date_picker_instance)
        assert hasattr(_object, "dispatch_action") is False
        assert hasattr(_object, "block_id") is False
        assert hasattr(_object, "hint") is False
        assert hasattr(_object, "optional") is False

    def test__it__dispatch_action(self, date_picker_instance):
        dispatch = True
        _object = InputBlock(label="test", element=date_picker_instance, dispatch_action=dispatch)
        assert _object.dispatch_action is dispatch

    def test__it__block_id(self, date_picker_instance):
        block_id ="test block id"
        _object = InputBlock(label="test", element=date_picker_instance, block_id=block_id)
        assert _object.block_id == block_id

    def test__it__hit(self, date_picker_instance):
        hint = "hello"
        _object = InputBlock(label="test", element=date_picker_instance, hint=hint)
        assert _object.hint.text == hint

    def test__it__optional(self, date_picker_instance):
        optional = True
        _object = InputBlock(label="test", element=date_picker_instance, optional=optional)
        assert _object.optional is optional


