"""Tests tutorials individually.

Unlike the tutorials, these tests do not use hosted pods on staging or production.
Instead, we create pods for these tests to use so that the tests can be run standalone
without dependencies on shared resources.

We use `testbook` to inject code into the first cell of each notebook that patches the
necessary objects and then again in the last cell to stop the patching. This code
injection must be done because we can't use monkeypatch/unittest to mock at the pytest
test level because each tutorial starts up a jupyter kernel within the pytest test which
is unaffected by our mocking attempts. We patch two things:

- `bitfount.hub.helper.BitfountSession`: we patch the BitfountSession for both Pod
and Modeller so that we can authenticate with the hub programmatically i.e. log in with
Selenium

- `"bitfount.federated.transport.oidc.webbrowser.open_new_tab`: we patch the webbrowser
opening call that is made in the OIDC authentication flow which happens when a training
request is made by the Modeller. Again, we open the URL with Selenium in a headless
browser, this time in a separate thread so that we don't block the Modeller's responses
to the OIDC challenges
"""
import asyncio
from contextlib import contextmanager
from dataclasses import dataclass
import json
import logging
from multiprocessing import Process
import os
from pathlib import Path
import textwrap
import time
from typing import Callable, Dict, Final, Generator, Tuple, Union, cast
from unittest.mock import Mock

from _pytest.monkeypatch import MonkeyPatch
from _pytest.tmpdir import TempPathFactory
import jupytext
from nbclient.client import CellTimeoutError
from nbformat.notebooknode import NotebookNode
import pytest
from pytest import fixture
from testbook import testbook
from testbook.client import TestbookNotebookClient
from testbook.reference import TestbookObjectReference
from testbook.translators import PythonTranslator
from testbook.utils import random_varname

from bitfount import config
from tests.integration.tutorials.notebook_logging import (
    LogQueueManager,
    notebook_queue_logging_code,
)
from tests.integration.utils import get_patched_authentication_code_nb, rm_tree
from tests.utils import PytestRequest
from tests.utils.helper import (
    tutorial_1_test,
    tutorial_2_test,
    tutorial_3_test,
    tutorial_4_test,
    tutorial_5_test,
    tutorial_6_test,
    tutorial_7_test,
    tutorial_8_test,
    tutorial_9_test,
    tutorial_10_test,
    tutorial_11_test,
    tutorial_test,
)

logger = logging.getLogger(__name__)

# User details for running tests
PASSWORD_ENVVAR: Final[str] = "BF_USER_PASSWORD"
ENVIRONMENT_ENVVAR: Final[str] = "BITFOUNT_ENVIRONMENT"
STAGING_USERNAME: Final[str] = "e2e_modeller"
PRODUCTION_USERNAME: Final[str] = "bitfount-rel"

MODELLER_TIMEOUT_PERIOD: Final[int] = 5 * 60  # 5 minutes
IMAGE_MODELLER_TIMEOUT_PERIOD: Final[int] = 12 * 60  # 12 minutes
MULTI_POD_MODELLER_TIMEOUT_PERIOD: Final[int] = 12 * 60  # 12 minutes
POD_TEST_TIMEOUT_PERIOD: Final[int] = 3 * 60  # 3 minutes

# This is the maximum time that a _background_ Pod will be running for.
# All tasks should comfortably be run in this time.
POD_TIMEOUT_PERIOD: Final[int] = 45 * 60  # 45 minutes
POD_TUTORIALS_DIR = "Connecting Data & Creating Pods"
BASIC_DATA_SCIENCE_TUTORIALS_DIR = "Running Basic Data Science Tasks"
ADVANCED_DATA_SCIENCE_TUTORIALS_DIR = "Advanced Data Science Tasks"
PRIVACY_PRESERVING_TUTORIALS_DIR = "Privacy-Preserving Techniques"
TUTORIALS: Final[Dict[int, str]] = {
    1: f"{POD_TUTORIALS_DIR}/running_a_pod",
    2: f"{BASIC_DATA_SCIENCE_TUTORIALS_DIR}/querying_and_training_a_model",
    3: f"{POD_TUTORIALS_DIR}/running_a_pod_using_yaml",
    4: f"{BASIC_DATA_SCIENCE_TUTORIALS_DIR}/training_a_model_on_two_pods",
    5: f"{POD_TUTORIALS_DIR}/running_an_image_data_pod",
    6: f"{BASIC_DATA_SCIENCE_TUTORIALS_DIR}/training_on_images",
    7: f"{ADVANCED_DATA_SCIENCE_TUTORIALS_DIR}/training_a_custom_model",
    8: f"{ADVANCED_DATA_SCIENCE_TUTORIALS_DIR}/using_pretrained_models",
    9: f"{PRIVACY_PRESERVING_TUTORIALS_DIR}/privacy_preserving_techniques",
    10: f"{POD_TUTORIALS_DIR}/running_a_segmentation_data_pod",
    11: f"{ADVANCED_DATA_SCIENCE_TUTORIALS_DIR}/training_a_custom_segmentation_model",
}

# Constants representing the names of the pods as in the tutorials
CENSUS_INCOME_POD_NAME: Final[str] = "census-income-demo"
CENSUS_INCOME_YAML_POD_NAME: Final[str] = "census-income-yaml-demo"
MNIST_POD_NAME: Final[str] = "mnist-demo"
SEGMENTATION_POD_NAME: Final[str] = "segmentation-data-demo"

# Path details
BITFOUNT_ROOT: Final[Path] = Path(__file__).parent.parent.parent.parent
TUTORIALS_ROOT: Final[Path] = BITFOUNT_ROOT / "tutorials"
TEST_SCHEMAS_PATH: Final[Path] = (
    BITFOUNT_ROOT / "tests" / "integration" / "resources" / "schemas"
)


@dataclass
class PodInfo:
    """Wrapper for background pod processes."""

    name: str
    process: Process


