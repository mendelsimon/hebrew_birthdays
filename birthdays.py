from convertdate import hebrew
from icalendar import Event, Calendar
from datetime import date

BIRTH_DATES = [('Test A Person', (1984, 4, 11)), ('Test B Person', (2009, 10, 11))]
ORDINAL_SUFFIX = ['th', 'st', 'nd', 'rd'] + ['th'] * 16 + ['th', 'st', 'nd', 'rd', 'th', 'th']
AGE_INFORMATION_THRESHOLD = 25
MAX_AGE = 120


def get_dates(birthday):
    dates = []
    first_year, month, day = hebrew.from_gregorian(*birthday)
    for year in range(first_year, first_year + MAX_AGE):
        gregorian_date = hebrew.to_gregorian(year, month, day)
        dates.append(date(*gregorian_date))
    return dates


def create_cal():
    cal = Calendar()  # Create the calendar object
    # Add the two required fields
    cal.add('version', '2.0')
    cal.add('prodid', '-//Mendel Simon//Hebrew birthday calendar')
    return cal


def add_birthday_events(cal, name, dates):
    for age, event_date in enumerate(dates):
        birthday = Event()  # Create the event

        # Add the date to the event
        birthday.add('dtstart', event_date)

        # Add the description to the event
        number = ''
        if age <= AGE_INFORMATION_THRESHOLD:
            number = ' ' + str(age) + ORDINAL_SUFFIX[age]
        description = f"{name}'s{number} hebrew birthday"
        birthday.add('summary', description)

        # Add the event to the calendar
        cal.add_component(birthday)


def write_calendar(calendar):
    with open(r'birthdays.ics', 'w') as file:
        output = calendar.to_ical().decode()
        output = output.replace('\r', '')
        file.write(output)


def main():
    calendar = create_cal()
    for name, birth_date in BIRTH_DATES:
        dates = get_dates(birth_date)
        add_birthday_events(calendar, name, dates)
    write_calendar(calendar)


if __name__ == '__main__':
    main()
