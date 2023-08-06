#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : body_parser
# @Date : 2022-01-21-22-44
# @Project: content-service-chat-assistant

from abc import ABC, abstractmethod
from typing import List, AnyStr, Dict, Union, Optional
from enum import Enum
from .exception import SlackBodyTypeError


_t_list_dict = List[dict]
_t_str = AnyStr
_t_list_string = List[AnyStr]
_t_dict = Dict


class BlockElementKey(Enum):
    button = 'value', _t_str
    plain_text_input = "value", _t_str
    checkboxes = "selected_options", _t_list_dict
    overflow = "selected_option", _t_dict
    radio_buttons = "selected_option", _t_dict
    datepicker = "selected_date", _t_str
    timepicker = "selected_time", _t_str
    external_select = "selected_option", _t_dict
    multi_external_select = "selected_options", _t_list_dict
    static_select = "selected_option", _t_dict
    multi_static_select = "selected_options", _t_list_dict
    users_select = "selected_user", _t_str
    multi_users_select = "selected_users", _t_list_string
    conversations_select = "selected_conversation", _t_str
    multi_conversations_select = "selected_conversations", _t_list_string
    channels_select = "selected_channel", _t_str
    multi_channels_select = "selected_channels", _t_list_string


def _fetch_actions_value(action: dict) -> Union[tuple, List[tuple]]:
    """Fetch action's value and display name

    Args:
        action (dict): action data on action event

    Returns:
        if tuple: action value, action display name
        if list: [(action value, action display name), (action value, action display name), ...]

    """
    _action_type = action['type']
    _element_type_key, data_type = getattr(BlockElementKey, _action_type).value
    if data_type is _t_list_dict:
        _action_value = []
        for option in action[_element_type_key]:
            _value = option['value']
            _text = option['text']['text']
            _action_value.append((_value, _text))
    elif data_type is _t_dict:
        _value = action[_element_type_key]['value']
        _text = action[_element_type_key]['text']['text']
        _action_value = (_value, _text)
    elif data_type is _t_list_string:
        _action_value = []
        for option in action[_element_type_key]:
            _action_value.append((option, option))
    else:
        if action.get("text") is not None:
            _text = action["text"]["text"]
        else:
            _text = action[_element_type_key]
        _action_value = (action[_element_type_key], _text)
    return _action_value


def _fetch_state_value(state: dict, block_id: str, action_id: str) -> Union[tuple, List[tuple]]:
    _action_state = state['values'][block_id][action_id]
    _action_state_type = _action_state['type']
    if _action_state_type in ('button', 'overflow'):
        _state_value = None
    else:
        _state_value = _fetch_actions_value(_action_state)
    return _state_value


class Parser(ABC):
    def __init__(self, body: dict):
        self._body = body

    @property
    def token(self) -> str:
        return self._body['token']

    @property
    def type(self):
        return None

    @property
    def team_id(self) -> str:
        return None

    @property
    def team(self):
        return None

    @property
    def channel_id(self):
        return None

    @property
    def channel(self):
        return None

    @property
    def user(self):
        return None

    @property
    @abstractmethod
    def user_id(self) -> str:
        pass

    @property
    @abstractmethod
    def payload(self) -> Union[dict, str, None]:
        pass


class InteractiveBodyParser(Parser):
    @property
    def user_id(self) -> str:
        return self._body['user']['id']

    @property
    def user(self):
        return self._body['user']['name']

    @property
    def team_id(self) -> str:
        return self._body['team']['id']

    @property
    def team(self) -> str:
        return self._body['team']['domain']

    @property
    def trigger_id(self) -> str:
        """A short-lived ID that can be used to open modals."""
        return self._body['trigger_id']

    @property
    @abstractmethod
    def state(self) -> str:
        pass

    def fetch_state_value(self, block_id: str, action_id) -> Union[tuple, List[tuple]]:
        return _fetch_state_value(self.state, block_id, action_id)


