import re
import mesop as me
from enum import Enum

from backend.state_machine.state import State
from backend.state_machine.database.manager import database_manager
from backend.state_machine.validation import (
    pattern_username, pattern_email, pattern_phone
)


class StagesAddUser(Enum):
    GET_USERNAME_ASK_EMAIL = 0
    GET_EMAIL_ASK_PHONE = 1
    GET_PHONE_END_DIALOG = 2


def interact_add_user(user_input: str) -> str:
    state: State = me.state(state=State)

    match state.stage:
        case StagesAddUser.GET_USERNAME_ASK_EMAIL.value:
            input_username: str = user_input

            if re.fullmatch(pattern=pattern_username, string=input_username) is None:
                raise ValueError('Provided username is not valid.')
            
            state.username = input_username
            state.stage = StagesAddUser.GET_EMAIL_ASK_PHONE.value

            return (
                'Accepted. \n\n'
                '2. Enter email. \n\n'
                'Example: address@email.com. \n\n'
                'Email can contain letters a-z, digits 0-9, and special symbols \n\n'
            )

        case StagesAddUser.GET_EMAIL_ASK_PHONE.value:
            input_email: str = user_input

            if re.fullmatch(pattern=pattern_email, string=input_email) is None:
                raise ValueError('Provided email is not valid.')
            
            state.email = input_email
            state.stage = StagesAddUser.GET_PHONE_END_DIALOG.value

            return (
                'Provided email satisfies requiremets. Next \n\n'
                '3. Enter the phone number. \n\n'
                'Example: 0970102033. \n\n'
                'Phone number consists of 10 digits. \n\n'
            )

        case StagesAddUser.GET_PHONE_END_DIALOG.value:
            input_phone: str = user_input

            if re.fullmatch(pattern=pattern_phone, string=input_phone) is None:
                raise ValueError('Provided phone number is not valid.')
            
            state.phone = input_phone

            report: str =  database_manager.add_user(
                username=state.username,
                email=state.email,
                phone=state.phone
            )

            report += 'Enter one of the available interactive commands to proceed. \n\n'

            state.reset()
            
            return report
        
        case _:
            raise ValueError('Unrecognized stage.')