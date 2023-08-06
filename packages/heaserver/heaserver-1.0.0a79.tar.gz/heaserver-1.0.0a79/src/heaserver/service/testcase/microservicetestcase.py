from .aiohttptestcase import HEAAioHTTPTestCase
from .collection import CollectionKey, simplify_collection_keys
from .expectedvalues import Action, Link, expected_values
from .. import wstl
from aiohttp.web import Application
from ..oidcclaimhdrs import SUB
from .testenv import app_context, RegistryContainerConfig, DockerContainerConfig
from ..db.database import DatabaseManager
from heaserver.service.testcase.mockmongo import MockMongoManager
from aiohttp import hdrs
from heaobject.user import NONE_USER
from heaobject.root import DesktopObjectDict
from abc import ABC
from typing import Optional, Any, Iterable, Type
from copy import deepcopy
from yarl import URL
import logging


class MicroserviceTestCase(HEAAioHTTPTestCase, ABC):
    """
    Abstract base class for testing HEA microservices. It provides many expected values that should be returned from
    requests.
    """

    def __init__(self,
                 coll: str,
                 desktop_objects: dict[str | CollectionKey, list[DesktopObjectDict]],
                 db_manager_cls: Optional[Type[DatabaseManager]] = MockMongoManager,
                 wstl_package: str = None,
                 href: Optional[str | URL] = None,
                 body_post: Optional[dict[str, dict[str, Any]]] = None,
                 body_put: Optional[dict[str, dict[str, Any]]] = None,
                 content_id: Optional[str] = None,
                 expected_all: Optional[list[dict[str, Any]]] = None,
                 expected_one: Optional[list[dict[str, Any]]] = None,
                 expected_one_wstl: Optional[dict[str, Any]] = None,
                 expected_all_wstl: Optional[dict[str, Any]] = None,
                 expected_one_duplicate_form: Optional[dict[str, Any]] = None,
                 expected_opener: Optional[str | URL] = None,
                 expected_opener_body: Optional[dict[str, Any]] = None,
                 content: Optional[dict[str, dict[str, bytes]]] = None,
                 content_type: Optional[str] = None,
                 put_content_status: Optional[int] = None,
                 methodName='runTest',
                 port: Optional[int] = None,
                 sub: Optional[str] = NONE_USER,
                 registry_docker_image: Optional[RegistryContainerConfig] = None,
                 other_docker_images: Iterable[DockerContainerConfig] = None):
        """
        Initializes a test case.

        :param coll: collection name (required).
        :param desktop_objects: HEA desktop objects to load into the database (required), as a map of collection ->
        list of desktop object dicts.
        :param db_manager_cls: the database factory class. Defaults to TestMockMongoManager.
        :param wstl_package: the name of the package containing the WeSTL data package.
        :param href: the resource being tested. If None, uses http://localhost:{port}/{coll}/, where {coll} is the
        collection name, and {port} is the port ultimately used by this test case.
        :param body_post: a Collection+JSON template as a dictionary, to be used for submitting POST requests.
        :param body_put: a Collection+JSON template as a dictionary, to be used for submitting PUT requests.
        :param content_id: the ID of an object that has content, to be used for getting and updating content.
        :param expected_all: the expected JSON dictionary list from a GET all request for a Collection+JSON document.
        :param expected_one: the expected JSON dictionary list from a GET one request for a Collection+JSON document.
        :param expected_one_wstl: the expected JSON dictionary list from a GET one request for a run-time WeSTL
        document.
        :param expected_all_wstl: the expected JSON dictionary list from a GET all request for a run-time WeSTL
        document.
        :param expected_one_duplicate_form: expected JSON from a GET request for a form template to duplicate an
        object.
        :param expected_opener: the expected URL of the resource that does the opening.
        :param expected_opener_body: the expected JSON dictionary for GET calls for an HEA desktop object's opener
        choices.
        :param content: content to send via a PUT content request. It should not be the same as the content already
        associated with the object whose ID is content_id.
        :param content_type: the MIME type of the content included with the objects (e.g., text/plain; charset=utf-8).
        Must be specified if content_type is specified.
        :param put_content_status: the status code expected from a response to a PUT content request.
        :param methodName: the name of the method to test.
        :param port: the port number to run aiohttp. If None, a random available port will be chosen.
        :param sub: the user from which the requests will be sent. Defaults to heaobject.user.NONE_USER.
        :param registry_docker_image: a RegistryContainerConfig for a docker image of the HEA Registry Microservice.
        :param other_docker_images: an iterable of DockerContainerConfigs for docker images of other microservices.
        """
        super().__init__(methodName=methodName, port=port)
        if href is None:
            href_ = f'/{coll}/'  # FIXME: href default needs to include root (http://localhost:...)
        else:
            href_ = str(href)
            if not href_.endswith('/'):
                href_ += '/'
        self._href = URL(href_)
        self._coll = str(coll)
        self._body_post = body_post
        self._body_put = body_put
        self._content_id = content_id
        self._expected_all = expected_all
        self._expected_one = expected_one
        self._expected_one_wstl = expected_one_wstl
        self._expected_all_wstl = expected_all_wstl
        self._expected_one_duplicate_form = expected_one_duplicate_form
        self._expected_opener = expected_opener
        self._expected_opener_body = expected_opener_body
        self._wstl_package = wstl_package
        self.__desktop_objects = deepcopy(desktop_objects)
        self._content = deepcopy(content)
        self._content_type = content_type
        self._put_content_status = put_content_status
        self._headers = {SUB: sub if sub is not None else NONE_USER, hdrs.X_FORWARDED_HOST: 'localhost:8080'}
        self.__registry_docker_image = registry_docker_image
        self.__other_docker_images = other_docker_images
        self.__db_manager_cls = MockMongoManager if db_manager_cls is None else db_manager_cls
        self.maxDiff = None

    def run(self, result=None):
        """
        Runs a test using a freshly created MongoDB Docker container. The container is destroyed upon concluding
        the test.

        :param result: a TestResult object into which the test's result is collected.
        :return: the TestResult object.
        """
        _logger = logging.getLogger(__name__)
        with self._caplog.at_level(logging.DEBUG):
            with app_context(db_manager_cls=self.__db_manager_cls,
                             desktop_objects=self.__desktop_objects,
                             other_microservice_images=list(self.__other_docker_images) if self.__other_docker_images is not None else None,
                             registry_docker_image=self.__registry_docker_image,
                             content=self._content,
                             wstl_builder_factory=wstl.builder_factory(self._wstl_package,
                                                                       href=self._href)) as app:
                self.__app = app
                self._content = simplify_collection_keys(self._content) if self._content is not None else None
                return super().run(result)

    async def get_application(self) -> Application:
        return self.__app


