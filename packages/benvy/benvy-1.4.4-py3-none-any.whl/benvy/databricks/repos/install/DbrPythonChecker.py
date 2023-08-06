import os
import sys
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface
from penvy.poetry import config_reader


class DbrPythonChecker(SetupStepInterface):
    def __init__(
        self,
        project_root_path: str,
        logger: Logger,
    ):
        self._project_root_path = project_root_path
        self._logger = logger

    def run(self):
        self._logger.info("Checking DBR python version")

        dbr_python_version = self._get_dbr_python_version()
        lock_python_version = self._get_lock_python_version()

        self._check_python_version(dbr_python_version, lock_python_version)

    def get_description(self):
        return "Check DBR python version"

    def should_be_run(self) -> bool:
        return "DAIPE_BOOTSTRAPPED" not in os.environ

    def _check_python_version(self, dbr_python_version: str, lock_python_version: str):
        if dbr_python_version == lock_python_version:
            self._logger.info("Python version OK")

        else:
            self._logger.warning(
                f"DBR python version '{dbr_python_version}' does not match poetry.lock version '{lock_python_version}'. "
                f"It's strongly recommended to lock to that python version in 'pyproject.toml'"
            )

    def _get_dbr_python_version(self) -> str:
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    def _get_lock_python_version(self) -> str:
        poetry_lock = config_reader.read(f"{self._project_root_path}/poetry.lock")

        return poetry_lock["metadata"]["python-versions"]