def _run_pod(
    tutorial_num: int,
    replacement_pod_name: str,
    pod_log_name: str,
    change_dir_code: str,
    extra_imports: str,
    patched_authentication_code: str,
    run_user: str,
) -> None:
    """Runs a pod from one of the tutorials. This is required for some tutorials.

    This is defined outside of the TestTutorials class so that it can be run as a
    separate `multiprocessing.Process` - otherwise it is not picklable.

    Args:
        tutorial_num: Relevant tutorial number.
        replacement_pod_name: The replacement, unique name to use for this pod.
        pod_log_name: Name to use to annotate log messages from this pod.
        change_dir_code: Code to change the directory.
        extra_imports: Code to import extra packages for testing.
        patched_authentication_code: Patched authentication code.
        run_user: The user to run the pod as.
    """
    try:
        tutorial_file: str = str(TUTORIALS_ROOT / f"{TUTORIALS[tutorial_num]}.md")
        logger.info(f"Running pod from {tutorial_file}.")

        # Need to set a new event loop in this process to ensure no gRPC clash
        asyncio.set_event_loop(asyncio.new_event_loop())

        nb = jupytext.read(tutorial_file)
        if tutorial_num in (1, 3):
            # Census income pod
            # As we know which tutorial this is we don't need to specify full set
            # of args, using empty strings for the ones we don't care about.
            nb = _perform_notebook_replacements(
                nb,
                tutorial_num,
                census_income_pod_name=replacement_pod_name,
                mnist_pod_name="",
                second_census_income_pod_name="",
                seg_pod_name="",
                run_user=run_user,
            )
        elif tutorial_num == 5:
            # MNIST pod
            # As we know which tutorial this is we don't need to specify full set
            # of args, using empty strings for the ones we don't care about.
            nb = _perform_notebook_replacements(
                nb,
                tutorial_num,
                census_income_pod_name="",
                mnist_pod_name=replacement_pod_name,
                second_census_income_pod_name="",
                seg_pod_name="",
                run_user=run_user,
            )
        else:  # tutorial_num == 10
            nb = _perform_notebook_replacements(
                nb,
                tutorial_num,
                census_income_pod_name="",
                mnist_pod_name="",
                second_census_income_pod_name="",
                seg_pod_name=replacement_pod_name,
                run_user=run_user,
            )
        with testbook(nb, execute=False, timeout=POD_TIMEOUT_PERIOD) as tb:
            logger.info("Injecting change_dir code")
            tb.inject(change_dir_code, pop=True)
            logger.info("Injecting mock authentication code")
            tb.inject(extra_imports, pop=True)
            tb.inject(patched_authentication_code, pop=True)

            # Add multiprocessing logging support
            logger.info("Injecting queue logging code")
            tb.inject(
                notebook_queue_logging_code(pod_log_name),
                after="logger_setup",
                run=False,
            )

            _execute(tb, fail_on_timeout=False)
    except Exception as e:
        logger.exception(e)
        raise e


def _execute(tb: TestbookNotebookClient, fail_on_timeout: bool = True) -> None:
    """Executes provided notebook.

    Args:
        tb: the notebook in testbook format
        fail_on_timeout: whether the test should fail if the timeout
            is exceeded. Defaults to True.

    Raises:
        Exception: Whatever exception is raised during notebook execution is re-raised
    """
    try:
        tb.execute()
    except Exception as e:
        if isinstance(e, CellTimeoutError):
            logger.error("Timeout error while executing notebook")
            if not fail_on_timeout:
                return

        # Fail test if there is an exception during execution
        # Displays outputs of all code cells for debugging
        cell_outputs = [
            cell["outputs"] for cell in tb.cells if cell["cell_type"] == "code"
        ]
        pytest.fail(json.dumps(cell_outputs, indent=2))


def _replace_in_notebook_source_code(
    query: str, replacement: str, notebook: NotebookNode
) -> NotebookNode:
    """Replaces all occurrences of `query` with `replacement` in `notebook` source code.

    Args:
        query: code to replace
        replacement: replacement code
        notebook: notebook to have code replaced

    Returns:
        The same notebook with updated source code.
    """
    loggable_query = query.replace("\n", "\\n")
    loggable_replacement = replacement.replace("\n", "\\n")
    logger.info(f'Replacing "{loggable_query}" with "{loggable_replacement}" ')

    changes_made = False
    for i, cell in enumerate(notebook["cells"]):
        orig_source_code: str = cell["source"]
        if cell["cell_type"] == "code" and query in orig_source_code:
            # Mark if changes have been made so we know that things have been
            # applied correctly; every replace should cause at least one change.
            # We know it will be applied because of the `query in` check above.
            changes_made = True
            new_source_code = orig_source_code.replace(query, replacement)
            notebook["cells"][i]["source"] = new_source_code

    if not changes_made:
        raise AssertionError(
            f'No code was replaced when trying to replace "{loggable_query}" '
            f'with "{loggable_replacement}"'
        )
    return notebook


