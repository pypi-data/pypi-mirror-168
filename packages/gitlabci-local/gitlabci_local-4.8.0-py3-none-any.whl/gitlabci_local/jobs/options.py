#!/usr/bin/env python3

# Options class, pylint: disable=too-many-instance-attributes
class Options:

    # Members
    __disabled = None
    __env_job_name = None
    __env_job_path = None
    __extends_available = None
    __extends_unknown = None
    __git_clone_path = None
    __host = None
    __quiet = None
    __silent = None
    __sockets = None
    __ssh = None

    # Constructor
    def __init__(self):

        # Prepare default options
        self.__disabled = None
        self.__env_job_name = ''
        self.__env_job_path = ''
        self.__extends_available = []
        self.__extends_unknown = []
        self.__git_clone_path = None
        self.__host = False
        self.__quiet = False
        self.__silent = False
        self.__sockets = False
        self.__ssh = False

    # Disabled
    @property
    def disabled(self):
        return self.__disabled

    # Disabled
    @disabled.setter
    def disabled(self, value):
        self.__disabled = value

    # Env job name
    @property
    def env_job_name(self):
        return self.__env_job_name

    # Env job name
    @env_job_name.setter
    def env_job_name(self, value):
        self.__env_job_name = value

    # Env job path
    @property
    def env_job_path(self):
        return self.__env_job_path

    # Env job path
    @env_job_path.setter
    def env_job_path(self, value):
        self.__env_job_path = value

    # Extends available
    @property
    def extends_available(self):
        return self.__extends_available

    # Extends available
    @extends_available.setter
    def extends_available(self, value):
        self.__extends_available = value

    # Extends unknown
    @property
    def extends_unknown(self):
        return self.__extends_unknown

    # Extends unknown
    @extends_unknown.setter
    def extends_unknown(self, value):
        self.__extends_unknown = value

    # Git clone path
    @property
    def git_clone_path(self):
        return self.__git_clone_path

    # Git clone path
    @git_clone_path.setter
    def git_clone_path(self, value):
        self.__git_clone_path = value

    # Host
    @property
    def host(self):
        return self.__host

    # Host
    @host.setter
    def host(self, value):
        self.__host = value

    # Quiet
    @property
    def quiet(self):
        return self.__quiet

    # Quiet
    @quiet.setter
    def quiet(self, value):
        self.__quiet = value

    # Silent
    @property
    def silent(self):
        return self.__silent

    # Silent
    @silent.setter
    def silent(self, value):
        self.__silent = value

    # Sockets
    @property
    def sockets(self):
        return self.__sockets

    # Sockets
    @sockets.setter
    def sockets(self, value):
        self.__sockets = value

    # SSH
    @property
    def ssh(self):
        return self.__ssh

    # SSH
    @ssh.setter
    def ssh(self, value):
        self.__ssh = value
