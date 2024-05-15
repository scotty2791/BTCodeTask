import re
import sys
from datetime import datetime


# Create a person object to store data about their sessions and duration
class Person:

    def __init__(self, name, sessions, duration, data):
        self.name = name
        self.sessions = sessions
        self.duration = duration
        self.data = data

    def add_session(self):
        self.sessions += 1

    def add_duration(self, time):
        self.duration += time

    def set_data(self, data):
        self.data = data


def main(inputfile):

    users = []
    # Collect all valid lines into a list
    file_contents = get_inputlines(inputfile)

    # Store the max and min time
    start_time = file_contents[0][0]
    end_time = file_contents[-1][0]

    # Create a set of all valid users and create a list of person objects from set
    for _ in sorted(set([x[1] for x in file_contents])):
        users.append(Person(_, 0, 0, []))

    # Add relevant data to each person object. Whole list won't be iterated over past this point - factor for larger logs perhaps
    for user in users:
        user.set_data([x for x in file_contents if x[1] == user.name])

    # For each user, calculate min duration and output result
    for user in users:
        collect_session_data(user, start_time, end_time)
        print("{0} {1} {2}".format(user.name, user.sessions, user.duration))


# Get the lines from the test file input, and create a list of only valid ones
def get_inputlines(pathname):

    file_lines = []

    with open(pathname, 'r') as rf:
        for line in rf:
            line = line.strip()
            if line_validation(line):
                file_lines.append(line.split())

    return file_lines


# Check each line is a valid format, and has a valid timestamp
def line_validation(inputline):

    return valid_line(inputline) and valid_time(inputline.split()[0])


# Check each line consists of
# Time as hh:mm:ss
# Name as alphanumerical chars
# Commands of Start or End only
def valid_line(inputline):

    PATTERN = re.compile(
        r"^\d{2}:\d{2}:\d{2}\s[A-Za-z0-9]+\s(?:Start|End)$")

    return bool(re.search(PATTERN, inputline))


# Check times are valid for a 24hr clock
def valid_time(timestamp):

    hour, min, sec = (int(x) for x in timestamp.split(':'))

    return (hour < 24 and min < 60 and sec < 60)


# Return time difference of two times in integer seconds
def calculate_delta(start_time, end_time):

    t1 = datetime.strptime(start_time, "%H:%M:%S")
    t2 = datetime.strptime(end_time, "%H:%M:%S")
    return int((t2-t1).total_seconds())


def collect_session_data(user, start_time, end_time):

    session_starts = []

    for dataentry in user.data:

        # Create a stack of start times for concurrent sessions that are not the last index
        if dataentry[2] == "Start":
            session_starts.append(dataentry[0])

        # When End appears, try and match with the earliest start time, else default to the earliest file time
        t1 = start_time

        if dataentry[2] == "End":
            if len(session_starts) > 0:
                t1 = session_starts.pop(0)

            t2 = dataentry[0]
            delta = calculate_delta(t1, t2)
            user.add_duration(delta)
            user.add_session()

    # Handle any leftover 'start' entries
    for session in session_starts:
        delta = calculate_delta(session, end_time)
        user.add_duration(delta)
        user.add_session()

    return user


if __name__ == "__main__":

    main(sys.argv[1])
