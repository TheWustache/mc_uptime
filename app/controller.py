import pexpect
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

path = '/Users/leo/Projects/minecraft_server/'

class Controller:
    def __init__(self, scheduler):
        self.online = False
        self.sched = scheduler

    def online(self):
        return online

    def start(self):
        self.mc = pexpect.spawn('java -Xmx1024M -Xms1024M -jar minecraft_server.1.12.2.jar nogui', cwd=path)
        self.mc.expect('.*Done.*')
        print('Server started.')
        self.online = True

    def stop(self):
        self.online = False
        self.mc.sendline('stop')
        self.mc.expect('.*Saving chunks.*')
        self.mc.terminate(force=True)
        print('Server stopped.')

    def run(self, duration):
        # TODO: add more signals
        self.start()
        # self.sched.add_job(self.mc.sendline, args=['§d§lServer §d§lclosing §d§lin §c§l1 §c§lhour.'], 'date', run_date=datetime.today()+timedelta(hours=duration/2-1))
        # self.sched.add_job(self.mc.sendline, args=['§d§lServer §d§lclosing §d§lin §c§l10 §c§lminutes.'], 'date', run_date=datetime.today()+timedelta(hours=duration/2-1, minutes=50))
        # self.sched.add_job(self.mc.sendline, args=['§d§lServer §d§lclosing §d§lin §c§l10 §c§lseconds.'], 'date', run_date=datetime.today()+timedelta(hours=duration/2-1, minutes=50, seconds=10))
        # self.sched.add_job(self.stop(), 'date', run_date=datetime.today()+timedelta(hours=duration/2))
