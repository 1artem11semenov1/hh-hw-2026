import pytest

from app.switchboard import Switchboard
from app.users import ForeignUser, LocalUser


def test_register_call_creates_two_local_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+79990000001"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, LocalUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_call_creates_two_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Alice Ivanova,+15551234568,2,Bob Petrov,+15551234567"
    )

    assert isinstance(active_call.caller, ForeignUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_call_creates_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_call_with_none_or_empty_returns_none() -> None:
    switchboard = Switchboard()

    active_call_none = switchboard.register_call(
        None
    )
    active_call_empty = switchboard.register_call(
        ""
    )

    assert active_call_none == None
    assert active_call_empty == None
    assert switchboard.get_active_calls_count() == 0


def test_register_call_with_wrong_number_of_fields() -> None:
    switchboard = Switchboard()

    active_call_1 = switchboard.register_call(
        "Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    active_call_2 = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567,3,Bob Smith,+15551234567"
    )

    assert active_call_1 == None
    assert active_call_2 == None
    assert switchboard.get_active_calls_count() == 0


def test_incorrect_id_fields_in_raw_call() -> None:
    switchboard = Switchboard()

    active_call_incorrect_uid = switchboard.register_call(
        "None,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    active_call_empty_uid = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,,John Smith,+15551234567"
    )

    assert active_call_incorrect_uid == None
    assert active_call_empty_uid == None
    assert switchboard.get_active_calls_count() == 0


def test_incorrect_name_fields_in_raw_call() -> None:
    switchboard = Switchboard()

    active_call_empty_name = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,,+15551234567"
    )
    active_call_spaces_name = switchboard.register_call(
        "1,   ,79990000000,2,John Smith,15551234567"
    )

    assert active_call_empty_name == None
    assert active_call_spaces_name == None
    assert switchboard.get_active_calls_count() == 0


def test_incorrect_number_fields_in_raw_call() -> None:
    switchboard = Switchboard()

    active_call_incorrect_number = switchboard.register_call(
        "1,Ivan Ivanov,79990000000,2,John Smith,15551234567"
    )
    active_call_incorrect_number_format = switchboard.register_call(
        "1,Ivan Ivanov,+7-(999)-000-0000,2,John Smith,15551234567"
    )

    assert active_call_incorrect_number == None
    assert active_call_incorrect_number_format == None
    assert switchboard.get_active_calls_count() == 0


def test_reverse_fields_in_raw_call() -> None:
    switchboard = Switchboard()

    active_call_reverse_call_data = switchboard.register_call(
        "+79990000000,Ivan Ivanov,1,+15551234567,John Smith,2"
    )

    assert active_call_reverse_call_data == None
    assert switchboard.get_active_calls_count() == 0


def test_register_call_counts_active_calls() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )
    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


def test_register_call_counts_calls_between_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3
    assert switchboard.get_cross_border_calls_count() == 1


def test_register_call_counts_active_calls_count_without_calls() -> None:
    switchboard = Switchboard()

    assert switchboard.get_active_calls_count() == 0
    assert switchboard.get_cross_border_calls_count() == 0