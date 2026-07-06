from datetime import date, time

from pawpal_system import Owner, Scheduler, Task

TODAY = date(2026, 7, 6)


def main() -> None:
    owner = Owner(name="Linh")

    biscuit = owner.create_pet(name="Biscuit", species="Dog", breed="Golden Retriever", age=3)
    whiskers = owner.create_pet(name="Whiskers", species="Cat", breed="Tabby", age=5)

    biscuit.add_task(Task("Morning walk", "Walk around the block", "high", TODAY, time(8, 0), 30))
    biscuit.add_task(Task("Feeding", "Breakfast kibble", "high", TODAY, time(9, 0), 10))
    whiskers.add_task(Task("Litter box cleaning", "Scoop and refresh litter", "medium", TODAY, time(10, 0), 15))

    scheduler = Scheduler(owner=owner)
    todays_schedule = scheduler.get_tasks_for_date(TODAY)

    print("=== Today's Schedule ===")
    for pet_name, tasks in todays_schedule.items():
        print(f"\n{pet_name}:")
        for task in sorted(tasks, key=lambda t: t.task_time):
            print(f"  {task.task_time.strftime('%H:%M')} — {task.task_name} ({task.duration_minutes} min) [priority: {task.priority}]")


if __name__ == "__main__":
    main()
