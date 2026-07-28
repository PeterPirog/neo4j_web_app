"""Safely stop local development services for this project.

The script stops only FastAPI/Uvicorn and Next.js processes that look related
to this repository. It never stops Neo4j and never talks to the database.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import signal
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


HOST = "127.0.0.1"
PROJECT_RELATED_PORT_OWNER_TOKENS = (
    "neo4j_web_app",
    "apps/api",
    "app.main",
    "uvicorn",
    ".venv",
    "fastapi",
)


def print_usage_banner() -> None:
    print("")
    print("Neo4j Web App - dev_stop.py")
    print("Stops local backend/frontend development services.")
    print("Neo4j is never stopped by this script.")
    print("")
    print("Usage:")
    print("  python scripts/dev_stop.py")
    print("      Ask before stopping detected backend/frontend services.")
    print("      If a process owns API/Web port but command line is unavailable,")
    print("      it is shown as an unconfirmed candidate.")
    print("")
    print("  python scripts/dev_stop.py --dry-run")
    print("      Show what would be stopped.")
    print("")
    print("  python scripts/dev_stop.py --check-only")
    print("      Check ports and candidates only.")
    print("")
    print("  python scripts/dev_stop.py --yes")
    print("      Stop detected API/Web port owners without asking.")
    print("      Use only after reviewing candidates with --dry-run.")
    print("")


@dataclass(frozen=True)
class ProcessInfo:
    pid: int
    ppid: int | None
    name: str
    command_line: str


@dataclass(frozen=True)
class StopCandidate:
    service: str
    process: ProcessInfo
    reason: str
    project_confirmed: bool
    listen_port: int | None = None


def find_project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def is_windows() -> bool:
    return platform.system().lower() == "windows"


def normalize(value: str) -> str:
    return value.replace("\\", "/").lower()


def is_port_open(host: str, port: int, timeout_seconds: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout_seconds):
            return True
    except OSError:
        return False


def run_capture(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def list_windows_processes() -> list[ProcessInfo]:
    powershell = "powershell"
    command = [
        powershell,
        "-NoProfile",
        "-Command",
        (
            "Get-CimInstance Win32_Process | "
            "Select-Object ProcessId,ParentProcessId,Name,CommandLine | "
            "ConvertTo-Json -Compress"
        ),
    ]
    completed = run_capture(command)
    if completed.returncode != 0 or not completed.stdout.strip():
        raise RuntimeError(f"Failed to list Windows processes: {completed.stderr.strip()}")

    data = json.loads(completed.stdout)
    if isinstance(data, dict):
        data = [data]

    processes: list[ProcessInfo] = []
    for item in data:
        command_line = item.get("CommandLine") or ""
        processes.append(
            ProcessInfo(
                pid=int(item["ProcessId"]),
                ppid=int(item["ParentProcessId"]) if item.get("ParentProcessId") is not None else None,
                name=item.get("Name") or "",
                command_line=command_line,
            )
        )
    return processes


def list_posix_processes() -> list[ProcessInfo]:
    completed = run_capture(["ps", "-eo", "pid=,ppid=,comm=,args="])
    if completed.returncode != 0:
        raise RuntimeError(f"Failed to list processes: {completed.stderr.strip()}")

    processes: list[ProcessInfo] = []
    for line in completed.stdout.splitlines():
        parts = line.strip().split(None, 3)
        if len(parts) < 4:
            continue
        pid, ppid, name, command_line = parts
        processes.append(ProcessInfo(int(pid), int(ppid), name, command_line))
    return processes


def list_processes() -> list[ProcessInfo]:
    if is_windows():
        return list_windows_processes()
    return list_posix_processes()


def get_windows_port_pids(port: int) -> set[int]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        (
            f"Get-NetTCPConnection -LocalPort {port} -State Listen -ErrorAction SilentlyContinue | "
            "Select-Object -ExpandProperty OwningProcess | Sort-Object -Unique | ConvertTo-Json -Compress"
        ),
    ]
    completed = run_capture(command)
    if completed.returncode != 0 or not completed.stdout.strip():
        return set()
    data = json.loads(completed.stdout)
    if isinstance(data, int):
        return {data}
    if isinstance(data, list):
        return {int(item) for item in data}
    return set()


def get_posix_port_pids(port: int) -> set[int]:
    if not shutil_which("lsof"):
        return set()
    completed = run_capture(["lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN", "-t"])
    if completed.returncode != 0:
        return set()
    return {int(line.strip()) for line in completed.stdout.splitlines() if line.strip().isdigit()}


def get_port_pids(port: int) -> set[int]:
    if is_windows():
        return get_windows_port_pids(port)
    return get_posix_port_pids(port)


def get_windows_process_info_by_pid(pid: int) -> ProcessInfo:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        (
            f"$p = Get-CimInstance Win32_Process -Filter \"ProcessId = {pid}\"; "
            "$result = if ($null -eq $p) { "
            f"[pscustomobject]@{{ProcessId={pid};ParentProcessId=$null;Name='<unavailable>';CommandLine='<unavailable>'}} "
            "} else { "
            "$p | Select-Object ProcessId,ParentProcessId,Name,CommandLine "
            "}; $result | ConvertTo-Json -Compress"
        ),
    ]
    completed = run_capture(command)
    if completed.returncode != 0 or not completed.stdout.strip():
        return ProcessInfo(pid, None, "<unavailable>", "<unavailable>")

    try:
        data = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return ProcessInfo(pid, None, "<unavailable>", "<unavailable>")

    return ProcessInfo(
        pid=int(data.get("ProcessId") or pid),
        ppid=int(data["ParentProcessId"]) if data.get("ParentProcessId") is not None else None,
        name=data.get("Name") or "<unavailable>",
        command_line=data.get("CommandLine") or "<unavailable>",
    )


def get_process_info_by_pid(processes: list[ProcessInfo], pid: int) -> ProcessInfo:
    for process in processes:
        if process.pid == pid:
            return process
    if is_windows():
        return get_windows_process_info_by_pid(pid)
    return ProcessInfo(pid, None, "<unavailable>", "<unavailable>")


def get_processes_listening_on_port(port: int) -> list[ProcessInfo]:
    pids = sorted(get_port_pids(port))
    if not pids:
        return []

    try:
        processes = list_processes()
    except RuntimeError:
        processes = []

    return [get_process_info_by_pid(processes, pid) for pid in pids]


def has_project_related_port_owner_command(process: ProcessInfo) -> bool:
    command_line = normalize(process.command_line)
    return any(token in command_line for token in PROJECT_RELATED_PORT_OWNER_TOKENS)


def shutil_which(command: str) -> str | None:
    for path in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(path) / command
        if candidate.exists():
            return str(candidate)
    return None


def command_has_port(command_line: str, port: int) -> bool:
    tokens = command_line.replace("=", " ").split()
    return str(port) in tokens


def command_mentions_project(command_line: str, project_root: Path) -> bool:
    cmd = normalize(command_line)
    root = normalize(str(project_root))
    api = normalize(str(project_root / "apps" / "api"))
    web = normalize(str(project_root / "apps" / "web"))
    return root in cmd or api in cmd or web in cmd


def add_port_owner_candidate(
    candidates: dict[int, StopCandidate],
    service: str,
    port: int,
    project_root: Path,
    stop_port_owners: bool,
) -> None:
    port_label = "API" if service == "backend" else "web"
    for process in get_processes_listening_on_port(port):
        if process.pid in candidates:
            continue

        project_related = has_project_related_port_owner_command(process) or command_mentions_project(
            process.command_line,
            project_root,
        )
        command_unavailable = process.command_line.strip().lower() in {"", "<unavailable>", "unavailable"}
        if project_related:
            reason = f"process listening on {port_label} port with project-related command line"
            candidates[process.pid] = StopCandidate(service, process, reason, True, port)
            continue

        if command_unavailable:
            reason = f"process listening on {port_label} port {port} with unavailable command line"
            candidates[process.pid] = StopCandidate(service, process, reason, False, port)
            continue

        reason = f"process listening on {port_label} port {port}"
        if stop_port_owners:
            reason = f"{reason} included by --stop-port-owners"
        candidates[process.pid] = StopCandidate(service, process, reason, False, port)


def is_backend_process(process: ProcessInfo, project_root: Path, api_port: int, port_pids: set[int]) -> tuple[bool, str, bool]:
    cmd = process.command_line
    cmd_lower = cmd.lower()
    has_backend_tokens = "uvicorn" in cmd_lower and "app.main:app" in cmd_lower
    has_port = command_has_port(cmd, api_port) or process.pid in port_pids
    mentions_project = command_mentions_project(cmd, project_root) or "apps/api" in normalize(cmd)

    if has_backend_tokens and has_port and mentions_project:
        return True, "uvicorn app.main:app for this project", True
    if has_backend_tokens and has_port:
        return True, "uvicorn app.main:app on the API port, project path not confirmed", False
    if has_backend_tokens and mentions_project:
        return True, "uvicorn app.main:app for this project on another visible port", True
    return False, "", False


def is_frontend_process(process: ProcessInfo, project_root: Path, web_port: int, port_pids: set[int]) -> tuple[bool, str, bool]:
    cmd = process.command_line
    cmd_lower = cmd.lower()
    cmd_norm = normalize(cmd)
    mentions_project = command_mentions_project(cmd, project_root)
    has_port = command_has_port(cmd, web_port) or process.pid in port_pids

    next_project = "next" in cmd_lower and mentions_project and ("node_modules/next" in cmd_norm or has_port)
    npm_dev_web = "npm" in cmd_lower and "dev:web" in cmd_lower and (mentions_project or has_port)
    next_dev = "next" in cmd_lower and "dev" in cmd_lower and (mentions_project or has_port)

    if next_project:
        return True, "Next.js server process for this project", True
    if npm_dev_web:
        return True, "npm run dev:web process for this project", mentions_project
    if next_dev and mentions_project:
        return True, "next dev process for this project", True
    if ("next" in cmd_lower or "npm" in cmd_lower) and has_port:
        return True, "frontend-looking process on the web port, project path not confirmed", False
    return False, "", False


def collect_candidates(
    project_root: Path,
    api_port: int,
    web_port: int,
    include_existing: bool,
    stop_port_owners: bool,
) -> list[StopCandidate]:
    processes = list_processes()
    api_port_pids = get_port_pids(api_port)
    web_port_pids = get_port_pids(web_port)
    candidates: dict[int, StopCandidate] = {}

    for process in processes:
        backend, reason, confirmed = is_backend_process(process, project_root, api_port, api_port_pids)
        if backend and (confirmed or include_existing):
            candidates[process.pid] = StopCandidate("backend", process, reason, confirmed, api_port)

        frontend, reason, confirmed = is_frontend_process(process, project_root, web_port, web_port_pids)
        if frontend and (confirmed or include_existing):
            candidates[process.pid] = StopCandidate("frontend", process, reason, confirmed, web_port)

    add_port_owner_candidate(candidates, "backend", api_port, project_root, stop_port_owners)
    add_port_owner_candidate(candidates, "frontend", web_port, project_root, stop_port_owners)

    return sorted(candidates.values(), key=lambda item: (item.service, item.process.pid))


def print_port_owner_details(label: str, port: int) -> None:
    owners = get_processes_listening_on_port(port)
    if not owners:
        print(f"[warn] {label} port {port} is open, but no owning process details were returned.")
        return

    print(f"[diagnostic] Processes listening on {label} port {port}:")
    for owner in owners:
        print(f"  PID: {owner.pid}")
        print(f"  Name: {owner.name}")
        print(f"  CommandLine: {owner.command_line}")


def print_port_status(project_root: Path, api_port: int, web_port: int, candidates: list[StopCandidate]) -> None:
    by_service = {candidate.service for candidate in candidates}

    api_open = is_port_open(HOST, api_port)
    web_open = is_port_open(HOST, web_port)
    print(f"[check] API port {api_port} open: {api_open}")
    print(f"[check] Web port {web_port} open: {web_open}")

    if api_open and "backend" not in by_service:
        print(
            f"[warn] Port {api_port} is open, but no matching project backend process was found. "
            "The process was not stopped automatically because its project relationship was not confirmed."
        )
        print_port_owner_details("API", api_port)
        print("[hint] Use --stop-port-owners only after reviewing the port owner above.")
    if web_open and "frontend" not in by_service:
        print(
            f"[warn] Port {web_port} is open, but no matching project frontend process was found. "
            "The process was not stopped automatically because its project relationship was not confirmed."
        )
        print_port_owner_details("Web", web_port)
        print("[hint] Use --stop-port-owners only after reviewing the port owner above.")

    # Neo4j is intentionally not stopped by this script. dev_start.py only checks Neo4j availability and does not start the database.
    print("[safe] Neo4j ports 7474 and 7687 are intentionally ignored.")


def print_candidates(candidates: list[StopCandidate]) -> None:
    if not candidates:
        print("[ok] No stop candidates found.")
        return

    print("")
    print("Stop candidates:")
    for candidate in candidates:
        flag = "project-confirmed" if candidate.project_confirmed else "unconfirmed-project"
        print(f"- service: {candidate.service}")
        print(f"  pid: {candidate.process.pid}")
        print(f"  name: {candidate.process.name}")
        print(f"  match: {flag}; {candidate.reason}")
        print(f"  command: {candidate.process.command_line}")


def format_candidate_summary(candidates: list[StopCandidate], max_items: int = 10) -> str:
    lines = []
    for candidate in candidates[:max_items]:
        lines.append(f"{candidate.service} PID {candidate.process.pid} {candidate.process.name}")

    remaining = len(candidates) - max_items
    if remaining > 0:
        lines.append(f"... and {remaining} more")

    return "\n".join(lines)


def unconfirmed_candidate_count(candidates: list[StopCandidate]) -> int:
    return sum(1 for candidate in candidates if not candidate.project_confirmed)


def confirm_stop_console(candidates: list[StopCandidate]) -> bool:
    print("")
    print("This will stop the listed FastAPI/Uvicorn backend and Next.js frontend processes.")
    print("Neo4j will NOT be stopped.")
    unconfirmed_count = unconfirmed_candidate_count(candidates)
    if unconfirmed_count > 0:
        print(f"Warning: {unconfirmed_count} candidate(s) are unconfirmed port owners.")
        print("They are included because they own the configured API/Web port.")
    answer = input("Stop all listed backend/frontend services? [y/N]: ").strip().lower()
    return answer in {"y", "yes", "t", "tak"}


def confirm_stop_gui(candidates: list[StopCandidate]) -> bool:
    root = None
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        unconfirmed_count = unconfirmed_candidate_count(candidates)
        unconfirmed_message = ""
        if unconfirmed_count > 0:
            unconfirmed_message = (
                f"Warning: {unconfirmed_count} candidate(s) are unconfirmed because Windows did not expose "
                "their command line.\n"
                "They are included because they own the configured API/Web port.\n\n"
            )

        message = (
            "Stop local development services for this project?\n\n"
            "This will stop only:\n"
            "- FastAPI / Uvicorn backend\n"
            "- Next.js frontend\n\n"
            f"{unconfirmed_message}"
            "Neo4j will NOT be stopped.\n"
            "No Cypher will be executed.\n"
            "No database data will be deleted.\n\n"
            "Detected candidates:\n"
            f"{format_candidate_summary(candidates)}"
        )

        result = messagebox.askyesno("Stop Neo4j Web App services?", message, parent=root)
        return bool(result)
    except Exception:
        print("[abort] Non-interactive runner detected, but GUI confirmation could not be opened.")
        print("[hint] Review candidates with: python scripts/dev_stop.py --dry-run")
        print("[hint] Stop without prompt with: python scripts/dev_stop.py --yes")
        return False
    finally:
        if root is not None:
            try:
                root.destroy()
            except Exception:
                pass


def confirm_stop(candidates: list[StopCandidate], yes: bool) -> bool:
    if not candidates:
        return False
    if yes:
        return True
    if sys.stdin.isatty():
        return confirm_stop_console(candidates)
    return confirm_stop_gui(candidates)


def is_windows_process_running(pid: int) -> bool:
    completed = run_capture(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"if (Get-Process -Id {pid} -ErrorAction SilentlyContinue) {{ exit 0 }} else {{ exit 1 }}",
        ]
    )
    return completed.returncode == 0


def is_running(pid: int) -> bool:
    if is_windows():
        return is_windows_process_running(pid)
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def is_pid_listening_on_port(pid: int, port: int | None) -> bool:
    if port is None:
        return False
    return pid in get_port_pids(port)


def print_completed_output(completed: subprocess.CompletedProcess[str]) -> None:
    if completed.stdout.strip():
        print(completed.stdout.strip())
    if completed.stderr.strip():
        print(completed.stderr.strip())


def stop_windows_process(pid: int, force_allowed: bool, listen_port: int | None = None) -> bool:
    if not is_running(pid) and not is_pid_listening_on_port(pid, listen_port):
        return True
    if not is_running(pid) and is_pid_listening_on_port(pid, listen_port):
        print(
            f"[warn] PID {pid} is not visible through Get-Process, "
            f"but it still owns port {listen_port}; attempting taskkill by PID."
        )

    gentle = subprocess.run(
        ["taskkill", "/PID", str(pid), "/T"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    print_completed_output(gentle)
    time.sleep(2)

    if not is_running(pid) and not is_pid_listening_on_port(pid, listen_port):
        return True

    if not force_allowed:
        return False

    forced = subprocess.run(
        ["taskkill", "/PID", str(pid), "/T", "/F"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    print_completed_output(forced)
    time.sleep(2)

    if is_running(pid) or is_pid_listening_on_port(pid, listen_port):
        fallback = run_capture(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                f"Stop-Process -Id {pid} -Force -ErrorAction SilentlyContinue",
            ]
        )
        print_completed_output(fallback)
        time.sleep(2)

    stopped = not is_running(pid) and not is_pid_listening_on_port(pid, listen_port)
    if not stopped and listen_port is not None:
        print(
            f"Port {listen_port} is still open after forced taskkill. "
            "Try running PyCharm/PowerShell as Administrator or stop the process manually:"
        )
        print(f"  Get-NetTCPConnection -LocalPort {listen_port} -State Listen")
        print(f"  taskkill /PID {pid} /T /F")
    return stopped


def stop_posix_process(pid: int, force_allowed: bool) -> bool:
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return True
    time.sleep(3)
    if not is_running(pid):
        return True
    if force_allowed:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            return True
        time.sleep(1)
    return not is_running(pid)


def stop_candidates(candidates: list[StopCandidate], force_allowed: bool) -> int:
    failures = 0
    service_order = {"frontend": 0, "backend": 1}
    ordered_candidates = sorted(candidates, key=lambda item: (service_order.get(item.service, 99), item.process.pid))
    for candidate in ordered_candidates:
        pid = candidate.process.pid
        if not is_running(pid) and not is_pid_listening_on_port(pid, candidate.listen_port):
            print(f"[ok] PID {pid} is already stopped")
            continue

        print(f"[stop] {candidate.service} PID {pid}")
        ok = (
            stop_windows_process(pid, force_allowed, candidate.listen_port)
            if is_windows()
            else stop_posix_process(pid, force_allowed)
        )
        if ok:
            print(f"[ok] stopped PID {pid}")
        else:
            print(f"[warn] PID {pid} is still running")
            failures += 1
    return failures


def print_final_port_status(api_port: int, web_port: int) -> None:
    print("")
    print("Final port status:")
    print(f"  API port {api_port} open: {is_port_open(HOST, api_port)}")
    print(f"  Web port {web_port} open: {is_port_open(HOST, web_port)}")
    print("  Neo4j ports 7474 and 7687 were not checked for stopping and were not touched.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Safely stop local Neo4j Web App development services.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/dev_stop.py
      Ask before stopping services. Console y/N or PyCharm Yes/No dialog.

  python scripts/dev_stop.py --check-only
      Check ports and matching processes. Do not stop anything.

  python scripts/dev_stop.py --dry-run
      Show detected backend/frontend processes. Do not stop anything.

  python scripts/dev_stop.py --yes
      Stop detected API/Web port owners without interactive confirmation.
      Use only after reviewing candidates with --dry-run.

  python scripts/dev_stop.py --api-port 8000 --web-port 3000 --dry-run
      Inspect custom ports.

  python scripts/dev_stop.py --stop-port-owners --dry-run
      Include API/web port owners even when their command line is incomplete.

Safety:
  This script does not stop Neo4j.
  This script does not execute Cypher.
  This script does not delete database data.
""",
    )
    parser.add_argument("--api-port", type=int, default=8000, help="FastAPI port, default: 8000")
    parser.add_argument("--web-port", type=int, default=3000, help="Next.js port, default: 3000")
    parser.add_argument("--yes", action="store_true", help="Stop matching processes without interactive confirmation")
    parser.add_argument("--dry-run", action="store_true", help="Only show what would be stopped")
    parser.add_argument(
        "--include-existing",
        action="store_true",
        help="Include matching processes even when the project path is not confirmed",
    )
    parser.add_argument(
        "--stop-port-owners",
        action="store_true",
        help="Include API/web port owners as stop candidates after review; never applies to Neo4j ports",
    )
    parser.add_argument("--check-only", action="store_true", help="Only check ports and candidates; do not stop anything")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = find_project_root()
    print_usage_banner()
    print(f"[root] {project_root}")

    try:
        candidates = collect_candidates(
            project_root,
            args.api_port,
            args.web_port,
            args.include_existing,
            args.stop_port_owners,
        )
    except Exception as exc:  # noqa: BLE001 - top-level diagnostics for local script
        print(f"[error] {exc}", file=sys.stderr)
        return 1

    print_port_status(project_root, args.api_port, args.web_port, candidates)
    print_candidates(candidates)

    if args.check_only:
        print("[check-only] No processes were stopped.")
        return 0

    if args.dry_run:
        print("[dry-run] No processes were stopped.")
        return 0

    if not confirm_stop(candidates, args.yes):
        print("[abort] No processes were stopped.")
        return 0

    failures = stop_candidates(candidates, force_allowed=True)
    print_final_port_status(args.api_port, args.web_port)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
