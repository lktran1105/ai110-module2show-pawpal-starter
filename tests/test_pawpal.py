from datetime import date, time

from pawpal_system import Owner, Pet, Scheduler, Task


def make_task(
    name="Morning walk",
    priority="high",
    task_date=date(2026, 7, 6),
    task_time=time(8, 0),
    duration_minutes=30,
    recurrence=None,
):
    return Task(name, "Walk around the block", priority, task_date, task_time, duration_minutes, recurrence=recurrence)


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


def test_sort_by_time_returns_chronological_order():
    pet = Pet(name="Biscuit", age=3, species="Dog", breed="Golden Retriever")
    owner = Owner(name="Jamie", pets=[pet])
    scheduler = Scheduler(owner=owner)

    evening_task = make_task(name="Evening walk", task_time=time(18, 0))
    morning_task = make_task(name="Morning walk", task_time=time(8, 0))
    afternoon_task = make_task(name="Afternoon feeding", task_time=time(13, 30))
    pet.add_task(evening_task)
    pet.add_task(morning_task)
    pet.add_task(afternoon_task)

    ordered = scheduler.sort_by_time(pet.get_tasks())

    assert [t.task_name for t in ordered] == ["Morning walk", "Afternoon feeding", "Evening walk"]


def test_completing_daily_task_creates_task_for_next_day():
    pet = Pet(name="Biscuit", age=3, species="Dog", breed="Golden Retriever")
    owner = Owner(name="Jamie", pets=[pet])
    scheduler = Scheduler(owner=owner)

    daily_task = make_task(name="Feed breakfast", task_date=date(2026, 7, 6), recurrence="daily")
    pet.add_task(daily_task)

    next_task = scheduler.complete_task(daily_task)

    assert daily_task.is_complete is True
    assert next_task is not None
    assert next_task.task_name == "Feed breakfast"
    assert next_task.task_date == date(2026, 7, 7)
    assert next_task.is_complete is False
    assert next_task in pet.get_tasks()


def test_completing_one_off_task_does_not_create_next_occurrence():
    pet = Pet(name="Biscuit", age=3, species="Dog", breed="Golden Retriever")
    owner = Owner(name="Jamie", pets=[pet])
    scheduler = Scheduler(owner=owner)

    one_off_task = make_task(name="Vet visit", recurrence=None)
    pet.add_task(one_off_task)

    next_task = scheduler.complete_task(one_off_task)

    assert next_task is None
    assert len(pet.get_tasks()) == 1


def test_find_time_conflicts_flags_duplicate_times():
    pet = Pet(name="Biscuit", age=3, species="Dog", breed="Golden Retriever")
    owner = Owner(name="Jamie", pets=[pet])
    scheduler = Scheduler(owner=owner)

    first_task = make_task(name="Morning walk", task_time=time(8, 0))
    second_task = make_task(name="Morning medication", task_time=time(8, 0))
    pet.add_task(first_task)
    pet.add_task(second_task)

    conflicts = scheduler.find_time_conflicts()

    assert len(conflicts) == 1
    conflicting_names = {first_task.task_name, second_task.task_name}
    assert {conflicts[0][0].task_name, conflicts[0][1].task_name} == conflicting_names


def test_find_time_conflicts_ignores_tasks_at_different_times():
    pet = Pet(name="Biscuit", age=3, species="Dog", breed="Golden Retriever")
    owner = Owner(name="Jamie", pets=[pet])
    scheduler = Scheduler(owner=owner)

    pet.add_task(make_task(name="Morning walk", task_time=time(8, 0)))
    pet.add_task(make_task(name="Evening walk", task_time=time(18, 0)))

    assert scheduler.find_time_conflicts() == []
