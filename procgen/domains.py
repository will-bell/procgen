import json


class Domain:

    def to_json(self, path: str):
        with open(path, 'w') as json_file:
            json.dump(self.__dict__, json_file)

    @classmethod
    def from_json(cls, path: str):
        obj = cls()
        with open(path) as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                setattr(obj, key, value)

        return obj

    def __repr__(self) -> str:
        statement = f'{self.__class__.__name__} {{\n'
        for key, value in self.__dict__.items():
            statement += f'   {key}: {value}\n'
        statement += '}'
        return statement


class BossfightDomainConfig(Domain):

    def __init__(self,
                 min_n_rounds: int = 1,
                 max_n_rounds: int = 6,

                 min_n_barriers: int = 1,
                 max_n_barriers: int = 4,

                 min_boss_round_health: int = 1,
                 max_boss_round_health: int = 10,
                 min_boss_invulnerable_duration: int = 3,
                 max_boss_invulnerable_duration: int = 3,
                 n_boss_attack_modes: int = 4,
                 min_boss_bullet_velocity: float = .5,
                 max_boss_bullet_velocity: float = .75,
                 boss_rand_fire_prob: float = .1,
                 boss_scale: float = 1.):

        self.game = 'Bossfight'

        self.min_n_rounds = min_n_rounds
        self.max_n_rounds = max_n_rounds

        self.min_n_barriers = min_n_barriers
        self.max_n_barriers = max_n_barriers

        self.min_boss_round_health = min_boss_round_health
        self.max_boss_round_health = max_boss_round_health
        self.min_boss_invulnerable_duration = min_boss_invulnerable_duration
        self.max_boss_invulnerable_duration = max_boss_invulnerable_duration
        self.n_boss_attack_modes = n_boss_attack_modes
        self.min_boss_bullet_velocity = min_boss_bullet_velocity
        self.max_boss_bullet_velocity = max_boss_bullet_velocity
        self.boss_rand_fire_prob = boss_rand_fire_prob
        self.boss_scale = boss_scale
