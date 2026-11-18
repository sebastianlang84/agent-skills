"""Exercise the shell launcher with real collection and a fake sibling reviewer."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("bash"), "doctor.sh requires Bash")
class DoctorLauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.scripts = self.root / "call-doctor/scripts"
        self.scripts.mkdir(parents=True)
        for name in ("doctor.sh", "collect.py"):
            shutil.copy2(SKILL / "scripts" / name, self.scripts / name)
        reviewer = self.root / "using-harnesses/scripts/review.py"
        reviewer.parent.mkdir(parents=True)
        reviewer.write_text(
            "import json, os, sys\n"
            "from pathlib import Path\n"
            "evidence = Path(sys.argv[-1]).read_text(encoding='utf-8')\n"
            "Path(os.environ['DOCTOR_TEST_LOG']).write_text(json.dumps(\n"
            "    {'args': sys.argv[1:], 'evidence': evidence}), encoding='utf-8')\n"
            "print('/tmp/fake-review-call')\n", encoding="utf-8")
        self.session = self.root / "session.jsonl"
        self.brief = self.root / "brief.md"
        self.brief.write_text("Diagnose missed context from evidence.\n", encoding="utf-8")
        self.log = self.root / "review.json"

    def tearDown(self):
        self.temp.cleanup()

    def invoke(self, launcher):
        env = {k: v for k, v in os.environ.items()
               if k not in ("CODEX_THREAD_ID", "CLAUDE_CODE_SESSION_ID")}
        env.update(DOCTOR_TEST_LOG=str(self.log), TMPDIR=str(self.root))
        result = subprocess.run(
            ["bash", str(launcher), "--session", str(self.session), str(self.brief)],
            capture_output=True, text=True, env=env, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "/tmp/fake-review-call")
        return json.loads(self.log.read_text())

    def test_claude_patient_uses_sibling_codex_reviewer(self):
        self.session.write_text(json.dumps({"type": "user", "message": {
            "content": "The agent missed the instruction."}}) + "\n")
        record = self.invoke(self.scripts / "doctor.sh")
        self.assertEqual(record["args"][:3], ["codex", "--effort", "medium"])
        self.assertIn("The agent missed the instruction.", record["evidence"])

    def test_codex_patient_uses_claude_through_symlinked_launcher(self):
        self.session.write_text(json.dumps({"type": "session_meta", "payload": {
            "cwd": "/path/to/project", "base_instructions": {"text": "Use evidence."}}}) + "\n")
        link = self.root / "doctor-link.sh"
        link.symlink_to(self.scripts / "doctor.sh")
        record = self.invoke(link)
        self.assertEqual(record["args"][:3], ["claude", "--effort", "medium"])
        self.assertIn("Use evidence.", record["evidence"])


if __name__ == "__main__":
    unittest.main()
