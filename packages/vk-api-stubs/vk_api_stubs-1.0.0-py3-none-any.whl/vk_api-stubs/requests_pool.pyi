
from typing import Any, NamedTuple, Sequence
from vk_api.execute import VkFunction

from vk_api.vk_api import VkApi


class RequestResult:...

class VkRequestsPool:
    def __init__(self, vk_session: VkApi) -> None: ...
    
    def method(self, method: str, values: dict=...)-> RequestResult:  ...
    
    def execute(self) -> None: ...
    
def check_one_method(pool: Sequence): ...

vk_one_method: VkFunction
def vk_many_methods(vk_session: VkApi, pool): ...

def vk_request_one_param_pool(vk_session: VkApi, method: str, key: str, values: list[dict],
                              default_values: dict=...) -> tuple[Any]: ...

vk_one_param: VkFunction
