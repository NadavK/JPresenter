#!/usr/bin/env python3

# TODO:
# rolling log files
# change this to a service: "service start/restart/stop/info": https://pypi.python.org/pypi/python-daemon/ CONSIDER HOW IT IS AUTOSTARTED, maybe start it from cron?


from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import datetime
import os
import pytz
from subprocess import Popen
import sys
from tendo import singleton as tendo_singleton
from jewish_dates import holidays, jtimes
import logging

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)
# fileHandler = logging.FileHandler('/home/pi/presenter/jscheduler.log')
fileHandler = logging.FileHandler('./log/jscheduler.log')
fileHandler.setLevel(logging.DEBUG)
# logging.basicConfig(filename='/home/pi/presenter/jscheduler.log', level=logging.DEBUG)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.DEBUG)
rootLogger.addHandler(consoleHandler)


PLAYLIST_FILE = '/home/pi/Documents/jpresenter/playlist'
candlelight_delta = 180  # minutes before sunset
presentation_base_path = r'/home/pi/Documents/Presentations'
location = 'Raanana_wiki'


class PlayerData:
    
    def __init__(self, day_part, folders=None):
        self.day_part = day_part
        self.folders = folders

    def __str__(self):
        s = ''
        for (name, val) in vars(self).items():
            if val is not None:
                s += str(name) + ":" + str(val) + ", "
        return s


# Global
data = PlayerData(day_part='None', folders=[])


# Returns the first existing folder, and adds the suffix-folder if it also exists
def find_existing_folders(base_folder, folders, suffix):
    logging.info('find_existing_folders(). base_folder: %s, folders: %s, suffix: %s', base_folder, folders, suffix)
    for folder in folders:
        path = os.path.join(base_folder, folder)
        if os.path.isdir(path):
            suffix_path = os.path.join(base_folder, folder, suffix)
            if os.path.isdir(suffix_path):
                return (path, suffix_path)
            else:
                return (path,)
    else:  # no folders found
        logging.error('find_existing_folders(). Folders not found in path (\'%s\'): %s', base_folder, folders)


# Write to file. The viewer script will pick up the changes
def write_playlist_file(folders, path=None):
    logging.info('Writing playlist file: %s (path=%s)', folders, path)
    with open(PLAYLIST_FILE, "w") as f:
        for folder in folders:
            f.write(folder + "\n")


def set_tv_source():
    def send_cec_command(cec):
        # on and set source to Pi  (where the command is sent from):
        # echo 'as'|cec-client -s
        # on:
        # echo "on 0" | cec-client -s
        # off:
        # echo "standby 0" | cec-client -s
        # Source 1:
        # echo 'tx 8f:82:10:00' | cec-client RPI -s
        cmd = 'echo "%s" | cec-client -s' % cec
        logging.info('CEC command: %s', cmd)
        Popen(cmd, shell=True)

    #now = datetime.datetime.now(pytz.utc)
    now = datetime.datetime.now(pytz.timezone('Asia/Jerusalem'))
    if 'Pesach' in data.folders and 2 <= now.hour < 7:
        send_cec_command('standby 0')
    elif 'Shabbat' in data.folders and now.hour < 7:
        send_cec_command('standby 0')
    elif now.hour < 6:                          # turn off everyday between 24:00 - 06:00
        send_cec_command('standby 0')
    elif 'Shabbat' in data.folders:
        send_cec_command('as')  # Set TV source to this machine (in case TV is displaying another source)
    else:
        send_cec_command('on 0')  # Turn on TV

    # elif data.day_part in ['Erev', 'Morning']:
    #    for file in data.files:
    #        if file == 'Shabbat':
    #            send_cec_command('as')
    #            return
    # elif data.day_part=='Morning':
    #    send_cec_command('on 0')


def play_presentation(just_test=False):
    logging.info('Presentation data: %s', str(data))

    set_tv_source()

    folders = find_existing_folders(presentation_base_path, data.folders, data.day_part)
    if folders:
        # prev play process is closed by the play script
        if just_test:
            logging.info('Presentation final folders: %s (original  folders=%s)', folders, str(data.folders))
        else:
            write_playlist_file(folders, presentation_base_path)
    else:  # no file found
        logging.error('Folders not found in these paths: %s', data.folders)


def midpoint(t1, t2):
    return t1 + ((t2 - t1) / 2)


