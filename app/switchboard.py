from __future__ import annotations

from dataclasses import dataclass

from app.users import User, LocalUser, ForeignUser


LOCAL_PHONE_PREFIX = "+7"


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self._active_in_border_calls: list[ActiveCall] = []
        self._active_cross_border_calls: list[ActiveCall] = []

    def register_call(self, raw_call: str) -> ActiveCall:
        '''
        Метод должен принимать только 1 строку и возвращать класс ActiveCall.
        На входе строка должна быть вида "caller_id,caller_name,caller_phone,reciever_id,reciever_name,reciever_phone"

        Например: "1001,Иван Петров,+71234567890,1085,Адам Яковлев,+71255556666"
        '''
        call_info = raw_call.split(",")
        if call_info[2].startswith(LOCAL_PHONE_PREFIX):
            caller = LocalUser(int(call_info[0]), call_info[1], call_info[2])
        else:
            caller = ForeignUser(int(call_info[0]), call_info[1], call_info[2])
        
        if call_info[5].startswith(LOCAL_PHONE_PREFIX):
            receiver = LocalUser(int(call_info[3]), call_info[4], call_info[5])
        else:
            receiver = ForeignUser(int(call_info[3]), call_info[4], call_info[5])
        
        call = ActiveCall(caller, receiver)
        if (call.is_cross_border):
            self._active_cross_border_calls.append(call)
        else:
            self._active_in_border_calls.append(call)

        return call

    def get_active_calls_count(self) -> int:
        return len(self._active_cross_border_calls) + len(self._active_in_border_calls)

    def get_cross_border_calls_count(self) -> int:
        return len(self._active_cross_border_calls)
