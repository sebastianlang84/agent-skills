"""Offline configuration regressions for neutral model selection."""
import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/models_conf.py"
SPEC = importlib.util.spec_from_file_location("harness_models_conf", SCRIPT)
models = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(models)


class ModelConfigTests(unittest.TestCase):
    def test_valid_model_ids_are_not_blocked_by_personal_policy(self):
        with tempfile.TemporaryDirectory() as temp:
            config = Path(temp) / "models.conf"
            for model in ("gpt-6-sol", "gpt-6-astra", "vendor/custom-model"):
                with self.subTest(model=model):
                    config.write_text(f"CODEX_MODEL={model}\n", encoding="utf-8")
                    values, sources = models.load(config)
                    self.assertEqual(values["CODEX_MODEL"], model)
                    self.assertEqual(sources["CODEX_MODEL"], "file")

    def test_example_matches_effective_defaults(self):
        values, _ = models.load(SCRIPT.parents[1] / "references/models.conf.example")
        self.assertEqual(values, models.DEFAULTS)


if __name__ == "__main__":
    unittest.main()
