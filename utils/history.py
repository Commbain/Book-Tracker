# utils/history.py
from collections import deque
from typing import List, Optional

class ActionHistory:
    """Хранит историю действий (стек для отмены, очередь для отображения)."""
    
    def __init__(self, max_size: int = 50):
        self._undo_stack: List[str] = []  # Стек для отмены
        self._action_queue: deque = deque(maxlen=max_size)  # Очередь для истории
    
    def add_action(self, action: str):
        """Добавляет действие в историю."""
        self._undo_stack.append(action)
        self._action_queue.append(action)
    
    def undo_last(self) -> Optional[str]:
        """Отменяет последнее действие (извлекает из стека)."""
        if self._undo_stack:
            return self._undo_stack.pop()
        return None
    
    def get_recent_actions(self, count: int = 10) -> List[str]:
        """Возвращает последние действия из очереди."""
        return list(self._action_queue)[-count:]
    
    def can_undo(self) -> bool:
        """Проверяет, есть ли действия для отмены."""
        return len(self._undo_stack) > 0
