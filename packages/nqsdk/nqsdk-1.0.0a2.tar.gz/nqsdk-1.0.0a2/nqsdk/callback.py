"""
Copyright (c) 2022 Inqana Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .enums import CallbackStatus

if TYPE_CHECKING:  # pragma: no cover
    from .abstract.message import SentMeta


class CallbackResponse:
    def __init__(self, *, status: CallbackStatus, meta: SentMeta = None, error: str = None):
        self._status = status
        self._meta = meta
        self._error = error

    @property
    def status(self) -> CallbackStatus:
        return self._status

    @property
    def meta(self) -> Optional[SentMeta]:
        return self._meta

    @property
    def error(self) -> Optional[str]:
        return self._error

    def get_code(self) -> int:
        """HTTP status code."""
        if self.status == CallbackStatus.OK:
            return 204
        else:
            return 400

    def get_content_type(self) -> Optional[str]:
        """Content type header value, e.g. `application/json`."""

    def get_content(self) -> Optional[str]:
        """Content as string."""
