from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Task:
    task_name: str
    description: str
    priority: str
    task_date: date
    task_time: time
    duration_minutes: int
    is_complete: bool = False

    def change_priority(self, new_priority: str) -> None:
        pass

    def change_date(self, new_date: date) -> None:
        pass


@dataclass
class Pet:
    name: str
    age: int
    species: str
    breed: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_name: str) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def create_pet(self, name: str, species: str, breed: str, age: int) -> Pet:
        pass

    def delete_pet(self, pet_name: str) -> None:
        pass

    def edit_pet_info(self, pet: Pet, attribute: str, value) -> None:
        pass


@dataclass
class Schedule:
    tasks: list[Task] = field(default_factory=list)

    def generate_schedule(self, available_minutes: int) -> list[Task]:
        pass

    def get_tasks_for_date(self, target_date: date) -> list[Task]:
        pass
