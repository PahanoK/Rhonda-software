import random

prefixes = "Annihilation, Agony, Apocalypse, Pain, Suffering"

pr2 = prefixes.split(',')
for i in range(len(pr2)):
    pr2[i] = pr2[i].strip()


class Character:
    def __init__(self, name):
        self.name = name
        self.str = 10
        self.agi = 10
        self.int = 10
        self.inventory = {}
        self.hand = {}
        self.base_damage = [self.str/10, self.str/5]
        self.damage = [self.str/10, self.str/5]
        self.hp = self.str*3
        self.base_aps = self.agi*0.1     # временные значения, многовато за поинт агилки
        self.aps = self.base_aps

    def update_stats(self):
        if len(self.hand) > 0:
            wep = list(self.hand.values())[0]
            self.damage = [self.base_damage[0] + wep.damage[0], self.base_damage[1] + wep.damage[1]]
            self.aps = self.base_aps + wep.aps
        else:
            self.damage = self.base_damage
            self.aps = self.base_aps

    def pick_item(self, item):
        for i in range(1, 100):
            if str(i) not in self.inventory:
                self.inventory.update({str(i): item})        # имя предмета - ключ
                break

    def look_inventory(self):
        for num, item in self.inventory.items():
            print(str(num) + '. ' + str(item))

    def look_equipped(self):
        for num, item in self.hand.items():
            print('You are wielding ' + str(item))

    def equip_item(self):
        choice = int(input('Enter position of desired weapon.'))
        if len(self.hand) > 0:
            pop = self.hand.popitem()
            self.pick_item(pop[1])

        pop = self.inventory.pop(str(choice))     # ищем в инвентаре item и вынимаем
        self.hand.update({pop.name: pop})
        self.update_stats()

    def get_damage(self):
        print('Your damage is ' + str(int(self.damage[0])) +
              '-'+str(int(self.damage[1])) + ', '+str(self.aps) + " attacks per second")


class Weapon:
    def __init__(self, name, rarity='normal'):
        self.damage = [0, 0]
        self.rarity = rarity
        self.suffixes = 0
        self.prefixes = 0
        if rarity == 'magical':
            self.suffixes += random.randint(0, 1)
            self.prefixes += random.randint(0, 1)
        self.name = str(str(random.choice(pr2)) + ' ' + name)
        self.aps = 0

    def get_damage(self):
        print('This ' + self.name + ' damage is ' + str(self.damage[0]) +
              '-'+str(self.damage[1]) + ', ' + str(self.aps) + " attacks per second" +
              ' and is of ' + self.rarity + ' quality.')

    def __repr__(self):
        return self.name


class Dagger(Weapon):
    def __init__(self):
        Weapon.__init__(self, 'Dagger')
        self.aps = random.randint(40, 60)/100 + 1
        self.damage[0], self.damage[1] = random.randint(2, 5), random.randint(4, 9)


dag = Dagger()
dag2 = Dagger()
dag3 = Dagger()
dag.get_damage()

MainChar = Character('Pavel')

MainChar.pick_item(dag)
MainChar.pick_item(dag2)
MainChar.pick_item(dag3)

print(MainChar.name)
MainChar.get_damage()
MainChar.look_inventory()
MainChar.look_equipped()

MainChar.equip_item()
MainChar.get_damage()

MainChar.look_inventory()
MainChar.look_equipped()

MainChar.equip_item()

MainChar.look_inventory()
MainChar.look_equipped()