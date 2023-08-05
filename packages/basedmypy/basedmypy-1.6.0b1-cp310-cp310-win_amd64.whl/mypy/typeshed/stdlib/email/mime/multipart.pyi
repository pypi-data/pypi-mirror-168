from collections.abc import Sequence
from email import _ParamsType
from email.message import Message
from email.mime.base import MIMEBase
from email.policy import Policy

__all__ = ["MIMEMultipart"]

class MIMEMultipart(MIMEBase):
    def __init__(
        self,
        _subtype: str = ...,
        boundary: str | None = ...,
        _subparts: Sequence[Message] | None = ...,
        *,
        policy: Policy | None = ...,
        **_params: _ParamsType,
    ) -> None: ...
