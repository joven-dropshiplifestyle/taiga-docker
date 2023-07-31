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


def check_email_exists(email: str) -> bool:
    with connections['taiga_db'].cursor() as cursor:
        cursor.execute("""
            SELECT id, email, user_id, project_id FROM public.projects_membership
            WHERE email = %s
        """, [email])
        row = cursor.fetchone()

    return row is not None


def check_user_exists(user_id: int) -> bool:
    with connections['taiga_db'].cursor() as cursor:
        cursor.execute("""
            SELECT id, email, user_id, project_id FROM public.projects_membership
            WHERE user_id = %s
        """, [str(user_id)])
        row = cursor.fetchone()

    return row is not None


def get_user_id_by_email(email: str) -> Optional[int]:
    with connections['taiga_db'].cursor() as cursor:
        cursor.execute("""
            SELECT id, username, email, is_active, full_name, new_email
            FROM public.users_user WHERE email=%s
        """, [email])
        row = cursor.fetchone()

    if row is not None:
        return row[0]

    return None