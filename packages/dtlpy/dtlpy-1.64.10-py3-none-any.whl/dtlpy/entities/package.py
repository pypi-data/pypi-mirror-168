import os
from collections import namedtuple
from enum import Enum
from typing import Union
import logging
import traceback
import attr
import json

from .. import repositories, entities, exceptions, services

logger = logging.getLogger(name='dtlpy')


class RequirementOperator(str, Enum):
    EQUAL = '==',
    GREATER_THAN = '>',
    LESS_THAN = '<',
    EQUAL_OR_LESS_THAN = '<=',
    EQUAL_OR_GREATER_THAN = '>='

    @staticmethod
    def keys():
        return [key.value for key in list(RequirementOperator)]


class PackageRequirement:

    def __init__(self, name: str, version: str = None, operator: str = None):
        self.name = name
        self.version = version

        valid_operators = RequirementOperator.keys()
        if operator is not None and operator not in valid_operators:
            raise Exception('Illegal operator: {}. Please select from: {}'.format(operator, valid_operators))

        self.operator = operator

    def to_json(self):
        _json = {'name': self.name}
        if self.version is not None:
            _json['version'] = self.version
        if self.operator is not None:
            _json['operator'] = self.operator
        return _json

    @classmethod
    def from_json(cls, _json: dict):
        return cls(**_json)


