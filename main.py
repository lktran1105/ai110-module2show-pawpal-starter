from datetime import date, time

from pawpal_system import Owner, Scheduler, Task

TODAY = date(2026, 7, 6)


def main() -> None:
    owner = Owner(name="Linh")

    biscuit = owner.create_pet(name="Biscuit", species="Dog", breed="Golden Retriever", age=3)
    whiskers = owner.create_pet(name="Whiskers", species="Cat", breed="Tabby", age=5)

    # Tasks are added out of order on purpose, to prove sort_by_time actually sorts.
    feeding = Task("Feeding", "Breakfast kibble", "high", TODAY, time(9, 0), 10, recurrence="daily")
    biscuit.add_task(feeding)
    biscuit.add_task(Task("Evening walk", "Walk around the block", "medium", TODAY, time(18, 30), 30))
    biscuit.add_task(Task("Morning walk", "Walk around the block", "high", TODAY, time(8, 0), 30))
    litter_box = Task("Litter box cleaning", "Scoop and refresh litter", "medium", TODAY, time(10, 0), 15, recurrence="weekly")
    whiskers.add_task(litter_box)
    whiskers.add_task(Task("Vet checkup", "Annual wellness visit", "high", TODAY, time(7, 30), 45))

    # Deliberate double-booking: same time, different pets, to exercise conflict detection.
    whiskers.add_task(Task("Grooming", "Brush and nail trim", "low", TODAY, time(8, 0), 20))

    scheduler = Scheduler(owner=owner)

    print("=== Checking for scheduling conflicts ===")
    warnings = scheduler.get_conflict_warnings(TODAY)
    if warnings:
        for warning in warnings:
            print(f"  {warning}")
    else:
        print("  No conflicts found.")

    print("=== Completing recurring tasks ===")
    for task in (feeding, litter_box):
        next_task = scheduler.complete_task(task)
        print(f"  Completed '{task.task_name}' -> next occurrence scheduled for {next_task.task_date} at {next_task.task_time.strftime('%H:%M')}")

    todays_schedule = scheduler.get_tasks_for_date(TODAY)

    print("=== Today's Schedule (sorted by time) ===")
    for pet_name, tasks in todays_schedule.items():
        print(f"\n{pet_name}:")
        for task in scheduler.sort_by_time(tasks):
            status = "done" if task.is_complete else "pending"
            print(f"  {task.task_time.strftime('%H:%M')} — {task.task_name} ({task.duration_minutes} min) [priority: {task.priority}] [{status}]")

    print("\n=== Pending tasks (filter_tasks: is_complete=False) ===")
    for task in owner.filter_tasks(is_complete=False):
        print(f"  {task.task_name} ({task.task_time.strftime('%H:%M')})")

    print("\n=== Completed tasks (filter_tasks: is_complete=True) ===")
    for task in owner.filter_tasks(is_complete=True):
        print(f"  {task.task_name} ({task.task_time.strftime('%H:%M')})")

    print("\n=== Biscuit's tasks only (filter_tasks: pet_name='Biscuit') ===")
    for task in owner.filter_tasks(pet_name="Biscuit"):
        print(f"  {task.task_name} ({task.task_time.strftime('%H:%M')})")


if __name__ == "__main__":
    main()
