from src.Movable import Movable


class Character(Movable):
    def __init__(self, name, pos, sprite, hp, max_move, strength, classes, equipments, lvl):
        Movable.__init__(self, name, pos, sprite, hp, max_move, strength, lvl)
        self.equipments = equipments
        self.classes = classes

    def display(self, screen):
        Movable.display(self, screen)
        for eq in self.equipments:
            eq.display(screen, self.pos, True)

    def get_weapon(self):
        for eq in self.equipments:
            if eq.body_part == 'right_hand':
                return eq
        return None

    def get_equipments(self):
        return self.equipments

    def get_classes(self):
        return self.classes

    def get_formatted_classes(self):
        formatted_string = ""
        for cl in self.classes:
            formatted_string += cl.capitalize() + ", "
        if formatted_string == "":
            return "None"
        return formatted_string[:-2]

    def equip(self, eq):
        for equip in self.equipments:
            if eq.body_part == equip.body_part:
                return False
        self.equipments.append(eq)
        self.remove_item(eq)
        return True

    def remove_equipment(self, eq):
        id = eq.get_id()
        for index, equip in enumerate(self.equipments):
            if equip.get_id() == id:
                return self.equipments.pop(index)

    def attack(self, ent):
        damages = self.strength
        weapon = self.get_weapon()
        if weapon:
            damages += weapon.get_power()
            if weapon.used() == 0:
                self.remove_equipment(weapon)
        return damages