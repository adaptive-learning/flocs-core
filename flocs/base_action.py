from pyrsistent import pmap
from flocs import entities
from flocs.context import dynamic
from flocs.utils.names import kebab_to_snake_case, camel_to_kebab_case

class BaseAction(entities.Action):
    """ Base class for specific actions

    Provides common factory for instantiating actions from data.
    Subclasses needs to provide action type, list of auto field and list of
    required fields.
    """
    auto_fields = []
    required_fields = []

    #def __init__(self, **fields, context=dynamic):
    #    return self.from_data(fields, context)

    @classmethod
    def get_type_name(cls):
        return camel_to_kebab_case(cls.__name__)

    @classmethod
    def from_data(cls, data, context=dynamic):
        """  Creates entities.Action from data

        Note that it only uses the specific action class as an action creator,
        but it returns plain entities.Action eventually (which is necessary for
        reducers to work). TODO: Make it explicit, that these classes are just
        action-creators (deserializers), but not the actions themselves.
        """
        snaked_data = kebab_to_snake_case(data)
        complete_data = cls.add_auto_fields(snaked_data, context)
        cls.validate_data(complete_data)
        return entities.Action(
            action_id=context.new_id(),
            type=cls.get_type_name(),
            data=pmap(complete_data),
            time=context.time,
            randomness=context.randomness,
            version=context.version,
        )

    @classmethod
    def add_auto_fields(cls, data, context):
        enriched_data = {**data}
        for auto_field in cls.auto_fields:
            if auto_field not in enriched_data:
                enriched_data[auto_field] = context.new_id()
        return enriched_data

    @classmethod
    def validate_data(cls, data):
        for field in cls.required_fields:
            if field not in data:
                tpl = 'Missing field {field}, which is required for {action} action'
                msg = tpl.format(field=field, action=cls.get_type_name())
                raise ValueError(msg)
        all_data_fields = cls.auto_fields + cls.required_fields
        for field in data:
            if field not in all_data_fields:
                tpl = 'Unknown field {field} passed for {action} action'
                msg = tpl.format(field=field, action=cls.get_type_name())
                raise ValueError(msg)
