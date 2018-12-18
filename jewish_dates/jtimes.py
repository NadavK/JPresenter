# NK

# from jewish_dates.sun import GetSunrise, GetSunset
import astral
import datetime
from tzlocal import get_localzone
from pytz import utc

# per http://www.yeshiva.co/calendar/, for Ra'anana Shabbat times, the most exact is Astral, with co-ords from Wiki, and -20 minutes

TZ = 0

astral._LOCATION_INFO = """Raanana_wiki,Israel,32°11'N,34°52'E,Asia/Jerusalem,48
    Raanana_google,Israel,32°18'N,34°87'E,Asia/Jerusalem,44"""


def astral_location(location):
    a = astral.Astral(astral.AstralGeocoder)
    geo = a.geocoder
    return geo[location]


def get_google_geo():
    # Use this to get google co-ords and elevation
    from astral.astral import GoogleGeocoder
    a = astral.Astral(astral.GoogleGeocoder)
    geo = a.geocoder
    loc = geo['Tel-Aviv']
    print(loc, loc.elevation)


def next_friday(date):
    # returns closest fri, or next fri if today is fri
    # http://stackoverflow.com/questions/8801084/how-to-calculate-next-friday-in-python
    friday = 4  # 0 based, starting from Monday
    return date + datetime.timedelta(((friday - 1) - date.weekday()) % 7 + 1)


def this_friday(date):
    # returns closest fri, and return today if today is fri
    # http://stackoverflow.com/questions/8801084/how-to-calculate-next-friday-in-python
    friday = 4  # 0 based, starting from Monday
    return date + datetime.timedelta((friday - date.weekday()) % 7)


def sunrise_sunset_astral(location, date):
    # local False for UTC
    astral = astral_location(location)
    return astral.sun(local=False, date=date)


def today_sunrise_sunset_astral(location):
    return sunrise_sunset_astral(location=location, date=datetime.date.today())


def sunrise_sunset(location, date):
    a = astral.Astral(astral.AstralGeocoder)
    geo = a.geocoder
    sun = sunrise_sunset_astral(location=location, date=date)

    sunrise_utc = sun['sunrise'].replace(tzinfo=utc)  # aastral times are utc, this is just for explicity
    sunset_utc = sun['sunset'].replace(tzinfo=utc)

    local_tz = get_localzone()
    # Convert time zone
    sunrise_local = sunrise_utc.astimezone(local_tz)
    sunset_local = sunset_utc.astimezone(local_tz)

    return (sunrise_local, sunset_local)


def today_sunrise_sunset(location):
    return sunrise_sunset(location, datetime.date.today())


def shabbat_start(location, date, candlelight_delta):
    return sunrise_sunset(location, date)[1] - datetime.timedelta(minutes=candlelight_delta)


def shabbat_times(location, num, candlelight_delta):
    # returns the next <num> shabbat times

    # a = astral.Astral(astral.AstralGeocoder)
    # geo = a.geocoder

    times = []

    fri = datetime.datetime.today()
    for i in range(1, num):
        fri = next_friday(fri)
        times.append(shabbat_start(location, fri, candlelight_delta))
    return times
