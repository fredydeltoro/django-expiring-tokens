django-expiring tokens
================

This Django application provides token-based authentication for your APIs. By default, creating a new token for a user
invalidates all existing tokens for that user.

This application is based on jpulgarian's [django-tokenapi](https://github.com/jpulgarin/django-tokenapi). In the
django-tokenapi implementation, tokens are based on a timestamp and timeout and are not stored in the database. This
has some advantages, but makes it impossible to invalidate tokens before they expire.

django-expiring-tokens solves this problem by storing tokens in the database. By default, creating a new token for a
user invalidates any existing tokens for that use. You can also manually invalidate a token by deleting it.

Usage
-----

### Obtaining a Token

You can obtain a token for a specific user by sending a POST request with a
username and password parameter to the `api_token_new` view.
Using [curl][], the request would look like:

    curl -d "username=jpulgarin&password=GGGGGG" http://www.yourdomain.com/token/new.json

[curl]: http://curl.haxx.se/

If the request is successful, you will receive a JSON response like so:

    {"success": true, "token": "2uy-420a8efff7f882afc20d", "user": 1}

An invalid username and password pair will produce a response like so:

    {"success": false, "errors": "Unable to log you in, please try again"}

You should store the `user` and `token` that are returned on the client
accessing the API, as all subsequent calls will require that the request have
a valid token and user pair.

### Verifying a Token

You can verify that a token matches a given user by sending a GET request
to the `api_token` view, and sending the token and user as part of the URL.
Using curl it would look like:

    curl http://www.yourdomain.com/token/2uy-420a8efff7f882afc20d/1.json

If valid, you will receive the following JSON response:

    {"success": true}

### Writing API Compatible Views

To allow a view to be accessed through token-based auth, use the
`tokenapi.decorators.token_required` decorator. There are also
JSON helper functions to make it easier to deal with JSON.
This is an example of an API compatible view:

    from tokenapi.decorators import token_required
    from tokenapi.http import JsonResponse, JsonError

    @token_required
    def index(request):
        if request.method == 'POST':
            data = {
                'test1': 49,
                'test2': 'awesome',
            }
            return JsonResponse(data)
        else:
            return JsonError("Only POST is allowed")

### Using a Token

The client can access any API compatible view by sending a request to it,
and including `user` and `token` as request parameters (either GET or POST).
Accessing the example view above using curl might look like:

    curl -d "user=1&token=2uy-420a8efff7f882afc20d" http://www.yourdomain.com/index.json

You would receive the following response:

    {"success": true, "test1": 49, "test2": "awesome"}


Alternately, you can access any API compatible view by including the user and token in
the Authorization header according to the
[basic access authentication](http://en.wikipedia.org/wiki/Basic_access_authentication)
scheme. To construct the Authorization header:

1. Combine user id and token into string "user:token"
2. Encode resulting string using Base64
3. Prepend "Basic " (including the trailing space) to the resulting Base64 encoded string
	
If, in the same request, you provide credentials via both request parameters and the
Authorization header, the Authorization header will be used for authentication.

Acknowledgements
----------------

Based heavily on jpulgarian's [django-tokenapi](https://github.com/jpulgarin/django-tokenapi), which is in turn based on
`django.contrib.auth.tokens`.
