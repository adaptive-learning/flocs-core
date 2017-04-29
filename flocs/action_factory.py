from collections import ChainMap
from pyrsistent import pmap
from flocs import entities
from flocs.utils.names import kebab_to_snake_case, camel_to_kebab_case
from flocs.extractors import new_id


class ActionIntent:
    """ Intent which can be transformed to an Action calling `at` method
    """
    required_fields = []
    auto_fields = []

    def __init__(self, **data):
        self.data = kebab_to_snake_case(data)
        self.validate_data()

    @classmethod
    def get_type_name(cls):
        return camel_to_kebab_case(cls.__name__)

    def complete_data(self, state):
        enriched_data = {**self.data}
        for field_name, extractor, *args in self.auto_fields:
            if field_name not in enriched_data:
                # TODO: inject additional required arguments to the extractor
                arg_values = [enriched_data[arg] for arg in args]
                enriched_data[field_name] = extractor(state, *arg_values)
        self.data = enriched_data

    def validate_data(self):
        for field in self.required_fields:
            if field not in self.data:
                tpl = 'Missing field {field}, which is required for {action} action'
                msg = tpl.format(field=field, action=self.get_type_name())
                raise ValueError(msg)
        all_data_fields = [field[0] for field in self.auto_fields] + list(self.required_fields)
        for field in self.data:
            if field not in all_data_fields:
                tpl = 'Unknown field {field} passed for {action} action'
                msg = tpl.format(field=field, action=self.get_type_name())
                raise ValueError(msg)

    def discard_action(self, state):
        return False

    def check_duplicate(self, state):
        """ Raise DuplicateAction exception if this intent is a duplicate

        Concrete actions can override this method and call
        self.raise_duplicate_action() if they find that this intent should
        be discarded as (near) duplicate of an already stored action
        """
        pass

    def raise_duplicate_action(self, **duplicate_data):
        # TODO: it should probably pass the original action, but current
        # application design does not support efficient action search, so
        # instead, we just pass a fake Action with possibly needed data
        action = entities.Action(
            action_id=None, time=None, randomness=None, version=None,
            type=self.get_type_name(),
            data=pmap(ChainMap(duplicate_data, self.data)),
        )
        raise DuplicateAction(action=action)


    def at(self, state):
        """ Create an Action from this intent, filling missing data from state
        """
        self.complete_data(state)
        self.check_duplicate(state)
        action = entities.Action(
            action_id=new_id(state),
            type=self.get_type_name(),
            data=pmap(self.data),
            time=state.context.time,
            randomness=state.context.randomness,
            version=state.context.version,
        )
        return action

    def __eq__(self, other):
        return self.get_type_name() == other.get_type_name() and self.data == other.data

    def __repr__(self):
        return '<{type} {data}>'.format(type=self.__class__.__name__, data=self.data)


class DuplicateAction(Exception):
    def __init__(self, action):
        super().__init__('This action is discarded as duplicate of {}'.format(action))
        self.action = action
