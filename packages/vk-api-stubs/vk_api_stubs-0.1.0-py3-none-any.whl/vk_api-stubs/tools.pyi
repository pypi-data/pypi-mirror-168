from typing import Any, Callable, Iterator
from .vk_api import VkApi
from .execute import VkFunction


class VkTools:
    def __init__(self, vk: VkApi) -> None: ...
    def get_all_iter(self, method: str, max_count: int, values:dict=..., key: str='items',
                     limit: int=..., stop_fn: Callable[[Any], bool]=..., negative_offset:bool=False) -> Iterator[Any]: ...
    
    def get_all(self, method: str, max_count: int, values:dict=..., key: str='items', limit: int=...,
                stop_fn: Callable[[Any], bool]=..., negative_offset: bool=False
                ) -> dict[Any, Any]:...
    
    def get_all_slow_iter(self, method: str, max_count: int, values: dict=..., key: str='items',
                          limit: int=..., stop_fn: Callable[[Any], bool]=..., negative_offset: bool=False) -> Iterator[Any]: ...
    
    def get_all_slow(self, method: str, max_count: int, values: dict=..., key: str='items',
                          limit: int=..., stop_fn: Callable[[Any], bool]=..., negative_offset: bool=False) -> list[Any]: ...
    
    
vk_get_all_items: VkFunction