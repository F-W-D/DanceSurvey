from typing import Optional

from data.dancers import Dancer
import services.data_service as svc

active_account: Dancer = None


def reload_account():
    global active_account
    if not active_account:
        return

    active_account = svc.find_account_by_email(active_account.email)
