"""django.contrib.auth.tokens, but without using last_login in hash"""

from datetime import datetime
from django.conf import settings
from .models import Token

class TokenGenerator(object):
    """
    Strategy object used to generate and check tokens
    """

    TOKEN_TIMEOUT_DAYS = getattr(settings, "TOKEN_TIMEOUT_DAYS", 7)

    def make_token(self, user):
        """
        Returns a token for a given user
        """
        return self._make_token_with_timestamp(user, self._now())

    def delete_token(self, user):
        try:
            tokens = Token.objects.filter(user=user)
            tokens.delete()
        except Token.DoesNotExist:
            pass
        return True

    def check_token(self, user, token):
        """
        Check that a token is correct for a given user.
        """
        try:
            valid_tokens = Token.objects.filter(user=user)
        except Token.DoesNotExist:
            return False

        for valid_token in valid_tokens:
            if valid_token.hash == token:
                return True
                
        return False

    def _make_token_with_timestamp(self, user, timestamp):

        try:
            from hashlib import sha1 as sha_constructor
        except ImportError:
            from django.utils.hashcompat import sha_constructor

        hash = sha_constructor(settings.SECRET_KEY + unicode(user.id) +
            user.password +
            unicode(timestamp)).hexdigest()[::2]

        self.delete_token(user)

        token = Token(user = user, hash = hash)
        token.save()
        return hash

    def _now(self):
        # Used for mocking in tests
        return datetime.today()


token_generator = TokenGenerator()
