from datetime import datetime, timedelta, timezone, time
from dateutil.parser import parse
import pytz


def convert_to_utc(talk_time, date_mention=False):
    """Convert the datetime string we get from SUTime to utcnow"""

    sutime_on_default = sutime_on_default_utc(parse(talk_time))

    if sutime_on_default:
        # get correct local year, month, day if sutime is still on default UTC
        local_tz = pytz.timezone('US/Pacific')
        local_date = datetime.now(local_tz)
        local_date_str = datetime.strftime(local_date, "%Y %m %d")
        year, month, day = local_date_str.split(" ")
    else:
        # check if utc between midnight and 7am if so use SUTime date -1 day to account
        # for portland day diff else use SUTime date as is. 
        pass


    # ---------------------------------------------
    if date_mention:
        # quick fix to change date to valid pycon date if date not picked up by SUTime
        month, day = date_mention[0].split("/")
        month = "0" + month

    # get SUTime parsed talk time and extract hours, mins
    sut_dt_obj = parse(talk_time)
    local_time_str = datetime.strftime(sut_dt_obj, "%H %M")
    hours, mins = local_time_str.split(" ")

    # ---------------------------------------------
    # build up correct datetime obj, normalize & localize, switch to utc 
    correct_dt = datetime(int(year), int(month), int(day), int(hours), int(mins))
    tz_aware_local = local_tz.normalize(local_tz.localize(correct_dt))
    local_as_utc = tz_aware_local.astimezone(pytz.utc)
    
    return local_as_utc

def sutime_on_default_utc(time):
    """Check to see if SUTime is still on default day or if it saw a time 
    mention
    """
    utc_date_str = datetime.strftime(datetime.utcnow(), "%Y %m %d")
    sut_date_str = datetime.strftime(time, "%Y %m %d")

    return True if utc_date_str == sut_date_str else False

def utc_bewteen_day_gap():
    """Check to see if current UTC time is one day ahead of Portland"""
    current_utc = datetime.utcnow()
    midnight = time(0,0)
    seven_am = time(7,0)
    if midnight <= current_utc.time() <= seven_am:
        return True
    else:
        return False

def get_local_clock_time():
    local_dt = datetime.now(pytz.timezone('US/Pacific'))
    local_clock_time = datetime.strftime(local_dt, "%H:%M")
    return local_clock_time

def check_start_time(talk_time):
    """If time of openspaces talk within next 30 mins return True"""
    time_diff = talk_time - datetime.now(timezone.utc)
    threshold = timedelta(minutes=30)

    if time_diff < threshold:
        return True
    else:
        return False
