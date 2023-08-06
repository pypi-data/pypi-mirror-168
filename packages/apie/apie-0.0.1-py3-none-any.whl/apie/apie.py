import os
import logging
import shutil
import jsonpickle
from pathlib import Path
import eons as e
import traceback
from flask import Flask
from flask import request
from waitress import serve

######## START CONTENT ########
# All APIer errors
class APIError(Exception): pass


# Exception used for miscellaneous API errors.
class OtherAPIError(APIError): pass

# Authenticator is a Functor which validates whether or not a request is valid.
# The inputs will be the method and path of the request and the request authentication.
# If you need to check whether the request parameters, data, files, etc. are valid, please do so in your endpoint.
# By limiting what we pass to an Authenticator, we speed up the authentication process for all requests.
# Because this class will be invoked often, we have made some performant modifications to the default UserFunctor methods.
# NOTE: All logic for *this should be in UserFunction. There are no extra functions called (e.g. PreCall, PostCall, etc.)
# UserFunction should either return False or raise an exception if the provided request is invalid and should return True if it is.
class Authenticator(e.UserFunctor):
    def __init__(this, name="Authenticator"):
        super().__init__(name)

        this.requiredKWArgs.append('path')
        
        this.optionalKWArgs['auth'] = None


    # Override of eons.Functor method. See that class for details
    # NOTE: All logic for *this should be in UserFunction. There are no extra functions called (e.g. PreCall, PostCall, etc.)
    # UserFunction should either return False or raise an exception if the provided request is invalid and should return True if it is.
    def UserFunction(this):
        return True

    # This will be called whenever an unauthorized request is made.
    def Unauthorized(this):
        return "Unauthorized", 401

    # Override of eons.Functor method. See that class for details
    def ValidateArgs(this):
        for rkw in this.requiredKWArgs:
            if (hasattr(this, rkw)):
                continue

            fetched = this.Fetch(rkw)
            if (fetched is not None):
                this.Set(rkw, fetched)
                continue

            # Nope. Failed.
            errStr = f"{rkw} required but not found."
            logging.error(errStr)
            raise MissingArgumentError(f"argument {rkw} not found in {this.kwargs}") #TODO: not formatting string??

        for okw, default in this.optionalKWArgs.items():
            if (hasattr(this, okw)):
                continue

            this.Set(okw, this.Fetch(okw, default=default))

    # Override of eons.Functor method. See that class for details
    def __call__(this, **kwargs) :
        this.kwargs = kwargs
        
        this.ParseInitialArgs()
        this.ValidateArgs()
        return this.UserFunction()
        

class APIE(e.Executor):

    def __init__(this):
        super().__init__(name="Application Program Interface with eons", descriptionStr="A readily extensible take on APIs.")

        # this.RegisterDirectory("ebbs")

        this.optionalKWArgs['host'] = "0.0.0.0"
        this.optionalKWArgs['port'] = 80
        this.optionalKWArgs['clean_start'] = True
        this.optionalKWArgs['authenticator'] = "none"

        this.supportedMethods = [
            'POST',
            'GET',
            'PUT',
            'DELETE',
            'PATCH'
        ]


    # Configure class defaults.
    # Override of eons.Executor method. See that class for details
    def Configure(this):
        super().Configure()

        this.defualtConfigFile = "apie.json"


    # Override of eons.Executor method. See that class for details
    def RegisterAllClasses(this):
        super().RegisterAllClasses()
        this.RegisterAllClassesInDirectory(str(Path(__file__).resolve().parent.joinpath("api")))
        this.RegisterAllClassesInDirectory(str(Path(__file__).resolve().parent.joinpath("auth")))


    # Acquire and run the given endpoint with the given request.
    def ProcessEndpoint(this, endpoint, request, **kwargs):
        endpoint = this.GetRegistered(endpoint, "api")
        return endpoint(executor=this, request=request, **kwargs)


    # What to do when a request causes an exception to be thrown.
    def HandleBadRequest(this, request):
        return "Bad request", 400


    # Override of eons.Executor method. See that class for details
    def UserFunction(this):
        super().UserFunction()

        if (this.clean_start):
            this.Clean()

        this.auth = this.GetRegistered(this.authenticator, "auth")

        this.flask = Flask(this.name)

        @this.flask.route("/", defaults={"path": ""}, methods = this.supportedMethods)
        def root(path):
            return "It works!", 200

        @this.flask.route("/<string:path>", methods = this.supportedMethods)
        @this.flask.route("/<path:path>", methods = this.supportedMethods)
        def handler(path):
            try:
                if (this.auth(executor=this, path=path, auth=request.authorization)):
                    endpoints = path.split('/')
                    return this.ProcessEndpoint(endpoints.pop(0), request, next=endpoints)
                else:
                    return this.auth.Unauthorized()
            except Exception as error:
                traceback.print_exc()
                logging.error(str(error))
                return this.HandleBadRequest(request)

        options = {}
        options['app'] = this.flask
        options['host'] = this.host
        options['port'] = this.port

        # Only applicable if using this.flask.run(**options)
        # if (this.args.verbose > 0):
        #     options['debug'] = True
        #     options['use_reloader'] = False

        serve(**options)


    # Remove possibly stale modules.
    def Clean(this):
        repoPath = Path(this.repo['store'])
        if (repoPath.exists()):
            shutil.rmtree(this.repo['store'])
        repoPath.mkdir(parents=True, exist_ok=True)

