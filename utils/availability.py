from datetime import datetime, timedelta
from backend.config.schedule import WORKING_HOURS
from backend.config.stylists import STYLISTS


def add_minutes(time_str: str, minutes: int):
    t = datetime.strptime(time_str, "%H:%M")
    t += timedelta(minutes=minutes)
    return t.strftime("%H:%M")


def get_duration(service: str, stylist: str):
    return STYLISTS[stylist]["services"][service]


def calculate_free_slots_backend(date: str, service: str, stylist: str, appointments):
    """
    Calcula los huecos libres para un estilista en una fecha concreta,
    teniendo en cuenta la duración del servicio y las citas existentes.
    """

    duration = get_duration(service, stylist)

    # Horario laboral
    start_time = WORKING_HOURS["start"]
    end_time = WORKING_HOURS["end"]

    # Convertir citas existentes a intervalos ocupados
    occupied = []
    for appt in appointments:
        appt_duration = get_duration(appt.service, appt.stylist)
        appt_end = add_minutes(appt.time, appt_duration)
        occupied.append((appt.time, appt_end))

    # Generar huecos libres
    free_slots = []
    current = start_time

    while add_minutes(current, duration) <= end_time:
        overlap = False

        for start, end in occupied:
            # Si se solapa, marcamos overlap
            if not (add_minutes(current, duration) <= start or current >= end):
                overlap = True
                break

        if not overlap:
            free_slots.append(current)

        current = add_minutes(current, 15)  # intervalos de 15 min

    return free_slots

