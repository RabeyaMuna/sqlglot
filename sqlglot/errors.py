from __future__ import annotations

import typing as t
from enum import auto

from sqlglot.helper import AutoName


class ErrorLevel(AutoName):
    IGNORE = auto()
    """Ignore all errors."""

    WARN = auto()
    """Log all errors."""

    RAISE = auto()
    """Collect all errors and raise a single exception."""

    IMMEDIATE = auto()
    """Immediately raise an exception on the first error found."""


class SqlglotError(Exception):
    pass


class UnsupportedError(SqlglotError):
    pass


class ParseError(SqlglotError):
    def __init__(
        self,
        message: str,
        errors: list[dict[str, t.Any]] | None = None,
    ):
        super().__init__(message)
        self.errors = errors or []

    @classmethod
    def new(
        cls,
        message: str,
        description: str | None = None,
        line: int | None = None,
        col: int | None = None,
        start_context: str | None = None,
        highlight: str | None = None,
        end_context: str | None = None,
        into_expression: str | None = None,
    ) -> ParseError:
        return cls(
            message,
            [
                {
                    "description": description,
                    "line": line,
                    "col": col,
                    "start_context": start_context,
                    "highlight": highlight,
                    "end_context": end_context,
                    "into_expression": into_expression,
                }
            ],
        )


class TokenError(SqlglotError):
    pass


class OptimizeError(SqlglotError):
    pass


class SchemaError(SqlglotError):
    pass


class ExecuteError(SqlglotError):
    pass


def concat_messages(errors: t.Sequence[t.Any], maximum: int) -> str:
    msg = [str(e) for e in errors[:maximum]]
    remaining = len(errors) - maximum
    if remaining > 0:
        msg.append(f"... and {remaining} more")
    return "\n\n".join(msg)


def merge_errors(errors: t.Sequence[ParseError]) -> list[dict[str, t.Any]]:
    return [e_dict for error in errors for e_dict in error.errors]
