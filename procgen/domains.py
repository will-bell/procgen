import json
from typing import Union, Dict, Any, Optional
import warnings
import time
import os
import pathlib
import datetime


Number = Union[int, float]


def datetime_name():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


class DomainConfig:
    """
    Base class for configuring game parameters in Procgen
    """

    game: str

    update_time: int

    _cache_name: str

    cache_directory: Optional[str]

    path: Optional[str]

    def __init__(self, cache_name: str = None):
        self.update_time = self._timestamp()

        self._cache_name = cache_name if cache_name is not None else 'cache-' + datetime_name()

        self.game = ''
        self.path = None
        self.cache_directory = None

    def __repr__(self) -> str:
        statement = f'{self.__class__.__name__} {{\n'
        for key, value in self.__dict__.items():
            statement += f'   {key}: {value}\n'
        statement += '}'
        return statement

    @staticmethod
    def _timestamp() -> int:
        """Get an integer timestamp. Useful for naming things

        :return: timestamp
        """
        return int(time.time() * 1000)

    def _json_data(self) -> Dict[str, Any]:
        """Get the attributes that we want to serialize to json

        All attributes that are not private will be written to the json file.

        :return: filtered version of the instance's __dict__
        """
        return {k: v for k, v in self.__dict__.items() if k[0] != '_'}

    @property
    def parameters(self) -> Dict[str, Any]:
        return {k: v for k, v in self._json_data() if k not in ['game', 'path', 'cache_directory']}

    def _to_json(self, path: Union[pathlib.Path, str]):
        """Write the configuration to a json file

        :param path: desired path for the json file
        :return: None
        """
        with open(str(path), 'w') as json_file:
            json.dump(self._json_data(), json_file)

    def to_json(self, path: Union[pathlib.Path, str]):
        """Write the configuration to a json file and set the path for later use

        :param path: desired path for the json file
        :return: None
        """
        if path != self.path:
            path_obj = pathlib.Path(path).absolute()
            self.path = str(path_obj)

            config_directory = path_obj.parent
            self.cache_directory = str(config_directory.joinpath(self._cache_name))
            if not os.path.isdir(self.cache_directory):
                os.mkdir(self.cache_directory)

            self._to_json(self.path)

    @classmethod
    def from_json(cls, path: Union[pathlib.Path, str]) -> 'DomainConfig':
        """Load a configuration from a json file

        :param path: path to the json file containing the configuration parameters
        :return: configuration loaded from the file
        """
        obj = cls()
        with open(str(path)) as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                setattr(obj, key, value)

        obj.path = path

        return obj

    def update_parameters(self, parameters: Dict[str, Number], cache: bool = True):
        """Update a configuration in place and optionally cache its current state

        If a configuration has already been written to a json file, then this method will update the json file with the
        new parameters. The path to the json file will not change. If we wish to cache the current state of the
        configuration before the parameters are changed, then the data will be copied to a new json file in the cache
        directory.

        :param parameters: new parameters for the configuration
        :param cache: cache the current state of the configuration
        :return: None
        """
        if cache and self.path:
            # Cache the current state of the environment configuration before modifying it.
            # In the future, this should maintain some graph structure to see how the configuration branches throughout
            # the ADR algorithm progression
            cache_path = str(pathlib.Path(self.cache_directory).joinpath('config-' + str(self.update_time) + '.json'))
            self._to_json(cache_path)

        self.update_time = self._timestamp()
        for name, value in parameters.items():
            try:
                setattr(self, name, value)

            except AttributeError:
                warnings.warn(f'{name} is not a parameter of {self.__class__.__name__}... passing...')

        # If the config has been written to a json file, then update the file
        if self.path:
            with open(self.path, 'w') as json_file:
                json.dump(self.__dict__, json_file)


class BossfightDomainConfig(DomainConfig):
    """
    Class for configuring the Bossfight game in Procgen
    """

    min_n_rounds: int
    max_n_rounds: int

    min_n_barriers: int
    max_n_barriers: int

    min_boss_round_health: int
    max_boss_round_health: int
    min_boss_invulnerable_duration: int
    max_boss_invulnerable_duration: int
    n_boss_attack_modes: int
    min_boss_bullet_velocity: float
    max_boss_bullet_velocity: float
    boss_rand_fire_prob: float
    boss_scale: float = 1.

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

        super().__init__()

        self.game = 'dc_bossfight'

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
