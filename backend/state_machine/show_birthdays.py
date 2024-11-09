import mesop as me
from enum import Enum

from backend.state_machine.state import State
from backend.state_machine.database.validation import IOError
from backend.state_machine.database.manager import database_manager


class StagesShowBirthdays(Enum):
    GET_NUMBER_END_DIALOG = 0


def interact_show_birthdays(user_input: str) -> str:
    state: State = me.state(state=State)

    match state.stage:
        case StagesShowBirthdays.GET_NUMBER_END_DIALOG.value:
            try:
                input_number: int = int(user_input)
            except:
                raise IOError('Provided input must be an integer number. \n\n')

            if input_number < 1 or input_number > 365:
                raise IOError(
                    'Provided number must belong to interval [1; 365] \n\n'
                )
            
            report: str = database_manager.show_birthdays(
                num_days_ahead=input_number
            )

            report += (
                'Enter one of the available '
                'interactive commands to proceed. \n\n'
            )

            state.reset()
            
            return report
        
        case _:
            raise IOError('Unrecognized stage. \n\n')