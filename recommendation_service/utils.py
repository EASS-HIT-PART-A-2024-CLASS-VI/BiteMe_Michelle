from datetime import datetime

def get_current_time_of_day():
    now = datetime.now()
    return now.strftime("%H:%M") # Returns the current time in HH:MM format