from django.db import connections
from typing import Optional


def get_token_by_email(email: str) -> Optional[str]:
    with connections['taiga_db'].cursor() as cursor:
        cursor.execute("""
            SELECT token FROM public.projects_membership
            WHERE email = %s
            ORDER BY id ASC
        """, [email])
        row = cursor.fetchone()

    if row is not None:
        return row[0]

    return None
