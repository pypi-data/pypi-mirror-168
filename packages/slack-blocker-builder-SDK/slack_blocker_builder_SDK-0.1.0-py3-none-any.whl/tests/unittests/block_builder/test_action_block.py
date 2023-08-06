# -*- coding: utf-8 -*-
# @Filename : test_action_block
# @Date : 2022-03-07-13-49
# @Project: content-service-chat-assistant
import pytest
from slack_block_builder.action_block import action_elements_checker, ActionBlock
import slack_block_builder.components.block_element as BlockElements
from slack_block_builder.components import PublicChannelListSelectMenuElement
from slack_block_builder.exception import BlockTypeError, BlockElementOutOfRangeError


class TestActionElementsChecker:
    def test__it__action_elements_checker__class(self):
        class_instance = BlockElements.PublicChannelListMultiSelectMenuElement("testing")
        with pytest.raises(BlockTypeError):
            action_elements_checker(class_instance)

    def test__it__action_elements_checker(self):
        class_instance = BlockElements.PublicChannelListSelectMenuElement("testing")
        action_elements_checker(class_instance)


class TestActionBlock:
    def test__ut__type(self):
        _object = ActionBlock()
        assert _object.type == "actions"

    def test__it__block_id(self):
        block_id = "test_block"
        _object = ActionBlock(block_id)
        assert _object.block_id == block_id

    def test__it__edit_block_id(self):
        block_id = "test_block"
        _object = ActionBlock()
        assert hasattr(_object, "block_id") is False
        _object.edit_block_id(block_id)
        assert _object.block_id == block_id

    def test__it__fetch_or_create_elements_attribute__create(self):
        _object = ActionBlock()
        assert hasattr(_object, "elements") is False
        result = _object._fetch_or_create_elements_attribute()
        assert hasattr(_object, "elements") is True
        assert getattr(_object, "elements") == []
        assert result == []

    def test__it__fetch_or_create_elements_attribute__fetch(self):
        _object = ActionBlock()
        mock_list = [1, 2, 3]
        setattr(_object, "elements", mock_list)
        assert _object._fetch_or_create_elements_attribute() == mock_list

    def test__it__add_element__out_of_bound(self):
        _object = ActionBlock()
        mock_list = [1, 2, 3, 4, 5]
        setattr(_object, "elements", mock_list)
        with pytest.raises(BlockElementOutOfRangeError):
            _object.add_element("text_class")

    def test__it__add_element__type_error(self):
        _object = ActionBlock()
        mock_list = [1, 2, 3, 4]
        setattr(_object, "elements", mock_list)
        with pytest.raises(BlockTypeError):
            _object.add_element("text_class")

    def test__it__add_element(self):
        _object = ActionBlock()
        _new_element = PublicChannelListSelectMenuElement(placeholder="test")
        _object.add_element(_new_element)
        assert getattr(_object, "elements")[0] is _new_element