@attr.s
class Package(entities.BaseEntity):
    """
    Package object
    """
    # platform
    id = attr.ib()
    url = attr.ib(repr=False)
    version = attr.ib()
    created_at = attr.ib()
    updated_at = attr.ib(repr=False)
    name = attr.ib()
    codebase = attr.ib()
    _modules = attr.ib()
    slots = attr.ib(type=list)
    ui_hooks = attr.ib()
    creator = attr.ib()
    is_global = attr.ib()
    type = attr.ib()
    service_config = attr.ib()
    # name change
    project_id = attr.ib()

    # sdk
    _project = attr.ib(repr=False)
    _client_api = attr.ib(type=services.ApiClient, repr=False)
    _revisions = attr.ib(default=None, repr=False)
    _repositories = attr.ib(repr=False)
    _artifacts = attr.ib(default=None)
    _codebases = attr.ib(default=None)

    # defaults
    requirements = attr.ib(default=None)

    @property
    def createdAt(self):
        return self.created_at

    @property
    def updatedAt(self):
        return self.updated_at

    @property
    def modules(self):
        return self._modules

    @property
    def platform_url(self):
        return self._client_api._get_resource_url("projects/{}/packages/{}/main".format(self.project.id, self.id))

    @property
    def codebase_id(self):
        if self.codebase is not None and self.codebase.type == entities.PackageCodebaseType.ITEM:
            return self.codebase.item_id
        return None

    @codebase_id.setter
    def codebase_id(self, item_id: str):
        self.codebase = entities.ItemCodebase(item_id=item_id)

    @modules.setter
    def modules(self, modules: list):
        if not self.unique_modules(modules):
            raise Exception('Cannot have 2 modules by the same name in one package.')
        if not isinstance(modules, list):
            raise Exception('Package modules must be a list.')
        self._modules = modules

    @staticmethod
    def unique_modules(modules: list):
        return len(modules) == len(set([module.name for module in modules]))

    @staticmethod
    def _protected_from_json(_json, client_api, project, is_fetched=True):
        """
        Same as from_json but with try-except to catch if error

        :param _json:  platform json
        :param client_api: ApiClient entity
        :return:
        """
        try:
            package = Package.from_json(_json=_json,
                                        client_api=client_api,
                                        project=project,
                                        is_fetched=is_fetched)
            status = True
        except Exception:
            package = traceback.format_exc()
            status = False
        return status, package

    @classmethod
    def from_json(cls, _json, client_api, project, is_fetched=True):
        """
        Turn platform representation of package into a package entity

        :param dict _json: platform representation of package
        :param dl.ApiClient client_api: ApiClient entity
        :param dtlpy.entities.project.Project project: project entity
        :param is_fetched: is Entity fetched from Platform
        :return: Package entity
        :rtype: dtlpy.entities.package.Package
        """
        if project is not None:
            if project.id != _json.get('projectId', None):
                logger.warning('Package has been fetched from a project that is not belong to it')
                project = None

        modules = [entities.PackageModule.from_json(_module) for _module in _json.get('modules', list())]
        slots = _json.get('slots', None)
        if slots is not None:
            slots = [entities.PackageSlot.from_json(_slot) for _slot in slots]

        if 'codebase' in _json:
            codebase = entities.Codebase.from_json(_json=_json['codebase'],
                                                   client_api=client_api)
        else:
            codebase = None

        requirements = _json.get('requirements', None)
        if requirements is not None:
            requirements = [PackageRequirement.from_json(r) for r in requirements]

        inst = cls(
            project_id=_json.get('projectId', None),
            codebase=codebase,
            created_at=_json.get('createdAt', None),
            updated_at=_json.get('updatedAt', None),
            version=_json.get('version', None),
            creator=_json.get('creator', None),
            is_global=_json.get('global', None),
            client_api=client_api,
            modules=modules,
            slots=slots,
            ui_hooks=_json.get('uiHooks', None),
            name=_json.get('name', None),
            url=_json.get('url', None),
            project=project,
            id=_json.get('id', None),
            service_config=_json.get('serviceConfig', None),
            requirements=requirements,
            type=_json.get('type', None)
        )
        inst.is_fetched = is_fetched
        return inst

    def to_json(self):
        """
        Turn Package entity into a platform representation of Package

        :return: platform json of package
        :rtype: dict
        """
        _json = attr.asdict(self,
                            filter=attr.filters.exclude(attr.fields(Package)._project,
                                                        attr.fields(Package)._repositories,
                                                        attr.fields(Package)._artifacts,
                                                        attr.fields(Package)._codebases,
                                                        attr.fields(Package)._client_api,
                                                        attr.fields(Package)._revisions,
                                                        attr.fields(Package).project_id,
                                                        attr.fields(Package)._modules,
                                                        attr.fields(Package).slots,
                                                        attr.fields(Package).is_global,
                                                        attr.fields(Package).ui_hooks,
                                                        attr.fields(Package).codebase,
                                                        attr.fields(Package).service_config,
                                                        attr.fields(Package).created_at,
                                                        attr.fields(Package).updated_at,
                                                        attr.fields(Package).requirements,
                                                        ))

        modules = self.modules
        # check in inputs is a list
        if not isinstance(modules, list):
            modules = [modules]
        # if is dtlpy entity convert to dict
        if modules and isinstance(modules[0], entities.PackageModule):
            modules = [module.to_json() for module in modules]
        _json['modules'] = modules
        if self.slots is not None:
            slot = [slot.to_json() for slot in self.slots]
            _json['slots'] = slot
        _json['projectId'] = self.project_id
        _json['createdAt'] = self.created_at
        _json['updatedAt'] = self.updated_at
        if self.is_global is not None:
            _json['global'] = self.is_global
        if self.codebase is not None:
            _json['codebase'] = self.codebase.to_json()
        if self.ui_hooks is not None:
            _json['uiHooks'] = self.ui_hooks
        if self.service_config is not None:
            _json['serviceConfig'] = self.service_config

        if self.requirements is not None:
            _json['requirements'] = [r.to_json() for r in self.requirements]

        return _json

    ############
    # entities #
    ############
    @property
    def revisions(self):
        if self._revisions is None:
            self._revisions = self.packages.revisions(package=self)
        return self._revisions

    @property
    def project(self):
        if self._project is None:
            self._project = self.projects.get(project_id=self.project_id, fetch=None)
        assert isinstance(self._project, entities.Project)
        return self._project

    ################
    # repositories #
    ################
    @_repositories.default
    def set_repositories(self):
        reps = namedtuple('repositories',
                          field_names=['executions', 'services', 'projects', 'packages'])

        r = reps(executions=repositories.Executions(client_api=self._client_api, project=self._project),
                 services=repositories.Services(client_api=self._client_api, package=self, project=self._project,
                                                project_id=self.project_id),
                 projects=repositories.Projects(client_api=self._client_api),
                 packages=repositories.Packages(client_api=self._client_api, project=self._project))
        return r

    @property
    def executions(self):
        assert isinstance(self._repositories.executions, repositories.Executions)
        return self._repositories.executions

    @property
    def services(self):
        assert isinstance(self._repositories.services, repositories.Services)
        return self._repositories.services

    @property
    def projects(self):
        assert isinstance(self._repositories.projects, repositories.Projects)
        return self._repositories.projects

    @property
    def packages(self):
        assert isinstance(self._repositories.packages, repositories.Packages)
        return self._repositories.packages

    @property
    def codebases(self):
        if self._codebases is None:
            self._codebases = repositories.Codebases(
                client_api=self._client_api,
                project=self._project,
                project_id=self.project_id
            )
        assert isinstance(self._codebases, repositories.Codebases)
        return self._codebases

    @property
    def artifacts(self):
        if self._artifacts is None:
            self._artifacts = repositories.Artifacts(
                client_api=self._client_api,
                project=self._project,
                project_id=self.project_id
            )
        assert isinstance(self._artifacts, repositories.Artifacts)
        return self._artifacts

    ##############
    # properties #
    ##############
    @property
    def git_status(self):
        status = 'Git status unavailable'
        try:
            if self.codebase.type == entities.PackageCodebaseType.ITEM:
                if 'git' in self.codebase.item.metadata:
                    status = self.codebase.item.metadata['git'].get('status', status)
        except Exception:
            logging.debug('Error getting codebase')
        return status

    @property
    def git_log(self):
        log = 'Git log unavailable'
        try:
            if self.codebase.type == entities.PackageCodebaseType.ITEM:
                if 'git' in self.codebase.item.metadata:
                    log = self.codebase.item.metadata['git'].get('log', log)
        except Exception:
            logging.debug('Error getting codebase')
        return log

    ###########
    # methods #
    ###########
    def update(self):
        """
        Update Package changes to platform

        :return: Package entity
        """
        return self.packages.update(package=self)

    def deploy(self,
               service_name=None,
               revision=None,
               init_input=None,
               runtime=None,
               sdk_version=None,
               agent_versions=None,
               verify=True,
               bot=None,
               pod_type=None,
               module_name=None,
               run_execution_as_process=None,
               execution_timeout=None,
               drain_time=None,
               on_reset=None,
               max_attempts=None,
               force=False,
               secrets: list = None,
               **kwargs):
        """
        Deploy package

        :param str service_name: service name
        :param str revision: package revision - default=latest
        :param init_input: config to run at startup
        :param dict runtime: runtime resources
        :param str sdk_version:  - optional - string - sdk version
        :param dict agent_versions: - dictionary - - optional -versions of sdk, agent runner and agent proxy
        :param str bot: bot email
        :param str pod_type: pod type dl.InstanceCatalog
        :param bool verify: verify the inputs
        :param str module_name: module name
        :param bool run_execution_as_process: run execution as process
        :param int execution_timeout: execution timeout
        :param int drain_time: drain time
        :param str on_reset: on reset
        :param int max_attempts: Maximum execution retries in-case of a service reset
        :param bool force: optional - terminate old replicas immediately
        :param list secrets: list of the integrations ids
        :return: Service object
        :rtype: dtlpy.entities.service.Service

        **Example**:

        .. code-block:: python

            package.deploy(service_name=package_name,
                            execution_timeout=3 * 60 * 60,
                            module_name=module.name,
                            runtime=dl.KubernetesRuntime(
                                concurrency=10,
                                pod_type=dl.InstanceCatalog.REGULAR_S,
                                autoscaler=dl.KubernetesRabbitmqAutoscaler(
                                    min_replicas=1,
                                    max_replicas=20,
                                    queue_length=20
                                )
                            )
                        )
        """
        return self.project.packages.deploy(package=self,
                                            service_name=service_name,
                                            project_id=self.project_id,
                                            revision=revision,
                                            init_input=init_input,
                                            runtime=runtime,
                                            sdk_version=sdk_version,
                                            agent_versions=agent_versions,
                                            pod_type=pod_type,
                                            bot=bot,
                                            verify=verify,
                                            module_name=module_name,
                                            run_execution_as_process=run_execution_as_process,
                                            execution_timeout=execution_timeout,
                                            drain_time=drain_time,
                                            on_reset=on_reset,
                                            max_attempts=max_attempts,
                                            force=force,
                                            jwt_forward=kwargs.get('jwt_forward', None),
                                            is_global=kwargs.get('is_global', None),
                                            secrets=secrets)

    def checkout(self):
        """
        Checkout as package

        :return:
        """
        return self.packages.checkout(package=self)

    def delete(self):
        """
        Delete Package object

        :return: True
        """
        return self.packages.delete(package=self)

    def push(self,
             codebase: Union[entities.GitCodebase, entities.ItemCodebase] = None,
             src_path: str = None,
             package_name: str = None,
             modules: list = None,
             checkout: bool = False,
             revision_increment: str = None,
             service_update: bool = False,
             service_config: dict = None,
             ):
        """
        Push local package

        :param dtlpy.entities.codebase.Codebase codebase: PackageCode object - defines how to store the package code
        :param bool checkout: save package to local checkout
        :param str src_path: location of pacjage codebase folder to zip
        :param str package_name: name of package
        :param list modules: list of PackageModule
        :param str revision_increment: optional - str - version bumping method - major/minor/patch - default = None
        :param  bool service_update: optional - bool - update the service
        :param  dict service_config: optional - json of service - a service that have config from the main service if wanted
        :return: package entity
        :rtype: dtlpy.entities.package.Package
        
        **Example**:

        .. code-block:: python

            packages.push(package_name='package_name',
                        modules=[module],
                        version='1.0.0',
                        src_path=os.getcwd()
                    )
        """
        return self.project.packages.push(
            package_name=package_name if package_name is not None else self.name,
            modules=modules if modules is not None else self.modules,
            revision_increment=revision_increment,
            codebase=codebase,
            src_path=src_path,
            checkout=checkout,
            service_update=service_update,
            service_config=service_config

        )

    def pull(self, version=None, local_path=None):
        """
        Pull local package

        :param str version: version
        :param str local_path: local path

        **Example**:

        .. code-block:: python

            package.pull(local_path='local_path')
        """
        return self.packages.pull(package=self,
                                  version=version,
                                  local_path=local_path)

    def open_in_web(self):
        """
        Open the package in web platform

        """
        self._client_api._open_in_web(url=self.platform_url)

    def test(self,
             cwd=None,
             concurrency=None,
             module_name=entities.package_defaults.DEFAULT_PACKAGE_MODULE_NAME,
             function_name=entities.package_defaults.DEFAULT_PACKAGE_FUNCTION_NAME,
             class_name=entities.package_defaults.DEFAULT_PACKAGE_CLASS_NAME,
             entry_point=entities.package_defaults.DEFAULT_PACKAGE_ENTRY_POINT
             ):
        """
        Test local package in local environment.

        :param str cwd: path to the file
        :param int concurrency: the concurrency of the test
        :param str module_name: module name
        :param str function_name: function name
        :param str class_name: class name
        :param str entry_point: the file to run like main.py
        :return: list created by the function that tested the output
        :rtype: list

        **Example**:

        .. code-block:: python

            package.test(cwd='path_to_package',
                        function_name='run')
        """
        return self.project.packages.test_local_package(
            cwd=cwd,
            concurrency=concurrency,
            package=self,
            module_name=module_name,
            function_name=function_name,
            class_name=class_name,
            entry_point=entry_point
        )

    @staticmethod
    def _mockify_input(input_type):
        _json = dict()
        if input_type == 'Dataset':
            _json.update({'dataset_id': 'id'})
        if input_type == 'Item':
            _json.update({'item_id': 'id', 'dataset_id': 'id'})
        if input_type == 'Annotation':
            _json.update({'annotation_id': 'id', 'item_id': 'id', 'dataset_id': 'id'})
        return _json

    def mockify(self, local_path=None, module_name=None, function_name=None):
        if local_path is None:
            local_path = os.getcwd()

        if module_name is None:
            if self.modules:
                module_name = self.modules[0].name
            else:
                raise exceptions.PlatformException('400', 'Package has no modules')

        modules = [module for module in self.modules if module.name == module_name]
        if not modules:
            raise exceptions.PlatformException('404', 'Module not found: {}'.format(module_name))
        module = modules[0]

        if function_name is None:
            funcs = [func for func in module.functions]
            if funcs:
                func = funcs[0]
            else:
                raise exceptions.PlatformException('400', 'Module: {} has no functions'.format(module_name))
        else:
            funcs = [func for func in module.functions if func.name == function_name]
            if not funcs:
                raise exceptions.PlatformException('404', 'Function not found: {}'.format(function_name))
            func = funcs[0]

        mock = dict()
        for module in self.modules:
            mock['module_name'] = module.name
            mock['function_name'] = func.name
            mock['init_params'] = {inpt.name: self._mockify_input(input_type=inpt.type) for inpt in module.init_inputs}
            mock['inputs'] = [{'name': inpt.name, 'value': self._mockify_input(input_type=inpt.type)} for inpt in
                              func.inputs]

        with open(os.path.join(local_path, 'mock.json'), 'w') as f:
            json.dump(mock, f)
