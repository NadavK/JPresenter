import datetime
from pyluach import parshios
from pyluach.dates import GregorianDate, HebrewDate
from pyluach.hebrewcal import Month, Year

# from pyluach.parshios import PARSHIOS
PARSHIOT = [
    'Bereshit', 'Noach', 'Lech Lecha', 'Vayera', 'Chayei Sarah',
    'Toldot', 'Vayetzei', 'Vayishlach', 'Vayeshev', 'Miketz',
    'Vayigash', 'Vayechi', 'Shemot', 'Vaera', 'Bo', 'Beshalach',
    'Yitro', 'Mishpatim', 'Teruma', 'Tetzave', 'Ki Tisa', 'Vayakhel',
    'Pekudei', 'Vayikra', 'Tzav', 'Shemini', 'Tazria', 'Metzora',
    'Acharei Mot', 'Kedoshim', 'Emor', 'Behar', 'Bechukotai', 'Bamidbar',
    'Naso', 'Bahaalotcha', 'Shelach', 'Korach', 'Chukat', 'Balak',
    'Pinchas', 'Matot', 'Masei', 'Devarim', 'Vaetchanan', 'Eikev',
    'Ree', 'Shoftim', 'Ki Tetzei', 'Ki Tavo', 'Nitzavim', 'Vayelech',
    'Haazinu', 'Vezot Habracha'
]

PARSHIOS_LIKE_PREVIOUS_ALGO = [
    "Bereshith", "Noah", "Le'h Leha", "Vayera", "Haye Sarah", "Toledoth", "Vayetse", "Vayishlah",
    "Vayesheb", "Mikkets", "Vayiggash", "Vayhee", "Shemoth", "Vaera", "Bo", "Beshallah", "Yithro",
    "Mishpatim", "Terumah", "Tetsavveh", "Ki Tissa", "Vayakhel", "Pekude", "Vayikra", "Tsav", "Shemini",
    "Tazria", "Metsora", "Aharemoth", "Kedoshim", "Emor", "Behar", "Behukkothai", "Bemidbar", "Naso",
    "Behaaloteha", "Shelah Leha", "Korah", "Hukath", "Balak", "Pinhas", "Matoth", "Maseh", "Debarim",
    "Vaethanan", "Ekeb", "Reeh", "Shofetim", "Ki Tetse", "Ki Tabo", "Nitsabim", "Vayeleh", "Haazinu"]


