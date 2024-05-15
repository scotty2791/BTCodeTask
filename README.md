# BTCodeTask

Uses:
    - Python 3.11
    - PyTest 7.4

Files:
    tool:
        - billing_calculator.py
    tests:
        - test_billing_calculator.py
        - testfile.txt
        - sampletests.txt
        - sampletests_invalidentry.txt

Usage:
    call "python billing_calculator <test file name>"

    For example, to use the data provided in the challenge brief use:
    "python billing_calculator testfile.txt"

Testing:
    Unit tests have been added to check functionality after any changes to the calculator. To run these, navigate to the directory containing all files, and call:

    "pytest"

    This will run all tests (7). If any tests fail, it indicates some broken functionality in the calculator.

    Expected output:
"
    test_billing_calculator.py .......                                                                                                                                                                                             [100%]

========================================================================================================= 7 passed in 0.12s ========================================================================================================="