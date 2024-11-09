import re
import mesop as me
from enum import Enum

from backend.state_machine.state import State
from backend.state_machine.database.manager import database_manager
from backend.state_machine.database.validation import IOError, pattern_username


class StagesShowUser(Enum):
    GET_USERNAME_END_DIALOG = 0


def interact_show_user(user_input: str) -> str:
    state: State = me.state(state=State)

    match state.stage:
        case StagesShowUser.GET_USERNAME_END_DIALOG.value:
            input_username: str = user_input

            if re.fullmatch(pattern=pattern_username, string=input_username) is None:
                raise IOError(
                    'Provided username does not satisfy requirements. \n\n'
                )
            
            state.username = input_username
            report: str = database_manager.show_user(username=state.username)

            report += (
                'Enter one of the available '
                'interactive commands to proceed. \n\n'
            )
            
            state.reset()
            
            return report
        
        case _:
            raise IOError('Unrecognized stage. \n\n')