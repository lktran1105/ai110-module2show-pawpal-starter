from dataclasses import dataclass, field
from datetime import date, time


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


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
        """Update this task's priority."""
        self.priority = new_priority

    def change_date(self, new_date: date) -> None:
        """Reschedule this task to a new date."""
        self.task_date = new_date

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.is_complete = True


@dataclass
class Pet:
    name: str
    age: int
    species: str
    breed: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task_name: str) -> None:
        """Remove a task from this pet by name."""
        self.tasks = [t for t in self.tasks if t.task_name != task_name]

    def get_tasks(self) -> list[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def create_pet(self, name: str, species: str, breed: str, age: int) -> Pet:
        """Create a new pet and add it to this owner's pets."""
        pet = Pet(name=name, age=age, species=species, breed=breed)
        self.pets.append(pet)
        return pet

    def delete_pet(self, pet_name: str) -> None:
        """Remove a pet from this owner by name."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def edit_pet_info(self, pet: Pet, attribute: str, value) -> None:
        """Update a single attribute on one of this owner's pets."""
        setattr(pet, attribute, value)

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


@dataclass
class Scheduler:
    owner: Owner

    def generate_schedule(self, available_minutes: int) -> dict[str, list[Task]]:
        """Build a priority-ordered, time-boxed schedule for each of the owner's pets."""
        schedule = {}
        for pet in self.owner.pets:
            schedule[pet.name] = self._fit_tasks_to_time(pet.get_tasks(), available_minutes)
        return schedule

    def get_tasks_for_date(self, target_date: date) -> dict[str, list[Task]]:
        """Return each pet's tasks that fall on the given date."""
        schedule = {}
        for pet in self.owner.pets:
            matching = [t for t in pet.get_tasks() if t.task_date == target_date]
            if matching:
                schedule[pet.name] = matching
        return schedule

    def _fit_tasks_to_time(self, tasks: list[Task], available_minutes: int) -> list[Task]:
        """Greedily select pending tasks by priority that fit within the time budget."""
        pending = [t for t in tasks if not t.is_complete]
        ordered = sorted(pending, key=lambda t: PRIORITY_ORDER.get(t.priority.lower(), len(PRIORITY_ORDER)))

        selected = []
        remaining_minutes = available_minutes
        for task in ordered:
            if task.duration_minutes <= remaining_minutes:
                selected.append(task)
                remaining_minutes -= task.duration_minutes
        return selected
