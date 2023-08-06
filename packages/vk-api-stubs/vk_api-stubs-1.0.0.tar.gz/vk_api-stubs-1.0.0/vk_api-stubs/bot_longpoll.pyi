from enum import Enum
from typing import Iterator, Literal
from vk_api.vk_api import VkApi


CHAT_START_ID: int
class DotDict(dict): ...

class VkBotEventType(Enum):
    MESSAGE_NEW: Literal['message_new']
    MESSAGE_REPLY: Literal['message_reply']
    MESSAGE_EDIT: Literal['message_edit']
    MESSAGE_EVENT: Literal['message_event']
    MESSAGE_TYPING_STATE: Literal['message_typing_state']
    MESSAGE_ALLOW: Literal['message_allow']
    MESSAGE_DENY: Literal['message_deny']
    PHOTO_NEW: Literal['photo_new']
    PHOTO_COMMENT_NEW: Literal['photo_comment_new']
    PHOTO_COMMENT_EDIT: Literal['photo_comment_edit']
    PHOTO_COMMENT_RESTORE: Literal['photo_comment_restore']
    PHOTO_COMMENT_DELETE: Literal['photo_comment_delete']
    AUDIO_NEW: Literal['audio_new']
    VIDEO_NEW: Literal['video_new']
    VIDEO_COMMENT_NEW : Literal['video_comment_new']
    VIDEO_COMMENT_EDIT: Literal['video_comment_edit']
    VIDEO_COMMENT_RESTORE: Literal['video_comment_restore']
    VIDEO_COMMENT_DELETE: Literal['video_comment_delete']
    WALL_POST_NEW: Literal['wall_post_new']
    WALL_REPOST: Literal['wall_repost']
    WALL_REPLY_NEW : Literal['wall_reply_new']
    WALL_REPLY_EDIT: Literal['wall_reply_edit']
    WALL_REPLY_RESTORE: Literal['wall_reply_restore']
    WALL_REPLY_DELETE: Literal['wall_reply_delete']
    BOARD_POST_NEW: Literal['board_post_new']
    BOARD_POST_EDIT: Literal['board_post_edit']
    BOARD_POST_RESTORE: Literal['board_post_restore']
    BOARD_POST_DELETE: Literal['board_post_delete']
    MARKET_COMMENT_NEW: Literal['market_comment_new']
    MARKET_COMMENT_EDIT: Literal['market_comment_edit']
    MARKET_COMMENT_RESTORE: Literal['market_comment_restore']
    MARKET_COMMENT_DELETE: Literal['market_comment_delete']
    GROUP_LEAVE: Literal['group_leave']
    GROUP_JOIN: Literal['group_join']
    USER_BLOCK: Literal['user_block']
    USER_UNBLOCK : Literal['user_unblock']
    POLL_VOTE_NEW : Literal['poll_vote_new']
    GROUP_OFFICERS_EDIT: Literal['group_officers_edit']
    GROUP_CHANGE_SETTINGS: Literal['group_change_settings']
    GROUP_CHANGE_PHOTO: Literal['group_change_photo']
    VKPAY_TRANSACTION: Literal['vkpay_transaction']
    
    
class VkBotEvent:
    raw: dict
    type: VkBotEventType
    obj: DotDict
    object: DotDict
    from_user: int

class VkBotMessageEvent(VkBotEvent): ...

class VkBotLongPoll:
    CLASS_BY_EVENT_TYPE: dict[str, VkBotMessageEvent]
    
    DEFAULT_EVENT_CLASS: VkBotEvent
    
    def __init__(self, vk: VkApi, group_id: int, wait: int=25) -> None: ...
    
    def _parse_event(self, raw_event: dict): ...
    
    def update_longpoll_server(self, update_ts: bool=True) -> None: ...
    
    def check(self) -> list: ...
    
    def listen(self) -> Iterator[VkBotEvent]: ...