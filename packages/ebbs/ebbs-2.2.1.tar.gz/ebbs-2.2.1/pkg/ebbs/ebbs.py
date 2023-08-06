import os
import logging
import eons as e
from pathlib import Path
import shutil
import jsonpickle

######## START CONTENT ########
# All builder errors
class BuildError(Exception): pass


# Exception used for miscellaneous build errors.
class OtherBuildError(BuildError): pass


# Project types can be things like "lib" for library, "bin" for binary, etc. Generally, they are any string that evaluates to a different means of building code.
class ProjectTypeNotSupported(BuildError): pass


class EBBS(e.Executor):

    def __init__(this):
        super().__init__(name="eons Basic Build System", descriptionStr="A hackable build system for all builds!")

        # this.RegisterDirectory("ebbs")


    #Configure class defaults.
    #Override of eons.Executor method. See that class for details
    def Configure(this):
        super().Configure()

        this.defualtConfigFile = "build.json"


    #Override of eons.Executor method. See that class for details
    def RegisterAllClasses(this):
        super().RegisterAllClasses()
        # this.RegisterAllClassesInDirectory(os.path.join(os.path.dirname(os.path.abspath(__file__)), "build"))


    #Override of eons.Executor method. See that class for details
    def AddArgs(this):
        super().AddArgs()
        this.argparser.add_argument('-b','--build', type = str, metavar = 'cpp', help = 'script to use for building', dest = 'builder')
        this.argparser.add_argument('-e','--event', type = str, action='append', nargs='*', metavar = 'release', help = 'what is going on that triggered this build?', dest = 'events')


    #Override of eons.Executor method. See that class for details
    def ParseArgs(this):
        super().ParseArgs()

        this.args.path = os.getcwd() #used to be arg; now we hard code
        this.rootPath = str(Path(this.args.path).resolve())

        this.events = set()
        if (this.args.events is not None):
            [[this.events.add(str(e)) for e in l] for l in this.args.events]

        if (not this.args.builder):
            logging.debug("No build specified. Assuming build pipeline is written in config.")


    #Override of eons.Executor method. See that class for details
    def InitData(this):
        this.rootPath = Path(this.Fetch('path', '../')).resolve() #ebbs is usually called from a build folder in a project, i.e. .../build/../ = /


    #Override of eons.Executor method. See that class for details
    def UserFunction(this):
        super().UserFunction()
        build_in = this.extraArgs.pop('build_in', this.Fetch('build_in', default="build"))
        if (this.Execute(this.args.builder, this.args.path, build_in, this.events, **this.extraArgs)):
            logging.info("Build process complete!")
        else:
            logging.info("Build failed.")


    #Run a build script.
    #RETURNS whether or not the build was successful.
    def Execute(this, build, path, build_in, events, **kwargs):
        if (build is None or not build):
            builder = Builder("EMPTY")
        else:
            builder = this.GetRegistered(build, "build")
        prettyPath = str(Path(path).joinpath(build_in).resolve())
        logging.debug(f"Executing {build} in {prettyPath} with events {events} and additional args: {kwargs}")
        builder(executor=this, path=path, build_in=build_in, events=events, **kwargs)
        return builder.DidBuildSucceed()


