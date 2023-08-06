# -*- coding: utf-8 -*-
# @Filename : test_section_block
# @Date : 2022-03-07-17-27
# @Project: content-service-chat-assistant

import pytest
from slack_block_builder.components import TextObject, Formatter, DatePickerElement
from slack_block_builder.section_block import SectionBlock, section_accessory_element_type_checker
from slack_block_builder.exception import BlockTypeError
import slack_block_builder.components.block_element as BlockElements


class TestActionElementsChecker:
    def test__it__action_elements_checker__class(self):
        class_instance = TextObject("1")
        with pytest.raises(BlockTypeError):
            section_accessory_element_type_checker(class_instance)

    def test__it__action_elements_checker(self):
        class_instance = BlockElements.PublicChannelListSelectMenuElement("testing")
        section_accessory_element_type_checker(class_instance)


class TestSectionBlock:
    def test__ut__type(self):
        _object = SectionBlock()
        assert _object.type == "section"

    def test__it__text(self):
        text = "test"
        _object = SectionBlock(text=text)
        assert _object.text.text == text

    def test__it__text_format(self):
        text = "test"
        format = Formatter.PlainText
        _object = SectionBlock(text=text, text_formatter=format)
        assert _object.text.type == format.value

    def test__it__block_id(self):
        block_id = "block_ id"
        _object = SectionBlock(block_id=block_id)
        assert _object.block_id == block_id

    def test__it__add_field(self):
        _object = SectionBlock()
        assert hasattr(_object, "fields") is False
        field_text = "new field"
        _object.add_field(text=field_text)
        assert _object.fields[0].text == field_text
        assert len(_object.fields) == 1

    def test__it__add_field_1(self):
        _object = SectionBlock()
        assert hasattr(_object, "fields") is False
        field_text = "new field"
        _object.add_field(text=field_text)
        _object.add_field(text=field_text)
        assert _object.fields[0].text == field_text
        assert len(_object.fields) == 2

    def test__it__edit_accessory(self):
        _object = SectionBlock()
        accessory_instance = DatePickerElement()
        assert hasattr(_object, "accessory") is False
        _object.edit_accessory(accessory_instance)
        assert _object.accessory is accessory_instance
