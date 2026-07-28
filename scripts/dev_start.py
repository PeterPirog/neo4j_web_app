"""Start local development services for the Neo4j Web App monorepo.

The script uses only the Python standard library. It starts missing local
services, waits for health checks, and stops only processes started by this
script when Ctrl+C is pressed.
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import webbrowser
from dataclasses import dataclass
from pathlib import Path


HOST = "127.0.0.1"
API_PREFIX = "/api/v1"


@dataclass
class StartedProcess:
    label: str
    process: subprocess.Popen
    stdout_path: Path
    stderr_path: Path
    stdout_file: object
    stderr_file: object


STARTED_PROCESSES: list[StartedProcess] = []


def find_project_root() -> Path:
    """Return the project root based on this file location."""
    return Path(__file__).resolve().parents[1]


def is_windows() -> bool:
    return platform.system().lower() == "windows"


def is_port_open(host: str, port: int, timeout_seconds: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout_seconds):
            return True
    except OSError:
        return False


def http_get(url: str, timeout_seconds: float = 5.0) -> tuple[bool, int | None, str]:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "dev-start/1.0"})
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8", errors="replace")
            return 200 <= response.status < 400, response.status, body
    except urllib.error.HTTPError as exc:
        return False, exc.code, exc.read().decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001 - user-facing diagnostic path
        return False, None, str(exc)


def wait_for_url(url: str, timeout_seconds: int, label: str) -> bool:
    deadline = time.monotonic() + timeout_seconds
    last_error = ""
    while time.monotonic() < deadline:
        ok, status, body = http_get(url, timeout_seconds=5)
        if ok:
            print(f"[ok] {label}: {url}")
            return True
        last_error = f"status={status}, body={body[:300]}"
        time.sleep(1)
    print(f"[error] {label} did not respond in {timeout_seconds}s: {last_error}")
    return False


def wait_for_any_url(urls: tuple[str, ...], timeout_seconds: int, label: str) -> bool:
    deadline = time.monotonic() + timeout_seconds
    last_error = ""
    while time.monotonic() < deadline:
        for url in urls:
            ok, status, body = http_get(url, timeout_seconds=5)
            if ok:
                print(f"[ok] {label}: {url}")
                return True
            last_error = f"{url}: status={status}, body={body[:300]}"
        time.sleep(1)
    print(f"[error] {label} did not respond in {timeout_seconds}s: {last_error}")
    return False


def run_command(command: list[str], cwd: Path, env: dict[str, str] | None = None, check: bool = True) -> int:
    display = " ".join(command)
    print(f"[run] {display}")
    try:
        completed = subprocess.run(command, cwd=str(cwd), env=env, check=False)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Command not found: {command[0]}") from exc

    if check and completed.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {completed.returncode}: {display}")
    return completed.returncode


def log_dir() -> Path:
    path = Path(tempfile.gettempdir()) / "neo4j_web_app_dev_start"
    path.mkdir(parents=True, exist_ok=True)
    return path


def start_process(command: list[str], cwd: Path, label: str, env: dict[str, str] | None = None) -> StartedProcess:
    stdout_path = log_dir() / f"{label}.stdout.log"
    stderr_path = log_dir() / f"{label}.stderr.log"
    stdout_file = stdout_path.open("w", encoding="utf-8", errors="replace")
    stderr_file = stderr_path.open("w", encoding="utf-8", errors="replace")

    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if is_windows() else 0
    print(f"[start] {label}: {' '.join(command)}")
    process = subprocess.Popen(
        command,
        cwd=str(cwd),
        env=env,
        stdout=stdout_file,
        stderr=stderr_file,
        creationflags=creationflags,
        start_new_session=not is_windows(),
    )
    started = StartedProcess(label, process, stdout_path, stderr_path, stdout_file, stderr_file)
    STARTED_PROCESSES.append(started)
    print(f"[start] {label} PID: {process.pid}")
    print(f"[log] {label} stdout: {stdout_path}")
    print(f"[log] {label} stderr: {stderr_path}")
    return started


def tail_file(path: Path, lines: int = 40) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    return "\n".join(text.splitlines()[-lines:])


def close_log_files(started: StartedProcess) -> None:
    for handle in (started.stdout_file, started.stderr_file):
        try:
            handle.close()
        except Exception:
            pass


def terminate_process_tree(started: StartedProcess) -> None:
    process = started.process
    if process.poll() is not None:
        close_log_files(started)
        return

    print(f"[stop] Stopping {started.label} PID {process.pid}")
    if is_windows():
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    else:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except Exception:
            process.terminate()

    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
    close_log_files(started)


def shutdown_started_processes() -> None:
    for started in reversed(STARTED_PROCESSES):
        terminate_process_tree(started)


def ensure_file_exists(path: Path, label: str) -> None:
    if not path.exists():
        raise RuntimeError(f"Missing {label}: {path}")


def check_project_layout(project_root: Path) -> None:
    ensure_file_exists(project_root / "apps" / "api", "apps/api")
    ensure_file_exists(project_root / "apps" / "api" / "app" / "main.py", "FastAPI app.main")
    ensure_file_exists(project_root / "apps" / "api" / "app" / "api" / "v1" / "router.py", "FastAPI API v1 router")
    ensure_file_exists(project_root / "apps" / "api" / "requirements.txt", "backend requirements.txt")
    ensure_file_exists(project_root / "apps" / "web", "apps/web")
    ensure_file_exists(project_root / "apps" / "web" / "package.json", "web package.json")
    ensure_file_exists(project_root / "packages" / "api-client" / "src" / "index.ts", "generated API client package")
    ensure_file_exists(project_root / "database" / "neo4j" / "migrations", "Neo4j migrations directory")
    ensure_file_exists(project_root / "package.json", "root package.json")


def copy_if_missing(source: Path, target: Path, label: str) -> bool:
    if target.exists():
        print(f"[ok] {label} exists: {target}")
        return False
    if not source.exists():
        raise RuntimeError(f"Cannot create {target}; missing example file: {source}")
    shutil.copyfile(source, target)
    print(f"[created] {target} from {source}")
    return True


def ensure_backend_env(project_root: Path, check_only: bool) -> None:
    env_path = project_root / "apps" / "api" / ".env"
    example_path = project_root / "apps" / "api" / ".env.example"
    if check_only:
        print(f"[check] apps/api/.env exists: {env_path.exists()}")
        return

    created = copy_if_missing(example_path, env_path, "backend env")
    if created:
        print("[warn] Created apps/api/.env from example. Fill NEO4J_PASSWORD if it is not already valid.")


def ensure_frontend_env(project_root: Path, api_port: int, check_only: bool) -> None:
    env_path = project_root / "apps" / "web" / ".env.local"
    example_path = project_root / "apps" / "web" / ".env.example"
    if check_only:
        print(f"[check] apps/web/.env.local exists: {env_path.exists()}")
        return

    if env_path.exists():
        print(f"[ok] frontend env exists: {env_path}")
        return

    if example_path.exists():
        shutil.copyfile(example_path, env_path)
        print(f"[created] {env_path} from {example_path}")
    else:
        env_path.write_text(f"NEXT_PUBLIC_API_BASE_URL=http://{HOST}:{api_port}\n", encoding="utf-8")
        print(f"[created] {env_path} with NEXT_PUBLIC_API_BASE_URL")


def check_neo4j_port(neo4j_bolt_port: int, check_only: bool) -> bool:
    if is_port_open(HOST, neo4j_bolt_port):
        print(f"[ok] Neo4j Bolt looks available on {HOST}:{neo4j_bolt_port}")
        return True

    print(f"[warn] Neo4j Bolt does not respond on {HOST}:{neo4j_bolt_port}. Start Neo4j before the backend.")
    if not check_only:
        raise RuntimeError("Neo4j Bolt is not available; stopping normal startup.")
    return False


def python_for_venv(api_dir: Path) -> Path:
    if is_windows():
        return api_dir / ".venv" / "Scripts" / "python.exe"
    return api_dir / ".venv" / "bin" / "python"


def create_venv(api_dir: Path) -> None:
    py_launcher = shutil.which("py") if is_windows() else None
    python_cmd = [py_launcher, "-m", "venv", ".venv"] if py_launcher else [sys.executable, "-m", "venv", ".venv"]
    run_command(python_cmd, cwd=api_dir)


def check_python_venv(project_root: Path, install: bool, no_install: bool, check_only: bool) -> Path:
    api_dir = project_root / "apps" / "api"
    venv_dir = api_dir / ".venv"
    venv_python = python_for_venv(api_dir)

    if check_only:
        print(f"[check] backend .venv exists: {venv_dir.exists()}")
        print(f"[check] backend venv python exists: {venv_python.exists()}")
        return venv_python

    if not venv_dir.exists():
        print("[setup] Creating backend virtual environment.")
        create_venv(api_dir)
        if not no_install:
            run_command([str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"], cwd=api_dir)
    elif install and not no_install:
        run_command([str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"], cwd=api_dir)
    else:
        print(f"[ok] backend virtual environment exists: {venv_dir}")

    if not venv_python.exists():
        raise RuntimeError(f"Backend venv Python not found: {venv_python}")
    return venv_python


def backend_health_url(api_port: int) -> str:
    return f"http://{HOST}:{api_port}{API_PREFIX}/health"


def backend_health_urls(api_port: int) -> tuple[str, ...]:
    return (
        backend_health_url(api_port),
        f"http://{HOST}:{api_port}/api/health",
    )


def start_backend_if_needed(project_root: Path, venv_python: Path, api_port: int) -> None:
    urls = backend_health_urls(api_port)
    if is_port_open(HOST, api_port):
        if wait_for_any_url(urls, 8, "backend"):
            print(f"[ok] backend already running on port {api_port}")
            return
        raise RuntimeError(
            f"Port {api_port} is busy, but it does not look like this project's backend. "
            f"Try --api-port another_port or stop the conflicting process."
        )

    api_dir = project_root / "apps" / "api"
    started = start_process(
        [str(venv_python), "-m", "uvicorn", "app.main:app", "--reload", "--port", str(api_port)],
        cwd=api_dir,
        label="backend",
    )
    if not wait_for_any_url(urls, 60, "backend"):
        print("[backend stdout]")
        print(tail_file(started.stdout_path))
        print("[backend stderr]")
        print(tail_file(started.stderr_path))
        raise RuntimeError("Backend did not become healthy.")


def require_npm() -> str:
    npm = shutil.which("npm")
    if not npm:
        raise RuntimeError("npm was not found on PATH.")
    return npm


def generate_openapi_client(project_root: Path, api_port: int, skip_openapi: bool) -> None:
    if skip_openapi:
        print("[skip] OpenAPI client generation skipped.")
        return

    npm = require_npm()
    if api_port == 8000:
        run_command([npm, "run", "generate:api-client"], cwd=project_root)
        return

    print("[warn] Root npm script targets port 8000; using npm exec for the custom API port.")
    run_command(
        [
            npm,
            "exec",
            "openapi-typescript",
            "--",
            f"http://{HOST}:{api_port}/openapi.json",
            "-o",
            "packages/api-client/src/schema.d.ts",
        ],
        cwd=project_root,
    )


def ensure_node_modules(project_root: Path, install: bool, no_install: bool, check_only: bool) -> None:
    node_modules = project_root / "node_modules"
    if check_only:
        print(f"[check] root node_modules exists: {node_modules.exists()}")
        return

    npm = require_npm()
    if install or (not node_modules.exists() and not no_install):
        run_command([npm, "install"], cwd=project_root)
    elif no_install:
        print("[skip] npm install skipped by --no-install.")
    else:
        print(f"[ok] root node_modules exists: {node_modules}")


def frontend_url(web_port: int) -> str:
    return f"http://{HOST}:{web_port}"


def start_frontend_if_needed(project_root: Path, api_port: int, web_port: int) -> None:
    url = frontend_url(web_port)
    if is_port_open(HOST, web_port):
        if wait_for_url(url, 8, "frontend"):
            print(f"[ok] frontend already running on port {web_port}")
            return
        raise RuntimeError(
            f"Port {web_port} is busy, but the frontend does not respond. "
            f"Try --web-port another_port or stop the conflicting process."
        )

    npm = require_npm()
    env = os.environ.copy()
    env["PORT"] = str(web_port)
    env["NEXT_PUBLIC_API_BASE_URL"] = f"http://{HOST}:{api_port}"
    started = start_process([npm, "run", "dev:web"], cwd=project_root, label="frontend", env=env)
    if not wait_for_url(url, 90, "frontend"):
        print("[frontend stdout]")
        print(tail_file(started.stdout_path))
        print("[frontend stderr]")
        print(tail_file(started.stderr_path))
        raise RuntimeError("Frontend did not become available.")


def print_summary(api_port: int, web_port: int) -> None:
    print("")
    print("Services are ready:")
    print(f"  Web app:    http://{HOST}:{web_port}")
    print(f"  Backend:    http://{HOST}:{api_port}")
    print(f"  API docs:   http://{HOST}:{api_port}/docs")
    print(f"  OpenAPI:    http://{HOST}:{api_port}/openapi.json")
    if STARTED_PROCESSES:
        print("")
        print("Processes started by this script:")
        for started in STARTED_PROCESSES:
            print(f"  {started.label}: PID {started.process.pid}")
    else:
        print("")
        print("No new processes were started; existing services are being used.")
    print("")
    print("Press Ctrl+C to stop processes started by this script.")


def check_only(project_root: Path, args: argparse.Namespace) -> int:
    ok = True
    try:
        check_project_layout(project_root)
        print("[ok] project layout looks complete")
    except RuntimeError as exc:
        ok = False
        print(f"[error] {exc}")

    ensure_backend_env(project_root, check_only=True)
    ensure_frontend_env(project_root, args.api_port, check_only=True)
    check_python_venv(project_root, install=False, no_install=True, check_only=True)
    ensure_node_modules(project_root, install=False, no_install=True, check_only=True)

    ok = check_neo4j_port(args.neo4j_bolt_port, check_only=True) and ok

    backend_results = [
        (url, *http_get(url, timeout_seconds=3)[:2])
        for url in backend_health_urls(args.api_port)
    ]
    backend_ok = any(result[1] for result in backend_results)
    for url, url_ok, status in backend_results:
        print(f"[check] backend health {url}: ok={url_ok}, status={status}")
    ok = backend_ok and ok

    frontend_ok, frontend_status, _ = http_get(frontend_url(args.web_port), timeout_seconds=3)
    print(f"[check] frontend: ok={frontend_ok}, status={frontend_status}")
    ok = frontend_ok and ok

    return 0 if ok else 1


def wait_until_interrupted() -> None:
    while True:
        time.sleep(3600)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start local Neo4j Web App development services.")
    parser.add_argument("--api-port", type=int, default=8000, help="FastAPI port, default: 8000")
    parser.add_argument("--web-port", type=int, default=3000, help="Next.js port, default: 3000")
    parser.add_argument("--neo4j-bolt-port", type=int, default=7687, help="Neo4j Bolt port, default: 7687")
    parser.add_argument("--skip-openapi", action="store_true", help="Skip OpenAPI client generation")
    parser.add_argument("--check-only", action="store_true", help="Only check service state; do not start or modify anything")

    install_group = parser.add_mutually_exclusive_group()
    install_group.add_argument("--install", action="store_true", help="Force dependency installation")
    install_group.add_argument("--no-install", action="store_true", help="Skip pip install and npm install")

    browser_group = parser.add_mutually_exclusive_group()
    browser_group.add_argument("--open-browser", action="store_true", help="Open the web app after startup")
    browser_group.add_argument("--no-browser", action="store_true", help="Do not open the browser")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = find_project_root()
    print(f"[root] {project_root}")

    if args.check_only:
        return check_only(project_root, args)

    try:
        check_project_layout(project_root)
        ensure_backend_env(project_root, check_only=False)
        ensure_frontend_env(project_root, args.api_port, check_only=False)
        check_neo4j_port(args.neo4j_bolt_port, check_only=False)

        venv_python = check_python_venv(
            project_root,
            install=args.install,
            no_install=args.no_install,
            check_only=False,
        )
        start_backend_if_needed(project_root, venv_python, args.api_port)
        generate_openapi_client(project_root, args.api_port, args.skip_openapi)

        ensure_node_modules(project_root, install=args.install, no_install=args.no_install, check_only=False)
        start_frontend_if_needed(project_root, args.api_port, args.web_port)

        print_summary(args.api_port, args.web_port)
        if args.open_browser:
            webbrowser.open(frontend_url(args.web_port))
        wait_until_interrupted()
    except KeyboardInterrupt:
        print("")
        print("[interrupt] Ctrl+C received.")
    except Exception as exc:  # noqa: BLE001 - top-level user-facing diagnostics
        print(f"[error] {exc}", file=sys.stderr)
        shutdown_started_processes()
        return 1
    finally:
        shutdown_started_processes()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
