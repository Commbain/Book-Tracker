# main.py
from utils.storage import BookStorage
from utils.history import ActionHistory
from controllers.book_controller import BookController
from views.console_view import ConsoleView

def main():
    storage = BookStorage("books.json")
    history = ActionHistory()
    controller = BookController(storage, history)
    view = ConsoleView()
    
    while True:
        view.display_menu()
        choice = view.get_input("Выберите действие (1-8): ")
        
        if choice == "1":  # Добавить книгу
            details = view.get_book_details()
            if details:
                if controller.add_book(**details):
                    view.display_message(f"Книга '{details['title']}' добавлена!")
                else:
                    view.display_message("Ошибка добавления книги", True)
        
        elif choice == "2":  # Редактировать книгу
            books = controller.get_all_books()
            index = view.select_book(books, "редактирования")
            if index is not None:
                details = view.get_book_details()
                if details:
                    if controller.edit_book(index, **details):
                        view.display_message(f"Книга обновлена!")
                    else:
                        view.display_message("Ошибка обновления", True)
        
        elif choice == "3":  # Удалить книгу
            books = controller.get_all_books()
            index = view.select_book(books, "удаления")
            if index is not None:
                if controller.delete_book(index):
                    view.display_message("Книга удалена!")
        
        elif choice == "4":  # Показать все книги
            books = controller.get_all_books()
            view.display_books(books, "Все книги")
        
        elif choice == "5":  # Фильтровать книги
            criteria = view.get_filter_criteria()
            if criteria:
                filtered = controller.filter_books(**criteria)
                view.display_books(filtered, "Отфильтрованные книги")
        
        elif choice == "6":  # История действий
            history = controller.get_history(10)
            view.display_books([], "История действий")
            for i, action in enumerate(history, 1):
                print(f"   {i}. {action}")
        
        elif choice == "7":  # Отменить действие
            controller.undo_last_action()
        
        elif choice == "8":  # Выход
            view.display_message("До свидания! 👋")
            break
        
        else:
            view.display_message("Неверный выбор! Попробуйте снова.", True)

if __name__ == "__main__":
    main()
