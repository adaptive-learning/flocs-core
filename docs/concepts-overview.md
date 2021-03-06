# Concepts Overview

Architecture, principles, requirements.

Concept | Meaning
------- | ----------
state | snapshot of the world we model in a single moment
state shape | which part of the state describes what
actions | describe events and interaction in the world
reducers | describe how the state changes under the actions
extractors | describe how to extract information from the state

Clients can specify which parts of the state they want to use (state shape).
They can provide a persistence shell, i.e. specify lazy loading of the state and how to store changes in the state.
They should also provide a persistent model for actions.

State, reducers and extractors depend on an agreed state shape, for example an extractor for task selection requires a tasks entities to be present in the state.
Each part of the state is associated with a reducer, that describe how this part of the state changes under all possible actions.
Actions and reducers are orthogonal concepts – one action may cause changes in several parts of the state
(e.g. creating a new attempt will not only change the set of attempts entities, but also update parameters of various skill and difficulty models).

Actions are domain-specific events and interactions, e.g. `start_task`, `solve_task` and `give_up_task`.
Clients does not need to know about the logic behind actions, they even does not need to which parts of the state are changed under which action.
When an action happens, they just delegate the change to the core, passing a current state and action to the reducer, which computes a new state.

An initial state and series of actions are the complete "source of truth"
(code of the reducer is also important, but it is specified by the meta information in each action).
This architecture enables to see how the parameters were changing, as well as well as how they would be changing for different models or parameters, without any additional logs.
It also enables to reconstruct any past state, which can be useful not only if something goes terribly wrong, but also for much easier debugging – one can see how the state changed when a problem occurred, which is great for understanding the situation.

Current state in DB (or in CSV tables) can be viewed as just a derivative of the primary source of truth (initial state and action stream).
This allows to optimize the current state for special purposes of the specific client, e.g. web does not need to have a quick access to the history of the parameters, only the current ones.

There are several extremely important non-functional requirements we follow:
the code should be easy and pleasure to use, to read, to extend and to test.
The code together with the tests should form a beautiful, clear and coherent story.
