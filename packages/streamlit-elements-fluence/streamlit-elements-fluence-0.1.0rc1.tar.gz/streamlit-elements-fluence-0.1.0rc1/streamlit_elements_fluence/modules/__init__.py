from streamlit_elements_fluence.modules.callbacks import sync, lazy, partial
from streamlit_elements_fluence.modules.dashboard import Dashboard
from streamlit_elements_fluence.modules.editors import Editors
from streamlit_elements_fluence.modules.events import Events
from streamlit_elements_fluence.modules.html import HTML
from streamlit_elements_fluence.modules.media import Media
from streamlit_elements_fluence.modules.mui import MUI
from streamlit_elements_fluence.modules.nivo import Nivo
from streamlit_elements_fluence.modules.extras import Extras

__all__ = [
    "dashboard",
    "editor",
    "event",
    "html",
    "lazy",
    "media",
    "mui",
    "nivo",
    "partial",
    "sync",
    "extras",
]


dashboard = Dashboard()
editor = Editors()
event = Events()
html = HTML()
media = Media()
mui = MUI()
nivo = Nivo()
extras = Extras()
