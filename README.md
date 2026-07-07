# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ⚙️ Features

- **Sorting by time** — `Scheduler.sort_by_time()` sorts a pet's tasks earliest-to-latest by `task_time`.
- **Priority-based time-boxing** — `Scheduler.generate_schedule()` greedily fills the available time budget in priority order (high → medium → low), skipping any task that no longer fits.
- **Conflict warnings** — `Scheduler.find_time_conflicts()` flags any tasks booked for the same date and time, including across different pets; `get_conflict_warnings()` turns those into human-readable warning strings instead of raising.
- **Daily/weekly recurrence** — `Task.get_next_occurrence()` and `Scheduler.complete_task()` automatically generate and schedule the next occurrence of a recurring task the moment the current one is marked complete.
- **Task filtering** — `Owner.filter_tasks()` filters tasks across all of an owner's pets by completion status, pet name, or both.
- **Date-scoped views** — `Scheduler.get_tasks_for_date()` returns each pet's tasks for a single day.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

The suite covers:

- **Task basics** — marking a task complete, adding a task to a pet.
- **Sorting correctness** — `Scheduler.sort_by_time()` returns tasks in chronological order regardless of the order they were added.
- **Recurrence logic** — completing a daily task marks it done, generates a new pending task for the next day, and adds it back onto the same pet; completing a one-off task produces no next occurrence.
- **Conflict detection** — `Scheduler.find_time_conflicts()` flags two tasks scheduled at the same date/time, and correctly reports no conflicts when tasks don't overlap.

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.11, pytest-9.1.1, pluggy-1.5.0 -- /opt/miniconda3/bin/python
cachedir: .pytest_cache
rootdir: /Users/linhtran/Desktop/ai110-module2show-pawpal-starter
plugins: anyio-4.12.1
collecting ... collected 7 items

tests/test_pawpal.py::test_mark_complete_changes_task_status PASSED      [ 14%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED   [ 28%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 42%]
tests/test_pawpal.py::test_completing_daily_task_creates_task_for_next_day PASSED [ 57%]
tests/test_pawpal.py::test_completing_one_off_task_does_not_create_next_occurrence PASSED [ 71%]
tests/test_pawpal.py::test_find_time_conflicts_flags_duplicate_times PASSED [ 85%]
tests/test_pawpal.py::test_find_time_conflicts_ignores_tasks_at_different_times PASSED [100%]

============================== 7 passed in 0.01s ===============================
```

**Confidence Level:** ⭐⭐⭐ (3/5)

The core sorting, recurrence, and conflict-detection paths are verified and passing. Confidence isn't higher yet because coverage is still thin around known trouble spots: `Scheduler.complete_task()` locates the owning pet by value equality rather than identity (risky with duplicate-looking tasks across pets), `Task.get_next_occurrence()` does a case-sensitive lookup on `recurrence` (a typo'd value silently fails to recur), and `Scheduler._fit_tasks_to_time()` (the greedy time-boxing logic) has no tests at all yet.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts a list of tasks earliest to latest by `task_time`. |
| Filtering | `Owner.filter_tasks(is_complete=None, pet_name=None)` | Filters tasks across an owner's pets by completion status, pet name, or both combined. |
| Conflict handling | `Scheduler.find_time_conflicts(target_date=None)`, `Scheduler.get_conflict_warnings(target_date=None)` | Groups tasks by `(task_date, task_time)` to detect double-bookings (same pet or different pets) in O(n); `get_conflict_warnings()` returns human-readable warning strings instead of raising, so a conflict never crashes the program. |
| Recurring tasks | `Task.get_next_occurrence()`, `Scheduler.complete_task(task)` | Tasks carry an optional `recurrence` ("daily"/"weekly"). Completing a recurring task via `Scheduler.complete_task()` marks it done and automatically schedules the next occurrence on the same pet. |

## 📸 Demo Walkthrough

### UI features

The Streamlit app (`app.py`) is organized into three sections:

- **Owner & Pets** — enter an owner name, then add one or more pets (name, species, breed, age). Added pets show up in a table.
- **Tasks** — pick a pet from a dropdown and add a task with a title, time, duration, priority (`low`/`medium`/`high`), and repeat setting (`none`/`daily`/`weekly`). That pet's tasks are listed below the form, always sorted earliest-to-latest by `Scheduler.sort_by_time()`. Each pending task has a "Mark complete" button; clicking it calls `Scheduler.complete_task()`, and if the task recurs, a toast confirms the date of the next occurrence.
- **Build Schedule** — enter the minutes available today and click "Generate schedule" to run `Scheduler.generate_schedule()`, which prints a priority-ordered, time-boxed plan per pet.

### Example workflow

1. Enter an owner name and add a pet (e.g., "Biscuit," a Golden Retriever).
2. Add a task for that pet — e.g., "Morning walk" at 8:00 AM, 30 minutes, high priority, no repeat.
3. Add a second task at the same time (e.g., "Grooming" at 8:00 AM for another pet) to see how a conflict would be flagged by the backend.
4. Add a recurring task — e.g., "Feeding" at 9:00 AM, daily — then click "Mark complete" on it and watch the toast confirm a new "Feeding" task was scheduled for the next day.
5. Enter the available minutes for the day and click "Generate schedule" to view today's plan, ordered by priority and fit to the time budget.

### Key Scheduler behaviors shown

- **Sorting** — tasks are always displayed earliest-to-latest, regardless of the order they were entered.
- **Conflict warnings** — `Scheduler.find_time_conflicts()`/`get_conflict_warnings()` catch two tasks booked at the same date and time, even across different pets, without ever raising an error.
- **Recurrence** — completing a daily/weekly task automatically creates and schedules its next occurrence.
- **Priority-based time-boxing** — `generate_schedule()` fills the available minutes in priority order, dropping lower-priority tasks that don't fit.
- **Filtering** — pending vs. completed tasks, and tasks scoped to a single pet, can all be pulled from the same underlying task list via `Owner.filter_tasks()`.

### Sample CLI output (`python main.py`)

`main.py` seeds the same scenario end-to-end — two pets, a deliberate double-booking, and two recurring tasks — then exercises every `Scheduler` behavior above:

```
=== Checking for scheduling conflicts ===
  Warning: 'Morning walk' and 'Grooming' are both scheduled at 08:00 on 2026-07-06.
=== Completing recurring tasks ===
  Completed 'Feeding' -> next occurrence scheduled for 2026-07-07 at 09:00
  Completed 'Litter box cleaning' -> next occurrence scheduled for 2026-07-13 at 10:00
=== Today's Schedule (sorted by time) ===

Biscuit:
  08:00 — Morning walk (30 min) [priority: high] [pending]
  09:00 — Feeding (10 min) [priority: high] [done]
  18:30 — Evening walk (30 min) [priority: medium] [pending]

Whiskers:
  07:30 — Vet checkup (45 min) [priority: high] [pending]
  08:00 — Grooming (20 min) [priority: low] [pending]
  10:00 — Litter box cleaning (15 min) [priority: medium] [done]

=== Pending tasks (filter_tasks: is_complete=False) ===
  Evening walk (18:30)
  Morning walk (08:00)
  Feeding (09:00)
  Vet checkup (07:30)
  Grooming (08:00)
  Litter box cleaning (10:00)

=== Completed tasks (filter_tasks: is_complete=True) ===
  Feeding (09:00)
  Litter box cleaning (10:00)

=== Biscuit's tasks only (filter_tasks: pet_name='Biscuit') ===
  Feeding (09:00)
  Evening walk (18:30)
  Morning walk (08:00)
  Feeding (09:00)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
