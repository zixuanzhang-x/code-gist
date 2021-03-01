from datetime import datetime
from zoneinfo import ZoneInfo

def convertTimezone(timestamp_str, from_zone_str='UTC', to_zone_str='America/Chicago'):
    utc_unaware = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
    utc_aware = utc_unaware.replace(tzinfo=ZoneInfo(from_zone_str))  # make aware
    local_aware = utc_aware.astimezone(ZoneInfo(to_zone_str))  # convert
    return f'{local_aware:%Y-%m-%d %H:%M:%S}'