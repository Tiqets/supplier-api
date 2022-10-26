from datetime import date, datetime, timedelta


def get_tomorrow() -> date:
    tomorrow = datetime.utcnow().date() + timedelta(days=1)
    return tomorrow
