from functions.system_design import Task, User, Priority, Status
from functions.agile_kanban import KanbanBoard
# from functions.maintenance_monitoring import MonitoringSystem, MonitoredTaskManager
from functions.requirements_analysis import TaskRequirement
from functions.task_manager import TaskManager
from functions.time_management import TimeEntry, TimeTracker
from datetime import datetime
import time

# Инициация объекта TaskManager
tm = TaskManager()

# Создание пользователей
user_Ibara = tm.create_user(name="Saegusa Ibara", email="saegusa.i@es.cospro.com")
user_Eichi = tm.create_user(name="Tenshouin Eichi", email="tenshouin.e@es.starpro.com")

# Создание задач
task_presentation = tm.create_task(title="Подготовить презентацию",
                         description="На основе отчёта о летних продажах подготовить презентацию",
                         priority=Priority.MEDIUM,
                         due_date=datetime(2027, 8, 25))
task_mouse = tm.create_task(title="Запустить мышей шпионов",
                         description="Маёй и Сома переловили всех мышей, нужно выпустить новых в восточное крыло",
                         priority=Priority.LOW,
                         due_date=datetime(2026, 11, 25))
task_chocolate = tm.create_task(title="Закупить шоколад",
                         description="Его Превосходительство хочет шоколадки с 55% какао из кондитерской Финти-флюшки",
                         priority=Priority.CRITICAL,
                         due_date=datetime(2026, 11, 7, 18, 0))
task_theatre = tm.create_task(title="Купить билеты",
                         description="Купить билеты на представление Ватару",
                         priority=Priority.CRITICAL,
                         due_date=datetime(2026, 11, 6, 18, 0))
task_DDD = tm.create_task(title="Распустить Trickstar",
                         description="Трикстары достали, надо их распустить",
                         priority=Priority.MEDIUM,
                         due_date=datetime(2016, 11, 6, 18, 0))

# Назначение задач
tm.assign_task(task_id=task_presentation.task_id, user_id=user_Ibara.user_id)
tm.assign_task(task_id=task_chocolate.task_id, user_id=user_Ibara.user_id)
tm.assign_task(task_id=task_mouse.task_id, user_id=user_Ibara.user_id)

# Актуализация статусов
task_chocolate.update_status(Status.REVIEW)
task_mouse.update_status(Status.DONE)

# Вывод всех задач пользователя
tasks = tm.get_user_tasks(user_Ibara.user_id)
for task in tasks:
    print(task)

# Вывод отчёта
report = tm.generate_report()
for k, i in report.items():
    print(f"{k}: {i}")

# ------------------------------------------------------
# Тестирование time_management.py

ttr = TimeTracker(tm)

# Ручной ввод записи
ttr.log_time(task_presentation.task_id, user_Ibara.user_id,
            start=datetime(2026, 4, 2), end=datetime(2026, 10, 31), comment="Отчёт готов")
print(ttr.total_hours_for_user(user_Ibara.user_id))

# Проверка таймера
ttr.start_timer(task_theatre.task_id, user_Eichi.user_id, comment="labui")
time.sleep(4)
ttr.stop_timer(task_theatre.task_id)

print(ttr.total_hours_for_user(user_Eichi.user_id))
print(ttr.total_seconds_for_user(user_Eichi.user_id))

# Проверка отчёта
report = ttr.generate_report()
for k, i in report.items():
    print(f"{k}: {i}")