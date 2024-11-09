import mesop as me
from enum import Enum

from backend.state_machine.state import State
from backend.state_machine.database.manager import database_manager


class StagesShowDatabase(Enum):
    GET_NUMBER_END_DIALOG = 0


def interact_show_database(user_input: str) -> str:
    state: State = me.state(state=State)

    match state.stage:
        case StagesShowDatabase.GET_NUMBER_END_DIALOG.value:
            try:
                input_number: int = int(user_input)
            except:
                raise ValueError('Provided input is not an integer nuber')

            if input_number < 1 or input_number > 100:
                raise ValueError(
                    'Provided number does not belong to interval [1; 100]'
                )
            
            report: str = database_manager.show_database(
                num_recent_records=input_number
            )

            report += 'Enter one of the available interactive commands to proceed. \n\n'

            state.reset()
            
            return report
        
        case _:
            raise ValueError('Unrecognized stage.')