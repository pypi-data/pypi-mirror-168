import typing as T

from maildiscover.common import MailConfig, SvcConf, MethodFailed, MalformedEmail
from maildiscover.autoconfig import Autoconfig
from maildiscover.dns import DNSSRV


def get(email: T.Text) -> MailConfig:
    """
    This is the main entrypoint of the library. This function requires the email
    address as input and tries all the methods available, with sane defaults.
    If some succeeds, it merges the results and returns them as a `MailConfig`
    object.
    """
    try:
        dns = DNSSRV(email)
        dns_cfg = dns.get()
    except MethodFailed:
        dns_cfg = None

    try:
        ac = Autoconfig(email)
        ac_cfg = ac.get()
    except MethodFailed:
        ac_cfg = None

    if dns_cfg is not None and ac_cfg is not None:
        return dns_cfg.merge(ac_cfg)
    elif dns_cfg is not None:
        return dns_cfg
    elif ac_cfg is not None:
        return ac_cfg
    else:
        return MailConfig()
