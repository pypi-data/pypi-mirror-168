# -*- coding: utf-8 -*-
# @Filename : test_block_builder
# @Date : 2022-03-08-13-52
# @Project: content-service-chat-assistant

import pytest
from slack_block_builder import BlockBuilder, Formatter, ButtonElement, ColorScheme, OverflowMenuElement, OptionObject


class TestBlockBuilder:
    @pytest.fixture(scope="function")
    def build_obj(self):
        return BlockBuilder()

    def test__it__type(self, build_obj):
        assert build_obj.blocks == []

    @pytest.mark.parametrize("load_test_json_data", ["test_message_data_1.json"], indirect=True)
    def test__it__built_message_1(self, build_obj, load_test_json_data):
        builder = build_obj
        # index 1
        builder.add_section_block(text='You have a new request:\n*<fakeLink.toEmployeeProfile.com|Fred Enriquez - New device request>*',
                                  text_formatter=Formatter.MarkDown)
        # index 2
        section_block = builder.add_section_block()
        section_block.add_field(text='*Type:*\nComputer (laptop)', formatter=Formatter.MarkDown)
        section_block.add_field(text='*When:*\nSubmitted Aut 10', formatter=Formatter.MarkDown)
        section_block.add_field(text='*Last Update:*\nMar 10, 2015 (3 years, 5 months)', formatter=Formatter.MarkDown)
        section_block.add_field(text="*Reason:*\nAll vowel keys aren't working.", formatter=Formatter.MarkDown)
        section_block.add_field(text="*Specs:*\n\"Cheetah Pro 15\" - Fast, really fast\"", formatter=Formatter.MarkDown)
        #index 3
        approve_button = ButtonElement(text="Approce", style=ColorScheme.Primary)
        deny_button = ButtonElement(text="Deny", style=ColorScheme.Danger)
        buttons_block = builder.add_action_block()
        buttons_block.add_element(approve_button)
        buttons_block.add_element(deny_button)
        # export to json
        assert builder.to_dict() == load_test_json_data

    @pytest.mark.parametrize("load_test_json_data", ["test_customer_info_page_data.json"], indirect=True)
    def test__it__customer_information_page(self, build_obj, load_test_json_data):
        builder = build_obj
        # customer name
        customer_blocker = builder.add_section_block(text="[MT PROD]APJ_4_A.S. Test Environment")
        customer_blocker.add_field(text="*Subscription ID:* \n value_1", formatter=Formatter.MarkDown)
        customer_blocker.add_field(text="*Tenant:* value_2", formatter=Formatter.MarkDown)
        customer_blocker.add_field(text="*Resource Group:* value_3", formatter=Formatter.MarkDown)
        customer_blocker.add_field(text="*Go Live Time:* N/A", formatter=Formatter.MarkDown)
        # header
        builder.add_header_block(text="Dynatrace Problems")
        # dynatrace info
        builder.add_section_block(text="Problem: App 0, Env: 0, Infra: 0, svn: 0", text_formatter=Formatter.PlainText)
        # header
        builder.add_header_block(text="APPs")
        # Apps Overflow
        app_section = builder.add_section_block(text="Generate Database Report")
        _option_1 = OptionObject(text="DB-1", value="DB-1")
        _option_2 = OptionObject(text="DB-2", value="DB-2")
        _action_id = "db_select"
        _overflow = OverflowMenuElement(options=[_option_2, _option_1], action_id=_action_id)
        # header
        builder.add_header_block(text="Links")
        link_action = builder.add_action_block()
        cp_buttom = ButtonElement(text="Commerce Cloud", url="https://cp.me", style=ColorScheme.Primary)
        ae_buttom = ButtonElement(text="Automation Engine", url="https://ae.me", style=ColorScheme.Primary)
        azure_buttom = ButtonElement(text="Azure, url", url="https://az.me", style=ColorScheme.Primary)
        link_action.add_element(cp_buttom)
        link_action.add_element(ae_buttom)
        link_action.add_element(azure_buttom)

        assert builder.to_dict() == load_test_json_data





