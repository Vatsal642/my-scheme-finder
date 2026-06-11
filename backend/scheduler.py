from apscheduler.schedulers.background import BackgroundScheduler
from refresh import run_refresh

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(
        func=run_refresh,
        trigger="cron",
        day_of_week="sun",
        hour=2,
        minute=0,
        id="weekly_refresh"
    )
    scheduler.start()
    print("Scheduler started — weekly refresh every Sunday 2am IST")
    return scheduler
