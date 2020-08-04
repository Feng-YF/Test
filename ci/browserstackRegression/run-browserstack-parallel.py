#!/usr/bin/env python3

import argparse
from datetime import datetime, timedelta
import itertools
import logging
import multiprocessing
import os
from subprocess import Popen, PIPE
from typing import List
from threading import Thread


# FIXME: Break into packages
class Platforms:
    ANDROID = "android"
    IOS = "ios"


class Status:
    NOT_STARTED = "not_started"
    STARTED = "started"
    FINISHED = "finished"
    ERRORED = "errored"
    TERMINATED = "terminated"
    TIMED_OUT = "timed_out"


class AppCenterLookup:
    # FIXME: There is inconsistency in the app-center naming convention making it difficult to dynamically aquire name
    # Determine cross section of difference, make a better lookup here
    lookup = {
        "armenia": {
            Platforms.ANDROID: "HSBC-Armenia-Cert-develop-1",
            Platforms.IOS: "HSBC-Armenia-Cert-develop"
        },
        "australia": {
            Platforms.ANDROID: "HSBC-Australia-Cert-develop",
            Platforms.IOS: "HSBC-Australia-Cert-develop-1"
        },
        "bahrain": {
            Platforms.ANDROID: "HSBC-Bahrain-Cert-develop-1",
            Platforms.IOS: "HSBC-Bahrain-Cert-develop"
        },
        "canada": {
            Platforms.ANDROID: "HSBC-Canada-Cert-develop",
            Platforms.IOS: "HSBC-Canada-Cert-develop-1"
        },
        "us": {
            Platforms.ANDROID: "HSBC-US-Cert-develop",
            Platforms.IOS: "HSBC-US-Cert-develop-1"
        }
    }


