# ===========================================================================
# Scenario 1
# ----------
# Getting recommendation for next task to solve
# (or next activity in general, which may be also to take a break).
# ---------------------------------------------------------------------------

# web: views.py
@allow_lazy_user
def get_recommendation(request):
    recommendation = get_recommendation_for_user(request.user)
    return JsonResponse(recommendation)

# ---------------------------------------------------------------------------

# web: services.py
from flocs.extractors import extract_next_task
from store import DjangoStore

def get_recommendation_for_user(user):
    # NOTE: user-> student conversion is common, dry using decorator
    student = StudentModel.objects.get_or_create(user=user)[0]
    recommendation = get_recommendation_for_student(student)
    return recommendation

def get_recommendation_for_student(student):
    store = DjangoStore()
    recommendation = extract_recommendation(store.state, student.pk)
    return recommendation

# ---------------------------------------------------------------------------

# web: store.py
from flocs.store import Store
from flocs.reducers import WORLD_REDUCER
from models import Action, Student, TaskInstance
from state import DjangoState
from django.db import transaction


class DjangoStore(Store):
    def __init__(self):
        # NOTE: in future, we will replace world reducer by some web-specific
        # reducer  (?)
        super().__init__(initial_state, WORLD_REDUCER)

    def __enter__(self):
        initial_state = DjangoState()
        pass

    def __exit__(self, *args):
        self.save()

    def save(self):
        diff = compute_diff(self.initial_state, self.state)
        apply_diff_atomicallly(diff)


def compute_diff(old_state, new_state):
    """ Return a list of minimum db actions to get from the old state to the
        new state
    """
    pass


def apply_diff_atomically(diff):
    if len(diff) > 0:
        with transaction.atomic():
            apply_diff(diff)
    else:
        apply_diff(diff)


def apply_diff(diff):
    for change in diff:
        apply_change(change)

# ---------------------------------------------------------------------------

# web: state.py

from flocs.state import State, LazyValue
from models import Student, TaskInstance


class DjangoState(State):
    def __init__(self):
        super().__init__({
            'entities.students': DjangoLazyValue(Student),
            'entities.task_instances': DjangoLazyValue(TaskInstance),
            'context.time': datetime.now(),
            'context.randomness_seed': random.randint(0, sys.maxsize),
            })

def DjangoLazyValue(model):
    def materialize_all():
        return [instance.to_domain_object() for instance in model.objects.all()]
    return LazyValue(materialize_all)


# ===========================================================================
# Scenario 2
# ----------
# Student wants to start solving new task.
# This can be a task recommended in a previews request (see scenario 1).
# ---------------------------------------------------------------------------

# web: views.py

@allow_lazy_user
def create_task_instance(request):
    # TODO: rest API, make sure it's POST, decode body, exceptions handling
    params = extract_params(request)
    task_instance = user_service.create_task_instance(request.user, params.task_id)
    # TODO: should return location or maybe just the created task instance (?)
    # TODO: serialization needed, but should be concentrated at one place
    return JsonResponse(task_instance)

# ---------------------------------------------------------------------------

# web: user_service.py
# just user->student conversion, TODO: do it better!

def create_student(user):
    # TODO: check that the user does not already have associated student
    student = services.create_student(student_id=user.pk)
    return student


def create_task_instance(user, task_id):
    # TODO: student must already exist -> raise exception if not
    student = StudentModel.objects.get(user=user)
    task_instance = services.create_task_instance(student.pk, task_id)
    return task_instance


def update_task_instance(user, task_instance):
    # TODO: check that student corresponding to the user is the same as stated
    # in the task_instance
    task_instance = services.update_task_instance(student.pk, task_instance)
    return task_instance


def get_task_instance(user, task_instance_id):
    # TODO: check that student corresponding to the user is the same as stated
    # in the task_instance
    task_instance = services.get_task_instance(task_instance_id)
    return task_instance

# ---------------------------------------------------------------------------

# web: services.py

from flocs.extractors import extract_task_instance
from flocs.actions import CreateTaskInstance
from store import DjangoStateTransaction
from flocs import intent, action

def get_task_instance(student, task_id):
    store = DjangoStore()  # TODO: DjangoState() should be enough! (no need to reduce anything...)
    task_instance = extract_task_instance(store.state, student_id=student.pk, task_id=task_id)
    return task_instance

def create_student(student_id):
    create_student_intent = intent.CreateStudent(student_id)
    django_store.perform_intent(create_student)

def create_task_instance(student_id, task_id):
    create_task_instance_intent = intent.CreateTaskInstance(student_id, task_id)
    django_store.perform_intent(create_task_instance_intent)

def update_task_instance(task_instance):
    update_task_instance_intent = intent.UpdateTaskInstance(task_instance)
    django_store.perform_intent(update_task_instance_intent)

# I am still not sure how to resolve intents, some crazy ideas/notes follows:

# django_store.py VERSION 1: dependency injection (data-layer injection)

def create_task_instance(student, task_id):
    with DjangoStore() as store:
        action = CreateTaskInstance(
            student_id=student.pk,
            task_id=task_id)
        store.dispatch(action)

# django_store.py VERSION 2: coroutines

def perform_intent(intent):
    intent_performer = perform(intent)
    effect = next(intent_performer)
    while effect:
        data = resolve_effect(effect)
        effect = intent_performer.send(data)
        action = reducer.send()

# django_store.py VERSION 3: coroutines, another way

def create_task_instance(student, task_id):
    intent = CreateTaskInstanceIntent(student, task_id)
    store = DjangoStore()
    store.perform(intent)


# DjangoStore:
    # ...
    def perform(self, intent):
        reducer = self.reducer(intent)
        action = next(reducer)
        while action:
            action = reducer.send()


# ===========================================================================
# Scenario 3
# ----------
# Export all actions from web and create CSV table of current state for
# analysis
# ---------------------------------------------------------------------------
# web: export.py

# TODO: from initial state?)
import json
from models import Action

def export_actions_to_json():
    actions = list(Action.objects.all())
    destination = # ...
    with open(destination, 'w') as outfile:
        json.dump(actions, outfile)

# ---------------------------------------------------------------------------
# analysis: import.py

import json
from flocs.store import world_reducer, empty_state

def create_csv_tables():
    actions = load_actions_from_json()
    tables = convert_actions_to_tables(actions)
    dump_csv_tables(tables)

def load_actions_from_json():
    with open('data/actions.json') as infile:
        actions = json.load(infile)
    return actions

def dump_csv_tables(tables):
    for name, table in tables.items():
        dump_csv_table(name, table)

def dump_csv_table(name, table):
    pass
    # TBA: using csv module, name->path, table is a list of entities
    # (same as in https://github.com/adaptive-learning/flocs/blob/master/flocs/management/commands/export_data_to_csv.py)

def convert_actions_to_tables(actions):
    state = convert_actions_to_state(actions)
    tables = convert_state_to_tables(state)
    return tables

def convert_actions_to_state(actions):
    return reduce(world_reducer, actions, empty_state)

def convert_state_to_tables(state):
    """ For each entity type in state return a list of entities
    """
    return state.entities  # this should be already what we want
