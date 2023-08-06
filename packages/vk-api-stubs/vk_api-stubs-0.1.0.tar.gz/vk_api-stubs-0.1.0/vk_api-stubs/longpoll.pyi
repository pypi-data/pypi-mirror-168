from enum import IntEnum
from typing import Any, Iterator, Type

from vk_api.vk_api import VkApi


CHAT_START_ID: int


class VkLongpollMode(IntEnum):
    GET_ATTACHMENTS: int
    GET_EXTENDED: int
    GET_PTS: int
    GET_EXTRA_ONLINE: int
    GET_RANDOM_ID: int


DEFAULT_MODE: int


class VkEventType(IntEnum):
    MESSAGE_FLAGS_REPLACE: int
    MESSAGE_FLAGS_SET: int
    MESSAGE_FLAGS_RESET: int
    MESSAGE_NEW: int
    MESSAGE_EDIT: int
    READ_ALL_INCOMING_MESSAGES: int
    READ_ALL_OUTGOING_MESSAGES: int
    USER_ONLINE: int
    USER_OFFLINE: int
    PEER_FLAGS_RESET: int
    PEER_FLAGS_REPLACE: int
    PEER_FLAGS_SET: int
    PEER_DELETE_ALL: int
    PEER_RESTORE_ALL: int
    CHAT_EDIT: int
    CHAT_UPDATE: int
    USER_TYPING: int
    USER_TYPING_IN_CHAT: int
    USER_RECORDING_VOICE: int
    USER_CALL: int
    MESSAGES_COUNTER_UPDATE: int
    NOTIFICATION_SETTINGS_UPDATE: int


class VkPlatform(IntEnum):
    MOBILE: int
    IPHONE: int
    IPAD: int
    ANDROID: int
    WPHONE: int
    WINDOWS: int
    WEB: int


class VkOfflineType(IntEnum):
    EXIT: int
    AWAY: int


class VkMessageFlag(IntEnum):
    UNREAD: int
    OUTBOX: int
    REPLIED: int
    IMPORTANT: int
    CHAT: int
    FRIENDS: int
    SPAM: int
    DELETED: int
    FIXED: int
    MEDIA: int
    HIDDEN: int
    DELETED_ALL: int


class VkPeerFlag(IntEnum):
    IMPORTANT: int
    UNANSWERED: int


class VkChatEventType(IntEnum):
    TITLE: int
    PHOTO: int
    ADMIN_ADDED: int
    SETTINGS_CHANGED: int
    MESSAGE_PINNED: int
    USER_JOINED: int
    USER_LEFT: int
    USER_KICKED: int
    ADMIN_REMOVED: int
    KEYBOARD_RECEIVED: int


MESSAGE_EXTRA_FIELDS: list[str]

MSGID: str
EVENT_ATTRS_MAPPING: dict[VkEventType, list]

def get_all_event_attrs() -> tuple: ...

ALL_EVENT_ATTRS: tuple
PARSE_PEER_ID_EVENTS: list[int]
PARSE_MESSAGE_FLAGS_EVENTS: list[VkEventType]

class Event:
    text: str
    user_id: int
    type: VkEventType
    to_me: bool
    obj: dict[Any, Any]
    from_user: int

class VkLongPoll:
    DEFAULT_EVENT_CLASS: Event
    PRELOAD_MESSAGE_EVENTS: list[VkEventType]
    
    def __init__(self, vk: VkApi, wait: int=25, mode: int = DEFAULT_MODE,
                 preload_messages: bool=False, group_id: int=...) -> None: ...
    
    def _parse_event(self, raw_event) -> Event: ...
    
    def update_longpoll_server(self, update_ts: bool=True) -> None: ...
    
    def check(self) -> list[Event]: ...
    
    def preload_message_events_data(self, events: list[Event]) -> None: ...
    
    def listen(self) -> Iterator[Event]: ...   
    