def get_test_case_cls_default(coll: str,
                              fixtures: dict[str | CollectionKey, list[DesktopObjectDict]],
                              duplicate_action_name: str,
                              db_manager_cls: Type[DatabaseManager] = MockMongoManager,
                              wstl_package: Optional[str] = None,
                              content: Optional[dict[str | CollectionKey, dict[str, bytes]]] = None,
                              content_type: Optional[str] = None,
                              put_content_status: Optional[int] = None,
                              include_root=False,
                              href: Optional[str | URL] = None,
                              get_actions: Optional[list[Action]] = None,
                              get_all_actions: Optional[list[Action]] = None,
                              expected_opener: Optional[Link] = None,
                              registry_docker_image: Optional[RegistryContainerConfig] = None,
                              other_docker_images: Iterable[DockerContainerConfig] = None,
                              port: Optional[int] = None,
                              sub: Optional[str] = NONE_USER,
                              exclude: Optional[list[str]] = None) -> Type[MicroserviceTestCase]:
    """
    Create a test case class for testing a specific HEA microservice.

    :param coll: the name of the collection that the microservice uses (required).
    :param fixtures: HEA desktop objects to load into the database, as a map of collection keys ->
    list of desktop object dicts (required).
    :param duplicate_action_name: the name of the duplication action for this microservice (required).
    :param db_manager_cls: the type of the database manager that will be used as the default for collection keys that
    are strings. Under typical circumstances, this should be used by the collection specified in coll. For Mongo unit
    tests, use MockMongoManager. For AWS unit tests, use MockS3ManagerWithMockMongo. For Mongo integration tests, use
    DockerMongoManager. For AWS integration tests, use MockS3Manager. Defaults to MockMongoManager.
    :param wstl_package: the name of the package containing the WeSTL data package, in standard module format
    (foo.bar).
    :param content: a mapping of collection keys -> HEA object IDs -> content that will be included with the
    objects inserted into the database. If None, objects will not have content.
    :param content_type: the MIME type of the content included with the objects (e.g., text/plain; charset=utf-8).
    Must be specified if content_type is specified.
    :param put_content_status: the expected HTTP response code for updating the content of the HEA object. Normally
    should be 204 if the content is updatable and 405 if not. Default is None, which will cause associated tests to be
    skipped.
    :param include_root: this parameter has been deprecated since version 1.0.0a71 and is no longer used. Will be
    removed in a future version of HEA Server Framework.
    :param href: the resource being tested. If None, uses http://localhost:{port}/{coll}/, where {coll} is the
    collection name, and {port} is the port ultimately used by this test case.
    :param get_actions: the list of actions associated with the GET one route of the microservice.
    :param get_all_actions: the list of actions associated with the GET all route of the microservice.
    :param expected_opener: The expected URL of the resource that does the opening, including a list of HTML rel
    values.
    :param registry_docker_image: a RegistryContainerConfig for a Docker image of the HEA Registry Microservice. It
    will be launched once the MongoDB container is live. If the microservice depends on there being a registry, you
    should use testenv.MockRegistryContainerConfig for unit tests and dockermongo.RealRegistryContainerConfig for
    integration tests. Must be specified if other_docker_images is specified.
    :param other_docker_images: an iterable of DockerContainerConfigs for Docker images of other microservices. They
    will be launched once the MongoDB container is live.
    :param port: the port number to run aiohttp. If None, a random available port will be chosen.
    :param sub: the user from which the requests will be sent. It should be set to heaobject.user.TEST_USER for
    permissions testing. Defaults to heaobject.user.NONE_USER.
    :param exclude: a list of expected value names to exclude from test case class creation. Tests that need any
    expected value you specify here will be skipped.
    :return: A test case class for testing the microservice.
    """
    exclude_ = exclude if exclude is not None else []
    coll_ = coll if isinstance(coll, CollectionKey) else CollectionKey(name=coll, db_manager_cls=db_manager_cls)
    expected_values_ = {k: v for k, v in expected_values(fixtures, coll_, wstl.builder(package=wstl_package),
                                                         duplicate_action_name, href,
                                                         get_actions=get_actions,
                                                         get_all_actions=get_all_actions,
                                                         opener_link=expected_opener,
                                                         default_db_manager_cls=db_manager_cls).items()
                        if k not in exclude_}
    return _get_test_case_cls(coll=coll, fixtures=fixtures, db_manager_cls=db_manager_cls,
                              wstl_package=wstl_package, href=href, content=content, content_type=content_type,
                              put_content_status=put_content_status, registry_docker_image=registry_docker_image,
                              other_docker_images=other_docker_images, port=port, sub=sub, **expected_values_)


