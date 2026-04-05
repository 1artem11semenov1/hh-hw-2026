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
    
    def create_correct_user(self, usr_data) -> User:
        if usr_data[2].startswith(LOCAL_PHONE_PREFIX):
            return LocalUser(int(usr_data[0]), usr_data[1], usr_data[2])
        
        return ForeignUser(int(usr_data[0]), usr_data[1], usr_data[2])

    def is_correct_call_info(self, call_info) -> bool:
        # проверяем длину
        if (len(call_info) != 6):
            return False
        
        # можно str -> int для id
        try:
            int(call_info[0])
            int(call_info[3])
        except:
            return False
        
        # Имя не пустая строка
        if ((not bool(call_info[1].strip())) or (not bool(call_info[4].strip()))):
            return False

        # Номер начинается с '+'
        if ((not call_info[2].startswith('+')) or (not call_info[5].startswith('+'))):
            return False
        
        return True
        

    def register_call(self, raw_call: str) -> ActiveCall:
        '''
        Метод должен принимать только 1 строку и возвращать класс ActiveCall.
        На входе строка должна быть вида "caller_id,caller_name,caller_phone,reciever_id,reciever_name,reciever_phone"

        Например: "1001,Иван Петров,+71234567890,1085,Адам Яковлев,+71255556666"
        '''
        if (raw_call != None):
            call_info = raw_call.split(",")
        
            if (self.is_correct_call_info(call_info)):
                caller = self.create_correct_user(call_info[:3])
        
                receiver = self.create_correct_user(call_info[3:])

                call = ActiveCall(caller, receiver)
                if (call.is_cross_border):
                    self._active_cross_border_calls.append(call)
                else:
                    self._active_in_border_calls.append(call)

                return call
        
        return None

    def get_active_calls_count(self) -> int:
        return len(self._active_cross_border_calls) + len(self._active_in_border_calls)

    def get_cross_border_calls_count(self) -> int:
        return len(self._active_cross_border_calls)
