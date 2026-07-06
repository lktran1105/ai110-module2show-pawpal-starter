from datetime import date, time

from pawpal_system import Pet, Task


def make_task(name="Morning walk"):
    return Task(name, "Walk around the block", "high", date(2026, 7, 6), time(8, 0), 30)


def test_mark_complete_changes_task_status():
    task = make_task()
    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", age=3, species="Dog", breed="Golden Retriever")
    assert len(pet.get_tasks()) == 0

    pet.add_task(make_task())

    assert len(pet.get_tasks()) == 1
