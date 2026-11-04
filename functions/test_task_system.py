# test_task_system.py
import unittest
from datetime import datetime, timedelta
from functions.task_manager import TaskManager
from functions.system_design import Priority, Status

class TestTaskSystem(unittest.TestCase):
    def setUp(self):
        """Настройка тестовой среды"""
        self.manager = TaskManager()
        self.user = self.manager.create_user("Тест User", "test@test.com")
        self.due_date = datetime.now() + timedelta(days=5)

    def test_task_creation(self):
        """Тест создания задачи"""
        task = self.manager.create_task(
            "Тестовая задача",
            "Описание тестовой задачи",
            Priority.MEDIUM,
            self.due_date
        )

        self.assertEqual(task.title, "Тестовая задача")
        self.assertEqual(task.status, Status.TODO)
        self.assertIsNone(task.assignee)

    def test_task_assignment(self):
        """Тест назначения задачи"""
        task = self.manager.create_task(
            "Назначаемая задача",
            "Должна быть назначена пользователю",
            Priority.HIGH,
            self.due_date
        )

        # Назначаем задачу
        success = self.manager.assign_task(task.task_id, self.user.user_id)

        self.assertTrue(success)
        self.assertEqual(task.assignee.user_id, self.user.user_id)
        self.assertEqual(task.status, Status.IN_PROGRESS)

    def test_overdue_detection(self):
        """Тест обнаружения просроченных задач"""
        # Создаем просроченную задачу
        past_date = datetime.now() - timedelta(days=1)
        overdue_task = self.manager.create_task(
            "Просроченная задача",
            "Должна быть обнаружена как просроченная",
            Priority.LOW,
            past_date
        )

        overdue_tasks = self.manager.get_overdue_tasks()
        self.assertIn(overdue_task, overdue_tasks)

    def test_user_tasks_retrieval(self):
        """Тест получения задач пользователя"""
        task1 = self.manager.create_task("Задача 1", "Описание 1", Priority.MEDIUM, self.due_date)
        task2 = self.manager.create_task("Задача 2", "Описание 2", Priority.LOW, self.due_date)

        self.manager.assign_task(task1.task_id, self.user.user_id)
        self.manager.assign_task(task2.task_id, self.user.user_id)

        user_tasks = self.manager.get_user_tasks(self.user.user_id)
        self.assertEqual(len(user_tasks), 2)

    def test_report_generation(self):
        """Тест генерации отчета"""
        # Создаем несколько задач
        for i in range(3):
            self.manager.create_task(
                f"Задача {i}",
                f"Описание {i}",
                Priority.MEDIUM,
                self.due_date
            )

        report = self.manager.generate_report()

        self.assertEqual(report["total_tasks"], 3)
        self.assertEqual(report["status_distribution"]["To Do"], 3)

# Запуск тестов
if __name__ == "__main__":
    # Создаем test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskSystem)

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print(f"\nРезультаты тестирования:")
    print(f"Пройдено тестов: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено тестов: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")