class Builder(e.UserFunctor):
    def __init__(this, name=e.INVALID_NAME()):
        super().__init__(name)

        # What can this build, "bin", "lib", "img", ... ?
        this.supportedProjectTypes = []

        this.projectType = None
        this.projectName = None

        this.clearBuildPath = False

        this.configNameOverrides = {
            "name": "projectName",
            "type": "projectType",
            "clear_build_path": "clearBuildPath"
        }

        this.enableRollback = False


    # Build things!
    # Override this or die.
    # Empty Builders can be used with build.json to start build trees.
    def Build(this):
        pass


    # Override this to perform whatever success checks are necessary.
    # This will be called before running the next build step.
    def DidBuildSucceed(this):
        return True


    # API compatibility shim
    def DidUserFunctionSucceed(this):
        return this.DidBuildSucceed()


    # Hook for any pre-build configuration
    def PreBuild(this):
        pass


    # Hook for any post-build configuration
    def PostBuild(this):
        pass


    # Sets the build path that should be used by children of *this.
    # Also sets src, inc, lib, and dep paths, if they are present.
    def PopulatePaths(this, rootPath, buildFolder):
        if (rootPath is None):
            logging.warn("no \"dir\" supplied. buildPath is None")
            return

        this.rootPath = os.path.abspath(rootPath)

        this.buildPath = os.path.join(this.rootPath, buildFolder)
        Path(this.buildPath).mkdir(parents=True, exist_ok=True)

        paths = [
            "src",
            "inc",
            "dep",
            "lib",
            "bin",
            "test"
        ]
        for path in paths:
            tmpPath = os.path.abspath(os.path.join(this.rootPath, path))
            if (os.path.isdir(tmpPath)):
                setattr(this, f"{path}Path", tmpPath)
            else:
                setattr(this, f"{path}Path", None)


    # Populate the configuration details for *this.
    def PopulateLocalConfig(this, configName="build.json"):
        this.config = None
        localConfigFile = os.path.join(this.rootPath, configName)
        logging.debug(f"Looking for local configuration: {localConfigFile}")
        if (os.path.isfile(localConfigFile)):
            configFile = open(localConfigFile, "r")
            this.config = jsonpickle.decode(configFile.read())
            configFile.close()
            logging.debug(f"Got local config contents: {this.config}")


    # Will try to get a value for the given varName from:
    #    first: this
    #    second: the local config file
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
        enableLocalConfig=True):
            
        # Duplicate code from eons.UserFunctor in order to establish precedence.
        if (enableThis and hasattr(this, varName)):
            logging.debug("...got {varName} from self ({this.name}).")
            return getattr(this, varName)

        if (enableLocalConfig and this.config is not None):
            for key, val in this.config.items():
                if (key == varName):
                    logging.debug(f"...got {varName} from local config.")
                    return val

        return super().Fetch(varName, default, enableThis, enableExecutor, enableArgs, enableExecutorConfig, enableEnvironment)

    # Override of eons.UserFunctor method. See that class for details.
    def ParseInitialArgs(this):
        super().ParseInitialArgs()
        this.events = this.kwargs.pop('events')


    # Calls PopulatePaths and PopulateVars after getting information from local directory
    # Projects should have a name of {project-type}_{project-name}.
    # For information on how projects should be labelled see: https://eons.llc/convention/naming/
    # For information on how projects should be organized, see: https://eons.llc/convention/uri-names/
    def PopulateProjectDetails(this):
        this.PopulatePaths(this.kwargs.pop("path"), this.kwargs.pop('build_in'))
        this.PopulateLocalConfig()

        # This is messy because we can't query this.name or executor.name and need to get "name" from a config or arg val to set projectName.
        for key, mem in this.configNameOverrides.items():
            this.Set(key, this.Fetch(key, default=this.executor.Fetch(key, default=None, enableThis=False), enableThis=False, enableExecutor=False))
            if (getattr(this, mem) is None):
                logging.warning(f"Not configured: {key}")

        details = os.path.basename(this.rootPath).split("_")
        if (this.projectType is None):
            this.projectType = details[0]
        if (this.projectName is None):
            if (len(details) > 1):
                this.projectName = '_'.join(details[1:])
            else:
                this.projectName = e.INVALID_NAME()


    # RETURNS whether or not we should trigger the next Builder based on what events invoked ebbs.
    # Anything in the "run_when_any" list will require a corresponding --event specification to run.
    # For example "run_when_any":["publish"] would require `--event publish` to enable publication Builders in the workflow.
    def ValidateNext(this, nextBuilder):
        if ("run_when_none" in nextBuilder):
            if ([r for r in nextBuilder["run_when_none"] if r in this.events]):
                logging.info(f"Skipping next builder: {nextBuilder['build']}; prohibitive events found (cannot have any of {nextBuilder['run_when_none']} and have {this.events})")
                return False

        if ("run_when_any" in nextBuilder):
            if (not [r for r in nextBuilder["run_when_any"] if r in this.events]): #[] is false
                logging.info(f"Skipping next builder: {nextBuilder['build']}; required events not met (needs any of {nextBuilder['run_when_any']} but only have {this.events})")
                return False

        if ("run_when_all" in nextBuilder):
            if (not set([str(r) for r in nextBuilder["run_when_all"]]).issubset(this.events)):
                logging.info(f"Skipping next builder: {nextBuilder['build']}; required events not met (needs all {nextBuilder['run_when_all']} but only have {this.events})")
                return False

        return True


    # Creates the folder structure for the next build step.
    # RETURNS the next buildPath.
    def PrepareNext(this, nextBuilder):
        logging.debug(f"<---- Preparing for next builder: {nextBuilder['build']} ---->")
        # logging.debug(f"Preparing for next builder: {nextBuilder}")

        nextPath = "."
        if ("path" in nextBuilder):
            nextPath = nextBuilder["path"]
        nextPath = os.path.join(this.buildPath, nextPath)
        # mkpath(nextPath) <- just broken.
        Path(nextPath).mkdir(parents=True, exist_ok=True)
        logging.debug(f"Next build path is: {nextPath}")

        if ("copy" in nextBuilder):
            for cpy in nextBuilder["copy"]:
                # logging.debug(f"copying: {cpy}")
                for src, dst in cpy.items():
                    this.Copy(src, dst, root=this.executor.rootPath)

        if ("config" in nextBuilder):
            nextConfigFile = os.path.join(nextPath, "build.json")
            logging.debug(f"writing: {nextConfigFile}")
            nextConfig = open(nextConfigFile, "w")
            for key, var in this.configNameOverrides.items():
                if (key not in nextBuilder["config"]):
                    val = getattr(this, var)
                    logging.debug(f"Adding to config: {key} = {val}")
                    nextBuilder["config"][key] = val
            nextConfig.write(jsonpickle.encode(nextBuilder["config"]))
            nextConfig.close()

        logging.debug(f">---- Completed preparation for: {nextBuilder['build']} ----<")
        return nextPath


    # Runs the next Builder.
    # Uses the Executor passed to *this.
    def BuildNext(this):
        #When fetching what to do next, everything is valid EXCEPT the environment. Otherwise we could do something like `export next='nop'` and never quit.
        #A similar situation arises when using the global config for each build step. We only use the global config if *this is the first builder and no local config was supplied.
        shouldUseExecutor = this.config is None
        if (shouldUseExecutor):
            logging.debug(f"{this.name} has no local config, so we will see if the Executor knows what to do next.")
        next = this.Fetch('next',
            default=None,
            enableThis=True,
            enableExecutor=shouldUseExecutor,
            enableArgs=shouldUseExecutor,
            enableExecutorConfig=shouldUseExecutor,
            enableEnvironment=False,
            enableLocalConfig=True)

        if (next is None):
            return

        for nxt in next:
            if (not this.ValidateNext(nxt)):
                continue
            nxtPath = this.PrepareNext(nxt)
            buildFolder = f"then_build_{nxt['build']}"
            if ("build_in" in nxt):
                buildFolder = nxt["build_in"]
            result = this.executor.Execute(
                build=nxt["build"],
                path=nxtPath,
                build_in=buildFolder,
                events=this.events)
            if (not result and ('tolerate_failure' not in nxt or not nxt['tolerate_failure'])):
                logging.error(f"Building {nxt['build']} failed. Aborting.")
                break



    # Override of eons.UserFunctor method. See that class for details.
    def ValidateArgs(this):
        # logging.debug(f"Got arguments: {this.kwargs}")

        this.PopulateProjectDetails()

        super().ValidateArgs()


    # Override of eons.Functor method. See that class for details
    def UserFunction(this):
        if (this.clearBuildPath):
            this.Delete(this.buildPath)

        # mkpath(this.buildPath) <- This just straight up doesn't work. Race condition???
        Path(this.buildPath).mkdir(parents=True, exist_ok=True)
        os.chdir(this.buildPath)

        this.PreBuild()

        if (len(this.supportedProjectTypes) and this.projectType not in this.supportedProjectTypes):
            raise ProjectTypeNotSupported(
                f"{this.projectType} is not supported. Supported project types for {this.name} are {this.supportedProjectTypes}")
        logging.info(f"Using {this.name} to build \"{this.projectName}\", a \"{this.projectType}\" in {this.buildPath}")

        logging.debug(f"<---- Building {this.name} ---->")
        this.Build()
        logging.debug(f">---- Done Building {this.name} ----<")

        this.PostBuild()

        if (this.DidBuildSucceed()):
            this.BuildNext()
        else:
            logging.error("Build did not succeed.")
