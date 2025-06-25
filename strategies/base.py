"""交易策略接口基類。"""

from abc import ABC, abstractmethod
from typing import Any


class BaseStrategy(ABC):
    """所有策略應繼承此類並實作對應方法。"""

    @abstractmethod
    def on_data(self, data: Any) -> None:
        """接收即時資料後呼叫。"""
        raise NotImplementedError

    @abstractmethod
    def generate_signals(self) -> None:
        """產生交易訊號。"""
        raise NotImplementedError
