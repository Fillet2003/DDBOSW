# test_time_management.py
import unittest
from datetime import datetime, timedelta

from functions.system_design import Priority, Status
from functions.task_manager import TaskManager
from functions.time_management import TimeTracker


class TestTimeTracker(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()
        self.user = self.manager.create_user("Иван", "ivan@test.com")
        self.user2 = self.manager.create_user("Мария", "maria@test.com")
        self.task = self.manager.create_task(
            "Тестовая задача", "Описание", Priority.HIGH,
            datetime.now() + timedelta(days=7),
        )
        self.tracker = TimeTracker(self.manager)

    """ Тестирование таймеров """

    def test_start_timer_creates_running_entry(self):
        entry = self.tracker.start_timer(self.task.task_id, self.user.user_id)
        self.assertIsNotNone(entry)
        self.assertTrue(entry.is_running())
        self.assertEqual(entry.task.task_id, self.task.task_id)
        self.assertEqual(entry.user.user_id, self.user.user_id)
        self.assertTrue(self.tracker.is_timer_running(self.task.task_id))

    def test_start_timer_unknown_task(self):
        self.assertIsNone(self.tracker.start_timer(999, self.user.user_id))

    def test_start_timer_unknown_user(self):
        self.assertIsNone(self.tracker.start_timer(self.task.task_id, 999))

    def test_start_timer_twice_returns_same_entry(self):
        e1 = self.tracker.start_timer(self.task.task_id, self.user.user_id)
        e2 = self.tracker.start_timer(self.task.task_id, self.user.user_id)
        self.assertEqual(e1.entry_id, e2.entry_id)
        self.assertEqual(len(self.tracker.entries), 1)

    def test_start_timer_sets_task_in_progress(self):
        self.tracker.start_timer(self.task.task_id, self.user.user_id)
        self.assertEqual(self.task.status, Status.IN_PROGRESS)

    def test_stop_timer_sets_end_time(self):
        self.tracker.start_timer(self.task.task_id, self.user.user_id)
        stopped = self.tracker.stop_timer(self.task.task_id)
        self.assertIsNotNone(stopped)
        self.assertFalse(stopped.is_running())
        self.assertIsNotNone(stopped.end_time)
        self.assertFalse(self.tracker.is_timer_running(self.task.task_id))

    def test_stop_nonexistent_timer_returns_none(self):
        self.assertIsNone(self.tracker.stop_timer(self.task.task_id))

    """ Тестирование ручного ввода записи времени """

    def test_log_time(self):
        now = datetime.now()
        entry = self.tracker.log_time(
            self.task.task_id, self.user.user_id,
            now - timedelta(hours=2), now,
        )
        self.assertIsNotNone(entry)
        self.assertFalse(entry.is_running())
        self.assertAlmostEqual(entry.hours(), 2.0)

    def test_log_time_invalid_dates(self):
        now = datetime.now()
        self.assertIsNone(self.tracker.log_time(
            self.task.task_id, self.user.user_id,
            now, now - timedelta(hours=1),  # конец раньше начала
        ))

    """ Тестирование общего времени """

    def test_total_hours_for_task(self):
        now = datetime.now()
        self.tracker.log_time(self.task.task_id, self.user.user_id,
                              now - timedelta(hours=2), now)
        self.tracker.log_time(self.task.task_id, self.user.user_id,
                              now - timedelta(hours=1), now)
        self.assertAlmostEqual(self.tracker.total_hours_for_task(self.task.task_id), 3.0)

    def test_total_hours_for_user(self):
        task2 = self.manager.create_task("Вторая", "...", Priority.LOW,
                                          datetime.now() + timedelta(days=3))
        now = datetime.now()
        self.tracker.log_time(self.task.task_id, self.user.user_id,
                              now - timedelta(hours=1), now)
        self.tracker.log_time(task2.task_id, self.user.user_id,
                              now - timedelta(hours=2), now)
        self.assertAlmostEqual(self.tracker.total_hours_for_user(self.user.user_id), 3.0)

    """ Тестирование отчётов """

    def test_generate_report(self):
        now = datetime.now()
        self.tracker.log_time(self.task.task_id, self.user.user_id,
                              now - timedelta(hours=2), now)
        report = self.tracker.generate_report()
        self.assertEqual(report["total_entries"], 1)
        self.assertAlmostEqual(report["total_hours"], 2.0)
        self.assertIn(self.task.title, report["by_task"])
        self.assertIn(self.user.name, report["by_user"])

    def test_generate_report_period_filter(self):
        now = datetime.now()
        # внутри периода
        self.tracker.log_time(self.task.task_id, self.user.user_id,
                              now - timedelta(hours=1), now)
        # вне периода
        old = now - timedelta(days=10)
        self.tracker.log_time(self.task.task_id, self.user.user_id,
                              old, old + timedelta(hours=5))
        report = self.tracker.generate_report(start=now - timedelta(days=1))
        self.assertEqual(report["total_entries"], 1)
        self.assertAlmostEqual(report["total_hours"], 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)