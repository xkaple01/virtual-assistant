import re
import mesop as me
from enum import Enum

from backend.state_machine.state import State
from backend.state_machine.database.manager import database_manager
from backend.state_machine.database.validation import IOError, pattern_username


class StagesAddNote(Enum):
    GET_USERNAME_ASK_TITLE = 0
    GET_TITLE_ASK_CONTENT = 1
    GET_CONTENT_END_DIALOG = 2


def interact_add_note(user_input: str) -> str:
    state: State = me.state(state=State)

    match state.stage:
        case StagesAddNote.GET_USERNAME_ASK_TITLE.value:
            input_username: str = user_input

            if re.fullmatch(pattern=pattern_username, string=input_username) is None:
                raise IOError('Provided username does not satisfy requirements.')
            
            database_manager.show_user(username=input_username)
            
            state.username = input_username
            state.stage = StagesAddNote.GET_TITLE_ASK_CONTENT.value
            
            return (
                'Next \n\n'
                '2. Enter the title of the note. \n\n'
                'Example: My title 1 \n\n'
                'Arbitrary text shorter than 100 characters is supported.\n\n'
            )
        
        case StagesAddNote.GET_TITLE_ASK_CONTENT.value:
            input_title: str = user_input

            if len(input_title) > 100:
                raise IOError(
                    'Length of provided title exceeds 100 characters.'
                )
            
            state.note_title = input_title
            state.stage = StagesAddNote.GET_CONTENT_END_DIALOG.value

            return (
                'Provided title is accepted. Now \n\n'
                '3. Enter the content of the note. \n\n'
                'Example: My content 1 \n\n'
                'Arbitrary text shorter than 1000 characters is supported.\n\n'
            )

        case StagesAddNote.GET_CONTENT_END_DIALOG.value:
            input_content: str = user_input

            if len(input_content) > 1000:
                raise IOError(
                    'Length of provided content exceeds 1000 characters. \n\n'
                )
            
            state.note_content = input_content
            
            report: str = database_manager.add_note(
                username=state.username,
                title=state.note_title,
                content=state.note_content
            )

            report += (
                'Enter one of the available '
                'interactive commands to proceed. \n\n'
            )
            
            state.reset()
            
            return report
        
        case _:
            raise IOError('Unrecognized stage. \n\n')