class TestProcess:

    def __init__(self, country: str, locale: str, platform: str, test_tags: List[str]):
        """
        TestProcess is used to track status for an individual test process.
        :param country: The country that this test process is executing
        :type country: str
        :param locale: The locale language that is being used to execute
        :type locale: str
        :param platform: The platform on which the test is being executed
        :type platform: str
        :param test_tags: Tags being used for this execution
        :type test_tags: List[str]
        """
        # noinspection PyTypeChecker
        self.start_time: datetime = None
        # noinspection PyTypeChecker
        self.end_time: datetime = None

        self.name = f"{country}-{locale}-{platform}"

        # noinspection PyTypeChecker
        self.test_process: multiprocessing.Process = None
        self._process_queue = multiprocessing.Queue()
        self.monitor_thread = Thread(target=self._monitor_loop, daemon=True)

        self.country = country
        self.locale = locale
        self.platform = platform
        self.tags = test_tags

        self.status = Status.NOT_STARTED
        self.timeout = timedelta(hours=4)

        self.log = logging.getLogger(self.name)
        self.log.level = logging.DEBUG

        self.base_command = "./ci/run-browserstack-test.sh"

    def __str__(self):
        return self.name

    def start(self):
        self.log.info("Starting")
        self.status = Status.STARTED
        # FIXME: Determine if upload should block here before thread start
        self.test_process = multiprocessing.Process(target=self._process_target,
                                                    args=[os.environ, self._process_queue],
                                                    daemon=True)
        self.test_process.start()
        self.monitor_thread.start()
        self.start_time = datetime.now()

    def kill(self):
        if self.test_process is not None:
            self.test_process.kill()

        if self.test_process.is_alive():
            self.test_process.join()

        self.status = Status.TERMINATED
        self.end_time = datetime.now()

    def is_running(self):
        if self.test_process is not None:
            status = self.test_process.is_alive()
        else:
            status = self.status in [Status.STARTED]
        return status

    def _upload_app_to_browser_stack(self):
        # FIXME: get time of last upload, compare, don't upload if same build
        self.log.info("Uploading app to Browser Stack")
        app_center_api = os.environ.get("APP_CENTER_TOKEN", "a287a6ca967f4633efcf4c133abb9b956b39d27f")
        owner_name = "hgsu-mobile-wzyt"
        app_name = AppCenterLookup.lookup.get(self.country).get(self.platform)

        command = [r'./ci/upload-latestbuild-to-bs-from-appcenter',
                   '--token',
                   app_center_api,
                   '--owner-name',
                   owner_name,
                   '--app-name',
                   app_name]
        self.log.debug(f"Executing: {command}")
        upload_process = Popen(command, stderr=PIPE, stdout=PIPE)
        upload_process.wait()
        app_id = upload_process.stdout.readline().strip()

        for line in upload_process.stderr:
            self.log.info(line.decode().rstrip())
        for line in upload_process.stdout:
            self.log.info(line.decode().rstrip())
        return app_id

    def _monitor_loop(self):
        self.status = self._process_queue.get()  # Blocking call for the moment
        self.end_time = datetime.now()

    def _process_target(self, environment, com_queue: multiprocessing.Queue):
        app_id = self._upload_app_to_browser_stack()
        os.environ = environment
        os.environ['BROWSERSTACK_APP_ID'] = app_id

        # FIXME: Need to determine a good way to construct tags dynamically, currently appending: '-<country>'
        parsed_tags = '"'
        for tag in self.tags:
            parsed_tags += f'{tag}-{self.country} '
        if self.platform == Platforms.ANDROID:
            parsed_tags += "@~ios"
        elif self.platform == Platforms.IOS:
            parsed_tags += "@~android"
        parsed_tags = parsed_tags.rstrip() + '"'

        args_list = [self.base_command, self.platform, self.country, self.locale, parsed_tags]
        self.log.debug(f"Executing: {args_list}")
        try:
            process = Popen(args_list, stdout=PIPE, stderr=PIPE)
            process.wait()
            # FIXME: realtime read of stderr? Will this make logs harder to follow?
            for line in process.stderr:
                self.log.info(line.decode().rstrip())

            if process.returncode == 0:
                self.status = Status.FINISHED
            else:
                self.status = Status.ERRORED

            self.log.info(f"Ending: {self.status}")

        except FileNotFoundError as exception:
            self.status = Status.ERRORED
            self.log.error(f"File not found: {exception}")

        com_queue.put(self.status)


