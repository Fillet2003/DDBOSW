# maintenance_monitoring.py
import logging
import time
from datetime import datetime
from typing import Dict, Any

class MonitoringSystem:
    """Система мониторинга для сопровождения ПО"""

    def __init__(self):
        self.setup_logging()
        self.performance_metrics: Dict[str, list] = {
            'response_times': [],
            'error_count': 0,
            'tasks_created': 0
        }

    def setup_logging(self):
        """Настройка системы логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('TaskManager')

    def log_operation(self, operation: str, duration: float = None, success: bool = True):
        """Логирование операций"""
        if duration is not None:
            self.performance_metrics['response_times'].append(duration)

        if not success:
            self.performance_metrics['error_count'] += 1

        if operation == 'create_task':
            self.performance_metrics['tasks_created'] += 1

        level = logging.INFO if success else logging.ERROR
        message = f"Operation: {operation}, Duration: {duration:.3f}s, Success: {success}"
        self.logger.log(level, message)

    def measure_performance(self, operation_name: str):
        """Декоратор для измерения производительности"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time
                    self.log_operation(operation_name, duration, True)
                    return result
                except Exception as e:
                    duration = time.time() - start_time
                    self.log_operation(operation_name, duration, False)
                    self.logger.error(f"Error in {operation_name}: {str(e)}")
                    raise
            return wrapper
        return decorator

    def generate_maintenance_report(self) -> Dict[str, Any]:
        """Генерация отчета для сопровождения"""
        response_times = self.performance_metrics['response_times']
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        report = {
            'timestamp': datetime.now().isoformat(),
            'performance_metrics': {
                'average_response_time': avg_response_time,
                'total_operations': len(response_times),
                'error_rate': self.performance_metrics['error_count'] / max(len(response_times), 1),
                'total_tasks_created': self.performance_metrics['tasks_created']
            },
            'recommendations': self.generate_recommendations(avg_response_time)
        }
        return report

    def generate_recommendations(self, avg_response_time: float) -> List[str]:
        """Генерация рекомендаций по улучшению"""
        recommendations = []

        if avg_response_time > 1.0:
            recommendations.append("Рассмотреть оптимизацию базы данных - высокое время ответа")

        if self.performance_metrics['error_count'] > 10:
            recommendations.append("Провести анализ ошибок - высокий уровень ошибок")

        if self.performance_metrics['tasks_created'] > 1000:
            recommendations.append("Рассмотреть масштабирование системы - высокий уровень использования")

        return recommendations if recommendations else ["Система работает стабильно"]

# Модифицированный TaskManager с мониторингом
class MonitoredTaskManager(TaskManager):
    def __init__(self):
        super().__init__()
        self.monitor = MonitoringSystem()

    @MonitoringSystem.measure_performance.__func__('create_task')
    def create_task(self, title: str, description: str,
                   priority: Priority, due_date: datetime) -> Task:
        return super().create_task(title, description, priority, due_date)

    @MonitoringSystem.measure_performance.__func__('assign_task')
    def assign_task(self, task_id: int, user_id: int) -> bool:
        return super().assign_task(task_id, user_id)

# Демонстрация системы мониторинга
def demo_maintenance():
    manager = MonitoredTaskManager()

    # Имитация работы системы
    for i in range(5):
        try:
            task = manager.create_task(
                f"Тестовая задача {i}",
                "Описание",
                Priority.MEDIUM,
                datetime.now() + timedelta(days=7)
            )

            if i % 3 == 0:  # Имитация occasional ошибок
                manager.assign_task(999, 999)  # Несуществующие ID
            else:
                user = manager.create_user(f"User{i}", f"user{i}@test.com")
                manager.assign_task(task.task_id, user.user_id)

        except Exception:
            pass  # Ошибки уже залогированы

    # Генерация отчета сопровождения
    report = manager.monitor.generate_maintenance_report()
    print("Отчет сопровождения:")
    for key, value in report.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    demo_maintenance()