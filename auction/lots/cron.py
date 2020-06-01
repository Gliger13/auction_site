from django_cron import CronJobBase, Schedule
from lots import check_lots


class StartLots(CronJobBase):
    RUN_EVERY_MINS = 60  # every hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'lots.check_lots'  # a unique code

    def do(self):
        check_lots.check_lots()
