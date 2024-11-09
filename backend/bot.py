import mesop as me
import mesop.labs as mel
from enum import Enum

from backend.state_machine.state import State
from backend.state_machine.add_user import StagesAddUser, interact_add_user
from backend.state_machine.remove_user import StagesRemoveUser, interact_remove_user
from backend.state_machine.add_note import StagesAddNote, interact_add_note
from backend.state_machine.remove_note import StagesRemoveNote, interact_remove_note
from backend.state_machine.show_user import StagesShowUser, interact_show_user
from backend.state_machine.show_notes import StagesShowNotes, interact_show_notes
from backend.state_machine.show_database import StagesShowDatabase, interact_show_database


class Commands(Enum):
    INITIAL = ''

    HELLO = 'hello'

    ADD_USER = 'add-user'
    REMOVE_USER = 'remove-user'
    
    ADD_NOTE = 'add-note'
    REMOVE_NOTE = 'remove-note'

    SHOW_USER = 'show-user'
    SHOW_NOTES = 'show-notes'
    SHOW_DATABASE = 'show-database'

    EXIT = 'exit'


def detect_command(user_input: str) -> None:
    state: State = me.state(state=State)

    cmd: str = user_input.lower()

    match cmd:
        case _ if Commands.HELLO.value in cmd:
            return (
                'Hi! Please, enter one of the available '
                'interactive commands to proceed. \n\n'
            )
        
        case _ if Commands.ADD_USER.value in cmd:
            state.command = Commands.ADD_USER.value
            state.stage = StagesAddUser.GET_USERNAME_ASK_EMAIL.value
            return (
                'Follow instructions '
                'to add the new user to the database. \n\n'
                '1. Enter the new username. \n\n'
                'Example: Username1 \n\n'
                'Provided username must be unique in the database. '
                'Username can contain only letters A-z and digits 0-9. \n\n'
            )
            
        case _ if Commands.REMOVE_USER.value in cmd:
            state.command = Commands.REMOVE_USER.value
            state.stage = StagesRemoveUser.GET_USERNAME_END_DIALOG.value
            return (
                'Follow instructions '
                'to remove an existing user from the database. \n\n'
                '1. Enter an existing username. \n\n'
                'Example: Username1 \n\n'
                'Username can contain only letters A-z and digits 0-9. \n\n'
            )
       
        case _ if Commands.ADD_NOTE.value in cmd:
            state.command = Commands.ADD_NOTE.value
            state.stage = StagesAddNote.GET_USERNAME_ASK_TITLE.value
            return (
                'Follow steps below '
                'to add the new note to the database. \n\n'
                '1. Enter the username of note author present in the database. \n\n'
                'Example: Username1 \n\n'
                'Username can contain only letters A-z and digits 0-9. \n\n'
            )

        case _ if Commands.REMOVE_NOTE.value in cmd:
            state.command = Commands.REMOVE_NOTE.value
            state.stage = StagesRemoveNote.GET_USERNAME_ASK_TITLE.value
            return (
                'Follow steps below ' 
                'to remove an existing note from the database. \n\n'
                '1. Enter the username of note author present in the database. \n\n'
                'Example: Username1 \n\n'
                'Username can contain only letters A-z and digits 0-9. \n\n'
            )

        case _ if Commands.SHOW_USER.value in cmd:
            state.command = Commands.SHOW_USER.value
            state.stage = StagesShowUser.GET_USERNAME_END_DIALOG.value
            return (
                'Provide the following data items '
                'to get detailed information '
                'about the user present in the database. \n\n'
                '1. Enter an exising username. \n\n'
                'Example: Username1 \n\n'
                'Username can contain only letters A-z and digits 0-9. \n\n'
            )

        case _ if Commands.SHOW_NOTES.value in cmd:
            state.command = Commands.SHOW_NOTES.value
            state.stage = StagesShowNotes.GET_USERNAME_END_DIALOG.value
            return (
                'Provide the following data items '
                'to display the notes written by a specified user. \n\n'
                '1. Enter an existing username. \n\n'
                'Example: Username1 \n\n'
                'Username can contain only letters A-z and digits 0-9. \n\n'
            )

        case _ if Commands.SHOW_DATABASE.value in cmd:
            state.command = Commands.SHOW_DATABASE.value
            state.stage = StagesShowDatabase.GET_NUMBER_END_DIALOG.value
            return (
                'Provide the following data items '
                'to get the usernames recently added to the database. \n\n'
                '1. Enter the maximum number usernames to be displayed. \n\n'
                'Example: 10 \n\n'
                'Number of users must be an integer from 1 to 100. \n\n'
            )
        
        case _ if Commands.EXIT.value in cmd:
            return (
                'Goodbye! '
                'You can refresh the page to start the new conversation.'
            )
            
        case _:
            return f'Please, enter one of the available interactive commands.'


def transform(user_input: str, history: list[mel.ChatMessage]) -> str:
    state: State = me.state(state=State)

    try:
        match state.command:
            case Commands.INITIAL.value:
                return detect_command(user_input=user_input)
            case Commands.ADD_USER.value:
                return interact_add_user(user_input=user_input)
            case Commands.REMOVE_USER.value:
                return interact_remove_user(user_input=user_input)
            case Commands.ADD_NOTE.value:
                return interact_add_note(user_input=user_input)
            case Commands.REMOVE_NOTE.value:
                return interact_remove_note(user_input=user_input)
            case Commands.SHOW_USER.value:
                return interact_show_user(user_input=user_input)
            case Commands.SHOW_NOTES.value:
                return interact_show_notes(user_input=user_input)
            case Commands.SHOW_DATABASE.value:
                return interact_show_database(user_input=user_input)
            case _:
                raise ValueError('Unrecognized command.')
    except:
        state.reset()
        return (
            'Provided data items do not satisfy requirements. '
            'To repeat the procedure '
            'please enter one of the available interactive commands '
        )