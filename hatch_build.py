from pathlib import Path
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        content = f'__version__ = "{Path("VERSION").read_text().strip()}"\n'
        for package_dir in ["python/qplot", "python/qplot_backend"]:
            Path(f"{package_dir}/_version.py").write_text(content)
