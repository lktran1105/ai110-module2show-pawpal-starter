from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
else:
    st.session_state.owner.name = owner_name

owner = st.session_state.owner

st.markdown("### Add a Pet")
col1, col2, col3, col4 = st.columns(4)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    breed = st.text_input("Breed", value="Mixed")
with col4:
    age = st.number_input("Age", min_value=0, max_value=30, value=2)

if st.button("Add pet"):
    owner.create_pet(name=pet_name, species=species, breed=breed, age=int(age))

if owner.pets:
    st.write("Current pets:")
    st.table(
        [{"name": p.name, "species": p.species, "breed": p.breed, "age": p.age} for p in owner.pets]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.markdown("### Tasks")
st.caption("Add tasks to a pet. These feed directly into the scheduler below.")

if owner.pets:
    selected_pet_name = st.selectbox("Pet", [p.name for p in owner.pets])
    selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_time = st.time_input("Time", value=time(8, 0))
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col5:
        recurrence = st.selectbox("Repeats", ["none", "daily", "weekly"])

    if st.button("Add task"):
        selected_pet.add_task(
            Task(
                task_title,
                "",
                priority,
                date.today(),
                task_time,
                int(duration),
                recurrence=None if recurrence == "none" else recurrence,
            )
        )

    scheduler = Scheduler(owner=owner)

    if selected_pet.get_tasks():
        st.write(f"Tasks for {selected_pet.name}:")
        for t in scheduler.sort_by_time(selected_pet.get_tasks()):
            row_cols = st.columns([3, 2, 2, 2, 2])
            row_cols[0].write(t.task_name)
            row_cols[1].write(t.task_time.strftime("%H:%M"))
            row_cols[2].write(f"{t.duration_minutes} min")
            row_cols[3].write(t.priority)
            if t.is_complete:
                row_cols[4].write("✅ done")
            elif row_cols[4].button("Mark complete", key=f"complete-{id(t)}"):
                next_task = scheduler.complete_task(t)
                if next_task is not None:
                    st.toast(f"'{t.task_name}' repeats {t.recurrence} — next one scheduled for {next_task.task_date}.")
                st.rerun()
    else:
        st.info(f"No tasks yet for {selected_pet.name}. Add one above.")
else:
    st.info("Add a pet before adding tasks.")

st.divider()

st.subheader("Build Schedule")
available_minutes = st.number_input("Available minutes today", min_value=1, max_value=600, value=60)

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=owner)
    schedule = scheduler.generate_schedule(int(available_minutes))

    if not any(schedule.values()):
        st.info("No tasks fit in the available time.")

    for pet_name_, tasks in schedule.items():
        if not tasks:
            continue
        st.markdown(f"**{pet_name_}**")
        for t in scheduler.sort_by_time(tasks):
            st.write(
                f"{t.task_time.strftime('%H:%M')} — {t.task_name} ({t.duration_minutes} min) [priority: {t.priority}]"
            )
