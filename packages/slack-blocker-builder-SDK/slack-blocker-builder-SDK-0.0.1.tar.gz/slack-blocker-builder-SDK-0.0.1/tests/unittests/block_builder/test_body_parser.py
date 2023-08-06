# -*- coding: utf-8 -*-
# @Filename : test_body_parser
# @Date : 2022-03-09-10-02
# @Project: content-service-chat-assistant

import pytest
from unittest import mock
from slack_block_builder.exception import SlackBodyTypeError
from slack_block_builder.body_parser import (
    _fetch_actions_value,
    _fetch_state_value,
    ActionBodyParser,
    CommandBodyParser,
    EventBodyParser,
    ViewSubmissionBodyParser,
    auto_parser
)


class TestSingleFunctions:
    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__fetch_actions_value(self, load_test_json_data):
        action_data = load_test_json_data['actions'][0]
        result = _fetch_actions_value(action_data)
        assert result == ("/iopsv2", "Iopsv2")

    def test__ut__fetch_action_value__button(self, action_button_data):
        result = _fetch_actions_value(action_button_data)
        assert result == ("click_me_123", "Approve")

    def test__ut__fetch_action_value__plain_text_input(self, action_plain_text_input_data):
        result = _fetch_actions_value(action_plain_text_input_data)
        assert result == ("212", "212")

    def test__ut__fetch_action_value__checkbox(self, action_checkbox_data):
        result = _fetch_actions_value(action_checkbox_data)
        assert result == [("value-1", "*this is plain_text text*"), ("value-0", "*this is plain_text text*")]

    def test__ut__fetch_action_value__overflow(self, action_overflow_data):
        result = _fetch_actions_value(action_overflow_data)
        assert result == ("value-1", "*this is plain_text text*")

    def test__ut__fetch_action_value__radio_button(self, action_radio_button_data):
        result = _fetch_actions_value(action_radio_button_data)
        assert result == ("value-0", "*this is plain_text text*")

    def test__ut__fetch_action_value__datepicker(self, action_datepicker_data):
        result = _fetch_actions_value(action_datepicker_data)
        assert result == ("1990-04-06", "1990-04-06")

    def test__ut__fetch_action_value__timepicker(self, action_timepicker_data):
        result = _fetch_actions_value(action_timepicker_data)
        assert result == ("04:00", "04:00")

    def test__ut__fetch_action_value__multi_static_select(self, action_multi_static_select_data):
        result = _fetch_actions_value(action_multi_static_select_data)
        assert result == [("value-2", "*this is plain_text text*"), ("value-1", "*this is plain_text text*")]

    def test__ut__fetch_action_value__static_select(self, action_static_select_data):
        result = _fetch_actions_value(action_static_select_data)
        assert result == ("value-2", "*this is plain_text text*")

    def test__ut__fetch_action_value__user_select(self, action_users_select_data):
        result = _fetch_actions_value(action_users_select_data)
        assert result == ("WBTHD9DCZ", "WBTHD9DCZ")

    def test__ut__fetch_action_value__multi_users_select(self, action_multi_users_select_data):
        result = _fetch_actions_value(action_multi_users_select_data)
        assert result == [("W01AG1MNWHW", "W01AG1MNWHW"), ("WBTHD9DCZ", "WBTHD9DCZ")]

    def test__ut__fetch_action_value__conversations_select(self, action_conversations_select_data):
        result = _fetch_actions_value(action_conversations_select_data)
        assert result == ("CAJ680C03", "CAJ680C03")

    def test__ut__fetch_action_value__multi_conversations_select(self, action_multi_conversations_select_data):
        result = _fetch_actions_value(action_multi_conversations_select_data)
        assert result == [("C01ALR6U7EW", "C01ALR6U7EW"), ("CFLE550G3", "CFLE550G3")]

    def test__ut__fetch_action_value__channel_select(self, action_channel_select_data):
        result = _fetch_actions_value(action_channel_select_data)
        assert result == ("CAAJPP7KK", "CAAJPP7KK")

    def test__ut__fetch_action_value__multi_channel_select(self, action_multi_channel_select_data):
        result = _fetch_actions_value(action_multi_channel_select_data)
        assert result == [("CFLE550G3", "CFLE550G3"), ("C01ALR6U7EW", "C01ALR6U7EW")]

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__fetch_state_value(self, load_test_json_data):
        _data = load_test_json_data['state']
        block_id = "dS6"
        action_id = "select_menu"
        result = _fetch_state_value(_data, block_id=block_id, action_id=action_id)
        assert result == ("/iopsv2", "Iopsv2")

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    @mock.patch("slack_block_builder.body_parser._fetch_actions_value")
    def test__ut__fetch_state_value(self, mock_fetch_actions_value, load_test_json_data):
        _data = load_test_json_data['state']
        block_id = "dS6"
        action_id = "select_menu"
        mock_fetch_actions_value.return_value = "1"
        result = _fetch_state_value(_data, block_id=block_id, action_id=action_id)
        assert result == "1"
        mock_fetch_actions_value.assert_called_once_with(_data["values"][block_id][action_id])

    @pytest.mark.parametrize("action_type", ["button", "overflow"])
    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    @mock.patch("slack_block_builder.body_parser._fetch_actions_value")
    def test__ut__fetch_state_value__button(self, mock_fetch_actions_value, load_test_json_data, action_type):
        _data = load_test_json_data['state']
        block_id = "dS6"
        action_id = "select_menu"
        _data["values"][block_id][action_id]["type"] = action_type
        result = _fetch_state_value(_data, block_id=block_id, action_id=action_id)
        assert result is None
        mock_fetch_actions_value.assert_not_called()


