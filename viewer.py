#!/usr/bin/env python3

import logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler('./log/viewer.log')
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.DEBUG)
rootLogger.addHandler(consoleHandler)

import datetime
from enum import Enum
import glob
import os
import pi3d
import pytz
from random import seed, randrange
import time

FADE_DURATION = 10
FPS = 30  # TODO: can change fps to 1 when not fading
PLAYLIST_FILE = '/home/pi/Documents/jpresenter/playlist'
SUPPORTED_FILE_TYPES = ['.jpg', '.bmp', '.png']
SLIDE_DURATION = 30 * 60  # Time interval how often to change slides


class FileWatch():
    State = Enum('State', 'ADDED REMOVED MODIFIED NONE')

    def __init__(self, file):
        logging.info('Watching: %s', file)
        self.file = file
        self.timestamp_base = None
        try:
            self.timestamp_base = os.path.getmtime(self.file)
            logging.info('FileWatch timestamp: %s', time.ctime(self.timestamp_base))
        except Exception as e:
            logging.exception('FileWatch init')

    def get_status(self):
        timestamp = None
        try:
            timestamp = os.path.getmtime(self.file)
        except:
            logging.info('FileWatch: file removed')

        if not self.timestamp_base and timestamp:
            res = self.State.ADDED
            logging.info('FileWatch: file created')
        elif self.timestamp_base and not timestamp:
            res = self.State.REMOVED
            logging.info('FileWatch: file deleted')
        elif self.timestamp_base != timestamp:
            res = self.State.MODIFIED
            logging.info('FileWatch: file updated: %s', time.ctime(self.timestamp_base))
        else:
            res = self.State.NONE

        self.timestamp_base = timestamp
        return res


class SlideShow():
    alpha = 0.00
    image_folders = []
    display = pi3d.Display.create(background=(0, 0, 0, 1), frames_per_second=FPS)
    shader = pi3d.Shader('uv_flat')
    slide1 = None
    slide2 = None
    file_watcher = FileWatch(PLAYLIST_FILE)

    def __init__(self):
        seed()
        self.read_playlist_file()
        self.slide1 = self.select_image_file(2.0)

    def read_playlist_file(self):
        self.image_folders = []
        try:
            logging.info('Reading playlist')
            with open(PLAYLIST_FILE) as f:
                lines = f.readlines()
            # remove whitespace characters like `\n` at the end of each line
            self.image_folders = [x.strip() for x in lines]
        except Exception as e:
            logging.exception('Failed read_playlist_file')

    def select_image_file(self, z_order=1.0):
        files = []
        for folder in self.image_folders:
            # make sure path has file wildcard
            if not folder.endswith('*'):
                folder += '*' if folder.endswith('/') else '/*'
            logging.debug('folder: "%s"', folder)
            files += glob.glob(folder)
        if len(files) == 0:
            logging.error('No files found in paths: "%s"', self.image_folders)
            return
        logging.debug('Number of files: "%d"', len(files))
        while True:
            # TODO: ensure its different from prev
            file = files[randrange(len(files))]
            if os.path.splitext(file)[1].lower() not in SUPPORTED_FILE_TYPES:
                logging.error('Unsupported file format: "%s"', file)
            else:
                try:
                    logging.debug('Selected file: "%s"', file)
                    return pi3d.ImageSprite(file, shader=self.shader, w=self.display.width, h=self.display.height, z=z_order)
                    # TODO: Do we need to load image with texture for mipmap?
                except Exception as e:
                    logging.exception('Failed loading image "%s"', file)

    # loads a new image, and starts the fade effect.
    # Should not be used for first image
    def display_new_image(self):
        self.slide2 = self.select_image_file()
        # if we found a file, so start the fade
        if self.slide2: self.alpha = 0.0

    def now_time_slot(self):
        return (time.time() + FADE_DURATION//2 + 2) // SLIDE_DURATION           # Extra 2 seconds to load image

    def show(self):
        # camera = pi3d.Camera(is_3d=False)
        last_slide_time_slot = self.now_time_slot()

        ####################
        # Prepare time text
        CAMERA2D = pi3d.Camera(is_3d=False)
        myfont = pi3d.Font('fonts/ERASDEMI.TTF', codepoints='0123456789 :', color=(200, 200, 200, 255), background_color=(0, 0, 0, 10), shadow=(0, 0, 0, 255), shadow_radius=5)
        myfont.blend = True
        last_text_frame = 0
        time_string = pi3d.String(camera=CAMERA2D, font=myfont, is_3d=False, string='88:88')
        time_string.set_shader(pi3d.Shader("uv_flat"))  # TODO: Consider different shader
        (lt, bm, ft, rt, tp, bk) = time_string.get_bounds()
        xpos = (self.display.width - rt + lt) / 2.0
        ypos = -(self.display.height - tp + bm) / 2.0
        time_string.position(xpos, ypos, 1.0)
        time_string.positionZ(0.0)
        time_string.draw()  # NB has to be drawn before quick_change() is called as buffer needs to exist
        ####################

        while self.display.loop_running():
            if self.alpha < 1.0:
                # increase fade
                self.alpha += 1.0 / FADE_DURATION / FPS
            else:
                # fade finished - close old slide
                if self.slide1 and self.slide2:
                    self.slide1 = self.slide2
                    self.slide1.positionZ(2.0)
                    self.slide1.set_alpha(1.0)
                    self.slide2 = None
            if self.slide2: self.slide2.set_alpha(self.alpha)
            if self.slide1: self.slide1.draw()
            if self.slide2: self.slide2.draw()

            # Things to check every second
            last_text_frame += 1
            if last_text_frame >= FPS:
                last_text_frame = 0

                # update time text
                now = datetime.datetime.utcnow()
                utc_now = pytz.utc.localize(now)
                pst_now = utc_now.astimezone(pytz.timezone("Israel"))
                time_string.quick_change(('{d.hour:>2}:{d.minute:02}'.format(d=pst_now)))

                # check if the slideshow file has changed
                status = self.file_watcher.get_status()
                if status in [FileWatch.State.ADDED, FileWatch.State.MODIFIED]:
                    logging.info('Playlist changed - load new image')
                    self.read_playlist_file()
                    self.display_new_image()

                # check if it's time to show a new image
                slide_time_slot = self.now_time_slot()
                if last_slide_time_slot != slide_time_slot:
                    logging.info('Time interval passed - load new image')
                    last_slide_time_slot = slide_time_slot
                    self.display_new_image()

            time_string.draw()


if __name__ == '__main__':
    # Set current dir (needed for remote-debug)
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    SlideShow().show()
