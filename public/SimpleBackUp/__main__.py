import sys
from . import backup
from . import cli
from . import screenctl

def main():
    # kein argument -> daemon direkt (wie früher)
    if len(sys.argv) == 1:
        backup.run_daemon()
        return

    cmd = sys.argv[1].lower()

    # SimpleBackUp run   -> daemon starten (für screen)
    if cmd == "run":
        backup.run_daemon()
        return

    # create job
    if cmd == "create" and len(sys.argv) >= 6 and sys.argv[2].lower() == "job":
        cli.create_job(sys.argv[3], sys.argv[4], sys.argv[5])
        return

    # add source
    if cmd == "add" and len(sys.argv) >= 5 and sys.argv[2].lower() == "source":
        jobname = sys.argv[3]
        src_path = sys.argv[4]
        excludes = sys.argv[5] if len(sys.argv) >= 6 else "-"
        cli.add_source(jobname, src_path, excludes)
        return

    # show
    if cmd == "show":
        jobname = sys.argv[2] if len(sys.argv) >= 3 else None
        cli.show(jobname)
        return

    # delete job
    if cmd == "delete" and len(sys.argv) >= 4 and sys.argv[2].lower() == "job":
        cli.delete_job(sys.argv[3])
        return

    # remove source
    if cmd == "remove" and len(sys.argv) >= 4:
        jobname = sys.argv[2]
        source_path = sys.argv[3]
        cli.remove_source(jobname, source_path)
        return

    # screen stuff
    if cmd == "start":
        screenctl.start()
        return
    if cmd == "stop":
        screenctl.stop()
        return
    if cmd == "restart":
        screenctl.restart()
        return
    
    # edit job
    if cmd == "edit" and len(sys.argv) >= 4 and sys.argv[2].lower() == "job":
        jobname = sys.argv[3]
        time_str = None
        duration = None
        for arg in sys.argv[4:]:
            if arg.startswith("time="):
                time_str = arg.split("=", 1)[1]
            elif arg.startswith("duration="):
                duration = arg.split("=", 1)[1]
        cli.edit_job(jobname, time_str, duration)
        return

    if len(sys.argv) == 1 or sys.argv[1].lower() in ("help", "--help", "-h"):
        print("SimpleBackUp v0.1.3 - Lightweight Backup Daemon\n")
        print("""
        SimpleBackUp - Commands & Usage
        ==================================

        Job Management:
        simplebackup create job <NAME> <TIME> <DURATION>
            Creates a new backup job.
            Example: simplebackup create job Website 03:00 1D

        simplebackup add source <JOBNAME> <PATH> [EXCLUDES]
            Adds a source to a job.
            Example: simplebackup add source Website /var/www "node_modules,.git"

        simplebackup remove source <JOBNAME> <PATH>
            Removes a source for one job.

        simplebackup delete job <NAME>
            Deletes a job completely.

        simplebackup edit job <NAME> [time=HH:MM] [duration=1D]
            Edits the time and/or interval of a job.
            Alternatively:
                simplebackup edit job <NAME> <TIME> [DURATION]
            Example:
                simplebackup edit job Website 22:00 2D

        simplebackup show [JOBNAME]
            Shows all jobs or details for a specific job.

        Backup Control:
        simplebackup start
            Starts the backup service (in a screen session).

        simplebackup stop
            Stops the backup service.

        simplebackup restart
            Restarts the backup service (stop + start).

        General:
        simplebackup help
            Shows this overview.

        Configuration:
        /etc/SimpleBackUp/backup_config.json
            All jobs and sources are stored here.
        """)
        return

    print("Unbekannter Befehl.")
    print("Beispiele:")
    print("  SimpleBackUp create job NAME 03:00 1D")
    print("  SimpleBackUp add source NAME /pfad \"node_modules,.git\"")
    print("  SimpleBackUp show [NAME]")
    print("  SimpleBackUp start|stop|restart")
