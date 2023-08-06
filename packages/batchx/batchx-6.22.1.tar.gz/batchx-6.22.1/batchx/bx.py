import grpc
import jwt  # pip install pyJWT, ATTENTION, no pip install jwt!!
import time
import os
import logging
from datetime import datetime
from retry import retry

from . import auth_pb2
from . import auth_pb2_grpc

# CONSTANTS
BX_HEADER_TOKEN_NAME = "bx_token"
CHANNEL_TIMEOUT = 40  # In seconds
LOGGER = logging.getLogger('batchx');

# CONFIG
CALL_DELAY = 0.5      # Initial delay (in seconds) between remote method call attempts.
CALL_BACKOFF = 2      # Multiplier applied to delay between attempts.
CALL_MAX_DELAY = 60   # Maximum value of delay (in seconds).
MAX_TRIES = 10        # The maximum number of attempts. default: -1 (infinite).
CALL_TIMEOUT = 60     # Unary call timeout in seconds.

channel = None  # Connection managed at module level. One common channel for all service classes within the module.
bx_token = None
access_token = None
bx_endpoint = None


class RecoverableException(Exception):
    """Raised when a recoverable error occurs.
    It's used just to detect failed connections attempts and try again.
    So, do nothing.
    """
    pass


def is_recoverable(exception):
    if exception is None or exception.code() is None:
        return False
    if grpc.StatusCode.PERMISSION_DENIED == exception.code():
        return check()
    return grpc.StatusCode.NOT_FOUND != exception.code() and \
           grpc.StatusCode.ALREADY_EXISTS != exception.code() and \
           grpc.StatusCode.UNKNOWN != exception.code() and \
           grpc.StatusCode.INVALID_ARGUMENT != exception.code() and \
           grpc.StatusCode.FAILED_PRECONDITION != exception.code() and \
           grpc.StatusCode.UNAUTHENTICATED != exception.code()


def connect():
    connect_to(os.environ["BATCHX_ENDPOINT"], os.environ["BATCHX_TOKEN"], "BATCHX_SECURE_CONNECTION" not in os.environ.keys() or os.environ["BATCHX_SECURE_CONNECTION"]!="OFF");

@retry(RecoverableException, delay=CALL_DELAY, backoff=CALL_BACKOFF, max_delay=CALL_MAX_DELAY, tries=MAX_TRIES)
def connect_to(endpoint, token, secure):
    global channel, bx_token, bx_endpoint
    if channel is None:
        try:
            if secure:
                channel = grpc.secure_channel(endpoint, grpc.ssl_channel_credentials(), options={
                    "grpc.keepalive_time_ms": 30000,
                    'grpc.keepalive_timeout_ms': 30*60*1000,
                    'grpc.keepalive_permit_without_calls': True
                }.items())
            else:
                channel = grpc.insecure_channel(endpoint)
            grpc.channel_ready_future(channel).result(CHANNEL_TIMEOUT)
        except grpc.FutureTimeoutError as exc:
            channel = None
            raise RecoverableException
    bx_token = token
    bx_endpoint = endpoint


def channel_is_working():
    global channel
    if channel is not None:
        try:
            grpc.channel_ready_future(channel).result(CHANNEL_TIMEOUT)
            return True
        except grpc.FutureTimeoutError:
            pass
    return False


def current_access_token_is_valid():
    global access_token
    if access_token is None:
        return False
    else:
        access_token_dict = jwt.decode(access_token, options={"verify_signature":False})
        return access_token_dict['exp'] > time.time()

# Refreshes the current token. Returns False if it was already valid
def check():
    """Check whether there exist a working channel and a valid access token."""
    global bx_endpoint, bx_token
    if not channel_is_working() and bx_endpoint is not None and bx_token is not None:
        connect(bx_endpoint, bx_token)
    if not current_access_token_is_valid():
        login()
        return True
    return False


@retry(RecoverableException, delay=CALL_DELAY, backoff=CALL_BACKOFF, max_delay=CALL_MAX_DELAY, tries=MAX_TRIES)
def make_call(func, request, auth_required=True, include_timeout=True):
    """Wrapper to manage remote method calls. It implements a retry policy with exponential backoff.

    :param str func: Function in charge of calling remote methods.
    :param str request: grpc message.
    :param str auth_required: if set to True or not passed, token header will be sent.
    :param str include_timeout: if set to True or not passed, default GRPC deadline will be set.
    :return: response returned by executing the function passed as parameter (func).
    """
    try:
        if include_timeout:
            timeout = CALL_TIMEOUT
        else:
            timeout = None;
        if auth_required:
            return func(request, metadata=[(BX_HEADER_TOKEN_NAME, access_token)], timeout=timeout)
        else:
            return func(request, timeout=timeout)
    except grpc.RpcError as exc:
        if is_recoverable(exc):
            raise RecoverableException  # If error is recoverable, retry call
        else:
            raise exc


def login():
    """ Connect to server and obtain an access token if needed."""
    global channel, bx_token, access_token
    if bx_token is not None:
        token = jwt.decode(bx_token, options={"verify_signature":False});
        if token['batchx-token-type'] == 'refresh':
            request_data = auth_pb2.RefreshTokenRequest(user_name=token['batchx-id'], refresh_token=bx_token)
            response = make_call(auth_pb2_grpc.AuthServiceStub(channel).RefreshToken, request_data, auth_required=False)
            access_token = response.access_token
        else:
            access_token = bx_token
    else:
        raise Exception("Batchx token not set. Please run: bx.connect()")