def _perform_notebook_replacements(
    nb: NotebookNode,
    nb_num: int,
    census_income_pod_name: str,
    mnist_pod_name: str,
    second_census_income_pod_name: str,
    seg_pod_name: str,
    run_user: str,
) -> NotebookNode:
    """Replaces code in the notebook denoted by `nb_num` for testing purposes.

    Args:
        nb: notebook object
        nb_num: number of the notebook

    Returns:
        The notebook with relevant source code modified
    """
    logger.info(f"Replacing content in notebook for tutorial {nb_num}")
    # If tutorials 2, 4, 7, 8, or 9:
    # - Change production pod(s) name to unique local pod name(s)
    # - Explicitly specify username as modeller
    if nb_num in (2, 4, 7, 8, 9):
        nb = _replace_in_notebook_source_code(
            CENSUS_INCOME_POD_NAME, census_income_pod_name, nb
        )

        pod_identifier = "first_pod_identifier" if nb_num == 4 else "pod_identifier"
        if nb_num != 4:
            nb = _replace_in_notebook_source_code(
                f"schema = get_pod_schema({pod_identifier})",
                "from bitfount import BitfountSchema\nschema = BitfountSchema."
                f"load_from_file('{str(TEST_SCHEMAS_PATH)}/census_income_schema.yaml')\n"  # noqa: B950
                f"schema.tables[0].name = '{census_income_pod_name}'",
                nb,
            )
        else:
            # Also replace the other pod for tutorial 4
            if not second_census_income_pod_name:
                raise ValueError("Second pod name is needed")
            nb = _replace_in_notebook_source_code(
                CENSUS_INCOME_YAML_POD_NAME,
                second_census_income_pod_name,
                nb,
            )
            nb = _replace_in_notebook_source_code(
                "schema = combine_pod_schemas([first_pod_identifier, second_pod_identifier])",  # noqa: B950
                f"schema = BitfountSchema.load_from_file('{str(TEST_SCHEMAS_PATH)}/census_income_schema.yaml')\n"  # noqa: B950
                "import copy;schema.tables.append(copy.deepcopy(schema.tables[0]))\n"  # noqa: B950
                f"schema.tables[0].name = '{census_income_pod_name}';schema.tables[1].name = '{second_census_income_pod_name}'",  # noqa: B950
                nb,
            )
    # If tutorials 1, 3, 5 or 10 (pod tutorials):
    # - Explicitly specify username as modeller
    # - Change pod name to be unique
    elif nb_num in (1, 3, 5, 10):
        # Explicitly add username as data provider
        if nb_num == 3:
            # Yaml pod explicitly add username as data provider
            nb = _replace_in_notebook_source_code(
                "pod_name:", f"username: {run_user}\npod_name:", nb
            )
        # Change pod name to be unique
        if nb_num == 1:
            old_pod_name = CENSUS_INCOME_POD_NAME
            replacement_pod_name = census_income_pod_name

        elif nb_num == 3:
            agg_pod_suffix = second_census_income_pod_name.split("-")[-1]
            nb = _replace_in_notebook_source_code(
                """approved_pods=[
                 "census-income-yaml-demo"
            ], """,
                f"""approved_pods=[
                "census-income-demo-{agg_pod_suffix}"
            ], """,
                nb,
            )
            old_pod_name = CENSUS_INCOME_YAML_POD_NAME
            replacement_pod_name = second_census_income_pod_name

        elif nb_num == 5:
            old_pod_name = MNIST_POD_NAME
            replacement_pod_name = mnist_pod_name
        elif nb_num == 10:
            old_pod_name = SEGMENTATION_POD_NAME
            replacement_pod_name = seg_pod_name
        # Replace pod name
        nb = _replace_in_notebook_source_code(old_pod_name, replacement_pod_name, nb)
        if nb_num == 1:
            # We use the pod from tutorial 1 twice in tutorial 4,
            # need to update the approve_pod name accordingly.
            agg_pod_suffix = census_income_pod_name.split("-")[-1]
            if "-2-" in census_income_pod_name:
                nb = _replace_in_notebook_source_code(
                    CENSUS_INCOME_YAML_POD_NAME,
                    f"{CENSUS_INCOME_POD_NAME}-{agg_pod_suffix}",
                    nb,
                )
            else:
                nb = _replace_in_notebook_source_code(
                    CENSUS_INCOME_YAML_POD_NAME,
                    f"{CENSUS_INCOME_POD_NAME}-2-{agg_pod_suffix}",
                    nb,
                )
        if nb_num in (1, 5, 10):
            # Load pod keys from file to slightly speed up the tests
            nb = _replace_in_notebook_source_code(
                "pod = Pod(",
                f'pod_keys=_get_pod_keys(user_storage_path / "{replacement_pod_name}")\npod = Pod(pod_keys=pod_keys,',  # noqa: B950
                nb,
            )
            if nb_num == 1:

                nb = _replace_in_notebook_source_code(
                    "data_config=PodDataConfig(",
                    f'username="{run_user}",\ndata_config=PodDataConfig(',
                    nb,
                )

            elif nb_num == 5:
                nb = _replace_in_notebook_source_code(
                    "data_config=image_data_config,",
                    f'username="{run_user}",\ndata_config=image_data_config,',
                    nb,
                )
            else:  # nb_num==10
                nb = _replace_in_notebook_source_code(
                    "data_config=segmentation_data_config,",
                    f'username="{run_user}",\ndata_config=segmentation_data_config,',
                    nb,
                )
    # If tutorial 6:
    # - Explicitly specify username as modeller
    # - Change pod name to be the unique pod created
    # - Load schema from file
    elif nb_num == 6:

        # # Change pod name to be the unique pod created
        nb = _replace_in_notebook_source_code(
            MNIST_POD_NAME,
            mnist_pod_name,
            nb,
        )
        # Load schema from file
        nb = _replace_in_notebook_source_code(
            "schema = get_pod_schema(pod_identifier)",
            "from bitfount import BitfountSchema\nschema = BitfountSchema."
            f"load_from_file('{str(TEST_SCHEMAS_PATH)}/mnist_schema.yaml')\n"  # noqa: B950
            f"schema.tables[0].name = '{mnist_pod_name}'",
            nb,
        )
    # If tutorial 11:
    # - Explicitly specify username as modeller
    # - Change pod name to be the unique pod created
    # - Load schema from file
    elif nb_num == 11:
        # # Change pod name to be the unique pod created
        nb = _replace_in_notebook_source_code(
            SEGMENTATION_POD_NAME,
            seg_pod_name,
            nb,
        )
        # Load schema from file
        nb = _replace_in_notebook_source_code(
            "schema = get_pod_schema(pod_identifier)",
            "from bitfount import BitfountSchema\nschema = BitfountSchema."
            f"load_from_file('{str(TEST_SCHEMAS_PATH)}/data-schema-segmentation-data-demo.yaml')\n"  # noqa: B950
            f"schema.tables[0].name = '{seg_pod_name}'",
            nb,
        )

    return nb


@contextmanager
def patch_key_saver(
    tb: TestbookNotebookClient,
) -> Generator[TestbookObjectReference, None, None]:
    """Used as contextmanager to patch objects in the kernel.

    Differs from the built-in `tb.patch()` option by allowing us to `pop` the initial
    patch code which avoids the issues described here:
    https://github.com/nteract/testbook/issues/146
    """
    mock_save_to_key_store = f"_mock_{random_varname()}"
    patcher = f"_patcher_{random_varname()}"

    tb.inject(
        f"""
        from unittest.mock import patch
        from bitfount.hub.helper import _save_key_to_key_store
        {patcher} = patch(
            {PythonTranslator.translate("bitfount.hub.helper._save_key_to_key_store")},
            wraps=_save_key_to_key_store,
        )
        {mock_save_to_key_store} = {patcher}.start()
        """,
        pop=True,
    )

    yield TestbookObjectReference(tb, mock_save_to_key_store)

    tb.inject(f"{patcher}.stop()", pop=True)


