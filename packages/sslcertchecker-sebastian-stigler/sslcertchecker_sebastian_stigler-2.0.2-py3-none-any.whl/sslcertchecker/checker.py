"""
    COPYRIGHT (C) 2016 by Sebastian Stigler

    NAME
        checker.py -- check ssl certificats


    FIRST RELEASE
        2016-12-09  Sebastian Stigler  sebastian.stigler@hs-aalen.de

"""
import argparse
import datetime
import os.path
import socket
import ssl
import sys

from colorama import init, Fore, Back, Style
import yaml

from sslcertchecker import __version__

__author__ = "Sebastian Stigler"
__copyright__ = "Sebastian Stigler"
__license__ = "mit"


class AlreadyExpired(Exception):
    pass


class ExpiresSoon(Exception):
    pass


def ssl_expiry_datetime(hostname):
    ssl_date_fmt = r"%b %d %H:%M:%S %Y %Z"

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 3 second timeout because Lambda has runtime limitations
    conn.settimeout(3.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    # parse the string from the certificate into a Python datetime object
    return datetime.datetime.strptime(ssl_info["notAfter"], ssl_date_fmt)


def ssl_valid_time_remaining(hostname):
    """Get the number of days left in a cert's lifetime."""
    expires = ssl_expiry_datetime(hostname)
    return expires - datetime.datetime.utcnow()


def ssl_expires_in(hostname, buffer_days=14):
    """Check if `hostname` SSL cert expires is within `buffer_days`.

    Raises `AlreadyExpired` if the cert is past due
    """
    remaining = ssl_valid_time_remaining(hostname)

    # if the cert expires in less than two weeks, we should reissue it
    if remaining < datetime.timedelta(days=0):
        # cert has already expired - uhoh!
        raise AlreadyExpired("Cert expired %s days ago." % remaining.days)
    elif remaining < datetime.timedelta(days=buffer_days):
        # expires sooner than the buffer
        raise ExpiresSoon("Cert expires in %s days." % remaining.days)
    else:
        # everything is fine
        return remaining.days


def parse_args(args):
    """
    Parse command line parameters

    :param args: command line parameters as list of strings
    :return: command line parameters as :obj:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="Check ssl certificates for expiredate"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="sslcertchecker {ver}".format(ver=__version__),
    )
    parser.add_argument("-H", "--host", dest="host", help="Check a single host")
    parser.add_argument(
        "-d",
        "--days",
        dest="days",
        type=int,
        default=14,
        help="Warn X days before the cert expires [default: %(default)d)]",
    )
    return parser.parse_args(args)


def make_output(host, days):
    """create an output"""
    init(autoreset=True)
    print("[" + Style.BRIGHT + Fore.LIGHTYELLOW_EX + host, end="")
    space = "-" * int((52 - len(host)))
    print("] " + space + "> ", end="")
    try:
        remaining = ssl_expires_in(host, days)
    except AlreadyExpired as exc:
        print(Fore.RED + str(exc))
    except ExpiresSoon as exc:
        print(Fore.YELLOW + str(exc))
    except Exception as exc:
        print(Back.YELLOW + Fore.RED + str(exc))
    else:
        print(Fore.GREEN + "OK (valid for %3d days)" % remaining)


def main(args):
    args = parse_args(args)
    if args.host:
        make_output(args.host, args.days)
    else:
        try:
            with open(os.path.expanduser("~/.sslcertcheck.yml")) as stream:
                hosts = yaml.load(stream, Loader=yaml.SafeLoader)
        except Exception as exc:
            print(Back.YELLOW + Fore.MAGENTA + str(exc))
        for host in hosts:
            make_output(host, args.days)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()


# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
