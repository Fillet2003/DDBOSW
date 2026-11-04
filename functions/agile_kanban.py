# agile_kanban.py
from dataclasses import dataclass
from typing import List, Dict
from functions.system_design import Task, Status


@dataclass
class KanbanBoard:
    """Канбан-доска для Agile управления"""
    todo: List[Task]
    in_progress: List[Task]
    review: List[Task]
    done: List[Task]

    def move_task(self, task: Task, from_column: str, to_column: str):
        """Перемещение задачи между колонками"""
        # Удаляем из исходной колонки
        getattr(self, from_column).remove(task)

        # Добавляем в целевую колонку
        getattr(self, to_column).append(task)

        # Обновляем статус задачи
        status_mapping = {
            'todo': Status.TODO,
            'in_progress': Status.IN_PROGRESS,
            'review': Status.REVIEW,
            'done': Status.DONE
        }
        task.update_status(status_mapping[to_column])

    def get_board_stats(self) -> Dict:
        """Статистика по доске"""
        return {
            'todo': len(self.todo),
            'in_progress': len(self.in_progress),
            'review': len(self.review),
            'done': len(self.done),
            'completion_rate': len(self.done) / max(sum([
                len(self.todo), len(self.in_progress),
                len(self.review), len(self.done)
            ]), 1)
        }