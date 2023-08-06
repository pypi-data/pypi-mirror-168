# -*- coding: utf-8 -*-
# @Filename : test_apphome_builder
# @Date : 2022-03-08-15-11
# @Project: content-service-chat-assistant


import pytest
from slack_block_builder import AppHomeBuilder, Formatter, ButtonElement, ColorScheme


class TestBlockBuilder:
    @pytest.fixture(scope="function")
    def build_obj(self):
        return AppHomeBuilder()

    def test__it__type(self, build_obj):
        assert build_obj.type == "home"

    @pytest.mark.parametrize("load_test_json_data", ["test_message_data_apphome.json"], indirect=True)
    def test__it__built_message_1(self, build_obj, load_test_json_data):
        builder = build_obj
        # index 1
        builder.add_section_block(
            text='You have a new request:\n*<fakeLink.toEmployeeProfile.com|Fred Enriquez - New device request>*',
            text_formatter=Formatter.MarkDown)
        # index 2
        section_block = builder.add_section_block()
        section_block.add_field(text='*Type:*\nComputer (laptop)', formatter=Formatter.MarkDown)
        section_block.add_field(text='*When:*\nSubmitted Aut 10', formatter=Formatter.MarkDown)
        section_block.add_field(text='*Last Update:*\nMar 10, 2015 (3 years, 5 months)',
                                formatter=Formatter.MarkDown)
        section_block.add_field(text="*Reason:*\nAll vowel keys aren't working.", formatter=Formatter.MarkDown)
        section_block.add_field(text="*Specs:*\n\"Cheetah Pro 15\" - Fast, really fast\"",
                                formatter=Formatter.MarkDown)
        # index 3
        approve_button = ButtonElement(text="Approce", style=ColorScheme.Primary)
        deny_button = ButtonElement(text="Deny", style=ColorScheme.Danger)
        buttons_block = builder.add_action_block()
        buttons_block.add_element(approve_button)
        buttons_block.add_element(deny_button)
        # export to json
        assert builder.to_dict() == load_test_json_data
