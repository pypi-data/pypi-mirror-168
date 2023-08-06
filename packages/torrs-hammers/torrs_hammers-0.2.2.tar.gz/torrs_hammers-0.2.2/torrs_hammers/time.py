from datetime import datetime

def current_time():
    return datetime.now()  # current date and time

def get_time():
    return current_time().strftime("%H:%M:%S")

def get_full_date():
    return current_time().strftime("%Y%m%d")

def get_full_data_time():
    return current_time().strftime("%Y%m%d_%H%M%S")

