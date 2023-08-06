"""
Collector plugin for RPM packages
"""
import os

from pathlib import Path
from typing import Any, Dict, Optional

from packageurl import PackageURL  # type: ignore

from hoppr import __version__
from hoppr.base_plugins.collector import CollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.context import Context
from hoppr.result import Result


def _artifact_string(purl):
    artifact_string = purl.name
    if purl.version is not None:
        artifact_string += f"-{purl.version}"

    # Limiting to an architecture using --archlist finds all compatible architectures,
    # not just the specified one, so . . .
    if "arch" in purl.qualifiers:
        artifact_string += f"*{purl.qualifiers.get('arch')}"

    return artifact_string


class CollectYumPlugin(CollectorPlugin):
    """
    Collector plugin for yum images
    """

    supported_purl_types = ["rpm"]
    required_commands = ["dnf"]

    def get_version(self) -> str:
        return __version__

    def __init__(self, context: Context, config: Optional[Dict] = None) -> None:
        super().__init__(context=context, config=config)

        if self.config is not None:
            if "yumdownloader_command" in self.config:
                self.required_commands = [self.config["yumdownloader_command"]]

    @hoppr_rerunner
    def collect(self, comp: Any, repo_url: str, creds=None):
        """
        Copy a component to the local collection directory structure
        """

        purl = PackageURL.from_string(comp.purl)

        artifact = _artifact_string(purl)

        self.get_logger().info(f"Copying yum package from {purl}")

        if creds is not None:
            setopts = [
                f"--setopt=username={creds.username}",
                f"--setopt=password={creds.password}",
            ]

            password_list = [creds.password]
        else:
            setopts = []
            password_list = None

        base_command = [
            self.required_commands[0],
            "--quiet",
            f"--repofrompath=hoppr,{repo_url}",
            "--repo=hoppr",
            *setopts,
            "--disableexcludes=all",
        ]

        command = [*base_command, "repoquery", "--location", artifact]

        result = self.run_command(command, password_list=password_list)

        if result.returncode != 0 or len(result.stdout.decode("utf-8")) == 0:
            msg = f"{self.required_commands[0]} failed to locate package for {purl}"
            self.get_logger().error(msg)

            return Result.retry(msg)

        # Taking the first URL if multiple are returned
        found_url_path = Path(result.stdout.decode("utf-8").strip().split("\n")[0])

        subdir = os.sep.join(found_url_path.parts[len(Path(repo_url).parts) : -1])
        target_dir = self.directory_for(purl.type, repo_url, subdir=subdir)

        command = [*base_command, "download", f"--destdir={target_dir}", artifact]

        result = self.run_command(command, password_list=password_list)

        if result.returncode != 0:
            msg = f"Failed to download Yum artifact {purl.name} version {purl.version}"
            return Result.retry(msg)

        return Result.success()
