import mesop as me


COLOR_HINT: str = '#eb984e'
COLOR_CMD: str = '#d2b4de'

MARGIN_L32: me.Margin = me.Margin(left='32px')
MARGIN_T24: me.Margin = me.Margin(top='24px')
MARGIN_B24: me.Margin = me.Margin(bottom='24px')

STYLE_CE: me.Style = me.Style(
    width='100%',
    height='100%',
    display='flex',
    flex_direction='row'
)

STYLE_CL: me.Style = me.Style(
    width='calc(30% - 32px)',
    display='flex',
    flex_direction='column',
    margin=MARGIN_L32
)

STYLE_CC: me.Style = me.Style(
    width='40%'
)

STYLE_HINT: me.Style = me.Style(color=COLOR_HINT)
STYLE_HINT_MT: me.Style = me.Style(color=COLOR_HINT, margin=MARGIN_T24)
STYLE_HINT_MB: me.Style = me.Style(color=COLOR_HINT, margin=MARGIN_B24)

STYLE_CMD: me.Style = me.Style(color=COLOR_CMD)
STYLE_CMD_MB: me.Style = me.Style(color=COLOR_CMD, margin=MARGIN_B24)