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


from . import tag_pb2
from . import tag_pb2_grpc
class TagService:

    def CreateTag(self, request):
        check()
        return make_call(tag_pb2_grpc.TagServiceStub(channel).CreateTag, request)

    def DeleteTag(self, request):
        check()
        return make_call(tag_pb2_grpc.TagServiceStub(channel).DeleteTag, request)

    def DisableTag(self, request):
        check()
        return make_call(tag_pb2_grpc.TagServiceStub(channel).DisableTag, request)

    def GetTag(self, request):
        check()
        return make_call(tag_pb2_grpc.TagServiceStub(channel).GetTag, request)

    def ListEnvironmentTags(self, request):
        check()
        return make_call(tag_pb2_grpc.TagServiceStub(channel).ListEnvironmentTags, request)

    def UpdateTag(self, request):
        check()
        return make_call(tag_pb2_grpc.TagServiceStub(channel).UpdateTag, request)


from . import organization_pb2
from . import organization_pb2_grpc
class OrganizationService:

    def CreateOrganization(self, request):
        check()
        return make_call(organization_pb2_grpc.OrganizationServiceStub(channel).CreateOrganization, request)

    def GetOrganization(self, request):
        check()
        return make_call(organization_pb2_grpc.OrganizationServiceStub(channel).GetOrganization, request)

    def HandleInvitation(self, request):
        check()
        return make_call(organization_pb2_grpc.OrganizationServiceStub(channel).HandleInvitation, request)

    def InviteMember(self, request):
        check()
        return make_call(organization_pb2_grpc.OrganizationServiceStub(channel).InviteMember, request)

    def UpdateOrganization(self, request):
        check()
        return make_call(organization_pb2_grpc.OrganizationServiceStub(channel).UpdateOrganization, request)


from . import picture_pb2
from . import picture_pb2_grpc
class PictureService:

    def CompleteUpload(self, request):
        check()
        return make_call(picture_pb2_grpc.PictureServiceStub(channel).CompleteUpload, request)

    def CropPicture(self, request):
        check()
        return make_call(picture_pb2_grpc.PictureServiceStub(channel).CropPicture, request)

    def Upload(self, request):
        check()
        return make_call(picture_pb2_grpc.PictureServiceStub(channel).Upload, request)


from . import image_pb2
from . import image_pb2_grpc
class ImageService:

    def AreImageExamplesCloned(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).AreImageExamplesCloned, request)

    def CloneImage(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).CloneImage, request)

    def CloneImageExamples(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).CloneImageExamples, request)

    def DeleteImage(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).DeleteImage, request)

    def GetImage(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).GetImage, request)

    def GetPushCredentials(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).GetPushCredentials, request)

    def ImportImage(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).ImportImage, request)

    def ListImageExamples(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).ListImageExamples, request)

    def ListImages(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).ListImages, request)

    def RemoveImageExample(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).RemoveImageExample, request)

    def SearchImages(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).SearchImages, request)

    def SetImageExample(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).SetImageExample, request)

    def ShareImage(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).ShareImage, request)

    def TagImage(self, request):
        check()
        return make_call(image_pb2_grpc.ImageServiceStub(channel).TagImage, request)


from . import token_pb2
from . import token_pb2_grpc
class TokenService:

    def AddToken(self, request):
        check()
        return make_call(token_pb2_grpc.TokenServiceStub(channel).AddToken, request)


from . import health_pb2
from . import health_pb2_grpc
class HealthService:


from . import profile_pb2
from . import profile_pb2_grpc
class ProfileService:


from . import auth_pb2
from . import auth_pb2_grpc
class AuthService:

    def ConfirmForgotPassword(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).ConfirmForgotPassword, request)

    def ConfirmSignup(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).ConfirmSignup, request)

    def ForgotPassword(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).ForgotPassword, request)

    def GoogleSignin(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).GoogleSignin, request)

    def GoogleSignup(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).GoogleSignup, request)

    def Login(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).Login, request)

    def RefreshToken(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).RefreshToken, request)

    def ResendSignupConfirmationCode(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).ResendSignupConfirmationCode, request)

    def RevokeRefreshToken(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).RevokeRefreshToken, request)

    def Signup(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).Signup, request)

    def StartSignup(self, request):
        check()
        return make_call(auth_pb2_grpc.AuthServiceStub(channel).StartSignup, request)


from . import user_pb2
from . import user_pb2_grpc
class UserService:

    def GetUser(self, request):
        check()
        return make_call(user_pb2_grpc.UserServiceStub(channel).GetUser, request)

    def ListAlerts(self, request):
        check()
        return make_call(user_pb2_grpc.UserServiceStub(channel).ListAlerts, request)

    def UpdateUser(self, request):
        check()
        return make_call(user_pb2_grpc.UserServiceStub(channel).UpdateUser, request)


from . import environment_pb2
from . import environment_pb2_grpc
class EnvironmentService:

    def GetEnvironment(self, request):
        check()
        return make_call(environment_pb2_grpc.EnvironmentServiceStub(channel).GetEnvironment, request)

    def ListRegions(self, request):
        check()
        return make_call(environment_pb2_grpc.EnvironmentServiceStub(channel).ListRegions, request)


