import re
import mesop as me
from enum import Enum

from backend.state_machine.state import State
from backend.state_machine.database.manager import database_manager
from backend.state_machine.validation import pattern_username


class StagesRemoveNote(Enum):
    GET_USERNAME_ASK_TITLE = 0
    GET_TITLE_END_DIALOG = 1


def interact_remove_note(user_input: str) -> str:
    state: State = me.state(state=State)

    match state.stage:
        case StagesRemoveNote.GET_USERNAME_ASK_TITLE.value:
            input_username: str = user_input

            if re.fullmatch(pattern=pattern_username, string=input_username) is None:
                raise ValueError('Provided username is not valid.')
            
            state.username = input_username
            state.stage = StagesRemoveNote.GET_TITLE_END_DIALOG.value

            return (
                'Next \n\n'
                '2. Enter the title of the note to remove. \n\n'
                'Example: My title 1 \n\n'
                'Arbitrary text shorter than 100 characters is supported.'
            )
        
        case StagesRemoveNote.GET_TITLE_END_DIALOG.value:
            input_title: str = user_input

            if len(input_title) > 100:
                raise ValueError(
                    'Length of provided title exceeds 100 characters.'
                )
            
            state.note_title = input_title
            
            report: str = database_manager.remove_note(
                username=state.username,
                title=state.note_title
            )

            report += 'Enter one of the available interactive commands to proceed. \n\n'
            
            state.reset()
            
            return report
            
        case _:
            raise ValueError('Unrecognized stage.')