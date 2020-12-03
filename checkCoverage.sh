#!/bin/bash

# Set of commands to check the coverage of the tests
if [ -d "htmlcov/" ]
then rm -Rf htmlcov
fi
rm .coverage
coverage run --source=. --omit=./tests/* -a tests/mocked-unit-tests.py
coverage run --source=. --omit=./tests/* -a tests/test_on_drawing_stroke.py
coverage run --source=. --omit=./tests/* -a tests/testEmitAllMessages.py
coverage run --source=. --omit=./tests/* -a tests/testEmitAllUsers.py
coverage run --source=. --omit=./tests/* -a tests/testEmitRoomHistory.py
coverage run --source=. --omit=./tests/* -a tests/testGoogleLogin.py
coverage run --source=. --omit=./tests/* -a tests/testOnConnect.py
coverage run --source=. --omit=./tests/* -a tests/testOnDisconnect.py
coverage run --source=. --omit=./tests/* -a tests/testOnNewMessage.py
coverage run --source=. --omit=./tests/* -a tests/testOnNewRoomCreation.py
coverage run --source=. --omit=./tests/* -a tests/testResetRoomPassword.py
coverage run --source=. --omit=./tests/* -a tests/testRoomDeparture.py
coverage run --source=. --omit=./tests/* -a tests/unmocked-unit-tests.py
coverage html