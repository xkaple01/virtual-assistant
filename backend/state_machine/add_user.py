import re
import mesop as me
from enum import Enum
from datetime import datetime

from backend.state_machine.state import State
from backend.state_machine.database.manager import database_manager
from backend.state_machine.database.validation import (
    IOError, pattern_username, pattern_email, pattern_phone, pattern_birthday
)


class StagesAddUser(Enum):
    GET_USERNAME_ASK_EMAIL = 0
    GET_EMAIL_ASK_PHONE = 1
    GET_PHONE_ASK_BIRTHDAY = 2
    GET_BIRTHDAY_END_DIALOG = 3


def interact_add_user(user_input: str) -> str:
    state: State = me.state(state=State)

    match state.stage:
        case StagesAddUser.GET_USERNAME_ASK_EMAIL.value:
            input_username: str = user_input

            if re.fullmatch(pattern=pattern_username, string=input_username) is None:
                raise IOError(
                    'Provided username does not satisfy requirements. \n\n'
                )
            
            state.username = input_username
            state.stage = StagesAddUser.GET_EMAIL_ASK_PHONE.value

            return (
                'Accepted. \n\n'
                '2. Enter email. \n\n'
                'Example: address@email.com \n\n'
                'Email can contain '
                'letters a-z, digits 0-9, and special symbols \n\n'
            )

        case StagesAddUser.GET_EMAIL_ASK_PHONE.value:
            input_email: str = user_input

            if re.fullmatch(pattern=pattern_email, string=input_email) is None:
                raise IOError(
                    'Provided email does not satisfy requirements. \n\n'
                )
            
            state.email = input_email
            state.stage = StagesAddUser.GET_PHONE_ASK_BIRTHDAY.value

            return (
                'Provided email satisfies requiremets. Next \n\n'
                '3. Enter the phone number. \n\n'
                'Example: 0970102033 \n\n'
                'Phone number consists of 10 digits. \n\n'
            )

        case StagesAddUser.GET_PHONE_ASK_BIRTHDAY.value:
            input_phone: str = user_input

            if re.fullmatch(pattern=pattern_phone, string=input_phone) is None:
                raise IOError(
                    'Provided phone number does not satisfy requirements. \n\n'
                )
            
            state.phone = input_phone
            state.stage = StagesAddUser.GET_BIRTHDAY_END_DIALOG.value

            return (
                'Format of the provided phone number is correct. Finally \n\n'
                '4. Enter the birthday. \n\n'
                'Example: 31.12.1990 \n\n'
                'Dates in format dd.mm.yyyy are accepted. \n\n'
            )

        case StagesAddUser.GET_BIRTHDAY_END_DIALOG.value:
            input_birthday: str = user_input

            try:
                datetime.strptime(input_birthday, pattern_birthday)
            except:
                raise IOError(
                    'Provided birthday does not satisfy requirements.\n\n'
                )
            
            state.birthday = input_birthday
            
            report: str =  database_manager.add_user(
                username=state.username,
                email=state.email,
                phone=state.phone,
                birthday=state.birthday
            )

            report += (
                'Enter one of the available '
                'interactive commands to proceed. \n\n'
            )

            state.reset()

            return report
        
        case _:
            raise IOError('Unrecognized stage. \n\n')