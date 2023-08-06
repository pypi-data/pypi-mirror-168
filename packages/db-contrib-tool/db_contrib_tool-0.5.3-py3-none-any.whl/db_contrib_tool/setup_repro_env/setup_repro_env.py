"""Setup MongoDB repro environment."""
import os
import re
from typing import List, NamedTuple, Optional

import inject
import structlog

from db_contrib_tool.clients.download_client import DownloadError
from db_contrib_tool.clients.file_service import FileService
from db_contrib_tool.clients.resmoke_proxy import ResmokeProxy
from db_contrib_tool.config import WINDOWS_BIN_PATHS_FILE, DownloadTarget
from db_contrib_tool.services.evergreen_service import EvergreenService
from db_contrib_tool.setup_repro_env.artifact_discovery_service import (
    ArtifactDiscoveryService,
    RequestTarget,
    RequestType,
)
from db_contrib_tool.setup_repro_env.download_service import (
    ArtifactDownloadService,
    DownloadOptions,
)
from db_contrib_tool.utils import evergreen_conn, is_windows

BINARY_ARTIFACT_NAME = "Binaries"
KNOWN_BRANCHES = {"master"}
RELEASE_VERSION_RE = re.compile(r"^\d+\.\d+$")
PATCH_VERSION_RE = re.compile(r"^\d+\.\d+\.\d+")
BRANCH_RE = re.compile(r"^v\d+\.\d+")
EXTERNAL_LOGGERS = [
    "evergreen",
    "github",
    "inject",
    "segment",
    "urllib3",
]

LOGGER = structlog.getLogger(__name__)


class SetupReproParameters(NamedTuple):
    """
    Parameters describing how a repro environment should be setup.

    * edition: MongoDB edition to download.
    * platform: Target platform to download.
    * architecture: Target architecture to download.
    * variant: Build Variant to download from.

    * versions: List of items to download.
    * install_last_lts: If True download last LTS version of mongo.
    * install_last_continuous: If True download last continuous version of mongo.
    * ignore_failed_push: Download version even if the push task failed.
    * fallback_to_master: Should the latest master be downloaded if the version doesn't exist.

    * evg_version_file: Write which evergreen version were downloaded from to this file.

    * download_options: Options specifying how downloads should occur.
    """

    edition: str
    platform: Optional[str]
    architecture: str
    variant: Optional[str]

    versions: List[str]
    install_last_lts: bool
    install_last_continuous: bool
    ignore_failed_push: bool
    fallback_to_master: bool

    evg_version_file: Optional[str]

    download_options: DownloadOptions

    def get_download_target(self, platform: Optional[str] = None) -> DownloadTarget:
        """
        Get the download target to use based on these parameters.

        :param platform: Override the platform with this platform.
        :return: Download target specified by this options.
        """
        platform = platform if platform is not None else self.platform
        return DownloadTarget(
            edition=self.edition, platform=platform, architecture=self.architecture
        )


