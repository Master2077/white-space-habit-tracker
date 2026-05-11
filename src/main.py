from pathlib import Path


FILE_PATH = Path('habits.json')


def load_habits() -> list[str]:
    """Загружает задачи из файла. Возвращает пустой список, если файла нет"""
    if not FILE_PATH.exists():
        return []

    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except Exception as e:
        print(f'⚠️ Ошибка чтения файла: {e}')


def save_habits(habits: list[str]) -> None :
    """Сохраняет задачи в файл"""
    try:
        with open(FILE_PATH, 'w', encoding='utf-8') as file:
            for habit in habits:
                file.write(habit + '\n')
    except Exception as e:
        print(f'❌ Ошибка записи в файл: {e}")')


def viev_habits() -> None:
    """Показывает список задач"""
    habits = load_habits()
    if not habits:
        print('У тебя пока нет привычек. Создай первую и стремись к вершине')
        return

    print('\nТвои привычки:')
    for i, habit in enumerate(habits, start=1):
        print(f'{i}. {habit}')


def add_habits() -> None:
    """Добавляем новую привычку"""
    habits = load_habits()
    new_habit = input('Новая привычка: ').strip()

    if not new_habit:
        print('Ничего — это не привычка')
        return

    if new_habit in habits:
        print('У тебя уже есть такая привычка. Не повторяйся')
        return

    habits.append(new_habit)
    save_habits(habits)
    print(f'✅ Привычка "{new_habit}" успешно добавлена')

def delet_habit() -> None:
    """Удаляет привычку по номеру"""
    habits = load_habits()
    if not habits:
        print('У тебя нет активных привычек')
        return

    viev_habits()
    try:
        num = int(input('\nНомер привычки для удаления: '))
        if 1<= num <= len(habits):
            removed = habits.pop(num - 1)
            save_habits(habits)
            print(f'Привычка "{removed}" удалена 🗑️')
        else:
            print('Данного номера не существует')
    except IndexError as i:
        print(f'❌ Ошибка индекса при удалении: {i}')
    except ValueError:
        print('Нужно ввести номер привычки, а не что-то другое')


def main_menu() -> None:
    """Меню пользователя"""
    print('\n'+'='*50)
    print('WHITE SPACE — ТРЕКЕР ПРИВЫЧЕК v0.1')
    print('='*50)
    print('1. Посмотреть привычки')
    print('2. Добавить новую привычку')
    print('3. Удалить привычку')
    print('4. Выйти')
    print('='*50)


def rum() -> None:
    """Результат операции пользователя"""
    while True:
        main_menu()
        choice = input('Выбери действие: ')

        if choice == '1':
            viev_habits()
        elif choice == '2':
            add_habits()
        elif choice == '3':
            delet_habit()
        elif choice == '4':
            print('Продолжим в следующей итерации')
            break
        else:
            print('Данного выбора не существует')


if __name__ == '__main__':
    rum()

