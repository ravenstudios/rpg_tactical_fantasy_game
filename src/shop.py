from copy import copy

from lxml import etree

from src import menuCreatorManager
from src.building import Building
from src.menus import ShopMenu


class Shop(Building):
    def __init__(self, name, pos, sprite, interaction, stock):
        Building.__init__(self, name, pos, sprite, interaction)
        self.stock = stock
        self.menu = menuCreatorManager.create_shop_menu(self.stock, 0)

    def get_item_entry(self, item):
        for entry in self.stock:
            if entry['item'].name == item.name:
                return entry
        return None

    def update_shop_menu(self, gold):
        for row in self.menu.entries:
            for entry in row:
                if entry['type'] == 'item_button':
                    item = self.get_item_entry(entry['item'])
                    if item:
                        entry['quantity'] = item['quantity']
                    else:
                        row.remove(entry)
                        if len(row) == 0:
                            self.menu.entries.remove(row)
                if entry['type'] == 'text':
                    entry['text'] = 'Your gold : ' + str(gold)
        self.menu.update_content(self.menu.entries)

    def interact(self, actor):
        self.update_shop_menu(actor.gold)

        entries = [[{'name': 'Buy', 'id': ShopMenu.BUY, 'type': 'button', 'args': [self]}],
                   [{'name': 'Sell', 'id': ShopMenu.SELL, 'type': 'button'}]]
        return entries

    def buy(self, actor, item):
        if actor.gold >= item.price:
            if len(actor.items) < actor.nb_items_max:
                actor.gold -= item.price
                actor.set_item(copy(item))

                entry = self.get_item_entry(item)
                entry['quantity'] -= 1
                if entry['quantity'] <= 0:
                    self.stock.remove(entry)

                # Update shop screen content (gold total amount has been reduced and stock)
                self.update_shop_menu(actor.gold)

                return "The item has been bought."
            # Not enough space in inventory
            return "Not enough space in inventory to buy this item."
        # Not enough gold to purchase item
        return "Not enough gold to buy this item."

    def sell(self, actor, item):
        if item.resell_price > 0:
            actor.remove_item(item)
            actor.gold += item.resell_price

            # Update shop screen content (gold total amount has been augmented)
            self.update_shop_menu(actor.gold)

            return True, "The item has been sold."
        return False, "This item can't be sold !"

    def save(self, tree_name):
        tree = Building.save(self, tree_name)

        # Specify nature
        nature = etree.SubElement(tree, 'type')
        nature.text = 'shop'

        # Specify content
        items = etree.SubElement(tree, 'items')
        for entry in self.stock:
            item = etree.SubElement(items, 'item')

            name = etree.SubElement(item, 'name')
            name.text = entry['item'].name

            quantity = etree.SubElement(item, 'quantity')
            quantity.text = str(entry['quantity'])

        return tree
