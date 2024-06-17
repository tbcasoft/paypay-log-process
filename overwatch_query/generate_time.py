from datetime import datetime, timedelta, timezone


def get_time():
    current_time = datetime.now(timezone.utc)

    end_time = current_time.replace(hour= 0, minute= 0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=1)
    
    s, e = format_timestamp(start_time), format_timestamp(end_time)
    print("start:", s)
    print("end:", e)
    print("\n")

    return s, e

def format_timestamp(time):
    return time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


