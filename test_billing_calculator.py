import billing_calculator as bc

VALIDTIME = "14:02:03"
INVALIDTIME = "44:02:03"
VALIDNAME = "ALICE99"
INVALIDNAME = "ALICE@~99"
VALIDTIME = "14:02:03"
INVALIDTIME = "14:2:0"
LARGETIME = "27:02:65"
VALIDCMD = "Start"
INVALIDCMD = "Starting"

TIME1 = "14:01:03"
TIME2 = "14:01:04"

SHORTVALIDTESTFILE = "./sampletests.txt"
SHORTINVALIDTESTFILE = "./sampletests_invalidentry.txt"
PROVIDEDTESTFILE = "./testfile.txt"


# Test the component parts of line_validation to ensure only correct inputs
# Without this, line_validation certainty not guaranteed
def test_valid_line():

    assert bc.valid_line(" ".join([VALIDTIME, VALIDNAME, VALIDCMD])) == True
    assert bc.valid_line(" ".join([INVALIDTIME, VALIDNAME, VALIDCMD])) == False
    assert bc.valid_line(" ".join([VALIDTIME, INVALIDNAME, VALIDCMD])) == False
    assert bc.valid_line(" ".join([VALIDTIME, VALIDNAME, INVALIDCMD])) == False
    assert bc.valid_line(" ".join([VALIDNAME, VALIDCMD])) == False
    assert bc.valid_line(" ".join([VALIDTIME, VALIDCMD])) == False
    assert bc.valid_line(" ".join([VALIDTIME, VALIDNAME])) == False


def test_valid_time():

    assert bc.valid_time(VALIDTIME) == True
    assert bc.valid_time(LARGETIME) == False


# Test complete validation, only one fail input needed as others tested in test_valid_line
def test_line_validation():

    assert bc.line_validation(
        " ".join([VALIDTIME, VALIDNAME, VALIDCMD])) == True
    assert bc.line_validation(INVALIDTIME) == False


# Test time delta calculations
def test_calculate_delta():
    assert bc.calculate_delta(TIME1, TIME2) == 1

# Test the file reading


def test_get_inputlines():

    assert bc.get_inputlines(
        SHORTVALIDTESTFILE) == [["14:02:03", "ALICE99", "Start"], ["14:02:34", "ALICE99", "End"]]
    assert bc.get_inputlines(
        SHORTINVALIDTESTFILE) == [["14:02:03", "ALICE99", "Start"], ["14:02:34", "ALICE99", "End"]]

# Test the calculations of user data


def test_collect_session_data():

    firt_time = "14:02:03"
    last_time = "14:02:10"
    DATA = [["14:02:03", "ALICE99", "Start"], [
        "14:02:04", "ALICE99", "End"], ["14:02:09", "ALICE99", "Start"], [
        "14:02:10", "ALICE99", "End"]]

    # Normal pairing
    data = DATA[:]
    user = bc.Person("ALICE99", 0, 0, data)

    bc.collect_session_data(user, firt_time, last_time)
    assert user.sessions == 2
    assert user.duration == 2

    # Additional start at end of file
    data = DATA[:]
    data.append(["14:02:10", "ALICE99", "Start"])
    user = bc.Person("ALICE99", 0, 0, data)

    bc.collect_session_data(user, firt_time, last_time)
    assert user.sessions == 3
    assert user.duration == 2

    # Additional start in file
    data = DATA[:]
    data.insert(2, ["14:02:05", "ALICE99", "Start"])
    user = bc.Person("ALICE99", 0, 0, data)

    bc.collect_session_data(user, firt_time, last_time)
    assert user.sessions == 3
    assert user.duration == 7

    # Additional end at end of file
    data = DATA[:]
    data.insert(2, ["14:02:11", "ALICE99", "End"])
    user = bc.Person("ALICE99", 0, 0, data)

    bc.collect_session_data(user, firt_time, last_time)
    assert user.sessions == 3
    assert user.duration == 10

    # Additional end in file
    data = DATA[:]
    data.append(["14:02:05", "ALICE99", "End"])
    user = bc.Person("ALICE99", 0, 0, data)

    bc.collect_session_data(user, firt_time, last_time)
    assert user.sessions == 3
    assert user.duration == 4


# Test full tool on sample data
def test_main(capfd):
    bc.main(SHORTVALIDTESTFILE)
    out, err = capfd.readouterr()
    assert out == "ALICE99 1 31\n"

    bc.main(SHORTINVALIDTESTFILE)
    out, err = capfd.readouterr()
    assert out == "ALICE99 1 31\n"

    bc.main(PROVIDEDTESTFILE)
    out, err = capfd.readouterr()
    assert out == "ALICE99 4 240\nCHARLIE 3 37\n"
