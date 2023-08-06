import logging
import typing as T

import dns.resolver

from maildiscover.common import get_domain_from_email, MethodFailed, MailConfig, SvcConf

logger = logging.getLogger(__name__)


class DNSSRV(object):
    _svc_map: T.Dict[T.Text, T.Text] = {
        "imap": "_imap._tcp",
        "imaps": "_imaps._tcp",
        "pop3": "_pop3._tcp",
        "pop3s": "_pop3s._tcp",
        "submission": "_submission._tcp",
        "smtp": "_smtp._tcp",
    }

    def __init__(self, email: T.Text) -> None:
        """
        This class implements connection information retrieval from canonical
        dns SRV records.

        Instantiate it passing just the email address and try to retrieve the
        configuration with the `get` method.
        """
        self.email = email
        self.domain = get_domain_from_email(email)

    def _try_get(self, svc: T.Text) -> T.Optional[SvcConf]:
        try:
            sub_dom = self._svc_map[svc]
            resp = dns.resolver.resolve(f"{sub_dom}.{self.domain}", "SRV")
            return self._parse(resp)
        except Exception as e:
            logger.error(e)
            return None

    @classmethod
    def _parse(cls, resp: T.Any) -> T.Optional[SvcConf]:
        try:
            parts = resp.rrset.to_text().split()
            if not parts:
                return None
            host = parts[-1]
            if len(host) < 1 or host == ".":
                return None
            else:
                # drop last . in dns name
                host = host[:-1]
            port = parts[-2]
            if not port or port == "0":
                return None
            else:
                port = int(port)

            return SvcConf(host, port, [])
        except Exception as e:
            logger.error(e)
            return None

    def get(self) -> MailConfig:
        imap = self._try_get("imap")
        imaps = self._try_get("imaps")
        pop3 = self._try_get("pop3")
        pop3s = self._try_get("pop3s")
        submission = self._try_get("submission")
        smtp = self._try_get("smtp")

        if all([conf is None for conf in (imap, imaps, pop3, pop3s, submission, smtp)]):
            raise MethodFailed

        return MailConfig(
            imap=imap,
            imaps=imaps,
            pop3=pop3,
            pop3s=pop3s,
            submission=submission,
            smtp=smtp,
        )
