

from collections import defaultdict
from typing import DefaultDict, Dict, Tuple

from enums.attribute import AttrEnum


class AttachmentManager:

    def __init__(self) -> None:
        self.entities: Dict[int, int] = {}
        self.list_attachments: DefaultDict[Tuple[int, AttrEnum], list] = defaultdict(list)

    def get_entity_attachment(self, entity, attribute, list_attachment: bool = False):
        if list_attachment:
            return self.list_attachments.get((entity.id, attribute), None)
        else:
            return self.entities.get((entity.id, attribute), None)
    
    def set_entity_attachment(self, entity, attribute, attachment):
        self.entities[(entity.id, attribute)] = attachment

    def push_entity_attachment(self, entity, attribute, attachment):
        self.list_attachments[(entity.id, attribute)].append(attachment)


    def remove_entity_attachment(self, entity):
        self.entities[entity.id] = None