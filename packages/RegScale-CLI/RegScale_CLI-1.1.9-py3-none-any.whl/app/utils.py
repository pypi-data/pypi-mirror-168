#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """
import re

from app.application import Application
from app.login import is_licensed
from exceptions.license_exception import LicenseException


def check_license():
    """Check RegScale License

    Raises:
        LicenseException: Custom Exception

    Returns:
        Application: application instance
    """
    app = Application()
    if not is_licensed(app):
        raise LicenseException(
            "This feature is limited to RegScale Enterprise, please check RegScale license"
        )
    return app


def validate_mac_address(mac_address: str) -> bool:
    """Simple validation of a mac address input

    Args:
        mac_address (str): mac address

    """
    if re.match(
        "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower()
    ):
        return True
    return False
