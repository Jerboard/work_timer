

def process_duration(minutes: int) -> str:
    hours = minutes // 60
    minutes = minutes % 60
    if hours < 10:
        hours = f'0{hours}'

    if minutes < 10:
        minutes = f'0{minutes}'

    return f'{hours}:{minutes}'
