#!/usr/bin/env python
import argparse

from procgen import ProcgenGym3Env
from procgen.domains import BossfightDomainConfig
from .env import ENV_NAMES
from gym3 import Interactive, VideoRecorderWrapper, unwrap
import pathlib
import datetime


class ProcgenInteractive(Interactive):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_state = None

    def _update(self, dt, keys_clicked, keys_pressed):
        if "LEFT_SHIFT" in keys_pressed and "F1" in keys_clicked:
            print("save state")
            self._saved_state = unwrap(self._env).get_state()
        elif "F1" in keys_clicked:
            print("load state")
            if self._saved_state is not None:
                unwrap(self._env).set_state(self._saved_state)
        super()._update(dt, keys_clicked, keys_pressed)


def make_interactive(vision, record_dir, **kwargs):
    info_key = None
    ob_key = None
    if vision == "human":
        info_key = "rgb"
        kwargs["render_mode"] = "rgb_array"
    else:
        ob_key = "rgb"

    env = ProcgenGym3Env(num=1, **kwargs)
    if record_dir is not None:
        env = VideoRecorderWrapper(
            env=env, directory=record_dir, ob_key=ob_key, info_key=info_key
        )
    h, w, _ = env.ob_space["rgb"].shape
    return ProcgenInteractive(
        env,
        ob_key=ob_key,
        info_key=info_key,
        width=w * 12,
        height=h * 12,
    )


INTERACTIVE_CONFIGS = {
    'dc_bossfight': BossfightDomainConfig(min_n_rounds=3,
                                          max_n_rounds=3,
                                          min_n_barriers=3,
                                          max_n_barriers=3,
                                          min_boss_round_health=5,
                                          max_boss_round_health=5,
                                          min_boss_invulnerable_duration=1,
                                          max_boss_invulnerable_duration=1,
                                          n_boss_attack_modes=4,
                                          min_boss_bullet_velocity=.2,
                                          max_boss_bullet_velocity=.2,
                                          min_boss_rand_fire_prob=.1,
                                          max_boss_rand_fire_prob=.5,
                                          min_boss_scale=.5,
                                          max_boss_scale=1.)
}


def datetime_name():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vision", choices=["agent", "human"], default="human")
    parser.add_argument("--record-dir", help="directory to record movies to")
    parser.add_argument(
        "--distribution-mode",
        default="hard",
        help="which distribution mode to use for the level generation",
    )
    parser.add_argument(
        "--env-name",
        default="dc_bossfight",
        help="name of game to create",
        choices=ENV_NAMES + ["coinrun_old"],
    )
    parser.add_argument(
        "--level-seed", type=int, help="select an individual level to use"
    )
    args = parser.parse_args()

    domain_config = INTERACTIVE_CONFIGS[args.env_name]
    experiment_dir = pathlib.Path().absolute() / 'interactive_test_experiments' / ('experiment-' + datetime_name())
    experiment_dir.mkdir(parents=True, exist_ok=False)
    config_dir = experiment_dir / 'domain_configs'
    config_dir.mkdir(parents=True, exist_ok=False)
    test_domain_config_path = config_dir / 'test_config.json'
    domain_config.to_json(test_domain_config_path)

    kwargs = {"domain_config_path": str(test_domain_config_path)}
    if args.env_name != "coinrun_old":
        kwargs["distribution_mode"] = args.distribution_mode
    if args.level_seed is not None:
        kwargs["start_level"] = args.level_seed
        kwargs["num_levels"] = 1
    ia = make_interactive(
        args.vision, record_dir=args.record_dir, env_name=args.env_name, **kwargs
    )
    ia.run()


if __name__ == "__main__":
    main()
