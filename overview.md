Overview
========
- concepts:
  - state, reducers and store
  - actions and intents
  - extractors
  - data, entitities, techniques
- actions and state are orthogonal concepts (one reducer may reduce a particular part of the state for a particular action)
- initial state and reducers are also orthogonal (because we will want to start in different initial states, consider web case)
  - but both depends on the "state shape" contract


Requirements
------------
General:
- code is easy and pleasure to use in projects on different level of abstraction (web and analysis)
- code is easy and pleasure to read, it forms a clear beautiful story
- code is easy and pleasure to extend for new features
- code is easy and pleasure to test and really tested

Specific:
- web does not need to know about the logic behind actions (even which parts of the world will be changed)
  - actions happens -> delegate the change to the core, than automatically find which parts of the world changed and save changes
  - web needs to know: structure of the world (to model its persistent counterpart) and which actions (or intents) to fire when
- all actions useful for analysis must by stored (full history)
  - series of actions are the complete "source of truth" enabling to reconstruct any past state without any additional information
  - this enables to see how the parameters were changing, as well as how they would be changing for different models
  - also enables to restore any past state if something goes wrong
  - enables to easily inspect and understand a situation when a bug in production occurred and fix it promptly
  - actions should be domain-specific (CreateStudent, StartTask, SolveTask, GiveUpTask),
    one action might require to change several entities (e.g. creating new attempt and update parameters of skill/difficulty models)
- state in DB (or a state in CSV tables / json dumps) are just derivatives of an action stream (and initial state)
  - e.g. does not need to know the history of parameters, only the current ones
- clients can set which  parts of the store they want to use and set their initial state
  (and for those used substates, the reducers should be specified by the core)
- state should be easily de/serializable (json)

Questions
---------
- state vs. store (what should be passed where - e.g. extractors, intents, reducers)
- best approach to customize store behavior (loading and storing state)?
  - possibilities: pass handlers (post commit hooks), inheritance (template method), composition (wrap)
- concept of intents
  - how to use them
  - how to represent them (function return an action, procedure modifying store, generator yielding actions, coroutine, class, namedtuples)
  - how should they receive info from shell (parameters, state/store dependency injection, coroutines: yield/send)
- should meta (id, parent_id, version) and context (time, randomness_seed) be part of each action?
  - why: because it changes often (at least time) and maybe it could allow for easier merging (rebasing?)
  - meta vs. context? (should we even destinguish these two and where does version belong)
- where to use dictionaries vs. namedtuples, advantages and disadvantages, pitfalls (e.g. see state: tasks or task_instances, etc.)
  - one consideration is (json) serialization, which is easier with dicts (for namedtuples, custom handler is necessary, and loading would be tricky)
  - namedtuples are immutable (also look better in code)
- code review (all modules, incl. test)
  - are the requirments above satisfied? (e.g. is it readable? what can be improved?)
  - project architecture and structure
  - classes vs. functions?
  - reducers.py: how to organize (or split) - even for performers are 2 orthogonal critera (which action type they reduce, which part of the state they reduce)
  - using OOP vs data+functions - where could be used one instead of another ot make the code more readable/testable (e.g. in reducers)
- how to make both initial states and reducers be orthogonal, but in sync (= both should be validated against (or depend on?) a common state shape?)
  - related question is how to enable choosing parts of store by clients (e.g. might not want some statistics which analysis need?)
  - another related: in reducers.py, should we rather pass packed or unpacked action.data (unpacked are easier to work with, but results in `**kwargs` sometimes, e.g. in stats reducer)
- State: should explicitly use special-purpose LazyValue objects vs. plain callables?
  - and generally, how to make it better
- how to dry dispatching actions ("switch" vs. dictionary dispatch vs. parameter dispatch (@multidispatch with type annotatations and nameduples))
- how to enable tasks versioning
- terminology:
  - actions (events, effects), intents
  - store, state, reducers
  - extractors (selectors, computers, derivers)
  - experiments, practice contexts
  - task, task instance (?)
  - entities, models (predictions), student, skill, task, difficulty, student-task interaction: time and flow
  - techniques (strategies, [algorithms], methods), (activity|task) recommendation/selection
  - practice session (training)
  - concept (learning component)
- pure or impure reducers (immutable, but not Pythonic)
  - is ChainMap a reasonable solution or not
  - or should I consider 3rd party immutable types (and namedtuples)
- clean architecture (pure core, io shell) - advantages and disadvantages
- does TaskStats belong to entities.py? (and similary for corresponding state and reducer)
- how to split reducers.py
  - diffent pieces: top reducers, delegated functions (by actions, by substate), `WORLD_REDUCER` (with combine reducers)
- plus with TODO's ([Q] flag)
- does store need to be a class (maybe just a namedtuple and plain functions/procedures are enough)
- [pylint] constants inside function (`test_recommendation`)?
- style: formatting of dictionaries (many places, e.g. state)
- reducers.py: `**action._as_dict()` or just to pass action?
- how to implement lazy store (ala environment...)
  - architecture: lazy store make all functions using it secretely stateful, what are the potential problems and is there a way to avoid this (e.g. using coroutines)
- usage - web:
 - how to improve/normalize the web part using REST API
   - if direct access without need of core make sense, than it should be used,
     because it's easier? But only if we don't want to remember the request
     (= action)
 - how to deal with the fact that no request with user (= all) can
   pottentially mutate DB (lazy user and new student)? should all these
   requests be POST?
 - better serialization than using to_json methods on django models?
 - how to deal with parallel transactions leading to collisions (two students want to create next task instance - and we need to choose ids for both of them)
    - possible solution is locking DB (django.db.transaction.atomic) for each view (or intent execution), but it hurts performance
