# -*- coding: utf-8 -*-
# @Filename : test_header_block
# @Date : 2022-03-07-16-24
# @Project: content-service-chat-assistant


from slack_block_builder.header_block import HeaderBlock
from slack_block_builder.components import Formatter


class TestHeaderBlock:
    def test__ut__type(self):
        _object = HeaderBlock("test")
        assert _object.type == "header"

    def test__it__text(self):
        _text = "test"
        _object = HeaderBlock(_text)
        assert _object.text.text == _text
        assert _object.text.type == Formatter.PlainText.value

    def test__it__edit_text(self):
        _text = "test"
        _object = HeaderBlock(_text)
        assert _object.text.text == _text
        assert _object.text.type == Formatter.PlainText.value
        _text = "test_new"
        _object.edit_text(_text)
        assert _object.text.text == _text
        assert _object.text.type == Formatter.PlainText.value

    def test__it__block_id(self):
        block_id = "test_block"
        _object = HeaderBlock("test", block_id)
        assert _object.block_id == block_id

    def test__it__edit_block_id(self):
        block_id = "test_block"
        _object = HeaderBlock("test")
        assert hasattr(_object, "block_id") is False
        _object.edit_block_id(block_id)
        assert _object.block_id == block_id

