import logging
import typing as T

import requests
from lxml import etree as et

from maildiscover.common import get_domain_from_email, MethodFailed, MailConfig, SvcConf


logger = logging.getLogger(__name__)


class Autoconfig(object):
    def __init__(self, email: T.Text, insecure: bool = False) -> None:
        """
        This class implements the autoconfig flow for config retrieval.

        Instantiate it passing just the email address and try to retrieve
        the configuration with the `get` method. You can enable insecure
        (http) retrieval specifying `insecure=True`.
        """
        self.email = email
        self.domain = get_domain_from_email(email)
        self.insecure = insecure

    def _try_get(self, url: T.Text) -> T.Optional[MailConfig]:
        try:
            resp = requests.get(url)
            if resp.status_code == 200 and resp.content:
                return self._parse(resp.content)
        except Exception as e:
            logger.error(e)
            return None

    @classmethod
    def _parse(cls, response: bytes) -> MailConfig:
        imap = None
        imaps = None
        pop3 = None
        pop3s = None
        submission = None
        smtp = None

        tree = et.XML(response)

        _imap = tree.xpath('//incomingServer[@type="imap"]')
        if _imap:
            for srv in _imap:
                imaps = cls._maybe_parse_srv(srv, "SSL", imaps)
                imap = cls._maybe_parse_srv(srv, "STARTTLS", imap)

        _pop3 = tree.xpath('//incomingServer[@type="pop3"]')
        if _pop3:
            for srv in _pop3:
                pop3s = cls._maybe_parse_srv(srv, "SSL", pop3s)
                pop3 = cls._maybe_parse_srv(srv, "STARTTLS", pop3)

        _smtp = tree.xpath('//outgoingServer[@type="smtp"]')
        if _smtp:
            for srv in _smtp:
                smtp = cls._maybe_parse_srv(srv, "SSL", smtp)
                submission = cls._maybe_parse_srv(srv, "STARTTLS", submission)

        return MailConfig(
            imap=imap,
            imaps=imaps,
            pop3=pop3,
            pop3s=pop3s,
            submission=submission,
            smtp=smtp,
        )

    @classmethod
    def _maybe_parse_srv(
        cls,
        node: et._Element,
        opt: T.Text,
        cur: T.Optional[SvcConf],
    ) -> T.Optional[SvcConf]:
        if cur:
            return cur
        if node.xpath(f'./socketType="{opt}"'):
            _host = node.xpath("./hostname")
            if len(_host) != 1:
                return None
            _port = node.xpath("./port")
            if len(_port) != 1:
                return None
            _auth = [a.text for a in node.xpath("./authentication")]

            return SvcConf(
                _host[0].text,
                int(_port[0].text),
                _auth,
            )

    def _get(self, proto: T.Text) -> T.Optional[MailConfig]:
        for url in [
            f"{proto}://autoconfig.thunderbird.net/v1.1/{self.domain}",
            f"{proto}://autoconfig.{self.domain}/mail/config-v1.1.xml?emailaddress={self.email}",  # noqa: E501
            f"{proto}://{self.domain}/.well-known/autoconfig/mail/config-v1.1.xml",
        ]:
            res = self._try_get(url)
            if res:
                return res
            logger.debug("Failed with request to: %s", url)
        return None

    def get(self) -> MailConfig:
        if res := self._get("https"):
            return res

        if self.insecure:
            if res := self._get("http"):
                return res

        raise MethodFailed
