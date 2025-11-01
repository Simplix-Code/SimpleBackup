import json
from .config import load_config, save_config

def create_job(name, time_str, duration):
    cfg, _ = load_config()
    jobs = cfg.setdefault("jobs", [])
    if any(j["name"] == name for j in jobs):
        raise SystemExit(f"Job {name} existiert schon.")
    jobs.append({
        "name": name,
        "time": time_str,
        "cycle": duration,
        "sources": []
    })
    save_config(cfg)
    print(f"[OK] Job {name} angelegt.")

def add_source(jobname, src_path, excludes_str="-"):
    cfg, _ = load_config()
    jobs = cfg.get("jobs", [])
    job = next((j for j in jobs if j["name"] == jobname), None)
    if not job:
        raise SystemExit(f"Job {jobname} nicht gefunden.")
    if "sources" not in job:
        job["sources"] = []
    excludes = []
    if excludes_str and excludes_str not in ("-", "none", "null"):
        excludes = [x.strip() for x in excludes_str.split(",") if x.strip()]
    job["sources"].append({"path": src_path, "exclude": excludes})
    save_config(cfg)
    print(f"[OK] Source zu {jobname} hinzugefügt.")

def show(jobname=None):
    cfg, _ = load_config()
    if not jobname:
        print(json.dumps(cfg, indent=2))
        return
    job = next((j for j in cfg.get("jobs", []) if j["name"] == jobname), None)
    if not job:
        raise SystemExit(f"Job {jobname} nicht gefunden.")
    print(json.dumps(job, indent=2))

def delete_job(jobname):
    cfg, _ = load_config()
    jobs = cfg.get("jobs", [])
    new_jobs = [j for j in jobs if j["name"] != jobname]
    if len(new_jobs) == len(jobs):
        raise SystemExit(f"Job {jobname} nicht gefunden.")
    cfg["jobs"] = new_jobs
    save_config(cfg)
    print(f"[OK] Job {jobname} gelöscht.")

def remove_source(jobname, source_path):
    cfg, _ = load_config()
    jobs = cfg.get("jobs", [])
    job = next((j for j in jobs if j["name"] == jobname), None)
    if not job:
        raise SystemExit(f"Job '{jobname}' not found.")

    sources = job.get("sources", [])
    new_sources = [s for s in sources if s["path"] != source_path]
    if len(new_sources) == len(sources):
        print(f"[WARN] Source '{source_path}' not found in job '{jobname}'.")
        return

    job["sources"] = new_sources
    save_config(cfg)
    print(f"[OK] Source '{source_path}' removed from job '{jobname}'.")

def edit_job(jobname, time_str=None, duration=None):
    cfg, _ = load_config()
    jobs = cfg.get("jobs", [])
    job = next((j for j in jobs if j["name"] == jobname), None)
    if not job:
        raise SystemExit(f"Job {jobname} nicht gefunden.")

    old_time = job.get("time", "-")
    old_cycle = job.get("cycle", "-")

    if time_str:
        job["time"] = time_str
    if duration:
        job["cycle"] = duration

    save_config(cfg)
    print(f"[OK] Job {jobname} aktualisiert.")
    print(f"  Zeit: {old_time} → {job['time']}")
    print(f"  Dauer: {old_cycle} → {job['cycle']}")