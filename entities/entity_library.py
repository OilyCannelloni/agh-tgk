
class EntityLibrary:
    _entity_dict = {}

    @staticmethod
    def register_entity(name: str, cls: type):
        if EntityLibrary._entity_dict.get(name) is None:
            EntityLibrary._entity_dict[name] = cls

    @staticmethod
    def create_entity(name: str, **kwargs):
        return EntityLibrary._entity_dict[name](**kwargs)
