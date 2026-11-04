# task_manager.py
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from functions.system_design import Task, User, Priority 

class TaskManager:
    """Класс для управления задачами"""

    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.users: Dict[int, User] = {}
        self.next_task_id = 1
        self.next_user_id = 1

    def create_user(self, name: str, email: str) -> User:
        """Создание нового пользователя"""
        user = User(self.next_user_id, name, email)
        self.users[self.next_user_id] = user
        self.next_user_id += 1
        return user

    def create_task(self, title: str, description: str,
                   priority: Priority, due_date: datetime) -> Task:
        """Создание новой задачи"""
        task = Task(self.next_task_id, title, description, priority, due_date)
        self.tasks[self.next_task_id] = task
        self.next_task_id += 1
        return task

    def assign_task(self, task_id: int, user_id: int) -> bool:
        """Назначение задачи пользователю"""
        task = self.tasks.get(task_id)
        user = self.users.get(user_id)

        if task and user:
            task.assign_to(user)
            return True
        return False

    def get_overdue_tasks(self) -> List[Task]:
        """Получение списка просроченных задач"""
        return [task for task in self.tasks.values() if task.is_overdue()]

    def get_user_tasks(self, user_id: int) -> List[Task]:
        """Получение задач конкретного пользователя"""
        return [task for task in self.tasks.values()
                if task.assignee and task.assignee.user_id == user_id]

    def generate_report(self) -> Dict:
        """Генерация отчета по задачам"""
        total_tasks = len(self.tasks)
        overdue_tasks = len(self.get_overdue_tasks())

        status_count = {}
        for task in self.tasks.values():
            status_count[task.status] = status_count.get(task.status, 0) + 1

        return {
            "total_tasks": total_tasks,
            "overdue_tasks": overdue_tasks,
            "status_distribution": {status.value: count for status, count in status_count.items()},
            "report_generated_at": datetime.now().isoformat()
        }

# Демонстрация работы системы
def demo_implementation():
    manager = TaskManager()

    # Создаем пользователей
    developer = manager.create_user("Алексей Кодлов", "alexey@company.com")
    tester = manager.create_user("Елена Тестова", "elena@company.com")

    # Создаем задачи
    task1 = manager.create_task(
        "Разработать REST API",
        "Создать API для управления задачами",
        Priority.HIGH,
        datetime.now() + timedelta(days=14)
    )

    task2 = manager.create_task(
        "Написать unit-тесты",
        "Покрыть код модульными тестами",
        Priority.MEDIUM,
        datetime.now() + timedelta(days=7)
    )

    # Назначаем задачи
    manager.assign_task(task1.task_id, developer.user_id)
    manager.assign_task(task2.task_id, tester.user_id)

    # Генерируем отчет
    report = manager.generate_report()
    print("Отчет по задачам:")
    print(json.dumps(report, indent=2, ensure_ascii=False))

    # Показываем задачи разработчика
    dev_tasks = manager.get_user_tasks(developer.user_id)
    print(f"\nЗадачи разработчика {developer.name}:")
    for task in dev_tasks:
        print(f"  - {task.title} ({task.status.value})")

if __name__ == "__main__":
    demo_implementation()