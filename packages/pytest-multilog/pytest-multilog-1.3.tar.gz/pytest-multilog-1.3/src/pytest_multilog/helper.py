# Common test class with miscellaneous utilities and fixtures
import logging
import os
import shutil
import time
from pathlib import Path
from re import Pattern
from typing import List, Union

import pytest
from _pytest.fixtures import FixtureRequest


@pytest.mark.usefixtures("logs")
class TestHelper:
    # Output folder
    @property
    def output_folder(self) -> Path:
        return self.root_folder / "out" / "tests"

    # Test folder (running)
    @property
    def test_folder(self) -> Path:
        return self.output_folder / "__running__" / self.worker / self.test_name

    # Test logs
    @property
    def test_logs(self) -> Path:
        return self.test_folder / "pytest.log"

    # Log content assertion
    def check_logs(self, expected: Union[str, Pattern, List[Union[str, Pattern]]], timeout: int = None):
        """
        Verify if expected pattern(s) can be found in current test logs.

        expected: may be:
            - a string (simple "contains" check)
            - a Pattern object (line match with regular expression)
            - a list of both (all list items must match)

        If timeout is provided, loop until either the pattern(s) is/are found or the timeout expires.
        """
        retry = True
        init_time = time.time()
        to_check = expected if isinstance(expected, list) else [expected]
        while retry:
            try:
                # Get logs content
                with self.test_logs.open("r", encoding="utf-8") as f:
                    logs = f.read()

                    # Verify all patterns are found in logs
                    for expected_pattern in to_check:
                        if isinstance(expected_pattern, Pattern):
                            # Check for regular expression (at least one line match)
                            for log_line in logs.splitlines(keepends=False):
                                if expected_pattern.search(log_line) is not None:
                                    break
                            else:
                                raise AssertionError(f"Expected pattern not found in logs: {expected_pattern.pattern}")
                        else:
                            # Simple string check
                            assert expected_pattern in logs, f"Expected pattern not found in logs: {expected_pattern}"

                    # If we get here: all expected patterns are found
                    retry = False
            except AssertionError as e:
                # Some pattern is still not found
                if timeout is None or (time.time() - init_time) >= timeout:
                    # No timeout, or timeout expired: raise assertion error
                    raise e
                else:
                    # Sleep a bit before checking logs again
                    time.sleep(0.5)

    # Test folder (final)
    @property
    def __test_final_folder(self) -> Path:
        return self.output_folder / self.test_name

    # Test name
    @property
    def test_name(self) -> str:
        return Path(os.environ["PYTEST_CURRENT_TEST"].split(" ")[0]).name.replace("::", "_").replace(".py", "")

    # Worker name in parallelized tests
    @property
    def worker(self) -> str:
        return os.environ["PYTEST_XDIST_WORKER"] if "PYTEST_XDIST_WORKER" in os.environ else "master"

    # Worker int index
    @property
    def worker_index(self) -> int:
        worker = self.worker
        return int(worker[2:]) if worker.startswith("gw") else 0

    # Per-test logging management
    @pytest.fixture
    def logs(self, request: FixtureRequest):
        # Set root folder
        self.root_folder = Path(request.config.rootdir).absolute().resolve()

        # Prepare test folder
        shutil.rmtree(self.test_folder, ignore_errors=True)
        shutil.rmtree(self.__test_final_folder, ignore_errors=True)
        self.test_folder.mkdir(parents=True, exist_ok=False)

        # Install logging
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        log_format = f"%(asctime)s.%(msecs)03d [{self.worker}/%(name)s] %(levelname)s %(message)s - %(filename)s:%(funcName)s:%(lineno)d"
        date_format = "%Y-%m-%d %H:%M:%S"
        logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=date_format)
        handler = logging.FileHandler(filename=str(self.test_logs), mode="w", encoding="utf-8")
        handler.setFormatter(logging.Formatter(log_format, date_format))
        logging.getLogger().addHandler(handler)

        logging.info("-----------------------------------------------------------------------------------")
        logging.info(f"    New test: {self.test_name}")
        logging.info("-----------------------------------------------------------------------------------")

        # Return to test
        yield

        # Flush logs
        logging.info("-----------------------------------------------------------------------------------")
        logging.info(f"    End of test: {self.test_name}")
        logging.info("-----------------------------------------------------------------------------------")
        logging.shutdown()

        # Move folder
        shutil.move(self.test_folder, self.__test_final_folder)
        self.test_folder.parent.rmdir()