class ActionBodyParser(InteractiveBodyParser):
    @property
    def type(self):
        return f"{self._body['type']}|{self.action_type}"

    @property
    def channel(self) -> str:
        channel = self._body.get('channel')
        if channel is not None:
            channel_name = self._body['channel']['name']
        else:
            channel_name = None
        return channel_name

    @property
    def channel_id(self) -> str:
        channel = self._body.get('channel')
        if channel is not None:
            channel_id = self._body['channel']['id']
        else:
            channel_id = None
        return channel_id

    @property
    def response_url(self) -> str:
        """A short-lived webhook that can be used to send messages in response to interactions."""
        return self._body['response_url']

    @property
    def current_actions(self) -> dict:
        return self._body['actions'][0]

    @property
    def action_type(self) -> str:
        return self.current_actions['type']

    @property
    def action_id(self) -> str:
        return self.current_actions['action_id']

    @property
    def action_value(self) -> Union[tuple, List[tuple]]:
        return _fetch_actions_value(self.current_actions)

    @property
    def block_id(self) -> str:
        return self.current_actions['block_id']

    @property
    def state(self) -> str:
        return self._body['state']

    @property
    def payload(self) -> Union[dict, str, None]:
        return self._body['actions']


class ViewSubmissionBodyParser(InteractiveBodyParser):
    @property
    def type(self):
        return f"{self._body['type']}|{self.view_type}"

    @property
    def view(self) -> dict:
        return self._body['view']

    @property
    def view_type(self) -> str:
        return self.view['type']

    @property
    def blocks(self) -> list:
        return self.view['blocks']

    @property
    def callback_id(self) -> str:
        return self.view['callback_id']

    @property
    def hash(self) -> str:
        return self.view['hash']

    @property
    def state(self) -> str:
        return self.view['state']

    @property
    def response_urls(self) -> list:
        return self._body['response_urls']

    @property
    def payload(self) -> Union[dict, str, None]:
        return self.view


class EventBodyParser(Parser):
    @property
    def type(self):
        return f"event|{self.event_type}"

    @property
    def event(self) -> dict:
        return self._body['event']

    @property
    def user_id(self) -> str:
        return self.event['user']

    @property
    def team_id(self) -> str:
        return self.event['team']

    @property
    def channel_id(self) -> str:
        return self.event['channel']

    @property
    def ts(self) -> str:
        return self.event['ts']

    @property
    def text(self) -> str:
        return self.event['text']

    @property
    def event_type(self):
        return self.event['type']

    @property
    def event_id(self):
        return self._body['event_id']

    @property
    def payload(self) -> Union[dict, str, None]:
        return self.event


class CommandBodyParser(Parser):
    @property
    def type(self):
        return f"command|{self.command}"

    @property
    def user_id(self) -> str:
        return self._body['user_id']

    @property
    def user(self) -> str:
        return self._body['user_name']

    @property
    def team_id(self) -> str:
        return self._body['team_id']

    @property
    def team(self):
        return self._body['team_domain']

    @property
    def channel_id(self) -> Optional[str]:
        return self._body.get('channel_id')

    @property
    def channel(self) -> Optional[str]:
        return self._body.get('channel_name')

    @property
    def command(self):
        return self._body['command']

    @property
    def text(self) -> str:
        return self._body['text']

    @property
    def trigger_id(self):
        return self._body['trigger_id']

    @property
    def response_url(self):
        return self._body['response_url']

    @property
    def payload(self) -> Union[dict, str, None]:
        return self.text


def auto_parser(body: dict) -> Parser:
    body_keys = body.keys()
    if "actions" in body_keys:
        _parser = ActionBodyParser
    elif "command" in body_keys:
        _parser = CommandBodyParser
    elif "event" in body_keys:
        _parser = EventBodyParser
    elif "view" in body_keys:
        _parser = ViewSubmissionBodyParser
    else:
        if body.get("token") is not None:
            body.pop("token")
        raise SlackBodyTypeError(f"Slack body not include any (action|event|view|command) fields.\n"
                                 f"body: {body}")
    return _parser(body)

