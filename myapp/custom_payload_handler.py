import uuid
from datetime import datetime, timedelta
from rest_framework_jwt.compat import get_username, get_username_field


def custom_payload_handler(user):
    username_field = get_username_field()
    username = get_username_field()

    payload = {
        'user_id': user.id,
        'username': user.email,
        'exp': datetime.utcnow() + timedelta(seconds=50)
    }
    if hasattr(user, 'email'):
        payload['email'] = user.email
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    payload[username_field] = username

    return payload
