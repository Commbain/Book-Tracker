# views/console_view.py
from typing import List, Optional
from models.book import Book

class ConsoleView:
    """Консольное представление (вывод меню и данных)."""
    
    @staticmethod
    def display_menu():
        """Отображает главное меню."""
        print("\n" + "=" * 50)
        print("📚 BOOK TRACKER - Управление книгами")
        print("=" * 50)
        print("1. ➕ Добавить книгу")
        print("2. 📝 Редактировать книгу")
        print("3. ❌ Удалить книгу")
        print("4. 📋 Показать все книги")
        print("5. 🔍 Фильтровать книги")
        print("6. 📜 История действий")
        print("7. ↩️ Отменить последнее действие")
        print("8. 💾 Сохранить и выйти")
        print("=" * 50)
    
    @staticmethod
    def get_input(prompt: str) -> str:
        """Получает ввод пользователя."""
        return input(prompt).strip()
    
    @staticmethod
    def display_books(books: List[Book], title: str = "Список книг"):
        """Отображает список книг."""
        if not books:
            print(f"\n📭 {title}: пусто")
            return
        
        print(f"\n📚 {title} ({len(books)} шт.):")
        print("-" * 60)
        for i, book in enumerate(books, 1):
            print(f"{i}. {book}")
        print("-" * 60)
    
    @staticmethod
    def display_book(book: Book, index: int):
        """Отображает одну книгу."""
        print(f"{index}. {book}")
    
    @staticmethod
    def display_message(message: str, is_error: bool = False):
        """Отображает сообщение."""
        prefix = "❌" if is_error else "✅"
        print(f"{prefix} {message}")
    
    @staticmethod
    def get_book_details() -> Optional[dict]:
        """Запрашивает у пользователя данные книги."""
        print("\n📝 Введите данные книги:")
        
        title = input("Название: ").strip()
        if not title:
            ConsoleView.display_message("Название не может быть пустым", True)
            return None
        
        author = input("Автор: ").strip()
        if not author:
            ConsoleView.display_message("Автор не может быть пустым", True)
            return None
        
        genre = input("Жанр: ").strip()
        if not genre:
            ConsoleView.display_message("Жанр не может быть пустым", True)
            return None
        
        try:
            pages = int(input("Количество страниц: "))
            if pages <= 0:
                raise ValueError
        except ValueError:
            ConsoleView.display_message("Количество страниц должно быть положительным числом", True)
            return None
        
        return {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        }
    
    @staticmethod
    def get_filter_criteria() -> Optional[dict]:
        """Запрашивает критерии фильтрации."""
        print("\n🔍 Фильтрация книг:")
        print("1. По жанру")
        print("2. По количеству страниц")
        print("3. По жанру и страницам")
        
        choice = input("Выберите фильтр (1-3): ").strip()
        
        if choice == "1":
            genre = input("Введите жанр: ").strip()
            if genre:
                return {"genre": genre}
        elif choice == "2":
            try:
                min_pages = int(input("Минимум страниц: "))
                max_pages = int(input("Максимум страниц: "))
                return {"min_pages": min_pages, "max_pages": max_pages}
            except ValueError:
                ConsoleView.display_message("Введите корректные числа", True)
        elif choice == "3":
            genre = input("Введите жанр: ").strip()
            try:
                min_pages = int(input("Минимум страниц: "))
                max_pages = int(input("Максимум страниц: "))
                if genre:
                    return {"genre": genre, "min_pages": min_pages, "max_pages": max_pages}
            except ValueError:
                ConsoleView.display_message("Введите корректные числа", True)
        
        return None
    
    @staticmethod
    def select_book(books: List[Book], action: str) -> Optional[int]:
        """Позволяет пользователю выбрать книгу."""
        if not books:
            ConsoleView.display_message("Нет книг для выбора", True)
            return None
        
        ConsoleView.display_books(books, f"Выберите книгу для {action}")
        try:
            choice = int(input(f"Введите номер (1-{len(books)}): "))
            if 1 <= choice <= len(books):
                return choice - 1
            else:
                ConsoleView.display_message("Неверный номер", True)
                return None
        except ValueError:
            ConsoleView.display_message("Введите число", True)
            return None
