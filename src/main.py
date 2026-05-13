from pathlib import Path
from datetime import datetime, date
import json


FILE_PATH = Path('habits.json')


def load_habits() -> list[dict]:
    """Загружает привычки из файла. Возвращает пустой список, если файла нет"""
    if not FILE_PATH.exists() or FILE_PATH.stat().st_size == 0:
        return []

    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f'⚠️ Ошибка. Файл чтения поврежден: {e}')
        return []


def save_habits(habits: list[dict]) -> None :
    """Сохраняет привычки в файл json"""
    try:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(habits, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f'❌ Ошибка записи в файл: {e}")')


def viev_habits() -> None:
    """Показывает список привычек"""
    habits = load_habits()
    if not habits:
        print('У тебя пока нет привычек. Создай первую и стремись к вершине')
        return

    print('\n🔥 Твои привычки:')
    for i, habit in enumerate(habits, start=1):
        status = '✅' if habit.get('done_today', False) else '⭕'
        print(f'{i}. {habit['name']} {status} — Стрик: {habit['streak']}')


def add_habits() -> None:
    """Добавляем новую привычку"""
    habits = load_habits()
    new_habit = input('Новая привычка: ').strip()

    if not new_habit:
        print('Ничего — это не привычка')
        return

    if any(h['name'].lower() == new_habit.lower() for h in habits):
        print('У тебя уже есть такая привычка. Не повторяйся')
        return

    habits.append({
        'name': new_habit,
        'created': datetime.now().isoformat(),
        'done_today': False,
        'streak': 0,
        'last_reset': date.today().isoformat(),
        'count_for_reset_streak': 0
    })
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
            print(f'Привычка "{removed['name']}" удалена 🗑️')
        else:
            print('Данного номера не существует')
    except IndexError as i:
        print(f'❌ Ошибка индекса при удалении: {i}')
    except ValueError:
        print('Нужно ввести номер привычки, а не что-то другое')


def mark_done() -> None:
    """Отмечаем выполненную привычку за день"""
    habits = load_habits()
    if not habits:
        print('Сначала создай привычку, потом отмечай')
        return
    viev_habits()
    try:
        num = int(input('\nНомер выполненной привычки: '))
        if not (1 <= num <= len(habits)):
            print('Неверный номер')

        habit = habits[num - 1]

        if habit.get('done_today', False):
            print('Ты уже выполнил эту привычку сегодня')
            return

        habit['done_today'] = True
        habit['streak'] = habit.get('streak', 0) + 1
        save_habits(habits)
        print(f'🔥 "{habit['name']}" выполнена! Стрик: {habit['streak']}')
    except IndexError as i:
        print(f'❌ Ошибка индекса при отметке: {i}')
    except ValueError:
        print('Нужно ввести номер привычки, а не что-то другое')


def reset_daily_habits() -> None:
    """Автоматический сброс done_today каждый новый день"""
    today_str = date.today().isoformat()
    habits = load_habits()
    changed = False

    for habit in habits:
        if habit.get('last_reset') != today_str:
            habit['last_reset'] = date.today().isoformat()
            habit['done_today'] = False
            changed = True

    if changed:
        save_habits(habits)
        print('Новый день! Все привычки сброшены. Начинаем снова!')


def reset_streak() -> None:
    """Автоматически обнуляет серию стриков при пропуске выполнения привычки за день"""
    habits = load_habits()
    today_str = date.today().isoformat()
    changed = False

    for habit in habits:
        last_reset = habit.get('last_reset')
        count = habit.get('count_for_reset_streak', 0)
        if habit.get('done_today', False) is False and last_reset != today_str:
            count += 1
            habit['count_for_reset_streak'] = count

        if count >= 2:
            habit['streak'] = 0
            habit['count_for_reset_streak'] = 0
        changed = True

    if changed:
        save_habits(habits)


def main_menu() -> None:
    """Меню пользователя"""
    print('\n'+'='*50)
    print('WHITE SPACE — ТРЕКЕР ПРИВЫЧЕК v0.2')
    print('='*50)
    print('1. Посмотреть привычки')
    print('2. Добавить новую привычку')
    print('3. Отметить выполненной')
    print('4. Удалить привычку')
    print('5. Выйти')
    print('='*50)


def run() -> None:
    """Результат операции пользователя"""
    reset_streak()
    reset_daily_habits()


    while True:
        main_menu()
        choice = input('Выбери действие: ')

        if choice == '1':
            viev_habits()
        elif choice == '2':
            add_habits()
        elif choice == '3':
            mark_done()
        elif choice == '4':
            delet_habit()
        elif choice == '5':
            print('Продолжим в следующей итерации')
            break
        else:
            print('Данного выбора не существует')


if __name__ == '__main__':
    run()