class SetupReproOrchestrator:
    """Orchestrator for setting up repro environments."""

    @inject.autoparams()
    def __init__(
        self,
        evg_service: EvergreenService,
        resmoke_proxy: ResmokeProxy,
        artifact_download_service: ArtifactDownloadService,
        artifact_discovery_service: ArtifactDiscoveryService,
        file_service: FileService,
    ) -> None:
        """
        Initialize the orchestrator.

        :param evg_service: Service for working with evergreen.
        :param resmoke_proxy: Proxy for working with resmoke.
        :param artifact_download_service: Service to download artifacts.
        :param artifact_discovery_service: Service to find artifacts.
        :param file_service: Service to work with the filesystem.
        """
        self.evg_service = evg_service
        self.resmoke_proxy = resmoke_proxy
        self.artifact_download_service = artifact_download_service
        self.artifact_discovery_service = artifact_discovery_service
        self.file_service = file_service

    def interpret_request(self, request: str) -> RequestTarget:
        """
        Translate the request from the user into an item we can understand.

        :param request: Request from user.
        :return: Targeted request to download.
        """
        if request in KNOWN_BRANCHES or BRANCH_RE.match(request):
            return RequestTarget(RequestType.GIT_BRANCH, request)

        if RELEASE_VERSION_RE.match(request):
            return RequestTarget(RequestType.MONGO_RELEASE_VERSION, request)

        if PATCH_VERSION_RE.match(request):
            return RequestTarget(RequestType.MONGO_PATCH_VERSION, request)

        if self.evg_service.query_task_existence(request):
            return RequestTarget(RequestType.EVG_TASK, request)

        if self.evg_service.query_version_existence(request):
            return RequestTarget(RequestType.EVG_VERSION, request)

        return RequestTarget(RequestType.GIT_COMMIT, request)

    def interpret_requests(
        self, request_list: List[str], last_lts: bool, last_continuous: bool
    ) -> List[RequestTarget]:
        """
        Translate all the requests from the user into items we can understand.

        :param request_list: Requests from user.
        :param last_lts: Should 'last lts' version be included.
        :param last_continuous: Should the 'last continuous' version be included.
        :return: List of targeted request to download.
        """
        requests = [self.interpret_request(request) for request in request_list]
        if last_lts or last_continuous:
            requests.extend(self._get_release_versions(last_lts, last_continuous))

        return requests

    def _get_release_versions(
        self, install_last_lts: Optional[bool], install_last_continuous: Optional[bool]
    ) -> List[RequestTarget]:
        """
        Create a list of multiversion versions that should be included.

        :param install_last_lts: True if the last LTS version should be included.
        :param install_last_continuous: True if the last continuous version should be included.
        :return: List of which multiversion versions should be included.
        """
        multiversionconstants = self.resmoke_proxy.get_multiversion_constants()
        releases = {
            multiversionconstants.last_lts_fcv: install_last_lts,
            multiversionconstants.last_continuous_fcv: install_last_continuous,
        }
        LOGGER.debug("LTS and continuous release inclusions", releases=releases)
        out = {
            RequestTarget.previous_release(version)
            for version, requested in releases.items()
            if requested
        }

        return list(out)

    @staticmethod
    def _get_bin_suffix(version: str, evg_project_id: str) -> str:
        """
        Get the multiversion bin suffix from the evergreen project ID.

        :param version: Version from the cmdline.
        :param evg_project_id: Evergreen project ID.
        :return: Bin suffix.
        """
        if re.match(r"(\d+\.\d+)", version):
            # If the cmdline version is already a semvar, just use that.
            return version

        project_version_search = re.search(r"(\d+\.\d+$)", evg_project_id)
        if project_version_search:
            # Extract version from the Evergreen project ID as fallback.
            return project_version_search.group(0)

        # If the version is not a semvar, we can't add a suffix.
        return ""

    def execute(self, setup_repro_params: SetupReproParameters) -> bool:
        """
        Execute setup repro env mongodb.

        :param setup_repro_params: Setup repro env parameters.
        :return: Whether succeeded or not.
        """
        request_list = self.interpret_requests(
            setup_repro_params.versions,
            setup_repro_params.install_last_lts,
            setup_repro_params.install_last_continuous,
        )

        downloaded_versions = []
        failed_requests = []
        link_directories = []

        download_target = setup_repro_params.get_download_target()
        LOGGER.info("Search criteria", search_criteria=download_target)

        for request in request_list:
            LOGGER.info("Setting up request", request=request)
            LOGGER.info("Fetching download URLs from Evergreen")

            try:
                urls_info = self.artifact_discovery_service.find_artifacts(
                    request,
                    setup_repro_params.variant,
                    download_target,
                    setup_repro_params.ignore_failed_push,
                    setup_repro_params.fallback_to_master,
                )

                if urls_info is None:
                    failed_requests.append(request)
                    LOGGER.warning("Unable to find artifacts for request", request=request)
                    continue

                bin_suffix = self._get_bin_suffix(request.identifier, urls_info.project_identifier)
                linked_dir = self.artifact_download_service.download_and_extract(
                    urls_info.urls,
                    bin_suffix,
                    urls_info.evg_version_id,
                    setup_repro_params.download_options,
                )
                if linked_dir:
                    link_directories.append(linked_dir)
                downloaded_versions.append(urls_info.evg_version_id)
                LOGGER.info("Setup request completed", request=request)
            except (
                evergreen_conn.EvergreenConnError,
                DownloadError,
            ):
                failed_requests.append(request)
                LOGGER.error("Setup request failed", request=request, exc_info=True)

        if is_windows():
            self.file_service.write_windows_install_paths(WINDOWS_BIN_PATHS_FILE, link_directories)

        if setup_repro_params.evg_version_file is not None:
            self.file_service.append_lines_to_file(
                setup_repro_params.evg_version_file, downloaded_versions
            )
            LOGGER.info(
                "Finished writing downloaded Evergreen versions",
                target_file=os.path.abspath(setup_repro_params.evg_version_file),
            )

        if len(downloaded_versions) < len(request_list):
            LOGGER.error("Some requests were not able to setup.", failed_requests=failed_requests)
            return False
        LOGGER.info("Downloaded versions", request_list=request_list)
        return True