def _get_test_case_cls(coll: str,
                       fixtures: dict[str | CollectionKey, list[DesktopObjectDict]],
                       db_manager_cls: Optional[Type[DatabaseManager]] = MockMongoManager,
                       wstl_package: Optional[str] = None,
                       href: Optional[str | URL] = None,
                       content: Optional[dict[str | CollectionKey, dict[str, bytes]]] = None,
                       content_type: Optional[str] = None,
                       put_content_status: Optional[int] = None,
                       body_post: Optional[dict[str, dict[str, Any]]] = None,
                       body_put: Optional[dict[str, dict[str, Any]]] = None,
                       content_id: Optional[str] = None,
                       expected_one: Optional[list[dict[str, Any]]] = None,
                       expected_one_wstl: Optional[dict[str, Any]] = None,
                       expected_one_duplicate_form: Optional[dict[str, Any]] = None,
                       expected_all: Optional[list[dict[str, Any]]] = None,
                       expected_all_wstl: Optional[dict[str, Any]] = None,
                       expected_opener: Optional[str | URL] = None,
                       expected_opener_body: Optional[dict[str, Any]] = None,
                       registry_docker_image: Optional[RegistryContainerConfig] = None,
                       other_docker_images: Iterable[DockerContainerConfig] = None,
                       port: Optional[int] = None,
                       sub: Optional[str] = NONE_USER) -> Type[MicroserviceTestCase]:
    """
    This function configures mocks. It returns a base test case class for testing a mongodb-based service with the
    provided fixtures. The test case class is a subclass of aiohttp.test_utils.AioHTTPTestCase, and the provided
    fixtures can be found in the following fields: _body_post, _body_put, _expected_all, and _expected_one.

    :param coll: the name of the collection that the microservice uses (required).
    :param fixtures: HEA desktop objects to load into the database, as a map of collection keys ->
    list of desktop object dicts (required).
    :param db_manager_cls: the type of the database manager that will be used as the default for collection keys that
    are strings. Under typical circumstances, this should be used by the collection specified in coll.
    :param wstl_package: the name of the package containing the WeSTL data package, in standard module format
    (foo.bar).
    :param href: the resource being tested. If None, uses http://localhost:{port}/{coll}/, where {coll} is the
    collection name, and {port} is the port ultimately used by this test case.
    :param content: a mapping of collection keys -> HEA object IDs -> content that will be included with the
    objects inserted into the database. If None, objects will not have content.
    :param content_type: the MIME type of the content included with the objects (e.g., text/plain; charset=utf-8).
    Must be specified if content_type is specified.
    :param put_content_status: the expected status code for updating the content of the HEA object (optional). Normally
    should be 204 if the content is updatable and 405 if not. Default is None, which will cause associated tests to be
    skipped.
    :param body_post: a Collection+JSON template as a dictionary, to be used for submitting POST requests.
    :param body_put: a Collection+JSON template as a dictionary, to be used for submitting PUT requests.
    :param expected_one: the expected JSON dictionary list from a GET one request for a Collection+JSON document. If
    None, expected_all will be used.
    :param expected_one_wstl: the expected JSON dictionary list from a GET one request for a run-time WeSTL
    document.
    :param expected_one_duplicate_form: expected JSON from a GET request for a form template to duplicate an
    object.
    :param expected_all_wstl: the expected JSON dictionary list from a GET all request for a run-time WeSTL document.
    :param expected_all: the expected JSON dictionary list from a GET all request for a Collection+JSON document.
    :param expected_opener: the expected URL of the resource that does the opening.
    :param expected_opener_body: the expected JSON dictionary for GET calls for an HEA desktop object's opener
    choices.
    :param expected_opener: the expected URL of the resource that does the opening.
    :param expected_opener_body: the expected JSON dict for GET calls for an HEA desktop object's opener choices.
    :param registry_docker_image: a RegistryContainerConfig for a Docker image of the HEA Registry Microservice. It
    will be launched once the MongoDB container is live. Must be specified if other_docker_images is specified.
    :param other_docker_images: an iterable of DockerContainerConfigs for Docker images of other microservices. They
    will be launched once the MongoDB container is live.
    :param port: the port number to run aiohttp. If None, a random available port will be chosen.
    :param sub: the user from which the requests will be sent. Defaults to heaobject.user.NONE_USER.
    :return: a base test case class for testing the microservice.
    """
    class RealMicroserviceTestCase(MicroserviceTestCase):
        """
        Test case class for testing a mongodb-based service.
        """

        def __init__(self, methodName: str = 'runTest') -> None:
            """
            Initializes a test case.

            :param methodName: the name of the method to test.
            """
            super().__init__(coll=coll, desktop_objects=fixtures, db_manager_cls=db_manager_cls,
                             wstl_package=wstl_package, href=href, body_post=body_post, body_put=body_put,
                             content_id=content_id,
                             expected_all=expected_all, expected_one=expected_one or expected_all,
                             expected_one_wstl=expected_one_wstl or expected_all_wstl,
                             expected_all_wstl=expected_all_wstl,
                             expected_one_duplicate_form=expected_one_duplicate_form, expected_opener=expected_opener,
                             expected_opener_body=expected_opener_body, content=content, content_type=content_type,
                             put_content_status=put_content_status, methodName=methodName, port=port, sub=sub,
                             registry_docker_image=registry_docker_image, other_docker_images=other_docker_images)

    return RealMicroserviceTestCase
