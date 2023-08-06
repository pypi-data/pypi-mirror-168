# -*- coding: utf-8 -*-
# @Filename : test_divider_block
# @Date : 2022-03-07-16-16
# @Project: content-service-chat-assistant


from slack_block_builder.divider_block import DividerHeader


class TestDividerHeader:
    def test__ut__type(self):
        _object = DividerHeader()
        assert _object.type == "divider"

    def test__it__block_id(self):
        block_id = "block_id test"
        _object = DividerHeader(block_id)
        assert _object.block_id == block_id

    def test__it__edit_block_id(self):
        _object = DividerHeader()
        assert hasattr(_object, "block_id") is False
        block_id = "block_id test"
        _object.edit_block_id(block_id)
        assert _object.block_id == block_id

