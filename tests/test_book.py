# tests/test_book.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.book import Book
from utils.history import ActionHistory
from utils.storage import BookStorage
import json
import tempfile

def test_book_creation():
    """Позитивный тест: создание книги."""
    book = Book("Война и мир", "Толстой", "Роман", 1225)
    assert book.title == "Война и мир"
    assert book.author == "Толстой"
    assert book.genre == "Роман"
    assert book.pages == 1225
    print("✅ test_book_creation пройден")

def test_book_validation():
    """Негативный тест: валидация полей."""
    try:
        book = Book("", "Автор", "Жанр", 100)
        assert False, "Должна быть ошибка"
    except ValueError:
        pass  # Ожидаемая ошибка
    
    try:
        book = Book("Название", "", "Жанр", 100)
        assert False
    except ValueError:
        pass
    
    try:
        book = Book("Название", "Автор", "", 100)
        assert False
    except ValueError:
        pass
    
    try:
        book = Book("Название", "Автор", "Жанр", -10)
        assert False
    except ValueError:
        pass
    
    print("✅ test_book_validation пройден")

def test_book_boundary():
    """Граничный тест: крайние значения."""
    book = Book("Малая книга", "Автор", "Жанр", 1)
    assert book.pages == 1
    
    book = Book("Большая книга", "Автор", "Жанр", 10000)
    assert book.pages == 10000
    
    try:
        book = Book("Слишком большая", "Автор", "Жанр", 10001)
        assert False
    except ValueError:
        pass
    
    print("✅ test_book_boundary пройден")

def test_history():
    """Тест истории действий."""
    history = ActionHistory(max_size=3)
    
    history.add_action("Действие 1")
    history.add_action("Действие 2")
    history.add_action("Действие 3")
    history.add_action("Действие 4")
    
    recent = history.get_recent_actions(3)
    assert len(recent) == 3
    assert recent[-1] == "Действие 4"
    
    assert history.can_undo()
    action = history.undo_last()
    assert action == "Действие 4"
    
    print("✅ test_history пройден")

def test_storage():
    """Тест JSON хранилища."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp_filename = tmp.name
    
    storage = BookStorage(tmp_filename)
    books = storage.load()
    assert len(books) == 0
    
    from models.book import Book
    book = Book("Тест", "Автор", "Жанр", 100)
    storage.save([book])
    
    loaded = storage.load()
    assert len(loaded) == 1
    assert loaded[0].title == "Тест"
    
    import os
    os.unlink(tmp_filename)
    print("✅ test_storage пройден")

def test_book_to_dict():
    """Тест преобразования в словарь."""
    book = Book("1984", "Оруэлл", "Антиутопия", 328)
    data = book.to_dict()
    assert data["title"] == "1984"
    assert data["author"] == "Оруэлл"
    assert data["genre"] == "Антиутопия"
    assert data["pages"] == 328
    print("✅ test_book_to_dict пройден")

def test_book_from_dict():
    """Тест создания из словаря."""
    data = {"title": "Мартин Иден", "author": "Лондон", "genre": "Роман", "pages": 480}
    book = Book.from_dict(data)
    assert book.title == "Мартин Иден"
    assert book.pages == 480
    print("✅ test_book_from_dict пройден")

if __name__ == "__main__":
    print("\n=== ЗАПУСК ТЕСТОВ ===\n")
    test_book_creation()
    test_book_validation()
    test_book_boundary()
    test_history()
    test_storage()
    test_book_to_dict()
    test_book_from_dict()
    print("\n🎉 Все тесты пройдены!")
