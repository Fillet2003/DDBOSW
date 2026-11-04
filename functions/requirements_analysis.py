# requirements_analysis.py
"""
Требования к системе управления задачами:
1. Функциональные требования:
   - Создание задач (название, описание, приоритет, срок)
   - Назначение задач пользователям
   - Отслеживание статуса задач
   - Уведомления о просроченных задачах

2. Нефункциональные требования:
   - Время отклика < 2 секунды
   - Поддержка 100+ пользователей
   - 99% доступность в рабочее время
"""

class TaskRequirement:
    def __init__(self, description, priority, category):
        self.description = description
        self.priority = priority  # High, Medium, Low
        self.category = category  # Functional, Non-functional

    def validate(self):
        """Валидация требований"""
        if not self.description:
            raise ValueError("Требование должно иметь описание")
        return True

# Пример требований
requirements = [
    TaskRequirement("Система должна позволять создавать задачи", "High", "Functional"),
    TaskRequirement("Время отклика менее 2 секунд", "Medium", "Non-functional")
]

print("Собранные требования:")
for req in requirements:
    print(f"- {req.description} ({req.category}, {req.priority})")