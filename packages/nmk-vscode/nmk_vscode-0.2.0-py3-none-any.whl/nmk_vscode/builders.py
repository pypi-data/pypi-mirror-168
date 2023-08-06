import json
from pathlib import Path
from typing import List

from nmk_base.common import TemplateBuilder


class JsonTemplateBuilder(TemplateBuilder):
    def contribute(self, settings: dict, update: dict):
        for k, v in update.items():
            # Already exists in target model?
            if k in settings:
                # List: extend
                if isinstance(v, list):
                    settings[k].extend(v)
                # Map: update
                elif isinstance(v, dict):
                    settings[k].update(v)
                # Otherwise: replace
                else:
                    settings[k] = v
            else:
                # New key
                settings[k] = v

    def build_json(self, files: List[str], items: dict = None):
        # Iterate on files to merge them
        json_model = {}
        for file_p in map(Path, files):
            self.logger.debug(f"Loading json model fragment: {file_p}")
            self.contribute(json_model, json.loads(self.render_template(file_p, {})))

        # Post-process with raw provided items (if any)
        if items is not None:
            self.logger.debug(f"Update json model from config: {items}")
            self.contribute(json_model, items)

        # Generate json_model file
        with self.main_output.open("w") as f:
            json.dump(json_model, f, indent=4)


class SettingsBuilder(JsonTemplateBuilder):
    def build(self, files: List[str], items: dict):
        self.build_json(files, items)


class LaunchBuilder(JsonTemplateBuilder):
    def build(self, files: List[str]):
        self.build_json(files)
