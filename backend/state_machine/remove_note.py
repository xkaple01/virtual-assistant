import re
import mesop as me
from enum import Enum

from backend.state_machine.state import State
from backend.state_machine.database.manager import database_manager
from backend.state_machine.database.validation import IOError, pattern_username


class StagesRemoveNote(Enum):
    GET_USERNAME_ASK_TITLE = 0
    GET_TITLE_END_DIALOG = 1


def interact_remove_note(user_input: str) -> str:
    state: State = me.state(state=State)

    match state.stage:
        case StagesRemoveNote.GET_USERNAME_ASK_TITLE.value:
            input_username: str = user_input

            if re.fullmatch(pattern=pattern_username, string=input_username) is None:
                raise IOError(
                    'Provided username does not safisfy requirements. \n\n'
                )
            
            report: str = database_manager.show_notes(username=input_username)
            
            state.username = input_username
            state.stage = StagesRemoveNote.GET_TITLE_END_DIALOG.value

            return report + (
                'Next \n\n'
                '2. Enter the title of the note to remove. \n\n'
                'Example: My title 1 \n\n'
                'Arbitrary text shorter than 100 characters is supported. \n\n'
            )
        
        case StagesRemoveNote.GET_TITLE_END_DIALOG.value:
            input_title: str = user_input

            if len(input_title) > 100:
                raise IOError(
                    'Length of provided title exceeds 100 characters. \n\n'
                )
            
            state.note_title = input_title
            
            report: str = database_manager.remove_note(
                username=state.username,
                title=state.note_title
            )
            
            state.reset()
            
            return report + (
                'Enter one of the available '
                'interactive commands to proceed. \n\n'
            )
            
        case _:
            raise IOError('Unrecognized stage. \n\n')