from datetime import datetime, timedelta, timezone


def set_time():

    current_time = datetime.now(timezone.utc)
    end_time = current_time.replace(minute=0, second=0, microsecond=0)

    start_time = end_time - timedelta(hours=1)

    s, e = int(start_time.timestamp()), int(end_time.timestamp())
    print(start_time, end_time)
    print(s, e)
    return s, e



