"""Builds the wheel, installs it in a new venv and uses it from outside the repo."""

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = """
from geothai import province
from geothai.abolished import abolished_areas
from geothai.types import Province

found: Province | None = province("84")
assert found is not None and found.name_en == "Surat Thani", found
assert len(abolished_areas()) > 0
"""


def run(*args: str, cwd: Path) -> str:
    done = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)
    if done.returncode != 0:
        sys.exit(f"{' '.join(args[:2])} failed:\n{done.stdout}{done.stderr}")
    return done.stdout


with tempfile.TemporaryDirectory(prefix="geothai-wheel-") as tmp:
    app = Path(tmp)
    run("uv", "build", "--wheel", "--out-dir", str(app), cwd=ROOT)
    wheel = next(app.glob("geothai-*.whl"))
    python = sys.argv[1] if len(sys.argv) > 1 else "3.11"
    run("uv", "venv", "--quiet", "--python", python, str(app / ".venv"), cwd=app)
    venv_python = str(app / ".venv" / "bin" / "python")
    run("uv", "pip", "install", "--quiet", "--python", venv_python, str(wheel), cwd=app)
    (app / "app.py").write_text(APP, encoding="utf-8")
    (app / "pyrightconfig.json").write_text('{"typeCheckingMode": "strict"}', encoding="utf-8")
    # Runs from the app folder, so a path that only works inside the repo fails here.
    run(venv_python, "app.py", cwd=app)
    run("pyright", "--pythonpath", venv_python, "app.py", cwd=app)
    version = run(venv_python, "--version", cwd=app).strip()
    print(f"{wheel.name}: import and types work on {version}")
