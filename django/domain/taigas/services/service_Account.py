from django.utils import timezone
from typing import List, Optional

# Models
from ..models import Account

import logging
logger = logging.getLogger(__name__)


def get_accounts() -> List[Account]:
    accounts = Account.objects.all()
    logger.info(f"{accounts} fetched")
    return accounts


def get_account_by_id(account_id: int) -> Account:
    account = Account.objects.filter(id=account_id).first()
    logger.info(f"{account} fetched")
    return account


def get_account_by_email(email: str) -> Optional[Account]:
    accounts = Account.objects.filter(email=email)

    if accounts.exists():
        account = accounts.first()
        logger.info(f"{account} fetched")
        return account

    logger.info(f"No account found with email {email}.")
    return None


def delete_account(account: Account) -> Account:
    account.delete()
    logger.info(f"{account} has been deleted.")
    return account


def create_account(
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        project_id: int,
        project_name: str,
        project_slug: str,
        project_description: str
) -> Account:

    account = Account.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        project_id=project_id,
        project_name=project_name,
        project_slug=project_slug,
        project_description=project_description
    )

    account.save()

    logger.info(f"\"{account.email}\" has been created")

    return account


def update_account(
        account: Account,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        # password: str,
        project_id: int,
        project_name: str,
        project_slug: str,
        project_description: str
) -> Account:
    account.username = username
    account.first_name = first_name
    account.last_name = last_name
    account.email = email
    # account.password = password
    account.project_id = project_id
    account.project_name = project_name
    account.project_slug = project_slug
    account.project_description = project_description
    account.updated_at = timezone.now()

    account.save()

    logger.info(f"\"{account.email}\" has been updated.")

    return account
