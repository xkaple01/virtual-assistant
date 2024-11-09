import mesop as me
import mesop.labs as mel

from backend.bot import Commands, transform 

from frontend.styles import STYLE_CE, STYLE_CL, STYLE_CC
from frontend.styles import STYLE_HINT, STYLE_HINT_MT, STYLE_HINT_MB
from frontend.styles import STYLE_CMD, STYLE_CMD_MB


def page_body() -> None:
    with me.box(style=STYLE_CE):
        with me.box(style=STYLE_CL):
            me.text(text='Type one of the available', style=STYLE_HINT_MT)
            me.text(text='interactive commands:', style=STYLE_HINT_MB)

            me.text(text=f'{Commands.HELLO.value}', style=STYLE_CMD_MB)
            
            me.text(text=f'{Commands.ADD_USER.value}', style=STYLE_CMD)
            me.text(text=f'{Commands.REMOVE_USER.value}', style=STYLE_CMD_MB)

            me.text(text=f'{Commands.ADD_NOTE.value}', style=STYLE_CMD)
            me.text(text=f'{Commands.REMOVE_NOTE.value}', style=STYLE_CMD_MB)

            me.text(text=f'{Commands.SHOW_USER.value}', style=STYLE_CMD)
            me.text(text=f'{Commands.SHOW_NOTES.value}', style=STYLE_CMD)
            me.text(text=f'{Commands.SHOW_DATABASE.value}', style=STYLE_CMD_MB)

            me.text(text=f'{Commands.EXIT.value}', style=STYLE_CMD_MB)

            me.text(text='And follow instructions', style=STYLE_HINT)
            me.text(text='provided by virtual assistant.', style=STYLE_HINT_MB)

        with me.box(style=STYLE_CC):
            mel.chat(transform=transform, bot_user='Bot')
