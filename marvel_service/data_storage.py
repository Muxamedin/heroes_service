"""Predefined data in tables for making tests of service
   tables:
      heroes, squads,

      heroes   - represents table with columns :
      'name'   - hero name - string
      'good',  - kind of hero - bool
      'power', - level of power - int
      'alive'  - state of health
            1 -  alive
            0.5 - injured
            0 - dead

      squads - table of groups - dict
      where:
          - key of dict is name of group
          - value of group - list of heroes

"""

DEAD = 0
ALIVE = 1
INJURED = 0.5
IGOOD = 0
IPOWER = 1
IALIVE = 2


heroes = {'spider_man':       [True, 2300, 1],
          'iron_fist':        [True, 2000, 1],
          'nova':             [True, 2000, 1],
          'white_tiger':      [True, 1500, 1],
          'human_torch':      [True, 1800, 1],
          'the_thing':        [True, 2100, 1],
          'invisible_girl':   [True, 1900, 1],
          'mister_fantastic': [True, 2100, 1],
          'venom':            [False, 2200, 1],
          'carnage':          [False, 2100, 1],
          'toxin':            [False, 2100, 1],
          'scream':           [False, 2100, 1],
          'red_skull':        [False, 2100, 1],
          'fisk':             [False, 2100, 1],
          'chameleon':        [False, 1300, 1],
          'doctor_octopus':   [False, 1900, 1],
          'captain_america':  [True, 2250, 1],
          'iron_man':         [True, 2200, 1],
          'hulk':             [True, 2100, 1],
          'loki':             [False, 1600, 1],
          'thor':             [True, 2300, 1],
          'donatello':        [True, 1700, 1],
          'raphael':          [True, 1850, 1],
          'leonardo':         [True, 1900, 1],
          'michelangelo':     [True, 1650, 1],
          'shredder':         [False, 2100, 1],
          'krang':            [False, 2200, 1],
          'baxter_stockman':  [False, 1200, 1],
          'karai':            [False, 1700, 1],
          'groot':            [True, 1800, 1],
          'rocket':           [True, 1500, 1],
          'star_lord':        [True, 1900, 1],
          'gamora':           [True, 1900, 1]
          }

squads = {'spider_man_team': ['spider_man',
                              'iron_fist',
                              'nova',
                              'white_tiger'],
          'fantastic_four': ['mister_fantastic',
                             'human_torch',
                             'the_thing',
                             'invisible_girl'],
          'future_foundation': ['spider_man',
                                'human_torch',
                                'the_thing',
                                'invisible_girl'],
          'hydra': ['fisk',
                    'chameleon',
                    'red_skull',
                    'doctor_octopus'],
          'avengers': ['captain_america',
                       'iron_man',
                       'hulk', 'thor'],
          'tmnt': ['leonardo',
                   'donatello',
                   'raphael',
                   'michelangelo'],
          'foot clan': ['shredder',
                        'krang',
                        'baxter_stockman',
                        'karai'],
          'guardians_ofthe_galaxy': ['groot',
                                     'rocket',
                                     'star_lord',
                                     'gamora'],
          'symbiots': ['venom', 'carnage', 'scream', 'toxin']
          }


class HeroesTableHandler:
    """Heroes - class for work with heroes tables """

    def __init__(self, ready_structure: dict = None):
        if ready_structure is None:
            self.heroes = {}
        else:
            self.heroes = ready_structure

    def validate_hero(self, name: str) -> bool:
        """is hero present at the table """

        status = False
        if name in self.heroes:
            status = True

        return status

    def validate_hero_params(self, params):
        if len(params) != 3:
            return False

        if type(params[IGOOD]) is not bool:
            return False

        if type(params[IPOWER]) != int:
            return False

        if not (params[IALIVE] == DEAD
                or params[IALIVE] == ALIVE
                or params[IALIVE] == INJURED):

            return False

        return True

    def add_entity(self, name, params: list) -> bool:

        if not self.validate_hero_params(params):
            return False

        self.heroes[name] = params

        return True

    def make_alive(self, name):
        if self.validate_hero(name):
            return False
        self.heroes[name][IALIVE] = ALIVE

    def make_injured(self, name):
        if name not in self.heroes:
            return False
        self.heroes[name][IALIVE] = INJURED

    def make_dead(self, name):
        if name not in self.heroes:
            return False
        self.heroes[name][IALIVE] = DEAD

    def set_good(self, name, good=True):
        if name not in self.heroes:
            return False
        self.heroes[name][IGOOD] = good

    def get_all_heroes(self):
        return list(self.heroes.keys())

    def get_hero_info(self, name: str) -> list:
        if self.validate_hero(name):
            return list(self.heroes[name])
        return []

    def delete_hero(self, name: str):
        if self.validate_hero(name):
            self.heroes.pop(name)


class SuperHeroSquads:
    """SuperHeroSquads - class of object which should process all data from squads
       object  - contains squads as a dict
    """

    def __init__(self, ready_structure: dict = None):
        if ready_structure is None:
            self.squads = {}
        else:
            self.squads = ready_structure

    def is_valid_squad(self, name):
        exists = False

        if name in self.squads:
            exists = True

        return exists

    def create_squad(self, name, params, available_heroes):
        params_filtered = [i for i in params if i in available_heroes]
        created = False
        if len(params_filtered) > 0:
            self.squads[name] = params_filtered
            created = True

        return created

    def get_all_squads(self):
        return list(self.squads.keys())

    def get_squad_info(self, name):
        if self.is_valid_squad(name):
            return list(self.squads[name])
        return []

    def delete_squad(self, name: str):
        if self.is_valid_squad(name):
            self.squads.pop(name)

    def delete_hero_from_squads(self, name: str):
        """Delete Hero from all groups"""

        for group in self.squads:
            while name in self.squads[group]:
                self.squads[group].remove(name)


def calculate_power(heroes, group, group_name1, group_name2):

    power_1: int = 0
    power_2: int = 0

    for name in group[group_name1]:
        power_1 += heroes[name][IPOWER] * heroes[name][IALIVE]

    for name in group[group_name2]:
        power_2 += heroes[name][IPOWER] * heroes[name][IALIVE]

    if power_1 > power_2:
        return group_name1
    if power_1 == power_2:
        return f'{group_name1}=={group_name2}'
    if power_1 < power_2:
        return group_name2


if __name__ == '__main__':
    hero = HeroesTableHandler(heroes)

