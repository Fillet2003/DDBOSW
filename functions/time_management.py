# time_management.py
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from functions.system_design import Task, User, Status
from functions.task_manager import TaskManager


@dataclass
class TimeEntry:
    """Одна сессия работы над задачей (завершённая или идущая)"""
    entry_id: int
    task: Task
    user: User
    start_time: datetime
    end_time: Optional[datetime] = None
    comment: str = ""

    def is_running(self) -> bool:
        """Идёт ли таймер прямо сейчас"""
        return self.end_time is None

    def duration(self) -> timedelta:
        """Длительность. Для бегущей записи — от старта до текущего момента"""
        end = self.end_time if self.end_time is not None else datetime.now()
        return end - self.start_time

    def hours(self) -> float:
        """Длительность в часах (дробное число)"""
        return self.duration().total_seconds() / 3600

    def stop(self):
        """Остановить запись, если она ещё идёт"""
        if self.is_running():
            self.end_time = datetime.now()

    def __str__(self):
        state = "▶ running" if self.is_running() else "■ stopped"
        return (f"TimeEntry #{self.entry_id} [{state}] "
                f"{self.hours():.2f}h on '{self.task.title}'")


class TimeTracker:
    """Модуль учёта времени"""

    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.entries: List[TimeEntry] = []
        self.active_timers: Dict[int, TimeEntry] = {}   # task_id -> running entry
        self.next_entry_id = 1

    """Управление таймерами"""

    def start_timer(self, task_id: int, user_id: int,
                    comment: str = "") -> Optional[TimeEntry]:
        """Запустить таймер для задачи.
        Возвращает запись или None, если задача/пользователь не найдены."""
        task = self.task_manager.tasks.get(task_id)
        user = self.task_manager.users.get(user_id)
        if not task or not user:
            return None

        # Если таймер уже идёт — вернуть существующий, не создавать повторение
        if task_id in self.active_timers:
            return self.active_timers[task_id]

        entry = TimeEntry(
            entry_id=self.next_entry_id,
            task=task,
            user=user,
            start_time=datetime.now(),
            end_time=None,
            comment=comment,
        )
        self.entries.append(entry)
        self.active_timers[task_id] = entry
        self.next_entry_id += 1

        # Обновить статус задачи — «в работе»
        if task.status != Status.IN_PROGRESS:
            task.update_status(Status.IN_PROGRESS)

        print("Таймер запущен")
        return entry

    def stop_timer(self, task_id: int) -> Optional[TimeEntry]:
        """Остановить таймер. Возвращает остановленную запись или None."""
        entry = self.active_timers.pop(task_id, None)
        if entry is None:
            return None
        entry.stop()
        print("Таймер остановлен")
        return entry

    def is_timer_running(self, task_id: int) -> bool:
        return task_id in self.active_timers

    def get_active_timers(self) -> List[TimeEntry]:
        return list(self.active_timers.values())

    """ Ручная запись (без таймера) """

    def log_time(self, task_id: int, user_id: int,
                 start: datetime, end: datetime,
                 comment: str = "") -> Optional[TimeEntry]:
        """Записать прошедший отрезок работы вручную."""
        task = self.task_manager.tasks.get(task_id)
        user = self.task_manager.users.get(user_id)
        if not task or not user or end < start:
            return None

        entry = TimeEntry(self.next_entry_id, task, user, start, end, comment)
        self.entries.append(entry)
        self.next_entry_id += 1
        return entry

    """ Общее время """

    def total_hours_for_task(self, task_id: int) -> float:
        """Общее время по задаче (включая идущий таймер)"""
        return sum(e.hours() for e in self.entries if e.task.task_id == task_id)

    def total_seconds_for_task(self, task_id: int) -> float:
            """Общее время по задаче (включая идущий таймер)"""
            return sum(e.duration().total_seconds() for e in self.entries if e.task.task_id == task_id)

    def total_hours_for_user(self, user_id: int) -> float:
        """Общее время по пользователю (включая идущий таймер)"""
        return sum(e.hours() for e in self.entries if e.user.user_id == user_id)

    def total_seconds_for_user(self, user_id: int) -> float:
            """Общее время по пользователю (включая идущий таймер)"""
            return sum(e.duration().total_seconds() for e in self.entries if e.user.user_id == user_id)

    """ Генерация отчётов """

    def generate_report(self, start: Optional[datetime] = None,
                        end: Optional[datetime] = None) -> Dict:
        """Отчёт по времени. Период необязателен: по умолчанию — всё до текущего момента."""
        end = end or datetime.now()
        relevant = [
            e for e in self.entries
            if (start is None or e.start_time >= start) and e.start_time <= end
        ]

        by_task: Dict[str, float] = {}
        by_user: Dict[str, float] = {}
        for e in relevant:
            by_task[e.task.title] = by_task.get(e.task.title, 0.0) + e.hours()
            by_user[e.user.name] = by_user.get(e.user.name, 0.0) + e.hours()

        return {
            "period": {
                "from": start.isoformat() if start else None,
                "to": end.isoformat(),
            },
            "total_entries": len(relevant),
            "total_hours": sum(e.hours() for e in relevant),
            "by_task": by_task,
            "by_user": by_user,
            "generated_at": datetime.now().isoformat(),
        }