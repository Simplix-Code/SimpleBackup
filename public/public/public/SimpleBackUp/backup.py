import os
import shutil
import time
import threading
from datetime import datetime, timedelta
from .config import load_config, DEFAULT_BACKUP_ROOT

def parse_cycle(cycle: str) -> timedelta:
    s = cycle.strip().upper()
    num = "".join(ch for ch in s if ch.isdigit())
    unit = "".join(ch for ch in s if not ch.isdigit())
    if not num:
        raise ValueError(f"Invalid cycle: {cycle}")
    n = int(num)
    if unit in ("D", "T"):
        return timedelta(days=n)
    if unit == "W":
        return timedelta(weeks=n)
    if unit == "H":
        return timedelta(hours=n)
    raise ValueError(f"Unknown unit in cycle: {cycle}")


def next_run_from_time(timestr: str) -> datetime:
    now = datetime.now()
    h, m = [int(x) for x in timestr.split(":")]
    candidate = now.replace(hour=h, minute=m, second=0, microsecond=0)
    return candidate if candidate > now else candidate + timedelta(days=1)


def copy_with_excludes(src: str, dst: str, excludes: list[str]):
    if not os.path.exists(src):
        print(f"[WARN] source not found: {src}")
        return
    os.makedirs(dst, exist_ok=True)

    if os.path.isfile(src):
        shutil.copy2(src, os.path.join(dst, os.path.basename(src)))
        return

    def ignore_func(dirpath, names):
        return [name for name in names if name in excludes]

    shutil.copytree(src, dst, ignore=ignore_func, dirs_exist_ok=True)


def zip_folder(folder_path: str, zip_path: str):
    base, _ = os.path.splitext(zip_path)
    root_dir = os.path.dirname(folder_path)
    base_dir = os.path.basename(folder_path)
    shutil.make_archive(base, "zip", root_dir=root_dir, base_dir=base_dir)


def job_worker(job: dict, backup_root: str):
    name = job["name"]
    time_str = job.get("time", "03:00")
    cycle = parse_cycle(job.get("cycle", "1D"))

    sources = job.get("sources")
    if not sources:
        sources = [{
            "path": job.get("path"),
            "exclude": job.get("exclude", [])
        }]

    print(f"[{name}] started. first run at {time_str}, every {cycle}.")

    next_run = next_run_from_time(time_str)

    while True:
        wait_sec = (next_run - datetime.now()).total_seconds()
        while wait_sec > 0:
            time.sleep(min(30, wait_sec))
            wait_sec -= 30

        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        run_dir = os.path.join(backup_root, f"{name}-{ts}")
        os.makedirs(run_dir, exist_ok=True)
        print(f"[{name}] backup -> {run_dir}")

        for src in sources:
            src_path = src["path"]
            excl = src.get("exclude", [])
            inner_name = os.path.basename(src_path.rstrip("/")) or "root"
            target = os.path.join(run_dir, inner_name)
            print(f"[{name}]  copying {src_path} -> {target} (exclude={excl})")
            copy_with_excludes(src_path, target, excl)

        zip_path = os.path.join(backup_root, f"{name}-{ts}.zip")
        print(f"[{name}] creating zip {zip_path}")
        zip_folder(run_dir, zip_path)

        shutil.rmtree(run_dir, ignore_errors=True)
        print(f"[{name}] done.")

        next_run = datetime.now() + cycle


def run_daemon():
    cfg, _ = load_config()
    backup_root = cfg.get("backup_root", DEFAULT_BACKUP_ROOT)
    os.makedirs(backup_root, exist_ok=True)
    jobs = cfg.get("jobs", [])
    if not jobs:
        print("no jobs configured")
        return

    for job in jobs:
        t = threading.Thread(target=job_worker, args=(job, backup_root), daemon=True)
        t.start()

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("bye")
