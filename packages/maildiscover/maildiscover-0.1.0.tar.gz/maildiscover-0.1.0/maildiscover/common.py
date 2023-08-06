from dataclasses import dataclass, field
import re
import typing as T


class MalformedEmail(Exception):
    def __init__(self, email: T.Text, *args, **kwargs) -> None:
        self.email = email
        super().__init__(*args, **kwargs)


class MethodFailed(Exception):
    pass


class ConflictingConfigs(Exception):
    pass


@dataclass
class SvcConf(object):
    host: T.Optional[T.Text] = None
    port: T.Optional[int] = None
    auth_type: T.List[T.Text] = field(default_factory=lambda: [])

    def to_tuple(self) -> T.Tuple[T.Optional[T.Text], T.Optional[int], T.List[T.Text]]:
        return (self.host, self.port, self.auth_type)

    def merge(self, other: "SvcConf") -> "SvcConf":
        if other is None:
            return self

        if self.host is None:
            self.host = other.host
        elif other.host is not None and other.host != self.host:
            raise ConflictingConfigs

        if self.port is None:
            self.port = other.port
        elif other.port is not None and other.port != self.port:
            raise ConflictingConfigs

        self.auth_type.extend(other.auth_type)
        self.auth_type = list(set(self.auth_type))

        return self


@dataclass
class MailConfig(object):
    """The output configuration is represented by this class"""

    imap: T.Optional[SvcConf] = None
    imaps: T.Optional[SvcConf] = None
    pop3: T.Optional[SvcConf] = None
    pop3s: T.Optional[SvcConf] = None
    submission: T.Optional[SvcConf] = None
    smtp: T.Optional[SvcConf] = None

    def merge(self, other: "MailConfig") -> "MailConfig":
        for attr in [
            _attr for _attr in self.__dict__.keys() if not _attr.startswith("_")
        ]:
            if this := getattr(self, attr):
                this.merge(getattr(other, attr))
            else:
                setattr(self, attr, getattr(other, attr))

        return self

    def imap_str(self) -> T.Text:
        if self.imap:
            return f"{self.imap.host}:{self.imap.port}"

        return ""

    def imaps_str(self) -> T.Text:
        if self.imaps:
            return f"{self.imaps.host}:{self.imaps.port}"

        return ""

    def pop3_str(self) -> T.Text:
        if self.pop3:
            return f"{self.pop3.host}:{self.pop3.port}"

        return ""

    def pop3s_str(self) -> T.Text:
        if self.pop3s:
            return f"{self.pop3s.host}:{self.pop3s.port}"

        return ""

    def submission_str(self) -> T.Text:
        if self.submission:
            return f"{self.submission.host}:{self.submission.port}"

        return ""

    def smtp_str(self) -> T.Text:
        if self.smtp:
            return f"{self.smtp.host}:{self.smtp.port}"

        return ""

    def to_dict(self) -> T.Dict[T.Text, T.Tuple[T.Text, int, T.List[T.Text]]]:
        """
        Convert the dataclass to a dict
        >>> config = MailConfig(
        ... imap=SvcConf("mail.example.com", 143, ["plain"]),
        ... submission=SvcConf("smtp.example.com", 587, ["plain", "OAuth2"]),
        ... )
        >>> config.to_dict()
        {'imap': ('mail.example.com', 143, ['plain']), 'submission': ('smtp.example.com', 587, ['plain', 'OAuth2'])}
        """
        result = {}
        for attr in [
            _attr for _attr in self.__dict__.keys() if not _attr.startswith("_")
        ]:
            if cfg := getattr(self, attr):
                result[attr] = cfg.to_tuple()

        return result


MAIL_RE = re.compile(r"^([^@]+)@([^@]+)$")


def get_domain_from_email(email: T.Text) -> T.Text:
    """Get the domain from the email or raise"""
    res = MAIL_RE.findall(email)
    if len(res) != 1 or len(res[0]) != 2:
        raise MalformedEmail(email)

    return res[0][1]
