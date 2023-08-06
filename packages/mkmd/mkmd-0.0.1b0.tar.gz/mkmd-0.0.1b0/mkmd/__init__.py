from __future__ import annotations

import inspect
import io
from pathlib import Path
import textwrap
from typing import Any, Optional, TextIO

from . import utils

class Markdown:
    def __init__(
        self,
        width: Optional[int] = None,
    ):
        self.lines: list[str] = []
        self._width = width
    
    @classmethod
    def from_string(
        cls,
        text: str,
        *args: Any,
        **kwargs: Any,
    ) -> Markdown:
        """
        Loads document from string.
        """
        md = cls(*args, **kwargs)
        md.lines.extend(text.splitlines())
        
        return md
    
    @classmethod
    def from_file(
        cls,
        path: str | Path | TextIO,
        *args: Any,
        **kwargs: Any,
    ) -> Markdown:
        """
        Loads document from file.
        """
        if isinstance(path, io.TextIOBase):
            return cls.from_string(path.read())
        return cls.from_string(Path(path).read_text())
    
    def __str__(self) -> str:
        return "\n".join(self.lines)
    
    def save(self, path: str | Path | TextIO) -> None:
        """
        Parameters
        ----------
        path
            A file-like object or path to save contents
            to.
            
        Example
        -------
        .. code-block:: python
           
           # these are all ewuivalent:
           
           with open("document.md", "w") as f:
               md.save(f)
           
           md.save("document.md")
           
           md.save(Path("document.md"))
        """
        if isinstance(path, io.TextIOBase):
            path = path.write(str(self))
            return
        
        path = Path(path)
        path.write_text(str(self))
    
    def _wrap(
        self,
        text: str,
    ) -> str:
        return text if self._width is None else textwrap.wrap(
            text,
            drop_whitespace = False,
            break_on_hyphens = False,
            width = self._width
        )
    
    def add_lines(
        self,
        *lines: Optional[str],
    ) -> None:
        """
        Adds lines.
        
        .. note::
           This method should only used by subclasses. Usually
           the wrapper method :meth:`add_paragraph` does the
           job.
        
        Parameters
        ----------
        lines
            Lines to add. ``None`` will be skipped.
        """
        self.lines.extend(self._wrap(l) for l in lines if l is not None)
    
    def add_heading(
        self,
        text: str,
        level: int = 1,
        alternate: bool = True,
    ) -> None:
        """
        Parameters
        ----------
        text
            The content of the heading.
        
        level
            A heading level between 1 and 7 inclusive.
        
        alternate
            Uses hyphens and equal signs respectively instead
            of number signs for heading level 1 and 2.
        """
        assert level in range(1, 7)
        
        if alternate and level in [1, 2]:
            lines = [
                text,
                ("=" if level == 1 else "-") * len(text)
            ]
        
        else:
            lines = [f"{'#' * level} {text}"]
        
        self.add_paragraph(*lines, wrapped = False)
    
    def add_paragraph(
        self,
        *lines: Optional[str],
        wrapped: bool = True,
    ) -> None:
        """
        Adds a paragraph.
        
        Parameters
        ----------
        lines
            Lines to add. ``None`` will be skipped.
        
        wrapped
            Whether the text should be wrapped. Useful when
            using indented multiline strings.
        """
        multiple = len(lines) != 1 or lines is None
        
        if multiple:
            lines = [l for l in lines if l is not None]
        
        else:
            if wrapped and not multiple:
                lines = inspect.cleandoc(lines[0])
            
            lines = lines.splitlines()
        
        self.add_lines(
            "" if self.lines and not utils._blank(self.lines[-1]) else None,
            *lines,
            ""
        )
    
    def add_codeblock(
        self,
        text: str,
        language: Optional[str] = None,
    ) -> None:
        """
        Adds a code block.
        
        Parameters
        ----------
        text
            The content of the code block.
        
        language
            The programming language of the content.
        """
        # TODO: escape ```
        # TODO: ignore width
        
        self.add_paragraph(
            "```" + ("" if language is None else language),
            inspect.cleandoc(text),
            "```",
        )
    
    def add_horizontal_rule(
        self,
        style: str = "-",
        width: Optional[int] = None,
    ) -> None:
        """
        Adds a horizontal rule
        
        Parameters
        ----------
        style
            What characters to use for the horizontal rule.
            One of ``*``, ``-`` or ``_``.
        
        width
            The width of the horizontal rule. Defaults to
            :attr:`width` if provided otherwise `20`.
        """
        assert style in "*-_"
        
        if width is None:
            if self.width is None:
                width = 20
            
            else:
                width = self.width
        
        self.add_paragraph(style * width)
    
    def add_reference(
        self,
        label: str,
        url: str,
        title: Optional[str] = None,
    ) -> None:
        """
        Adds a reference.
        
        Parameters
        ----------
        label
            The unique lable of the reference.
        
        url
            The url to link to.
        
        title
            An optional title to use.
        """
        self.add_lines(
            "",
            f"[{label}]: <{utils._url_escape(url)}>" + ("" if title is None else f' "{title}"')
        )
    
    def add_image(
        self,
        alt_text: str,
        path_or_url: str | Path,
        title: Optional[str] = None,
        link: Optional[str] = None,
    ) -> None:
        """
        Adds an image.
        
        Parameters
        ----------
        alt_text
            The alternative text to display.
        
        path_or_url
            Path or url of image to display.
            
            .. note::
               Paths are relative from the markdown document and
               not the python file.
        
        title
            An optional title to use.
        
        link
            Optional url to link to.
        """
        text = f"![{alt_text}][{path_or_url}" + ("" if title is None else f' "{title}"') + "]"
        
        if link is not None:
            text = utils.link(text, link)
        
        self.add_paragraph(text)
    
    def add_unordered_list(
        self,
        *items: str,
        style: str = "-",
    ) -> None:
        """
        Adds an unordered list.
        
        Parameters
        ----------
        items
            All list items.
        
        style
            What characters to use list.
            One of ``-``, ``*`` or ``+``.
        """
        # TODO: initial indent when width is reached
        assert style in "-*+"
        
        self.add_paragraph(*(f"{style} {item}" for item in items))
    
    def add_ordered_list(
        self,
        *items: str,
    ) -> None:
        """
        Adds an ordered list.
        
        Parameters
        ----------
        items
            All list items.
        """
        self.add_paragraph(*(
            f"{number}. {item}" for number, item in enumerate(items, start = 1)
        ))

