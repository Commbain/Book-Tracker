# models/book.py
from typing import Dict, Any

class Book:
    """Модель книги с инкапсуляцией данных."""
    
    def __init__(self, title: str, author: str, genre: str, pages: int):
        self._title = title
        self._author = author
        self._genre = genre
        self._pages = pages
    
    # Геттеры и сеттеры (инкапсуляция)
    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Название не может быть пустым")
        self._title = value.strip()
    
    @property
    def author(self) -> str:
        return self._author
    
    @author.setter
    def author(self, value: str):
        if not value or not value.strip():
            raise ValueError("Автор не может быть пустым")
        self._author = value.strip()
    
    @property
    def genre(self) -> str:
        return self._genre
    
    @genre.setter
    def genre(self, value: str):
        if not value or not value.strip():
            raise ValueError("Жанр не может быть пустым")
        self._genre = value.strip()
    
    @property
    def pages(self) -> int:
        return self._pages
    
    @pages.setter
    def pages(self, value: int):
        if value <= 0:
            raise ValueError("Количество страниц должно быть положительным числом")
        if value > 10000:
            raise ValueError("Количество страниц не может превышать 10000")
        self._pages = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует книгу в словарь для JSON."""
        return {
            "title": self._title,
            "author": self._author,
            "genre": self._genre,
            "pages": self._pages
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Book':
        """Создает книгу из словаря."""
        return cls(
            title=data["title"],
            author=data["author"],
            genre=data["genre"],
            pages=data["pages"]
        )
    
    def __str__(self) -> str:
        return f"📖 {self._title} | {self._author} | {self._genre} | {self._pages} стр."
    
    def __repr__(self) -> str:
        return f"Book('{self._title}', '{self._author}', '{self._genre}', {self._pages})"
