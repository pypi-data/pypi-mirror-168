"""Interactions with the db-contrib-tool bisect command."""
import logging
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import structlog

from db_contrib_tool.config import SetupReproEnvConfig
from db_contrib_tool.services.evergreen_service import EvergreenService
from db_contrib_tool.utils import evergreen_conn

LOGGER = structlog.getLogger(__name__)

BISECT_DIR = os.path.dirname(os.path.abspath(__file__))
SETUP_TEST_ENV_SH = os.path.join(BISECT_DIR, "setup_test_env.sh")
TEARDOWN_TEST_ENV_SH = os.path.join(BISECT_DIR, "teardown_test_env.sh")
RUN_USER_SCRIPT_SH = os.path.join(BISECT_DIR, "run_user_script.sh")


def setup_logging(debug: bool = False) -> None:
    """
    Enable logging.

    :param debug: Whether to setup debug logging.
    """
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format="[%(asctime)s - %(name)s - %(levelname)s] %(message)s",
        level=log_level,
        stream=sys.stdout,
    )
    structlog.configure(logger_factory=structlog.stdlib.LoggerFactory())


class Bisect:
    """Main class for the Bisect subcommand."""

    def __init__(
        self,
        branch: str,
        lookback: int,
        variant: str,
        script: str,
        python_installation: str,
        evergreen_config: Optional[str] = None,
        debug: bool = False,
    ):
        """Initialize."""
        setup_logging(debug)
        self.branch = branch
        self.lookback = lookback
        self.variant = variant
        self.script = script
        self.python_installation = python_installation
        self.evergreen_config = evergreen_config
        self.evg_api = evergreen_conn.get_evergreen_api(evergreen_config)
        self.evg_service = EvergreenService(self.evg_api, SetupReproEnvConfig.empty_config())

    @staticmethod
    def _teardown_test_env(version: str) -> None:
        """
        Remove any directories added during testing process.

        :param version: Version reference.
        """
        try:
            subprocess.run(["bash", TEARDOWN_TEST_ENV_SH], check=True)
        except subprocess.CalledProcessError as err:
            LOGGER.error("Could not teardown test environment for bisect.", version=version)
            raise err
        LOGGER.info("Completed teardown of test environment for bisect.", version=version)

    def _setup_test_env(self, version: str) -> None:
        """
        Set up a test environment for the given version.

        :param version: Version reference.
        """
        try:
            subprocess.run(
                [
                    "bash",
                    SETUP_TEST_ENV_SH,
                    self.python_installation,
                    self.evergreen_config if self.evergreen_config else "",
                    self.variant,
                    version,
                ],
                check=True,
            )
        except subprocess.CalledProcessError:
            LOGGER.error(
                "Could not setup test environment for bisect -- retrying.", version=version
            )
            try:
                subprocess.run(
                    [
                        "bash",
                        SETUP_TEST_ENV_SH,
                        self.python_installation,
                        self.evergreen_config if self.evergreen_config else "",
                        self.variant,
                        version,
                    ],
                    check=True,
                )
            except subprocess.CalledProcessError as err:
                LOGGER.error("Could not setup test environment for bisect.", version=version)
                raise err
        LOGGER.info("Completed setup of test environment for bisect.", version=version)

    def _run_user_script(self, version: str) -> int:
        """
        Run the user script in a virtual environment.

        :param version: Version reference.
        :return: Return code of script run.
        """
        return subprocess.run(
            ["bash", RUN_USER_SCRIPT_SH, version, self.script], check=False
        ).returncode

    def _test_version_with_script(self, version: str) -> bool:
        """
        Test the given version with the user provided script.

        :param version: Version reference.
        :return: Whether succeeded or not.
        """
        self._setup_test_env(version)
        success = self._run_user_script(version)
        self._teardown_test_env(version)
        return success == 0

    def bisect(self, versions: List[str]) -> Optional[str]:
        """
        Bisect to find latest passing version assuming ordered by oldest to latest version.

        :param versions: List of versions that have binaries.
        :return: Found version or None.
        """
        if len(versions) == 0:
            return None
        midpoint = len(versions) // 2
        success = self._test_version_with_script(versions[midpoint])
        # if success, keep checking right
        if success:
            LOGGER.info(
                "Version passed user script.",
                version=versions[midpoint],
            )
            return self.bisect(versions[midpoint + 1 :]) or versions[midpoint]
        # if fail, keep checking left
        else:
            LOGGER.info("Version failed user script.", version=versions[midpoint])
            return self.bisect(versions[0:midpoint])

    def find_versions_with_binaries(self) -> List[str]:
        """
        Find versions that have binaries for the user provided variant in the lookback period.

        :return: List of versions that have binaries ordered from earliest to latest.
        """
        versions_with_binaries = []
        for version in self.evg_api.versions_by_project_time_window(
            project_id=f'mongodb-mongo-{"" if self.branch == "master" else "v"}{self.branch}',
            before=datetime.now(timezone.utc),
            after=datetime.now(timezone.utc) - timedelta(self.lookback),
        ):
            urls = self.evg_service.get_compile_artifact_urls(
                version, self.variant, ignore_failed_push=True
            )
            if urls is not None and urls.urls.get("Artifacts") and urls.urls.get("Binaries"):
                versions_with_binaries.append(version.revision)

        versions_with_binaries.reverse()
        return versions_with_binaries

    def execute(self) -> bool:
        """
        Perform bisect for the provided branch, variant & lookback period based on result of script.

        Print the last passing version and first failing version.

        :return: Whether succeeded or not.
        """
        versions_with_binaries = self.find_versions_with_binaries()

        # No versions found
        if not versions_with_binaries:
            LOGGER.info(
                "No versions with binaries found for given branch, variant & lookback period.",
                branch=self.branch,
                variant=self.variant,
                lookback=self.lookback,
            )
            return True

        LOGGER.info(
            "Performing bisect on the following versions: ", versions=versions_with_binaries
        )

        last_passing_version = self.bisect(versions_with_binaries)
        first_failing_version = None

        # All versions failed
        if last_passing_version is None:
            first_failing_version = versions_with_binaries[0]
            LOGGER.info("All versions in lookback period failed.")

        # All versions passed
        elif last_passing_version == versions_with_binaries[-1]:
            LOGGER.info("All versions in lookback period passed.")

        else:
            first_failing_version = versions_with_binaries[
                versions_with_binaries.index(last_passing_version) + 1
            ]

        print(f"Last Known Passing Version: {last_passing_version}")
        print(f"First Known Failing Version: {first_failing_version}")
        return True
