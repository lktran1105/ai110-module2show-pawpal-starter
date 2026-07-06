# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

#note in working: ask AI to fill in the missing pieces, as well as the relationships between the classes

- The 4 classes and its attributes (information it needs to hold) and methods (actions it can perform)
    - Pet
        - Attributes: name, age, species, breed
        - Methods: tasks: list[Task] add task, remove task, get task
    - Owner: 
        - Attributes: name
        - Methods: create a pet, delete a pet, edit pet information, pets: list[Pet]
    - Task: 
        - Attribute: date, time, priority, task name, task description, completion status
        - Method: change priority, change task date
    - Schedule: 
        - Attribute: list of tasks
        - Method: generate schedule, get tasks for date
- Briefly describe your initial UML design.
    - The initial design centers on four classes: Owner, Pet, Task, and Schedule. An Owner holds a list of Pets and is responsible for creating, deleting, and editing pets. Each Pet holds its own list of Tasks (walks, feeding, meds, etc.) and can add, remove, or retrieve them. Task stores the details of a single care item — name, description, priority, date/time, duration, and completion status — along with methods to update its priority or date. Schedule takes a pet's tasks and generates a daily plan based on available time, and can retrieve tasks for a specific date. The relationships are one-to-many throughout: one Owner → many Pets, one Pet → many Tasks, and Schedule organizes a set of Tasks. This keeps ownership/management logic (Owner) separate from care-tracking (Pet/Task) and separate again from the scheduling algorithm (Schedule).
- What classes did you include, and what responsibilities did you assign to each?
    - Owner — manages the collection of pets. Responsible for creating, deleting, and editing pet records. Holds a pets: list[Pet] attribute.
    - Pet — represents an individual pet and manages its own care tasks. Holds identifying info (name, age, species, breed) and a tasks: list[Task] attribute, with methods to add, remove, and retrieve tasks.
    - Task — represents a single care item (e.g., a walk or feeding). Holds the task's details (name, description, priority, date, time, duration, completion status) and methods to update its priority or reschedule its date.
    - Schedule — responsible for turning a pet's tasks into an actual daily plan. Takes a list of tasks and generates an ordered schedule based on available time, and can retrieve tasks for a specific date.




**b. Design changes**

- Did your design change during implementation?
    -   Yes
- If yes, describe at least one change and why you made it.
    - Change: Originally, Schedule held its own tasks: list[Task] attribute, separate from the tasks list already stored on Pet. I changed Schedule to instead hold a reference to a Pet (pet: Pet) and derive the tasks it needs directly from pet.tasks, rather than keeping a second copy.
    - Why: Having two lists that were supposed to represent the same data (Pet.tasks and Schedule.tasks) created a risk of them drifting out of sync — for example, adding a task to a Pet wouldn't automatically update its Schedule, and vice versa. This is a classic single-source-of-truth problem: whichever object doesn't own the "real" data can become stale. By having Schedule reference the Pet object instead of duplicating its task list, there's only one place where a pet's tasks live, and the schedule is always generated from current data.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
