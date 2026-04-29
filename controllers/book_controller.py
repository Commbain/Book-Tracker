# controllers/book_controller.py
from typing import List, Optional
from models.book import Book
from utils.storage import BookStorage
from utils.history import ActionHistory

class BookController:
    """Контроллер - обрабатывает команды пользователя."""
    
    def __init__(self, storage: BookStorage, history: ActionHistory):
        self._storage = storage
        self._history = history
        self._books: List[Book] = []
        self._load_books()
    
    def _load_books(self):
        """Загружает книги из хранилища."""
        self._books = self._storage.load()
    
    def _save_books(self):
        """Сохраняет книги в хранилище."""
        self._storage.save(self._books)
    
    def _add_to_history(self, action: str):
        """Добавляет действие в историю."""
        self._history.add_action(action)
    
    def add_book(self, title: str, author: str, genre: str, pages: int) -> bool:
        """Добавляет новую книгу."""
        try:
            book = Book(title, author, genre, pages)
            self._books.append(book)
            self._save_books()
            self._add_to_history(f"Добавлена книга: {title}")
            return True
        except ValueError as e:
            print(f"❌ Ошибка: {e}")
            return False
    
    def edit_book(self, index: int, title: str, author: str, genre: str, pages: int) -> bool:
        """Редактирует книгу."""
        if index < 0 or index >= len(self._books):
            return False
        
        try:
            old_title = self._books[index].title
            self._books[index].title = title
            self._books[index].author = author
            self._books[index].genre = genre
            self._books[index].pages = pages
            self._save_books()
            self._add_to_history(f"Отредактирована книга: {old_title} → {title}")
            return True
        except ValueError as e:
            print(f"❌ Ошибка: {e}")
            return False
    
    def delete_book(self, index: int) -> bool:
        """Удаляет книгу."""
        if index < 0 or index >= len(self._books):
            return False
        
        deleted_book = self._books.pop(index)
        self._save_books()
        self._add_to_history(f"Удалена книга: {deleted_book.title}")
        return True
    
    def get_all_books(self) -> List[Book]:
        """Возвращает все книги."""
        return self._books.copy()
    
    def filter_books(self, genre: Optional[str] = None, 
                     min_pages: Optional[int] = None, 
                     max_pages: Optional[int] = None) -> List[Book]:
        """Фильтрует книги по критериям."""
        filtered = self._books.copy()
        
        if genre:
            filtered = [b for b in filtered if b.genre.lower() == genre.lower()]
        
        if min_pages is not None:
            filtered = [b for b in filtered if b.pages >= min_pages]
        
        if max_pages is not None:
            filtered = [b for b in filtered if b.pages <= max_pages]
        
        return filtered
    
    def get_history(self, count: int = 10) -> List[str]:
        """Возвращает историю действий."""
        return self._history.get_recent_actions(count)
    
    def undo_last_action(self) -> bool:
        """Отменяет последнее действие (удаляет запись из истории)."""
        if self._history.can_undo():
            action = self._history.undo_last()
            print(f"↩️ Отменено действие: {action}")
            return True
        else:
            print("❌ Нет действий для отмены")
            return False
    
    def get_total_books(self) -> int:
        """Возвращает количество книг."""
        return len(self._books)