# returns a dictionary with the name of the holiday types, with the priority as key
def get_holidays(date=datetime.date.today(), diaspora=False):
    hebYear, hebMonth, hebDay = GregorianDate(date.year, date.month, date.day).to_heb().tuple()

    # Holidays in Nisan
    if hebDay == 15 and hebMonth == 1:
        return {0: 'Pesach', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 16 and hebMonth == 1:
        return {0: 'Pesach', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 17 and hebMonth == 1:
        return {0: 'Pesach', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 18 and hebMonth == 1:
        return {0: 'Pesach', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 19 and hebMonth == 1:
        return {0: 'Pesach', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 20 and hebMonth == 1:
        return {0: 'Pesach', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 21 and hebMonth == 1:
        return {0: 'Pesach', 3: 'Hag', 4: 'Shabbat'}
    # if hebDay == 22 and hebMonth == 1 and diaspora:
    #    return {0: 'Pesach'})

    # Yom Hashoah
    if HebrewDate(hebYear, 1, 27).weekday() == 6 and hebDay == 26 and hebMonth == 1:
        return {0: 'YomHashoah'}
    elif hebYear >= 5757 and HebrewDate(hebYear, 1, 27).weekday() == 1 and hebDay == 28 and hebMonth == 1:
        return {0: 'YomHashoah'}
    elif hebDay == 27 and hebMonth == 1:
        return {0: 'YomHashoah'}

    # Holidays in Iyar

    # Yom Hazikaron
    if HebrewDate(hebYear, 2, 4).weekday() == 6 and hebDay == 2 and hebMonth == 2:  # If 4th of Iyar is a Thursday then Yom Hazikaron is on 2th of Iyar
        return {2: 'YomHazikaron'}
    elif HebrewDate(hebYear, 2, 4).weekday() == 5 and hebDay == 3 and hebMonth == 2:
        return {2: 'YomHazikaron'}
    elif hebYear >= 5764 and HebrewDate(hebYear, 2, 4).weekday() == 1 and hebDay == 5 and hebMonth == 2:
        return {2: 'YomHazikaron'}
    elif hebDay == 4 and hebMonth == 2:
        return {2: 'YomHazikaron'}

    # Yom Ha'Azmaut
    if HebrewDate(hebYear, 2, 5).weekday() == 7 and hebDay == 3 and hebMonth == 2:
        return {1: 'YomHaatzmaut', 3: 'Hag', 4: 'Shabbat'}
    elif HebrewDate(hebYear, 2, 5).weekday() == 6 and hebDay == 4 and hebMonth == 2:
        return {1: 'YomHaatzmaut', 3: 'Hag', 4: 'Shabbat'}
    elif hebYear >= 5764 and HebrewDate(hebYear, 2, 4).weekday() == 1 and hebDay == 6 and hebMonth == 2:
        return {1: 'YomHaatzmaut', 3: 'Hag', 4: 'Shabbat'}
    elif hebDay == 5 and hebMonth == 2:
        return {1: 'YomHaatzmaut', 3: 'Hag', 4: 'Shabbat'}

    if hebDay == 18 and hebMonth == 2:
        return {0: 'LagBaomer'}
    if hebDay == 28 and hebMonth == 2:
        return {0: 'YomYerushalayim'}

    # Holidays in Sivan
    if hebDay == 6 and hebMonth == 3:
        return {0: 'Shavuot', 3: 'Hag', 4: 'Shabbat'}

    # Holidays in Av
    if HebrewDate(hebYear, 5, 9).weekday() == 7 and hebDay == 10 and hebMonth == 5:
        return {0: 'TishaBAv'}
    elif hebDay == 9 and hebMonth == 5:
        return {0: 'TishaBAv'}

    if hebDay == 15 and hebMonth == 5:
        return {0: 'TuBAv'}

    # Holidays in Tishrei
    if hebDay == 1 and hebMonth == 7:
        return {0: 'RoshHashana', 1: 'ShabbatShuva', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 2 and hebMonth == 7:
        return {0: 'RoshHashana', 1: 'ShabbatShuva', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 3 and hebMonth == 7:
        return {1: 'ShabbatShuva'}
    if hebDay == 4 and hebMonth == 7:
        return {1: 'ShabbatShuva'}
    if hebDay == 5 and hebMonth == 7:
        return {1: 'ShabbatShuva'}
    if hebDay == 6 and hebMonth == 7:
        return {1: 'ShabbatShuva'}
    if hebDay == 7 and hebMonth == 7:
        return {1: 'ShabbatShuva'}
    if hebDay == 8 and hebMonth == 7:
        return {1: 'ShabbatShuva'}
    if hebDay == 9 and hebMonth == 7:
        return {1: 'ShabbatShuva'}
    if hebDay == 10 and hebMonth == 7:
        return {1: 'YomKippur', 2: 'ShabbatShuva', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 15 and hebMonth == 7:
        return {1: 'Sukkot', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 16 and hebMonth == 7:
        return {1: 'Sukkot', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 17 and hebMonth == 7:
        return {1: 'Sukkot', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 18 and hebMonth == 7:
        return {1: 'Sukkot', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 19 and hebMonth == 7:
        return {1: 'Sukkot', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 20 and hebMonth == 7:
        return {1: 'Sukkot', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 21 and hebMonth == 7:
        return {1: 'Sukkot', 3: 'Hag', 4: 'Shabbat'}
    if hebDay == 22 and hebMonth == 7:
        return {1: 'SimchatTorah', 3: 'Hag', 4: 'Shabbat'}

    # Holidays in Kislev
    if hebDay == 25 and hebMonth == 9:
        return {0: 'Hanukka'}
    if hebDay == 26 and hebMonth == 9:
        return {0: 'Hanukka'}
    if hebDay == 27 and hebMonth == 9:
        return {0: 'Hanukka'}
    if hebDay == 28 and hebMonth == 9:
        return {0: 'Hanukka'}
    if hebDay == 29 and hebMonth == 9:
        return {0: 'Hanukka'}
    if len(Month(hebYear, 9)) == 30:
        if hebDay == 30 and hebMonth == 9:
            return {0: 'Hanukka'}
        elif hebDay == 1 and hebMonth == 10:
            return {0: 'Hanukka'}
        elif hebDay == 2 and hebMonth == 10:
            return {0: 'Hanukka'}
    else:  # if len(Month(hebYear, 9)) == 29:
        if hebDay == 1 and hebMonth == 10:
            return {0: 'Hanukka'}
        elif hebDay == 2 and hebMonth == 10:
            return {0: 'Hanukka'}
        elif hebDay == 3 and hebMonth == 10:
            return {0: 'Hanukka'}

    # Holidays in Shevat
    if hebDay == 15 and hebMonth == 11:
        return {0: 'TuBShvat'}

    # Holidays in Adar (I)/Adar II
    if Year(hebYear).leap:
        monthEsther = 13
    else:
        monthEsther = 12
    if hebDay == 14 and hebMonth == monthEsther:
        return {0: 'Purim', 3: 'Hag', 4: 'Shabbat'}
    elif hebDay == 15 and hebMonth == monthEsther:
        return {0: 'Purim', 3: 'Hag', 4: 'Shabbat'}     # Shushan Purim


def get_season(date=datetime.date.today()):
    hebYear, hebMonth, hebDay = GregorianDate(date.year, date.month, date.day).to_heb().tuple()

    if hebMonth >= 10:
        return ['Winter', ]
    elif hebMonth >= 7:
        return ['Fall', ]
    elif hebMonth >= 4:
        return ['Summer', ]
    else:
        return ['Spring', ]


def get_personal(date=datetime.date.today()):
    hebYear, hebMonth, hebDay = GregorianDate(date.year, date.month, date.day).to_heb().tuple()

    if date.month == 5 and date.day == 4:       # May the 4th be With You
        return {3: 'StarWars'}








#TODO: this should be read from an external file














def get_hags(date=datetime.date.today(), days_range_future=0, days_range_past=0, return_shabbat=True):
    holidays_dict = get_holidays(date)

    if not holidays_dict:
        if return_shabbat and date.weekday() == 5:  # 5 == Shabbat
            holidays_dict = {9: 'Shabbat'}  # lowest priority

            ###############################################################################################################################################
            #       The marked code includes parashot and special shabbatot (Para, Hodesh, etc), but has a bug that 2020-05-30 does not have a parasha    #
            ###############################################################################################################################################
            #
            # import date_utils.calendar_util
            # from jewish_dates.parasha import getTorahSections
            # shabbat = date #+ datetime.timedelta(days=1)
            # julian = date_utils.calendar_util.gregorian_to_jd(shabbat.year, shabbat.month, shabbat.day)
            # hebYear, hebMonth, hebDay = date_utils.calendar_util.jd_to_hebrew(julian)
            # str = getTorahSections(hebMonth, hebDay, hebYear, False)
            # if str:
            #    folders_dict.update({8: str})  # second-lowest priority

            # TODO: Add special shabbatot: http://individual.utoronto.ca/kalendis/hebrew/parshah.htm
            # TODO: maybe ;ppk at this package: https://pypi.org/project/convertdate/
            parashot = parshios.getparsha(GregorianDate(date.year, date.month, date.day), israel=True)
            if parashot:
                for index, parash in enumerate(parashot):
                    holidays_dict.update({8 + index / 100: PARSHIOT[parash]})  # second-lowest priority
        else:
            for i in range(1, max(days_range_future, days_range_past) *2+2):              # check if any holidays next/past x days
                day_offset = i//2 * (1, -1)[i % 2]          # returns this order of values: 0, +1, -1, +2, -2, +3, -3, etc...
                if day_offset > days_range_future or day_offset < -days_range_past:
                    continue
                offset_date = date + datetime.timedelta(days=day_offset)
                holidays_dict = get_holidays(offset_date)
                if not holidays_dict:
                    holidays_dict = get_personal(offset_date)
                if holidays_dict:
                        break

    # export list of holidays, in order of priority
    sorted_folders = []
    if holidays_dict and len(holidays_dict) > 0:
        for key in sorted(holidays_dict):
            sorted_folders += [holidays_dict[key]]

    return sorted_folders
