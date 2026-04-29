# utils/storage.py
import json
import os
from typing import List
from models.book import Book

class BookStorage:
    """Сохраняет и загружает книги в JSON файл."""
    
    def __init__(self, filename: str = "books.json"):
        self._filename = filename
    
    def save(self, books: List[Book]):
        """Сохраняет список книг в файл."""
        data = [book.to_dict() for book in books]
        try:
            with open(self._filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return False
    
    def load(self) -> List[Book]:
        """Загружает список книг из файла."""
        if not os.path.exists(self._filename):
            return []
        
        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [Book.from_dict(item) for item in data]
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            return []
