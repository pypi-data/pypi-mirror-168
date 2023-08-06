# -*- coding: utf-8 -*-
# @Filename : test_image_block
# @Date : 2022-03-07-17-06
# @Project: content-service-chat-assistant

from slack_block_builder.image_block import ImageBlock
from slack_block_builder.components import Formatter


class TestImageBlock:
    def test__ut__type(self):
        url = "https://test.me"
        text = "test"
        _object = ImageBlock(url, text)
        assert _object.type == "image"

    def test__it__image_url(self):
        url = "https://test.me"
        text = "test"
        _object = ImageBlock(url, text)
        assert _object.image_url == url

    def test__it__alt_text(self):
        url = "https://test.me"
        text = "test"
        _object = ImageBlock(url, text)
        assert _object.alt_text == text

    def test__it__title(self):
        url = "https://test.me"
        text = "test"
        title = "this is test title"
        _object = ImageBlock(url, text, title=title)
        assert _object.title.text == title
        assert _object.title.type == Formatter.PlainText.value

    def test__it__block_id(self):
        url = "https://test.me"
        text = "test"
        block_id = "block id test"
        _object = ImageBlock(url, text, block_id=block_id)
        assert _object.block_id == block_id

