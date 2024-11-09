import mesop as me
from frontend.bot import page_body


@me.page(
    path='/',
    title='Virtual Assistant',
    on_load=lambda e: me.set_theme_mode(theme_mode='dark'),
    security_policy=me.SecurityPolicy(dangerously_disable_trusted_types=True),
)
def page_main() -> None:
    page_body()