# NK

import astral
import datetime
from pytz import utc

# per http://www.yeshiva.co/calendar/, for Ra'anana Shabbat times, the most exact is Astral, with co-ords from Wiki, and -20 minutes

TZ = 0

astral._LOCATION_INFO = """Raanana_wiki,Israel,32°11'N,34°52'E,Asia/Jerusalem,48
    Raanana_google,Israel,32°18'N,34°87'E,Asia/Jerusalem,44"""


def get_google_geo():
    # Use this to get google co-ords and elevation
    from astral.astral import GoogleGeocoder
    a = astral.Astral(astral.GoogleGeocoder)
    geo = a.geocoder
    loc = geo['Tel-Aviv']
    print(loc, loc.elevation)


def __sunrise_sunset_astral(location, date):
    # local False for UTC
    geo = astral.Astral(astral.AstralGeocoder).geocoder[location]
    return geo.sun(local=False, date=date)


def today_sunrise_sunset_astral(location):
    return __sunrise_sunset_astral(location=location, date=datetime.date.today())


def sunrise_sunset(location, date):
    sun = __sunrise_sunset_astral(location=location, date=date)

    sunrise_utc = sun['sunrise'].replace(tzinfo=utc)  # astral times are utc, this is just for explicitly
    sunset_utc = sun['sunset'].replace(tzinfo=utc)

    #https: // stackoverflow.com / questions / 2720319 / python - figure - out - local - timezone
    local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    # Convert time zone
    sunrise_local = sunrise_utc.astimezone(local_tz)
    sunset_local = sunset_utc.astimezone(local_tz)

    return sunrise_local, sunset_local


def shabbat_start(location, date, candlelight_delta):
    return sunrise_sunset(location, date)[1] - datetime.timedelta(minutes=candlelight_delta)


def shabbat_times(location, num, candlelight_delta):
    def next_friday(date):
        # returns closest fri, or next fri if today is fri
        # http://stackoverflow.com/questions/8801084/how-to-calculate-next-friday-in-python
        friday = 4  # 0 based, starting from Monday
        return date + datetime.timedelta(((friday - 1) - date.weekday()) % 7 + 1)

    # returns the next <num> shabbat times

    # a = astral.Astral(astral.AstralGeocoder)
    # geo = a.geocoder

    times = []

    fri = datetime.datetime.today()
    for i in range(1, num):
        fri = next_friday(fri)
        times.append(shabbat_start(location, fri, candlelight_delta))
    return times