- how to version tasks and other data, or even changes in actions (and reducers)
  - use special-purpose action like ChangeDomain, ChangePackageVersion
- can lazy loading from DB (if the requests are handled non-atomicly) lead to some inconsistencies?!
  - (probably yes)



TODO
----
- move TODOs and Questions to GH issues
- move overview/requirements to docstrings and README
- finish prove of concept including web (min. viable product), then consult and improve
- unit tests and integration tests, s.t. they are easily reused for web/analysis stores
- improve architecture, s.t. clients doesn't need to use subclassing (which requires knowing internals of the core), but rather just class/function composition [Q]
- implement and test basic intents
  - [Q] how? injecting state/store (alt. is using corouintes)
- implement and test basic store
  - it should be a context manager: commit on each `__enter__` and/or `__exit__` (but after saving)
  - method for computing diff
  - thinking about usage: web/analysis can subclass and provide save method, but is there better way - maybe just providng import/export handler [Q]
- tests for all modules
  - important: reducers, lazy state
  - using fixtures
  - comprehensive, test also all edge cases
- create identity_reducer - can be used many times in reducers.py (instead of lambdas and possibly Nones - more explicit)
- dry state shape [Q]
  - now it's defined in reducers.py (`WOLRD_REDUCER`) and state.py, should be on a single place [Q]
  - the current version can easily change the state shape after the reduce (e.g. by a typo in state.py or reducers.py)
  - combine reducers should maybe make it more explicit that some parts of the store remain unchanged via identityReducer instead of None
- add time to all actions (or even whole context) [Q]
  - consider moving version into context [Q]
- dry reducers
  - factor out dispatching actions from reducers
  - factor out common code from `solve_task_instance` and `give_up_task_instance`
  - factor out common code from `increase_[started|given_up|solved]_count` (maybe just one function with partial application in the stats reducer)
  - (maybe even creating/updating entities)
- dry actions (Action enum is just extraction from all nameduples from the action module, so can't we omit it completely?) [Q]
- create README:
  - project overview (with simple diagram/table of modules and dependencies between them)
  - how to use the package
  - how to develop the package (incl. infrastructure and principle, but don't duplicate code)
- State should check that all keys are valid (at least on initialization?)
  - why: to prevent typo-erros when creating own initial state
- data.py: split types and data [Q]
- make it more explicit which functions are pure (e.g are all reducers pure? consider immutable types)
- extractors: annotation to extract function parameters from state
  - e.g.: `@extract_state(tasks='entities.tasks')` ([Q]: name? `extract_state`, `extract_params`, `state_params`)
  - but consider testability [Q]
- implement extractor for selecting task in a fixed order
- generalize task selectors (uniform treatment without duplicite code, allow for model parameters)
  - plus: builder design patter for recommender combining criteria into a weighted sum (recommendation.py)
- [pylint] unused arguments in extractors [Q]
  - possible solutions: ignore this warning (pylintrc) or use sth. like `*_args`
- add test states and create and clearly describe how they follow each other (ascii diagram or just a list of a -[action]-> b)
- visualization of entities and other parts of the state (using React components)
- consider convention of always mapping entities on the entities in DB (or static data?) and context to a computed values
- generalize recommendation: recommend different activity than task (break) - add a session (training) layer
- recommendation - merge the current code (or replace) with sth. like:
- react visualization component for exploring actions with time travel (can dispatch/close actions, explore state, commit/rollback) - like redux dev tools, but the changes will affect backend

```
# extractors.py

from collections import namedtuples
from flocs.utils import instantiate_function

def extract_recommendation(state, student_id):
    # NOTE: can use all information in the store (about student, current
    # experiments, parameters of models, time, randomness seed, ...)
    recommender_id = state.current_recommender
    recommend, parameters = extract_recommender(state, recommender_id)
    next_task = recommend(state, student_id, **parameters)
    recommendation = Recommendation(next_task=next_task)
    return recommendation


def extract_recommender(state, recommender_id):
    """ Return instantiated recommender
    """
    entitity = state.entities.recommenders[recommender_id]
    recommend = instantiate_function('recommenders', entity.func_name)
    parameters = entitity.parameters._as_dict()
    return recommend, parameters

# recommendation.py

"""
Task recommenders. Protocol: Each recommender is a pure function with two
positional parameters (state and student id) and any other keyword parameters.
They return a single task id, which must be among state.tasks, unless
state.tasks is empty or non-existent in which case they should raise ValueError
(TODO: and it should be exception specialized from ValueError to distinguish
between missing/non-existent student or misconfigured parameters).
"""

from collections import namedtuple
import random

# QUESTION: is there a need for classes or not?

def recommend_random_task(state, student_id):
    # NOTE: it does not need student_id argument but it's required to
    # follow "recommenders' protocol"
    # NOTE: it only operates over task IDs as it doesn't need to know details
    tasks = state.tasks  # this should be a list of all tasks IDs (?)
    random.seed(state.randomness_seed)  # OR: state.context.randomness_seed
    next_task = random.choice(tasks)
    return next_task


def recommend_task_in_fixed_order(state, student_id, order, solved_tasks):
    try:
        next_task = next(task for task in order
                              if task not in solved_tasks[student_id])
    except StopIteration:
        next_task = order[-1]
    finally:
        return next_task
```
