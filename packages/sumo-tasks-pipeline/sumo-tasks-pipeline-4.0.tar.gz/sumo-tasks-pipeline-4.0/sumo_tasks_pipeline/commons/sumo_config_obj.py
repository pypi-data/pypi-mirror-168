import dataclasses
import pathlib
import typing


@dataclasses.dataclass
class SumoConfigObject(object):
    """Configurations to run simulations.

    Args:
        job_id: unique id to distinguish simulations
        seed: random seed of a simulation. The argument puts the "--seed" option. -1 represents not to use the --seed option.
    """
    scenario_name: str
    path_config_dir: pathlib.Path
    config_name: str = 'sumo.cfg'
    path_config_dir_original: typing.Optional[pathlib.Path] = None
    job_id: typing.Optional[str] = None
    seed: int = -1

    def __post_init__(self):
        assert self.path_config_dir.exists(), f'No directory found at {self.path_config_dir}'
        assert self.path_config_dir.joinpath(self.config_name).exists()
        if self.job_id is None:
            self.job_id = self.scenario_name
        else:
            self.job_id = self.job_id