@tutorial_test
class TestTutorials:
    """Tests tutorials to ensure they are working as expected.

    The tests below differ slightly depending on the value of the BITFOUNT_ENVIRONMENT
    environment variable.
    """

    @fixture(scope="module")
    def bitfount_env(self) -> str:
        """Determines the Bitfount environment to run the tests against.

        Defaults to staging if not explicitly set.
        """
        env = os.getenv(ENVIRONMENT_ENVVAR, config._STAGING_ENVIRONMENT)
        logging.info(f'Using the "{env}" environment for these tutorial tests.')
        return env

    @fixture(autouse=True, scope="module")
    def set_bitfount_environment(
        self, bitfount_env: str, monkeypatch_module_scope: MonkeyPatch
    ) -> None:
        """Monkeypatches Bitfount environment for tutorial tests.

        Guarantees that the envvar will be restored to the original value when
        tests finish.
        """
        monkeypatch_module_scope.setenv(ENVIRONMENT_ENVVAR, bitfount_env)

    @fixture(autouse=True, scope="module")
    def cleanup(self) -> Generator[None, None, None]:
        """Removes models before and after all tests."""
        models = (
            "training_a_model.pt",
            "training_a_model_on_two_pods.pt",
            "training_on_images.pt",
            "training_a_custom_model.pt",
            "training_a_custom_segmentation_model.pt",
        )
        for model in models:
            output = TUTORIALS_ROOT / model
            output.unlink(missing_ok=True)

        try:
            yield
        finally:
            for model in models:
                output = TUTORIALS_ROOT / model
                output.unlink(missing_ok=True)
            # Remove dummy segmentation data
            if (TUTORIALS_ROOT / "segmentation").exists():
                rm_tree(TUTORIALS_ROOT / "segmentation")
            # This gets overwritten in Tutorial 8 so no need
            # to remove beforehand as well
            Path("MyCustomModel.py").unlink(missing_ok=True)
            (TUTORIALS_ROOT / "MyCustomModel.py").unlink(missing_ok=True)
            Path("MyCustomSegmentationModel.py").unlink(missing_ok=True)
            (TUTORIALS_ROOT / "MyCustomSegmentationModel.py").unlink(missing_ok=True)

    @fixture(scope="module")
    def change_dir_code(self) -> str:
        """Changes the directory of the jupyter notebook execution to `tutorials`."""
        return "%cd tutorials"

    @fixture(scope="module")
    def extra_imports(self) -> str:
        """Extra imports needed for testing."""
        return (
            "from bitfount.federated.pod_keys_setup import _get_pod_keys\n"
            "from pathlib import Path\n"
            "from typing import Tuple, Any\n"
            "import unittest"
        )

    @fixture(scope="module")
    def authentication_user(self, bitfount_env: str) -> str:
        """Returns the username to use for authentication."""
        if bitfount_env == config._STAGING_ENVIRONMENT:
            user = STAGING_USERNAME
        elif bitfount_env == config._PRODUCTION_ENVIRONMENT:
            user = PRODUCTION_USERNAME
        else:
            raise ValueError(
                f"No authentication user defined"
                f' for Bitfount environment "{bitfount_env}"'
            )

        logging.info(f'Authentication user "{user}" will be used for these tests.')
        return user

    @fixture(scope="module")
    def authentication_password(self) -> str:
        """Returns the password for logging in as the target user.

        This will be supplied as the BF_USER_PASSWORD environment variable.
        """
        if not (pswd := os.getenv(PASSWORD_ENVVAR)):
            raise ValueError("No user password provided, unable to proceed.")
        else:
            return pswd

    @fixture(scope="module")
    def token_dir(self, tmp_path_factory: TempPathFactory) -> Path:
        """Temporary directory for tokens."""
        return tmp_path_factory.mktemp(".bitfount", numbered=False) / "bitfount_tokens"

    @fixture
    def keystore_path(self, tmp_path_factory: TempPathFactory) -> Path:
        """Temporary file for key storage."""
        return tmp_path_factory.mktemp("key_store") / "known_workers.yml"

    @fixture
    def keystore_path_code(self, keystore_path: Path) -> str:
        """Code for replacing keystore path in notebook.

        Ensures the keys are clear for each test run.
        """
        return textwrap.dedent(
            f"""
                from pathlib import Path
                import bitfount.hub.helper

                bitfount.hub.helper.BITFOUNT_KEY_STORE = Path("{str(keystore_path)}")
            """
        )

    # This needs to be function-scoped so that a new BitfountSession is created
    # each time, even if the username and password are the same for each run.
    @fixture(scope="function")
    def patched_authentication_code(
        self, authentication_password: str, authentication_user: str, token_dir: Path
    ) -> str:
        """Returns code that patches bitfount session and OIDC authentication.

        This enables them to be run in a headless environment and still perform
        the OAuth logins required.
        """
        return get_patched_authentication_code_nb(
            authentication_user, authentication_password, token_dir
        )

    @fixture(scope="module")
    def patched_authentication_cleanup_code(self) -> str:
        """Stops the BitfountSession and OIDC patchers.

        Should be injected at the end of the notebook execution. Relies on variables
        defined in the `patched_authentication_code` fixture.
        """
        return "session_patcher.stop(); oidc_patcher.stop()"

    @fixture
    def fixed_notebooks(
        self,
        authentication_user: str,
        census_income_pod_name: str,
        mnist_pod_name: str,
        request: PytestRequest,
        second_census_income_pod_name: str,
        seg_pod_name: str,
    ) -> Union[NotebookNode, Tuple[NotebookNode, NotebookNode]]:
        """Opens requested notebook(s), performs modifications and returns it."""
        nb_nums = request.param
        if not isinstance(nb_nums, tuple):
            nb_nums = (nb_nums,)

        fixed_notebooks = []

        for nb_num in nb_nums:
            nb = jupytext.read(f"tutorials/{TUTORIALS[nb_num]}.md")
            fixed_notebooks.append(
                _perform_notebook_replacements(
                    nb=nb,
                    nb_num=nb_num,
                    census_income_pod_name=census_income_pod_name,
                    mnist_pod_name=mnist_pod_name,
                    second_census_income_pod_name=second_census_income_pod_name,
                    seg_pod_name=seg_pod_name,
                    run_user=authentication_user,
                )
            )

        if len(fixed_notebooks) == 1:
            return fixed_notebooks[0]
        elif len(fixed_notebooks) == 2:
            return cast(Tuple[NotebookNode, NotebookNode], tuple(fixed_notebooks))
        else:
            raise ValueError("Too many notebooks output.")

    @fixture(scope="module")
    def pod_run_user(self, authentication_user: str) -> str:
        """User who will be running the background pods.

        Currently, just the same as the authentication_user.
        """
        return authentication_user

    @fixture(scope="module")
    def pod_run_password(self, authentication_password: str) -> str:
        """Password for user running background pods.

        Currently, just the same as the authentication_password.
        """
        return authentication_password

    @fixture(scope="module")
    def pod_factory(
        self,
        change_dir_code: str,
        extra_imports: str,
        log_queue_manager: LogQueueManager,
        pod_run_user: str,
        pod_run_password: str,
        pod_suffix: str,
        token_dir: Path,
    ) -> Callable[[str, str], PodInfo]:
        """Returns pod process function.

        Returns function which returns either 'mnist' or 'census-income' pod process.
        """

        def get_pod_process(process_name: str, replacement_pod_name: str) -> PodInfo:
            """Returns either mnist or census income pod process."""
            if "census-income" in replacement_pod_name:
                tutorial_num = 1
            elif "mnist" in replacement_pod_name:
                tutorial_num = 5
            elif "seg" in replacement_pod_name:
                tutorial_num = 10

            else:
                raise ValueError(f"Invalid pod name {replacement_pod_name}")

            # Cannot use fixture version as that is at "function" scope so instead
            # have to call code creator directly
            patched_authentication_code = get_patched_authentication_code_nb(
                pod_run_user, pod_run_password, token_dir
            )

            pod_process = Process(
                name=process_name,
                target=_run_pod,
                args=(
                    tutorial_num,
                    replacement_pod_name,
                    process_name,
                    change_dir_code,
                    extra_imports,
                    patched_authentication_code,
                    pod_run_user,
                ),
            )

            # Start pod
            logger.info(f"Starting pod {process_name}:{replacement_pod_name}")
            pod_process.start()

            # We sleep for 60 seconds to give time for the pod to start up
            # Without this sleep, there ends up being confusion around encryption keys
            # and the pod is unable to decrypt the messages from the Modeller.
            logger.info(
                f"Waiting for pod {process_name}:{replacement_pod_name} to start "
                f"up and register"
            )
            time.sleep(60)
            logger.info(
                f"Pod {process_name}:{replacement_pod_name} should be started by now"
            )
            return PodInfo(replacement_pod_name, pod_process)

        return get_pod_process

    @fixture(scope="module")
    def pod_suffix(self) -> str:
        """Generate a unique suffix for all pods in this test run."""
        return str(int(time.time()))  # unix timestamp

    @fixture(scope="module")
    def census_income_pod_name(self, pod_suffix: str) -> str:
        """Name of the census income pod."""
        pod_name = f"{CENSUS_INCOME_POD_NAME}-{pod_suffix}"
        logger.info(f"Census income pod name: {pod_name}")
        return pod_name

    @fixture(scope="module")
    def census_income_pod(
        self,
        pod_factory: Callable[[str, str], PodInfo],
        census_income_pod_name: str,
    ) -> Generator[PodInfo, None, None]:
        """Returns Census income pod at the module level.

        Terminates the pod after all tests have run.
        """
        logger.info("Creating census income pod")
        pod_info = pod_factory("census-income", census_income_pod_name)
        yield pod_info
        logger.info("Stopping census income pod")
        pod_info.process.terminate()
        pod_info.process.join()

    @fixture(scope="module")
    def mnist_pod_name(self, pod_suffix: str) -> str:
        """Name of the MNIST pod."""
        mnist_pod_name = f"{MNIST_POD_NAME}-{pod_suffix}"
        logger.info(f"MNIST pod name: {mnist_pod_name}")
        return mnist_pod_name

    @fixture(scope="module")
    def mnist_pod(
        self,
        mnist_pod_name: str,
        pod_factory: Callable[[str, str], PodInfo],
    ) -> Generator[PodInfo, None, None]:
        """Returns MNIST pod at the module level.

        Terminates the pod after all tests have run.
        """
        logger.info("Creating MNIST pod")
        mnist_pod_info = pod_factory("mnist", mnist_pod_name)
        yield mnist_pod_info
        logger.info("Stopping MNIST pod")
        mnist_pod_info.process.terminate()
        mnist_pod_info.process.join()

    @fixture(scope="module")
    def seg_pod_name(self, pod_suffix: str) -> str:
        """Name of the Segmentation pod."""
        seg_pod_name = f"{SEGMENTATION_POD_NAME}-{pod_suffix}"
        logger.info(f"Segmentation pod name: {seg_pod_name}")
        return seg_pod_name

    @fixture(scope="module")
    def seg_pod(
        self,
        seg_pod_name: str,
        pod_factory: Callable[[str, str], PodInfo],
    ) -> Generator[PodInfo, None, None]:
        """Returns Segmentation pod at the module level.

        Terminates the pod after all tests have run.
        """
        logger.info("Creating Segmentation pod")
        seg_pod_info = pod_factory("seg", seg_pod_name)
        yield seg_pod_info
        logger.info("Stopping Segmentation pod")
        seg_pod_info.process.terminate()
        seg_pod_info.process.join()

    @fixture(scope="module")
    def second_census_income_pod_name(self, pod_suffix: str) -> str:
        """Name of the second census income pod."""
        pod_name = f"{CENSUS_INCOME_POD_NAME}-2-{pod_suffix}"
        logger.info(f"Second census income pod name: {pod_name}")
        return pod_name

    @fixture(scope="module")
    def second_census_income_pod(
        self,
        pod_factory: Callable[[str, str], PodInfo],
        second_census_income_pod_name: str,
    ) -> Generator[PodInfo, None, None]:
        """Second census_income pod used for Tutorial 4."""
        logger.info("Creating second Census income Pod")
        pod_process_info = pod_factory("census-income-2", second_census_income_pod_name)
        yield pod_process_info
        logger.info("Stopping second Census income Pod")
        pod_process_info.process.terminate()
        pod_process_info.process.join()

    @tutorial_1_test
    @pytest.mark.parametrize(
        argnames="fixed_notebooks",
        argvalues=(1,),
        indirect=True,
    )
    def test_tutorial_1(
        self,
        authentication_user: str,
        change_dir_code: str,
        clear_log_queue: None,
        fixed_notebooks: NotebookNode,
        keystore_path_code: str,
        patched_authentication_code: str,
    ) -> None:
        """Tests that we can start a fresh pod."""
        tutorial_1: NotebookNode = fixed_notebooks
        with testbook(tutorial_1, execute=False, timeout=POD_TEST_TIMEOUT_PERIOD) as tb:
            tb.inject(change_dir_code, pop=True)
            tb.inject(patched_authentication_code, pop=True)
            tb.inject(keystore_path_code, pop=True)

            # Add notebook logging support
            tb.inject(
                notebook_queue_logging_code("tutorial_1"),
                after="logger_setup",
                run=False,
            )

            logger.info("Running tutorial 1")
            with patch_key_saver(tb) as mock_save_to_key_store_tb_obj:
                # Not technically a Mock but can be used directly as one
                mock_save_to_key_store: Mock = cast(Mock, mock_save_to_key_store_tb_obj)
                _execute(tb)
                # Should only have been called once as cached afterwards
                mock_save_to_key_store.assert_called_once()

            cell_outputs = [
                cell["outputs"] for cell in tb.cells if cell["cell_type"] == "code"
            ]

        # We check the outputs of the second last item of the last cell of the notebook
        # The reason it is the second last output of the cell is because the stack
        # trace that gets outputted when the pod is halted is the last item
        assert "Pod started... press Ctrl+C to stop" in cell_outputs[-1][-2]["text"]

    @tutorial_2_test
    @pytest.mark.parametrize(
        argnames="fixed_notebooks",
        argvalues=(2,),
        indirect=True,
    )
    def test_tutorial_2(
        self,
        authentication_user: str,
        census_income_pod: PodInfo,
        change_dir_code: str,
        clear_log_queue: None,
        extra_imports: str,
        fixed_notebooks: NotebookNode,
        keystore_path_code: str,
        patched_authentication_cleanup_code: str,
        patched_authentication_code: str,
    ) -> None:
        """Tests that modeller can train on census income pod."""
        tutorial_2: NotebookNode = fixed_notebooks

        with testbook(tutorial_2, execute=False, timeout=MODELLER_TIMEOUT_PERIOD) as tb:
            tb.inject(change_dir_code, pop=True)
            tb.inject(extra_imports, pop=True)
            tb.inject(patched_authentication_code, pop=True)
            tb.inject(keystore_path_code, pop=True)

            # Add notebook logging support
            tb.inject(
                notebook_queue_logging_code("tutorial_2"),
                after="logger_setup",
                run=False,
            )

            logger.info("Running tutorial 2")
            with patch_key_saver(tb) as mock_save_to_key_store_tb_obj:
                # Not technically a Mock but can be used directly as one
                mock_save_to_key_store: Mock = cast(Mock, mock_save_to_key_store_tb_obj)
                _execute(tb)
                # Should only have been called once as cached afterwards
                mock_save_to_key_store.assert_called_once()

            tb.inject(patched_authentication_cleanup_code, pop=True)

        assert (TUTORIALS_ROOT / "training_a_model.pt").exists()

    @tutorial_3_test
    @pytest.mark.skip(
        "This tutorial works and should pass but it fails due to a CellTimeOutError. "
        + "Needs further investigation."
    )
    @pytest.mark.parametrize(
        argnames="fixed_notebooks",
        argvalues=(3,),
        indirect=True,
    )
    def test_tutorial_3(
        self,
        authentication_user: str,
        change_dir_code: str,
        clear_log_queue: None,
        extra_imports: str,
        fixed_notebooks: NotebookNode,
        keystore_path_code: str,
        patched_authentication_code: str,
    ) -> None:
        """Tests that we can start a fresh pod using the yaml configuration."""
        tutorial_3: NotebookNode = fixed_notebooks
        with testbook(tutorial_3, execute=False, timeout=POD_TEST_TIMEOUT_PERIOD) as tb:
            tb.inject(change_dir_code, pop=True)
            tb.inject(extra_imports, pop=True)
            tb.inject(patched_authentication_code, pop=True)
            tb.inject(keystore_path_code, pop=True)

            # Add notebook logging support
            tb.inject(
                notebook_queue_logging_code("tutorial_3"),
                after="logger_setup",
                run=False,
            )

            logger.info("Running tutorial 3")
            with patch_key_saver(tb):
                _execute(tb, fail_on_timeout=False)

            cell_outputs = [
                cell["outputs"] for cell in tb.cells if cell["cell_type"] == "code"
            ]

        # We check the outputs of the second last item of the last cell of the notebook
        # The reason it is the second last output of the cell is because the stack
        # trace that gets outputted when the pod is halted is the last item
        assert "Pod started... press Ctrl+C to stop" in cell_outputs[-1][-2]["text"]

    @tutorial_4_test
    @pytest.mark.parametrize(
        argnames="fixed_notebooks",
        argvalues=(4,),
        indirect=True,
    )
    def test_tutorial_4(
        self,
        authentication_user: str,
        census_income_pod: PodInfo,
        change_dir_code: str,
        clear_log_queue: None,
        extra_imports: str,
        fixed_notebooks: NotebookNode,
        keystore_path_code: str,
        patched_authentication_cleanup_code: str,
        patched_authentication_code: str,
        second_census_income_pod: PodInfo,
    ) -> None:
        """Tests that we can train on multiple pods in one task."""
        tutorial_4: NotebookNode = fixed_notebooks
        with testbook(
            tutorial_4, execute=False, timeout=MULTI_POD_MODELLER_TIMEOUT_PERIOD
        ) as tb:
            tb.inject(change_dir_code, pop=True)
            tb.inject(extra_imports, pop=True)
            tb.inject(patched_authentication_code, pop=True)
            tb.inject(keystore_path_code, pop=True)

            # Add notebook logging support
            tb.inject(
                notebook_queue_logging_code("tutorial_4"),
                after="logger_setup",
                run=False,
            )

            logger.info("Running tutorial 4")
            with patch_key_saver(tb):
                _execute(tb)

            tb.inject(patched_authentication_cleanup_code, pop=True)

        assert (TUTORIALS_ROOT / "training_a_model_on_two_pods.pt").exists()

    @tutorial_5_test
    @pytest.mark.parametrize(
        argnames="fixed_notebooks",
        argvalues=(5,),
        indirect=True,
    )
    def test_tutorial_5(
        self,
        authentication_user: str,
        change_dir_code: str,
        clear_log_queue: None,
        extra_imports: str,
        fixed_notebooks: NotebookNode,
        keystore_path_code: str,
        patched_authentication_code: str,
    ) -> None:
        """Tests running image data pod."""
        tutorial_5: NotebookNode = fixed_notebooks
        with testbook(tutorial_5, execute=False, timeout=POD_TEST_TIMEOUT_PERIOD) as tb:
            tb.inject(change_dir_code, pop=True)
            tb.inject(extra_imports, pop=True)
            tb.inject(patched_authentication_code, pop=True)
            tb.inject(keystore_path_code, pop=True)

            # Add notebook logging support
            tb.inject(
                notebook_queue_logging_code("tutorial_5"),
                after="logger_setup",
                run=False,
            )

            logger.info("Running tutorial 5")
            with patch_key_saver(tb) as mock_save_to_key_store_tb_obj:
                # Not technically a Mock but can be used directly as one
                mock_save_to_key_store: Mock = cast(Mock, mock_save_to_key_store_tb_obj)
                _execute(tb, fail_on_timeout=False)
                # Should only have been called once as cached afterwards
                mock_save_to_key_store.assert_called_once()

            cell_outputs = [
                cell["outputs"] for cell in tb.cells if cell["cell_type"] == "code"
            ]

        # We check the outputs of the second last item of the last cell of the notebook
        # The reason it is the second last output of the cell is because the stack
        # trace that gets outputted when the pod is halted is the last item
        assert "Pod started... press Ctrl+C to stop" in cell_outputs[-1][-2]["text"]

    @tutorial_6_test
    @pytest.mark.parametrize(
        argnames="fixed_notebooks",
        argvalues=(6,),
        indirect=True,
    )
    def test_tutorial_6(
        self,
        authentication_user: str,
        change_dir_code: str,
        clear_log_queue: None,
        extra_imports: str,
        fixed_notebooks: NotebookNode,
        keystore_path_code: str,
        mnist_pod: PodInfo,
        patched_authentication_cleanup_code: str,
        patched_authentication_code: str,
    ) -> None:
        """Tests training on images."""
        tutorial_6: NotebookNode = fixed_notebooks
        with testbook(
            tutorial_6, execute=False, timeout=IMAGE_MODELLER_TIMEOUT_PERIOD
        ) as tb:
            tb.inject(change_dir_code, pop=True)
            tb.inject(extra_imports, pop=True)
            tb.inject(patched_authentication_code, pop=True)
            tb.inject(keystore_path_code, pop=True)

            # Add notebook logging support
            tb.inject(
                notebook_queue_logging_code("tutorial_6"),
                after="logger_setup",
                run=False,
            )

            logger.info("Running tutorial 6")
            with patch_key_saver(tb) as mock_save_to_key_store_tb_obj:
                # Not technically a Mock but can be used directly as one
                mock_save_to_key_store: Mock = cast(Mock, mock_save_to_key_store_tb_obj)
                _execute(tb)
                # Should only have been called once as cached afterwards
                mock_save_to_key_store.assert_called_once()

            tb.inject(patched_authentication_cleanup_code, pop=True)

        assert (TUTORIALS_ROOT / "training_on_images.pt").exists()

    @tutorial_7_test
    @pytest.mark.parametrize(
        argnames="fixed_notebooks",
        argvalues=(7,),
        indirect=True,
    )
    def test_tutorial_7(
        self,
        authentication_user: str,
        census_income_pod: PodInfo,
        change_dir_code: str,
        clear_log_queue: None,
        extra_imports: str,
        fixed_notebooks: NotebookNode,
        keystore_path_code: str,
        patched_authentication_cleanup_code: str,
        patched_authentication_code: str,
    ) -> None:
        """Tests custom models."""
        tutorial_7: NotebookNode = fixed_notebooks
        with testbook(tutorial_7, execute=False, timeout=MODELLER_TIMEOUT_PERIOD) as tb:
            tb.inject(change_dir_code, pop=True)
            tb.inject(extra_imports, pop=True)
            tb.inject(patched_authentication_code, pop=True)
            tb.inject(keystore_path_code, pop=True)

            # Add notebook logging support
            tb.inject(
                notebook_queue_logging_code("tutorial_7"),
                after="logger_setup",
                run=False,
            )

            logger.info("Running tutorial 7")
            with patch_key_saver(tb) as mock_save_to_key_store_tb_obj:
                # Not technically a Mock but can be used directly as one
                mock_save_to_key_store: Mock = cast(Mock, mock_save_to_key_store_tb_obj)
                _execute(tb)
                # Should only have been called once as cached afterwards
                mock_save_to_key_store.assert_called_once()

            tb.inject(patched_authentication_cleanup_code, pop=True)

        assert (TUTORIALS_ROOT / "training_a_custom_model.pt").exists()

    @tutorial_8_test
    @pytest.mark.parametrize(
        argnames="fixed_notebooks",
        argvalues=((2, 8),),
        indirect=True,
    )
    def test_tutorial_8(
        self,
        authentication_user: str,
        census_income_pod: PodInfo,
        change_dir_code: str,
        clear_log_queue: None,
        extra_imports: str,
        fixed_notebooks: Tuple[NotebookNode, NotebookNode],
        keystore_path_code: str,
        patched_authentication_cleanup_code: str,
        patched_authentication_code: str,
    ) -> None:
        """Tests pretrained models.

        First runs tutorial 3 to get the pretrained model that gets generated before
        running tutorial 8.
        """
        tutorial_2, tutorial_8 = fixed_notebooks
        with testbook(tutorial_2, execute=False, timeout=MODELLER_TIMEOUT_PERIOD) as tb:
            tb.inject(change_dir_code, pop=True)
            tb.inject(extra_imports, pop=True)
            tb.inject(patched_authentication_code, pop=True)
            tb.inject(keystore_path_code, pop=True)

            # Add notebook logging support
            tb.inject(
                notebook_queue_logging_code("tutorial_2"),
                after="logger_setup",
                run=False,
            )

            logger.info("Running tutorial 2")
            with patch_key_saver(tb) as mock_save_to_key_store_tb_obj:
                # Not technically a Mock but can be used directly as one
                mock_save_to_key_store: Mock = cast(Mock, mock_save_to_key_store_tb_obj)
                _execute(tb)
                # Should only have been called once as cached afterwards
                mock_save_to_key_store.assert_called_once()

            tb.inject(patched_authentication_cleanup_code, pop=True)

        assert (TUTORIALS_ROOT / "training_a_model.pt").exists()

        with testbook(tutorial_8, execute=False, timeout=MODELLER_TIMEOUT_PERIOD) as tb:
            tb.inject(change_dir_code, pop=True)
            tb.inject(extra_imports, pop=True)
            tb.inject(patched_authentication_code, pop=True)
            tb.inject(keystore_path_code, pop=True)

            # Add notebook logging support
            tb.inject(
                notebook_queue_logging_code("tutorial_8"),
                after="logger_setup",
                run=False,
            )

            logger.info("Running tutorial 8")
            with patch_key_saver(tb) as mock_save_to_key_store_tb_obj:
                # Not technically a Mock but can be used directly as one
                mock_save_to_key_store: Mock = cast(Mock, mock_save_to_key_store_tb_obj)  # type: ignore[no-redef] # Reason: In a separate with statement # noqa: B950
                _execute(tb)
                # Should NOT have been called as already cached from running Tutorial 3
                mock_save_to_key_store.assert_not_called()

            tb.inject(patched_authentication_cleanup_code, pop=True)

    @tutorial_9_test
    @pytest.mark.parametrize(
        argnames="fixed_notebooks",
        argvalues=(9,),
        indirect=True,
    )
    def test_tutorial_9(
        self,
        authentication_user: str,
        census_income_pod: PodInfo,
        change_dir_code: str,
        clear_log_queue: None,
        extra_imports: str,
        fixed_notebooks: NotebookNode,
        keystore_path_code: str,
        patched_authentication_cleanup_code: str,
        patched_authentication_code: str,
    ) -> None:
        """Tests that modeller can train privately on census income pod."""
        tutorial_9: NotebookNode = fixed_notebooks

        with testbook(
            tutorial_9,
            execute=False,
            # Privacy tutorial takes longer to run, so give 8 minutes timeout
            timeout=8 * 60,
        ) as tb:
            tb.inject(change_dir_code, pop=True)
            tb.inject(extra_imports, pop=True)
            tb.inject(patched_authentication_code, pop=True)
            tb.inject(keystore_path_code, pop=True)

            # Add notebook logging support
            tb.inject(
                notebook_queue_logging_code("tutorial_9"),
                after="logger_setup",
                run=False,
            )

            logger.info("Running tutorial 9")
            with patch_key_saver(tb) as mock_save_to_key_store_tb_obj:
                # Not technically a Mock but can be used directly as one
                mock_save_to_key_store: Mock = cast(Mock, mock_save_to_key_store_tb_obj)
                _execute(tb)
                # Should only have been called once as cached afterwards
                mock_save_to_key_store.assert_called_once()

            tb.inject(patched_authentication_cleanup_code, pop=True)

    @tutorial_10_test
    @pytest.mark.parametrize(
        argnames="fixed_notebooks",
        argvalues=(10,),
        indirect=True,
    )
    def test_tutorial_10(
        self,
        authentication_user: str,
        change_dir_code: str,
        clear_log_queue: None,
        extra_imports: str,
        fixed_notebooks: NotebookNode,
        keystore_path_code: str,
        patched_authentication_code: str,
    ) -> None:
        """Tests running segmentation data pod."""
        tutorial_10: NotebookNode = fixed_notebooks
        with testbook(
            tutorial_10, execute=False, timeout=POD_TEST_TIMEOUT_PERIOD
        ) as tb:
            tb.inject(change_dir_code, pop=True)
            tb.inject(extra_imports, pop=True)
            tb.inject(patched_authentication_code, pop=True)
            tb.inject(keystore_path_code, pop=True)

            # Add notebook logging support
            tb.inject(
                notebook_queue_logging_code("tutorial_10"),
                after="logger_setup",
                run=False,
            )

            logger.info("Running tutorial 10")
            with patch_key_saver(tb) as mock_save_to_key_store_tb_obj:
                # Not technically a Mock but can be used directly as one
                mock_save_to_key_store: Mock = cast(Mock, mock_save_to_key_store_tb_obj)
                _execute(tb, fail_on_timeout=False)
                # Should only have been called once as cached afterwards
                mock_save_to_key_store.assert_called_once()

            cell_outputs = [
                cell["outputs"] for cell in tb.cells if cell["cell_type"] == "code"
            ]

        # We check the outputs of the second last item of the last cell of the notebook
        # The reason it is the second last output of the cell is because the stack
        # trace that gets outputted when the pod is halted is the last item
        assert "Pod started... press Ctrl+C to stop" in cell_outputs[-1][-2]["text"]

    @tutorial_11_test
    @pytest.mark.parametrize(
        argnames="fixed_notebooks",
        argvalues=(11,),
        indirect=True,
    )
    def test_tutorial_11(
        self,
        authentication_user: str,
        change_dir_code: str,
        clear_log_queue: None,
        extra_imports: str,
        fixed_notebooks: NotebookNode,
        keystore_path_code: str,
        patched_authentication_cleanup_code: str,
        patched_authentication_code: str,
        seg_pod: PodInfo,
    ) -> None:
        """Tests custom segmentation models."""
        tutorial_11: NotebookNode = fixed_notebooks
        with testbook(
            tutorial_11, execute=False, timeout=IMAGE_MODELLER_TIMEOUT_PERIOD
        ) as tb:
            tb.inject(change_dir_code, pop=True)
            tb.inject(extra_imports, pop=True)
            tb.inject(patched_authentication_code, pop=True)
            tb.inject(keystore_path_code, pop=True)

            # Add notebook logging support
            tb.inject(
                notebook_queue_logging_code("tutorial_11"),
                after="logger_setup",
                run=False,
            )

            logger.info("Running tutorial 11")
            with patch_key_saver(tb):
                _execute(tb)

            tb.inject(patched_authentication_cleanup_code, pop=True)

        assert (TUTORIALS_ROOT / "training_a_custom_segmentation_model.pt").exists()