# Endpoints are what is run when a given request is successfully authenticated.
# Put all your actual API logic in these!
# Keep in mind that Endpoints will be made available in a just-in-time, as-needed basis. There is no need to preload logic, etc.
# That also means that each Endpoint should operate in isolation and not require any other Endpoint to function.
# The exception to this isolation is when Endpoints are intended to be called in sequence.
# Any number of Endpoints can be chained together in any order. The behavior of the first affects the behavior of the last.
# This allows you to create generic "upload" Endpoints, where what is uploaded is determined by the preceding Endpoint.
# For example, you might have 3 Endpoints: "package", "photo", and "upload"; both package and photo set a member called "file_data"; upload Fetches "file_data" and puts it somewhere; you can thus use upload with either predecessor (e.g. .../package/upload and .../photo/upload).
# What is returned by an Endpoint is the very last Endpoint's return value. All intermediate values are skipped (so you can throw errors if calling things like .../package without a further action).
# NOTE: Endpoints should be published as api_s (i.e. projectType="api")
class Endpoint(e.UserFunctor):
    def __init__(this, name=e.INVALID_NAME()):
        super().__init__(name)

        this.enableRollback = False

        this.requiredKWArgs.append('request')
        
        this.optionalKWArgs['next'] = []
        this.optionalKWArgs['cachable'] = False
        this.optionalKWArgs['mode'] = 'json' #or html

        #this.response is returned by UserFunction().
        this.response = {}
        this.response['content_data'] = {}
        this.response['content_string'] = ""
        this.response['code'] = 200


    # Call things!
    # Override this or die.
    def Call(this):
        pass


    # Override this to perform whatever success checks are necessary.
    # Override of eons.Functor method. See that class for details
    def DidCallSucceed(this):
        return True


    # API compatibility shim
    def DidUserFunctionSucceed(this):
        return this.DidCallSucceed()


    # Hook for any pre-call configuration
    # Override of eons.Functor method. See that class for details
    def PreCall(this):
        pass


    # Hook for any post-call configuration
    # Override of eons.Functor method. See that class for details
    def PostCall(this):
        pass

    # Called right before *this returns.
    # Handles json pickling, etc.
    def ProcessResponse(this):
        if (this.mode == 'json'):
            if (len(this.response['content_string'])):
                logging.warning(f"Clobbering content_string ({this.response['content_string']})")

            this.response['content_string'].update({'cachable': this.cachable})
            this.response['content_string'] = jsonpickle.encode(this.response['content_data'])

    # Override of eons.Functor method. See that class for details
    def UserFunction(this):
        this.Call()
        if (not this.next):
            this.ProcessResponse()
            return this.response['content_data'], this.response['code']
        return this.CallNext()


    def CallNext(this):
        return this.executor.ProcessEndpoint(this.next.pop(0), this.request, predecessor=this, next=this.next)


    #### SPECIALIZED OVERRIDES. IGNORE THESE ####


    #Grab any known and necessary args from this.kwargs before any Fetch calls are made.
    def ParseInitialArgs(this):
        super().ParseInitialArgs()
        if ('predecessor' in this.kwargs):
            this.predecessor = this.kwargs.pop('predecessor')
        else:
            this.predecessor = None


    # Will try to get a value for the given varName from:
    #    first: this
    #    second: the endpoint preceding *this
    #    third: the executor (args > config > environment)
    # RETURNS the value of the given variable or None.
    def Fetch(this,
        varName,
        default=None,
        enableThis=True,
        enableExecutor=True,
        enableArgs=True,
        enableExecutorConfig=True,
        enableEnvironment=True,
        enablePrecedingEndpoint=True):
            
        # Duplicate code from eons.UserFunctor in order to establish precedence.
        if (enableThis and hasattr(this, varName)):
            logging.debug("...got {varName} from self ({this.name}).")
            return getattr(this, varName)

        if (enablePrecedingEndpoint and this.predecessor is not None):
            val = this.predecessor.Fetch(varName, default, enableThis, enableExecutor, enableArgs, enableExecutorConfig, enableEnvironment, enablePrecedingEndpoint)
            if (val is not None):
                logging.debug(f"...got {varName} from predecessor.")
                return val
        else: #No need to call the super method multiple times if the predecessor already did.
            return super().Fetch(varName, default, enableThis, enableExecutor, enableArgs, enableExecutorConfig, enableEnvironment)