class BrowserStackExecutionManager:
    max_parallel_executors = 3
    last_start = datetime.min
    start_offset = timedelta(seconds=5)

    running = False

    locales = [
        "canada_en",
        "us_en"
    ]

    platforms = [
        "ios",
        "android"
    ]

    tags = [
        "@smoke-tests"
    ]

    run_list: List[TestProcess] = []
    active_runs: List[TestProcess] = []

    def __init__(self, **kwargs):
        """
        BrowserStackExecutionManager provides methods to start and track execution threads for Browser Stack tests.
        Parallelization is managed here
        :param kwargs: Optional keyword arguments for manager settings
        :keyword max_executors: Maximumum number of parallel threads to use
        :keyword locales: List of locales to be tested. e.g. ["canada_en", "us_en", ...]
        :keyword platforms: List of platforms to be tested. e.g. ["android", "ios"]
        :keyword tags: List of test tags to use. Tags will be suffixed with country. e.g. ["smoke-tests", ...] becomes
        ["smoke-tests-canada", ...]
        """
        self.log = logging.getLogger("Execution Manager")
        self.log.setLevel(logging.DEBUG)

        self.max_parallel_executors = kwargs.get("max_executors", self.max_parallel_executors)
        self.locales = kwargs.get("locales", self.locales)
        self.platforms = kwargs.get("platforms", self.platforms)
        self.tags = kwargs.get("tags", self.tags)

    def _create_permutations(self):
        """
        Generate initial execution order of tests, store as self.run_list.
        Order generated is by locale then platform, i.e. all entities on android, then all entities on iOS
        :return: None
        """
        # FIXME: determine best execution order of permutations: platform:entity, entity:platform, etc.
        permutations = itertools.product(self.platforms, self.locales)
        for test_description in permutations:
            locale_split = test_description[1].split("_")
            test_process = TestProcess(locale_split[0], locale_split[1],
                                       test_description[0],
                                       self.tags)
            self.run_list.append(test_process)

    def _get_next_process(self):
        """
        Determine the next test to run. Decision is based on initial execution order, what entities are currently
        running, and which entities have already been completed. The goal is to prioritize execution based on available
        resources.
        :return: TestProcess of the next test to be run
        :rtype: TestProcess
        """
        entities_completed: List[TestProcess] = []
        entities_in_progress: List[TestProcess] = []
        fallback: List[TestProcess] = []

        for test_process in self.run_list:
            # Has this process been started?
            if test_process.status is not Status.NOT_STARTED:
                # It has been started: Is it done?
                if test_process.status == Status.STARTED:
                    entities_in_progress.append(test_process)
                elif test_process.status not in [Status.STARTED, Status.NOT_STARTED]:
                    entities_completed.append(test_process)
            else:
                # Entity has not been started previously: Is it currently in progress?
                if test_process.country not in entities_in_progress:
                    # Not currently in progress, good to start
                    return test_process
                else:
                    # Currently in progress, de-prioritize
                    fallback.append(test_process)

        # All entries searched, remaining items (if any) are for entities that have been previously started
        if len(fallback) == 0:
            # Nothing left to do
            return None

        # for remaining, prioritize completed entities over in progress
        for test_process in fallback:
            if test_process.country in [process.country for process in entities_completed]:
                return test_process

        # No better options, get the next on the heap
        return fallback.pop()

    def execute_all(self):
        """
        Generate test permutations based on list of entities and platforms
        Execute each with the predefined maximum number of parallel threads
        :return: None
        """
        self._create_permutations()

        self.log.info("Queued Jobs:")
        for job in self.run_list:
            self.log.info(f"\t\t{job.name}")

        self.running = True
        while self.running:
            # Throttle test starts
            if datetime.now() < self.last_start + self.start_offset:
                continue
            # Do we have available parallel threads?
            elif len(self.active_runs) < self.max_parallel_executors:
                # add executor
                next_run = self._get_next_process()
                if next_run is not None:
                    self.log.debug(f"Adding Executor: {next_run}")
                    self.active_runs.append(next_run)
                    next_run.start()
                    self.last_start = datetime.now()

            # Check for completed processes
            for active_process in self.active_runs:
                if not active_process.is_running():
                    self.active_runs.remove(active_process)

            # Check if we're done
            for run in self.run_list:
                if run.status == Status.NOT_STARTED or run.is_running():
                    break
            else:
                self.running = False

        self.log.info("All Executions Completed")
        for run in self.run_list:
            self.log.info(f"\n\t\t{run.name}\n"
                          f"\t\t\tStatus: {run.status}\n"
                          f"\t\t\tStarted: {run.start_time}\n"
                          f"\t\t\tEnded: {run.end_time}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute Regression in parallel via BrowserStack")
    parser.add_argument('--max_executors', metavar='MAX_EXECUTORS', help='Maximum number of parallel executions',
                        default=3)
    parser.add_argument('--locales', metavar='locales', help='Locales to be executed',
                        default=["canada_en", "us_en", "mexico_es"], nargs="*")
    parser.add_argument('--platforms', metavar='platforms', help='Platforms to be executed',
                        default=["android", "ios"], nargs="*")
    parser.add_argument("--test_tags", help="Prefixes for tags to be tested, will append with country name",
                        default=["@smoke-tests"], nargs="*")

    args = parser.parse_args()
    max_executors = args.max_executors
    locales = args.locales
    platforms = args.platforms
    tags = args.test_tags

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)-15s - %(name)-15s - %(message)s")

    executor = BrowserStackExecutionManager(max_executors=max_executors, locales=locales,
                                            platforms=platforms, test_tags=tags)
    executor.execute_all()