from . import admin_pb2
from . import admin_pb2_grpc
class AdminService:

    def AddEnvironmentCredits(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).AddEnvironmentCredits, request)

    def CreateMembership(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).CreateMembership, request)

    def CreateOrg(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).CreateOrg, request)

    def CreateUser(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).CreateUser, request)

    def GeneratePromoCode(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).GeneratePromoCode, request)

    def GetGlobalProperties(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).GetGlobalProperties, request)

    def RemoveUser(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).RemoveUser, request)

    def SetGlobalProperty(self, request):
        check()
        return make_call(admin_pb2_grpc.AdminServiceStub(channel).SetGlobalProperty, request)


from . import filesystem_pb2
from . import filesystem_pb2_grpc
class FilesystemService:

    def CancelUpload(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).CancelUpload, request)

    def CompleteUpload(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).CompleteUpload, request)

    def Copy(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).Copy, request)

    def DeleteFile(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).DeleteFile, request)

    def DownloadPresigned(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).DownloadPresigned, request)

    def GetBlob(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).GetBlob, request)

    def GetFile(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).GetFile, request)

    def ListBlobPointers(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ListBlobPointers, request)

    def ListBlobs(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ListBlobs, request)

    def ListFolder(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ListFolder, request)

    def ReportUploadStatus(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ReportUploadStatus, request)

    def SetBlobStatus(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).SetBlobStatus, request)

    def ShareFile(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).ShareFile, request)

    def UploadPresigned(self, request):
        check()
        return make_call(filesystem_pb2_grpc.FilesystemServiceStub(channel).UploadPresigned, request)


from . import consumer_pb2
from . import consumer_pb2_grpc
class ConsumerService:

    def GetMetrics(self, request):
        check()
        return make_call(consumer_pb2_grpc.ConsumerServiceStub(channel).GetMetrics, request)


from . import common_pb2
from . import common_pb2_grpc
class CommonService:


from . import docker_pb2
from . import docker_pb2_grpc
class DockerService:


from . import audit_pb2
from . import audit_pb2_grpc
class AuditService:

    def ListEvents(self, request):
        check()
        return make_call(audit_pb2_grpc.AuditServiceStub(channel).ListEvents, request)


from . import provider_pb2
from . import provider_pb2_grpc
class ProviderService:

    def GetMetrics(self, request):
        check()
        return make_call(provider_pb2_grpc.ProviderServiceStub(channel).GetMetrics, request)

    def ListPayouts(self, request):
        check()
        return make_call(provider_pb2_grpc.ProviderServiceStub(channel).ListPayouts, request)

    def ListRevenueByCustomer(self, request):
        check()
        return make_call(provider_pb2_grpc.ProviderServiceStub(channel).ListRevenueByCustomer, request)

    def ListRevenueByTools(self, request):
        check()
        return make_call(provider_pb2_grpc.ProviderServiceStub(channel).ListRevenueByTools, request)


from . import job_pb2
from . import job_pb2_grpc
class JobService:

    def Cancel(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).Cancel, request)

    def CloseWorkflow(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).CloseWorkflow, request)

    def CreateWorkflow(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).CreateWorkflow, request)

    def Delete(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).Delete, request)

    def DeleteWorkflow(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).DeleteWorkflow, request)

    def GetComputationalCost(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).GetComputationalCost, request)

    def GetJob(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).GetJob, request)

    def GetLogs(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).GetLogs, request)

    def GetWorkflow(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).GetWorkflow, request)

    def GetWorkflowGraph(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).GetWorkflowGraph, request)

    def ListJobs(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).ListJobs, request)

    def ListWorkflows(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).ListWorkflows, request)

    def Stream(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).Stream, request, include_timeout=False)

    def Submit(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).Submit, request)

    def TagJob(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).TagJob, request)

    def TagWorkflow(self, request):
        check()
        return make_call(job_pb2_grpc.JobServiceStub(channel).TagWorkflow, request)

    def Run(self, submit_request):
        submit_response = self.Submit(submit_request)
        if submit_response.WhichOneof("case") == "suggested_parameters":
            raise Exception("Unsupported job parametrization. Suggested one is: " + str(submit_response.suggested_parameters))
        request_stream = self.StreamRequest(environment=submit_request.environment, job_id=submit_response.job_id, logs_enabled=True)
        return self.__ProcessStream(submit_request, request_stream)

    @retry(RecoverableException, delay=CALL_DELAY, backoff=CALL_BACKOFF, max_delay=CALL_MAX_DELAY, tries=MAX_TRIES)
    def __ProcessStream(self, submit_request, request_stream):
        try:
            response = self.Stream(request_stream)
            for r in response:
                for job_event in r.event:
                    if job_event.WhichOneof("type") == "job_status":
                        LOGGER.warning("["+request_stream.environment+"#"+str(request_stream.job_id)+"] Job status: " + job_pb2.Status.Name(job_event.job_status))
                    elif job_event.WhichOneof("type") == "log_record":
                        LOGGER.warning("["+request_stream.environment+"#"+str(request_stream.job_id)+"|"+request_stream.environment+"@"+submit_request.image+"] ["+str(datetime.fromtimestamp(job_event.log_record.ts_millis/1000.0))+"] " +  job_event.log_record.message)
                    elif job_event.WhichOneof("type") == "return_value":
                        return job_event.return_value;
        except grpc.RpcError as exc:
            if is_recoverable(exc):
                raise RecoverableException  # If error is recoverable, retry call
            else:
                raise exc


from . import log_pb2
from . import log_pb2_grpc
class LogService:

