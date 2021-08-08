from typing import List

import color
from components.component import Component

from entity import Entity


class InventoryComponent(Component):
    def __init__(self, maxItems: int):
        self.items: List[Entity] = []
        self.maxItems = maxItems

    def onOwnerChanged(self):
        self.owner.inventoryComponent = self

    def addItem(self, item: Entity):
        if len(self.items) == self.maxItems:
            return

        self.items.append(item)
