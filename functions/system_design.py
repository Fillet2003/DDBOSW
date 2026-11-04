# system_design.py
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class Status(Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    REVIEW = "Review"
    DONE = "Done"

class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    def __str__(self):
        return f"User({self.name}, {self.email})"

class Task:
    def __init__(self, task_id: int, title: str, description: str,
                 priority: Priority, due_date: datetime):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.status = Status.TODO
        self.assignee: Optional[User] = None
        self.created_at = datetime.now()

    def assign_to(self, user: User):
        """Назначение задачи пользователю"""
        self.assignee = user
        self.status = Status.IN_PROGRESS

    def update_status(self, new_status: Status):
        """Обновление статуса задачи"""
        self.status = new_status

    def is_overdue(self) -> bool:
        """Проверка просрочки задачи"""
        return datetime.now() > self.due_date

    def __str__(self):
        return f"Task '{self.title}' ({self.status.value})"

# Пример использования проектирования
def demonstrate_design():
    # Создаем пользователей
    user1 = User(1, "Иван Петров", "ivan@company.com")
    user2 = User(2, "Мария Сидорова", "maria@company.com")

    # Создаем задачу
    due_date = datetime.now() + timedelta(days=7)
    task = Task(1, "Разработать модуль аутентификации",
                "Создать систему входа и регистрации пользователей",
                Priority.HIGH, due_date)

    # Назначаем задачу
    task.assign_to(user1)
    print(f"Задача создана: {task}")
    print(f"Исполнитель: {task.assignee}")

if __name__ == "__main__":
    demonstrate_design()