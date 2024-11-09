import mesop as me


@me.stateclass
class State:
    command: str = ''
    stage: int = 0
   
    username: str = ''
    email: str = ''
    phone: str = ''
    
    note_title: str = ''
    note_content: str = ''

    def reset(self) -> None:
        self.command = ''
        self.stage = 0

        self.username = ''
        self.email = ''
        self.phone = ''

        self.note_title = ''
        self.note_content = ''
