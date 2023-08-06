# -*- coding: utf-8 -*-
# @Filename : test_content_block
# @Date : 2022-03-07-15-48
# @Project: content-service-chat-assistant

import pytest
from slack_block_builder.context_block import ContextBlock
from slack_block_builder.components import Formatter
from slack_block_builder.exception import BlockElementOutOfRangeError


class TestContextBlock:
    def test__ut__type(self):
        _object = ContextBlock()
        assert _object.type == "context"

    def test__it__block_id(self):
        block_id = "test_block"
        _object = ContextBlock(block_id)
        assert _object.block_id == block_id

    def test__it__edit_block_id(self):
        block_id = "test_block"
        _object = ContextBlock()
        assert hasattr(_object, "block_id") is False
        _object.edit_block_id(block_id)
        assert _object.block_id == block_id

    def test__it__fetch_or_create_elements_attribute__create(self):
        _object = ContextBlock()
        assert hasattr(_object, "elements") is False
        result = _object._fetch_or_create_elements_attribute()
        assert hasattr(_object, "elements") is True
        assert getattr(_object, "elements") == []
        assert result == []

    def test__it__fetch_or_create_elements_attribute__fetch(self):
        _object = ContextBlock()
        mock_list = [1, 2, 3]
        setattr(_object, "elements", mock_list)
        assert _object._fetch_or_create_elements_attribute() == mock_list

    def test__it__fetch_or_create_elements_attribute__out_of_bound(self):
        _object = ContextBlock()
        mock_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        setattr(_object, "elements", mock_list)
        with pytest.raises(BlockElementOutOfRangeError):
            _object._fetch_or_create_elements_attribute()

    def test__it__add_text_element(self):
        _object = ContextBlock()
        _text = "testing"
        _object.add_text_element(text=_text)
        assert getattr(_object, "elements")[0].text == _text

    def test__it__add_text_element__format(self):
        _object = ContextBlock()
        _text = "testing"
        formatter = Formatter.MarkDown
        _object.add_text_element(text=_text, formatter=formatter)
        assert getattr(_object, "elements")[0].text == _text
        assert getattr(_object, "elements")[0].type == formatter.value

    def test__it__add_image_element(self):
        _object = ContextBlock()
        image_url = "https://test.me"
        alt_text = "testing"
        _object.add_image_element(image_url, alt_text)
        assert getattr(_object, "elements")[0].image_url == image_url
        assert getattr(_object, "elements")[0].alt_text == alt_text

