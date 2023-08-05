from datetime import datetime, timedelta

from kih_api import global_common
from kih_api.wise.models import Transaction, Account, UserProfile, ProfileType

account = Account.get_by_profile_type_and_currency(ProfileType.Personal, global_common.Currency.NZD)
test = Transaction.get_all(account, datetime.now() - timedelta(days=30), datetime.now())
pass