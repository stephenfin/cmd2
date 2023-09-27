import sys
from typing import (
    Any,
    Callable,
    IO,
    Optional,
    TextIO,
    Union,
)

from rich import Console

try:
    from typing import (
        Protocol,
        runtime_checkable,
)
except ImportError:
    from typing_extensions import (  # type: ignore[misc]
        Protocol,
        runtime_checkable,
    )


class Cmd2PrintProtocol(Protocol):
    debug: bool

    def print_to(
        self,
        dest: Union[TextIO, IO[str]],
        msg: Any,
        *,
        end: str = '\n',
        style: Optional[Callable[[str], str]] = None,
        paged: bool = False,
        chop: bool = False,
    ) -> None:
        """Print output to the specified stream with the provided style and format options.

        :param dest: Destination stream to write to.
        :param msg: object to print
        :param end: string appended after the end of the message, default a newline
        :param style: Optional style format function to apply
        :param paged: If True, pass the output through the configured pager.
        :param chop: If paged is True, True to truncate long lines or False to wrap long lines.
        """

    def poutput(
        self,
        msg: Any = '',
        *,
        end: str = '\n',
        apply_style: bool = True,
        paged: bool = False,
        chop: bool = False,
    ) -> None:
        """Print message to self.stdout and appends a newline by default

        Also handles BrokenPipeError exceptions for when a command's output has
        been piped to another process and that process terminates before the
        cmd2 command is finished executing.

        :param msg: object to print
        :param end: string appended after the end of the message, default a newline
        :param apply_style: If True, then ansi.style_output will be applied to the message text. Set to False in cases
                            where the message text already has the desired style. Defaults to True.
        :param paged: If True, pass the output through the configured pager.
        :param chop: If paged is True, True to truncate long lines or False to wrap long lines.
        """

    # noinspection PyMethodMayBeStatic
    def perror(
        self,
        msg: Any = '',
        *,
        end: str = '\n',
        apply_style: bool = True,
        paged: bool = False,
        chop: bool = False,
    ) -> None:
        """Print message to sys.stderr

        :param msg: object to print
        :param end: string appended after the end of the message, default a newline
        :param apply_style: If True, then ansi.style_error will be applied to the message text. Set to False in cases
                            where the message text already has the desired style. Defaults to True.
        :param paged: If True, pass the output through the configured pager.
        :param chop: If paged is True, True to truncate long lines or False to wrap long lines.
        """

    def psuccess(
        self,
        msg: Any = '',
        *,
        end: str = '\n',
        paged: bool = False,
        chop: bool = False,
    ) -> None:
        """Writes to stdout applying ansi.style_success by default

        :param msg: object to print
        :param end: string appended after the end of the message, default a newline
        :param paged: If True, pass the output through the configured pager.
        :param chop: If paged is True, True to truncate long lines or False to wrap long lines.
        """

    def pwarning(
        self,
        msg: Any = '',
        *,
        end: str = '\n',
        apply_style: bool = True,
        paged: bool = False,
        chop: bool = False,
    ) -> None:
        """Wraps perror, but applies ansi.style_warning by default

        :param msg: object to print
        :param end: string appended after the end of the message, default a newline
        :param apply_style:
            If True, then ansi.style_warning will be applied to the message text. Set to False in cases
            where the message text already has the desired style. Defaults to True.

            .. deprecated: 2.4.4
                Use :meth:`~cmd2.Cmd.print_to` instead to print to stderr without style applied.
        :param paged: If True, pass the output through the configured pager.
        :param chop: If paged is True, True to truncate long lines or False to wrap long lines.
        """

    def pfailure(
        self,
        msg: Any = '',
        *,
        end: str = '\n',
        paged: bool = False,
        chop: bool = False,
    ) -> None:
        """Writes to stderr applying ansi.style_error by default

        :param msg: object to print
        :param end: string appended after the end of the message, default a newline
        :param paged: If True, pass the output through the configured pager.
        :param chop: If paged is True, True to truncate long lines or False to wrap long lines.
        """

    def pexcept(self, msg: Any, *, end: str = '\n', apply_style: bool = True) -> None:
        """Print Exception message to sys.stderr. If debug is true, print exception traceback if one exists.

        :param msg: message or Exception to print
        :param end: string appended after the end of the message, default a newline
        :param apply_style: If True, then ansi.style_error will be applied to the message text. Set to False in cases
                            where the message text already has the desired style. Defaults to True.
        """

    def pfeedback(
        self,
        msg: Any,
        *,
        end: str = '\n',
        apply_style: bool = True,
        paged: bool = False,
        chop: bool = False,
    ) -> None:
        """For printing nonessential feedback.  Can be silenced with `quiet`.
        Inclusion in redirected output is controlled by `feedback_to_output`.

        :param msg: object to print
        :param end: string appended after the end of the message, default a newline
        :param apply_style: If True, then ansi.style_output will be applied to the message text. Set to False in cases
                            where the message text already has the desired style. Defaults to True.
        :param paged: If True, pass the output through the configured pager.
        :param chop: If paged is True, True to truncate long lines or False to wrap long lines.
        """


class RichCmd(Cmd2PrintProtocol):
    """
    Mixin class that swaps out the cmd2.Cmd output calls to use the ``rich`` library.

    NOTE: Mixin classes should be placed to the left of the base Cmd class in the inheritance declaration.
    """
    def __init__(self, *args, **kwargs) -> None:
        super(RichCmd, self).__init__(*args, **kwargs)
        self.rich_out = Console(file=self.stdout)
        self.rich_err = Console(stderr=True)

    def pexcept(self, msg: Any, *, end: str = '\n', apply_style: bool = True) -> None:
        if self.debug and sys.exc_info() != (None, None, None):
            self.rich_err.print_exception(show_locals=True)
        else:
            super().pexcept(msg, end=end, apply_style=apply_style)