def set_hebdaily_jobs(scheduler, today=datetime.date.today(), test=False, dont_rerun=False):
    global data

    sunrise, sunset = jtimes.sunrise_sunset(location, today)
    logging.debug('today suntimes: %s, %s', sunrise, sunset)

    now = datetime.datetime.now(pytz.utc)
    tomorrow = today + datetime.timedelta(days=1)
    yesterday = today - datetime.timedelta(days=1)
    today_folders = holidays.get_hags(today)
    tomorrow_folders = holidays.get_hags(tomorrow)
    yesterday_folders = holidays.get_hags(yesterday)
    seven7days_files = holidays.get_hags(today, 3, 0)

    logging.debug('Today: %s', today_folders)
    logging.debug('Tomorrow: %s', tomorrow_folders)
    logging.debug('Yesterday: %s', yesterday_folders)
    if seven7days_files:
        logging.debug('Holiday within 3 days: %s', seven7days_files)
    else:
        logging.debug('No holidays within 3 days')

    if tomorrow_folders and not today_folders:  # If tomorrow is hag, and not today, then start early
        next_heb_day = sunset - datetime.timedelta(minutes=candlelight_delta)
    elif today_folders and not tomorrow_folders:  # now is Motzei hag, so extend by an 1 hour and 15 minutes
        next_heb_day = sunset + datetime.timedelta(minutes=75)
    else:  # nothing, or second-day hag
        next_heb_day = sunset

    logging.debug('next_heb_day: %s', next_heb_day)
    logging.debug('now: %s', now)

    if next_heb_day > now:
        # Run again tomorrow
        logging.debug("Next run time: %s", next_heb_day)
        if scheduler: scheduler.add_job(set_hebdaily_jobs, 'date', run_date=next_heb_day, args=[scheduler, tomorrow])
        # and continue with today...
    elif not dont_rerun:
        # we missed the heb-start time for today, so re-run this func as if it was tomorrow
        logging.debug('We are after new-heb day - run again')
        return set_hebdaily_jobs(scheduler, tomorrow, test=test, dont_rerun=True)

    if seven7days_files:
        today_folders = seven7days_files
    else:
        today_folders = holidays.get_season(today)

    if today_folders:
        today_folders += ['Default', ]  # always add the default folder, in case the holiday is not found e.g. tu-b'shvat

        # Erev
        data = PlayerData(day_part='Erev', folders=today_folders)
        play_presentation(test)  # Play now

        # Morning
        start_time = sunrise
        data = PlayerData(day_part='Morning', folders=today_folders)
        if scheduler: scheduler.add_job(play_presentation, 'date', run_date=start_time)
        logging.debug('Morning: %s', start_time)

        # Afternoon
        start_time = midpoint(sunset, sunrise)
        data = PlayerData(day_part='Afternoon', folders=today_folders)
        if scheduler: scheduler.add_job(play_presentation, 'date', run_date=start_time)
        logging.debug('Afternoon: %s', start_time)
    else:
        folders = ['Default', ]
        if yesterday_folders:  # Yesterday (now) was a holiday, so we are motzei
            data = PlayerData(day_part='Motzei', folders=yesterday_folders)
        else:  # Regular day
            data = PlayerData(day_part='Evening', folders=folders)
        play_presentation(test)  # Play now
        logging.debug('Now: %s', data.folders)

        # Morning
        start_time = sunrise
        data = PlayerData(day_part='Morning', folders=folders)
        if scheduler: scheduler.add_job(play_presentation, 'date', run_date=start_time)
        logging.debug('Morning: %s', start_time)

        # Afternoon
        start_time = midpoint(sunset, sunrise)
        data = PlayerData(day_part='Afternoon', folders=today_folders)
        if scheduler: scheduler.add_job(play_presentation, 'date', run_date=start_time)
        logging.debug('Afternoon: %s', start_time)

    if scheduler:
        scheduler.print_jobs()


def main(argv):
    try:
        # ensure single instance process
        me = tendo_singleton.SingleInstance()

        # set high priority
        # os.nice(-20)
        # os.setpriority(os.PRIO_PROCESS, 0, -20)
        # import psutil
        # p = psutil.Process()
        # p.ionice(0)

        logging.info("Started")

        loop = asyncio.get_event_loop()

        # https://stackoverflow.com/questions/2720319/python-figure-out-local-timezone
        local_tz_str = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo.tzname(datetime.datetime.now())
        logging.info("TZ: " + local_tz_str)
        #scheduler = BackgroundScheduler(timezone=local_tz_str, standalone=False, job_defaults={'misfire_grace_time': 60 * 60}, )
        scheduler = BackgroundScheduler(timezone=None, standalone=False, job_defaults={'misfire_grace_time': 60 * 60}, )
        scheduler.add_job(set_tv_source, 'cron', minute=0)      # Turn the TV on/off, and set the TV source
        scheduler.add_job(set_tv_source, 'cron', minute=30)     # Turn the TV on/off, and set the TV source


        # Daily reset job
        # scheduler.add_job(daily_check, 'cron', hour='3', minute='0', args=[scheduler])
        # scheduler.add_job(set_daily_jobs, 'cron', hour='0', minute='1', args=[scheduler])
        scheduler.start()
        scheduler.print_jobs()

        set_hebdaily_jobs(scheduler)  # check the times for now
        logging.debug('waiting...')

        loop.run_forever()
        loop.close()
        scheduler.shutdown(wait=False)

    except Exception:
        logging.exception('unhandled exception')
    except SystemExit:
        logging.debug('System Exiting')


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except:
        logging.info('main exception caught')
    logging.info('Exiting main')
