""" Representation of a world state

State composition examples:
    - state.empty + Student(...) + Action(...)
    - state.default + SimulationContext(...) + students
"""
from collections import namedtuple, Iterable
from pyrsistent import pmap
from .action_factory import ActionIntent
from .context import static, Context
from .data import blocks, instructions, levels, toolboxes, categories, tasks
from .entities import Block, Instruction, Level, Toolbox, Category, Task
from .entities import Action, Student, TaskSession, SeenInstruction, Session, ProgramSnapshot
from .entity_map import EntityMap
from . import reducers


class State(namedtuple('State', ['entities', 'context'])):
    """ State of the world at a specific moment (immutable snapshot)
    """
    __slots__ = ()

    def __new__(cls, entities=None, context=static):
        entities = pmap(entities)
        return super().__new__(cls, entities=entities, context=context)

    @classmethod
    def build(cls, *components):
        """ Create new state from a sequence of components

        Component can be a state, entity, action, context or even iterable of
        nested components, they will be handled differently according to their
        type, see __add__ for details. (builder design patter)
        """
        return empty.add(*components)

    def add(self, *components):
        """ Create new state from a the current one, adding new components
        """
        return sum(components, self)

    def __add__(self, component):
        """ Create a new state from the current one by adding a new component

        Component can be a state, entity, action, context or even iterable of
        nested components.
        """
        #if isinstance(component, DynamicContext):
        #    return self.add_context(context=component.snapshot)
        if isinstance(component, Context):
            return self.add_context(context=component)
        #if isinstance(component, State):
        #    return self.add_state(state=component)
        #if isinstance(component, Action):
        #    return self.reduce(action=component)
        if isinstance(component, tuple):  # TODO: test for Entity base class
            return self.add_entity(entity=component)
        if isinstance(component, Iterable):
            return self.add(*component)
        raise ValueError('Cannot add {c} to the state'.format(c=component))

    #def add_state(self, state):
    #    TODO: merged_entities = self.entities.update_with(lambda l, r: ??, state.entities)
    #    new_state = state._replace(entities=merged_entities)
    #    return new_state

    def add_context(self, context):
        return self._replace(context=context)

    def add_entity(self, entity):
        if entity.__class__ in self.entities:
            old_entity_map = self.entities[entity.__class__]
            new_entity_map = old_entity_map.set(entity)
        else:
            new_entity_map = EntityMap.from_list([entity])
        new_entities = self.entities.set(entity.__class__, new_entity_map)
        new_state = self._replace(entities=new_entities)
        return new_state

    def reduce(self, action):
        # TODO: allow to reduce multiple actions at once
        return reduce_state(state=self, action=action)

    def total_entities(self):
        return sum(len(entity_map) for entity_map in self.entities.values())

    @property
    def actions(self):
        return self.entities[Action]

    @property
    def levels(self):
        return self.entities[Level]

    @property
    def instructions(self):
        return self.entities[Instruction]

    @property
    def program_snapshots(self):
        return self.entities[ProgramSnapshot]

    @property
    def seen_instructions(self):
        return self.entities[SeenInstruction]

    @property
    def sessions(self):
        return self.entities[Session]

    @property
    def students(self):
        return self.entities[Student]

    @property
    def tasks(self):
        return self.entities[Task]

    @property
    def task_sessions(self):
        return self.entities[TaskSession]

    @property
    def toolboxes(self):
        return self.entities[Toolbox]


def reduce_state(state, action):
    if isinstance(action, ActionIntent):
        action = action.at(state)
    new_entities = reduce_entities(state.entities, action)
    new_state = State(entities=new_entities, context=action.context)
    return new_state


def reduce_entities(old_entities, action):
    new_entities = pmap({
        entity_class: reduce_entity_map(entity_class, entity_map, action)
        for entity_class, entity_map in old_entities.items()
    })
    return new_entities


def reduce_entity_map(entity_class, entity_map, action):
    if entity_class == Action:
        return entity_map.set(action)
    reducer = reducers.get(entity_class, action.type)
    next_entity_map = reducer(entity_map, action)
    return next_entity_map


# some prepared immutable states

empty = State(entities=pmap({
    Block: EntityMap(),
    Instruction: EntityMap(),
    Level: EntityMap(),
    Toolbox: EntityMap(),
    Category: EntityMap(),
    Task: EntityMap(),
    Action: EntityMap(),
    Student: EntityMap(),
    TaskSession: EntityMap(),
    SeenInstruction: EntityMap(),
    Session: EntityMap(),
    ProgramSnapshot: EntityMap(),
}), context=static)

default = State(entities=pmap({
    Block: EntityMap.from_list(blocks),
    Instruction: EntityMap.from_list(instructions),
    Level: EntityMap.from_list(levels),
    Toolbox: EntityMap.from_list(toolboxes),
    Category: EntityMap.from_list(categories),
    Task: EntityMap.from_list(tasks),
    Action: EntityMap(),
    Student: EntityMap(),
    TaskSession: EntityMap(),
    SeenInstruction: EntityMap(),
    Session: EntityMap(),
    ProgramSnapshot: EntityMap(),
}), context=static)
