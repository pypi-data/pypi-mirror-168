from typing import Optional

def _blank(text: str) -> bool:
    return not text or text.isspace()

def _url_escape(url: str) -> str:
    return url.replace(" ", "%20")

#def escape(text: str) -> str:
#    # https://www.markdownguide.org/basic-syntax/#characters-you-can-escape

def italic(text: str) -> str:
    return f"*{text}*"

def bold(text: str) -> str:
    return f"**{text}**"

def bold_and_italic(text: str) -> str:
    return f"***{text}***"

def link(url: str, title: Optional[str] = None) -> str:
    url = _url_escape(url)
    
    if title is None:
        return f"<{url}>"
    
    else:
        return f"[{title}]({url})"

def email(adresse: str) -> str:
    return f"<{adresse}>"

def refer(text: str, label: str) -> str:
    return f"[{text}][{label}]"