class TestActionBodyParser:
    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__type(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.type == f"{load_test_json_data['type']}|{load_test_json_data['actions'][0]['type']}"

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__user_id(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.user_id == load_test_json_data["user"]["id"]

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__user(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.user == load_test_json_data["user"]["name"]

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__team_id(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.team_id == load_test_json_data["team"]["id"]

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__team(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.team == load_test_json_data["team"]["domain"]

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__trigger_id(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.trigger_id == load_test_json_data['trigger_id']

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__channel(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.channel == load_test_json_data["channel"]["name"]

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__channel__none(self, load_test_json_data):
        load_test_json_data['channel'] = None
        parser = ActionBodyParser(load_test_json_data)
        assert parser.channel is None

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__channel_id(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.channel_id == load_test_json_data["channel"]["id"]

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__channel_id__none(self, load_test_json_data):
        load_test_json_data['channel'] = None
        parser = ActionBodyParser(load_test_json_data)
        assert parser.channel_id is None

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__response_url(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.response_url == load_test_json_data["response_url"]

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__current_actions(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.current_actions == load_test_json_data["actions"][0]

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__action_type(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.action_type == load_test_json_data["actions"][0]['type']

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__action_id(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.action_id == load_test_json_data["actions"][0]["action_id"]

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__block_id(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.block_id == load_test_json_data["actions"][0]["block_id"]

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__state(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.state == load_test_json_data["state"]

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__payload(self, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        assert parser.payload == load_test_json_data["actions"]

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    @mock.patch("slack_block_builder.body_parser._fetch_actions_value")
    def test__ut__action_value(self, mock_fetch_action_value, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        parser.action_value
        mock_fetch_action_value.assert_called_once_with(load_test_json_data['actions'][0])

    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    @mock.patch("slack_block_builder.body_parser._fetch_state_value")
    def test__ut__fetch_state_value(self, mock_fetch_state_value, load_test_json_data):
        parser = ActionBodyParser(load_test_json_data)
        block_id = "ass"
        action_id = "ssss"
        parser.fetch_state_value(block_id=block_id, action_id=action_id)
        mock_fetch_state_value.assert_called_once_with(load_test_json_data["state"], block_id, action_id)


class TestViewSubmissionBodyParser:
    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__type(self, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        assert parser.type == f"{load_test_json_data['type']}|{load_test_json_data['view']['type']}"

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__user_id(self, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        assert parser.user_id == load_test_json_data["user"]["id"]

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__user(self, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        assert parser.user == load_test_json_data["user"]["name"]

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__team_id(self, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        assert parser.team_id == load_test_json_data["team"]["id"]

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__team(self, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        assert parser.team == load_test_json_data["team"]["domain"]

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__trigger_id(self, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        assert parser.trigger_id == load_test_json_data['trigger_id']

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__view(self, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        assert parser.view == load_test_json_data['view']

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__view_type(self, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        assert parser.view_type == load_test_json_data['view']['type']

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__blocks(self, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        assert parser.blocks == load_test_json_data['view']['blocks']

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__callback_id(self, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        assert parser.callback_id == load_test_json_data['view']['callback_id']

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__hash(self, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        assert parser.hash == load_test_json_data['view']['hash']

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__state(self, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        assert parser.state == load_test_json_data['view']['state']

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__response_urls(self, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        assert parser.response_urls == load_test_json_data['response_urls']

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__payload(self, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        assert parser.payload == parser.view

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    @mock.patch("slack_block_builder.body_parser._fetch_state_value")
    def test__ut__fetch_state_value(self, mock_fetch_state_value, load_test_json_data):
        parser = ViewSubmissionBodyParser(load_test_json_data)
        block_id = "ass"
        action_id = "ssss"
        parser.fetch_state_value(block_id=block_id, action_id=action_id)
        mock_fetch_state_value.assert_called_once_with(load_test_json_data["view"]["state"], block_id, action_id)


class TestEventBodyParser:
    @pytest.mark.parametrize("load_test_json_data", ["event_body.json"], indirect=True)
    def test__it__type(self, load_test_json_data):
        parser = EventBodyParser(load_test_json_data)
        assert parser.type == f"event|{load_test_json_data['event']['type']}"

    @pytest.mark.parametrize("load_test_json_data", ["event_body.json"], indirect=True)
    def test__it__event(self, load_test_json_data):
        parser = EventBodyParser(load_test_json_data)
        assert parser.event == load_test_json_data['event']

    @pytest.mark.parametrize("load_test_json_data", ["event_body.json"], indirect=True)
    def test__it__team(self, load_test_json_data):
        parser = EventBodyParser(load_test_json_data)
        assert parser.team is None

    @pytest.mark.parametrize("load_test_json_data", ["event_body.json"], indirect=True)
    def test__it__team_id(self, load_test_json_data):
        parser = EventBodyParser(load_test_json_data)
        assert parser.team_id == load_test_json_data["event"]["team"]

    @pytest.mark.parametrize("load_test_json_data", ["event_body.json"], indirect=True)
    def test__it__user(self, load_test_json_data):
        parser = EventBodyParser(load_test_json_data)
        assert parser.user is None

    @pytest.mark.parametrize("load_test_json_data", ["event_body.json"], indirect=True)
    def test__it__user_id(self, load_test_json_data):
        parser = EventBodyParser(load_test_json_data)
        assert parser.user_id == load_test_json_data['event']["user"]

    @pytest.mark.parametrize("load_test_json_data", ["event_body.json"], indirect=True)
    def test__it__channel(self, load_test_json_data):
        parser = EventBodyParser(load_test_json_data)
        assert parser.channel is None

    @pytest.mark.parametrize("load_test_json_data", ["event_body.json"], indirect=True)
    def test__it__channel_id(self, load_test_json_data):
        parser = EventBodyParser(load_test_json_data)
        assert parser.channel_id == load_test_json_data['event']["channel"]

    @pytest.mark.parametrize("load_test_json_data", ["event_body.json"], indirect=True)
    def test__it__ts(self, load_test_json_data):
        parser = EventBodyParser(load_test_json_data)
        assert parser.ts == load_test_json_data['event']["ts"]

    @pytest.mark.parametrize("load_test_json_data", ["event_body.json"], indirect=True)
    def test__it__text(self, load_test_json_data):
        parser = EventBodyParser(load_test_json_data)
        assert parser.text == load_test_json_data['event']["text"]

    @pytest.mark.parametrize("load_test_json_data", ["event_body.json"], indirect=True)
    def test__it__event_type(self, load_test_json_data):
        parser = EventBodyParser(load_test_json_data)
        assert parser.event_type == load_test_json_data['event']["type"]

    @pytest.mark.parametrize("load_test_json_data", ["event_body.json"], indirect=True)
    def test__it__event_id(self, load_test_json_data):
        parser = EventBodyParser(load_test_json_data)
        assert parser.event_id == load_test_json_data["event_id"]

    @pytest.mark.parametrize("load_test_json_data", ["event_body.json"], indirect=True)
    def test__it__payload(self, load_test_json_data):
        parser = EventBodyParser(load_test_json_data)
        assert parser.payload == parser.event


class TestCommandBodyParser:
    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__type(self, load_test_json_data):
        parser = CommandBodyParser(load_test_json_data)
        assert parser.type == f"command|{load_test_json_data['command']}"

    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__team(self, load_test_json_data):
        parser = CommandBodyParser(load_test_json_data)
        assert parser.team == load_test_json_data['team_domain']

    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__team_id(self, load_test_json_data):
        parser = CommandBodyParser(load_test_json_data)
        assert parser.team_id == load_test_json_data["team_id"]

    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__user(self, load_test_json_data):
        parser = CommandBodyParser(load_test_json_data)
        assert parser.user == load_test_json_data['user_name']

    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__user_id(self, load_test_json_data):
        parser = CommandBodyParser(load_test_json_data)
        assert parser.user_id == load_test_json_data['user_id']

    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__channel(self, load_test_json_data):
        parser = CommandBodyParser(load_test_json_data)
        assert parser.channel == load_test_json_data['channel_name']

    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__channel_id(self, load_test_json_data):
        parser = CommandBodyParser(load_test_json_data)
        assert parser.channel_id == load_test_json_data['channel_id']

    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__channel__none(self, load_test_json_data):
        del load_test_json_data["channel_name"]
        parser = CommandBodyParser(load_test_json_data)
        assert parser.channel is None

    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__channel_id(self, load_test_json_data):
        del load_test_json_data["channel_id"]
        parser = CommandBodyParser(load_test_json_data)
        assert parser.channel_id is None

    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__command(self, load_test_json_data):
        parser = CommandBodyParser(load_test_json_data)
        assert parser.command == load_test_json_data['command']

    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__text(self, load_test_json_data):
        parser = CommandBodyParser(load_test_json_data)
        assert parser.text == load_test_json_data['text']

    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__trigger_id(self, load_test_json_data):
        parser = CommandBodyParser(load_test_json_data)
        assert parser.trigger_id == load_test_json_data['trigger_id']

    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__response_url(self, load_test_json_data):
        parser = CommandBodyParser(load_test_json_data)
        assert parser.response_url == load_test_json_data['response_url']

    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__payload(self, load_test_json_data):
        parser = CommandBodyParser(load_test_json_data)
        assert parser.payload == parser.text


class TestAutoFetchParser:
    @pytest.mark.parametrize("load_test_json_data", ["action_body.json"], indirect=True)
    def test__it__action_parser(self, load_test_json_data):
        assert isinstance(auto_parser(load_test_json_data), ActionBodyParser)

    @pytest.mark.parametrize("load_test_json_data", ["command_body.json"], indirect=True)
    def test__it__command_parser(self, load_test_json_data):
        assert isinstance(auto_parser(load_test_json_data), CommandBodyParser)

    @pytest.mark.parametrize("load_test_json_data", ["event_body.json"], indirect=True)
    def test__it__event_parser(self, load_test_json_data):
        assert isinstance(auto_parser(load_test_json_data), EventBodyParser)

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__view_parser(self, load_test_json_data):
        assert isinstance(auto_parser(load_test_json_data), ViewSubmissionBodyParser)

    @pytest.mark.parametrize("load_test_json_data", ["view_body.json"], indirect=True)
    def test__it__body_type_error(self, load_test_json_data):
        load_test_json_data.pop("view")
        with pytest.raises(SlackBodyTypeError):
            auto_parser(load_test_json_data)

