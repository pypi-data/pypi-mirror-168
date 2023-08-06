import sys
import contextlib
from unittest.case import (
    addModuleCleanup,
    FunctionTestCase,
    SkipTest,
    skip,
    skipIf,
    skipUnless,
    expectedFailure,
)
from unittest.case import TestCase as TestCaseSrc
from unittest.case import _Outcome, _ShouldStop, warnings, safe_repr


class Outcome(_Outcome):
    def __init__(self, result=None):
        super().__init__(result)
        self.error_stages = (
            []
        )  # 失败发生在的步骤：_miniClassSetUp, _miniSetUp, _miniTearDown, setUpClass, tearDownClass, setUp, tearDown, testMethod

    @contextlib.contextmanager
    def testPartExecutor(self, test_case, isTest=False, error_stage=None):
        """
        rewrite for error_stages
        :error_stage: current error stage name
        """
        old_success = self.success
        self.success = True
        try:
            yield
        except KeyboardInterrupt:
            raise
        except SkipTest as e:
            self.success = False
            self.skipped.append((test_case, str(e)))
        except _ShouldStop:
            pass
        except:
            exc_info = sys.exc_info()
            if self.expecting_failure:
                self.expectedFailure = exc_info
            else:
                self.success = False
                self.errors.append((test_case, exc_info))
            # explicitly break a reference cycle:
            # exc_info -> frame -> exc_info
            exc_info = None
        else:
            if self.result_supports_subtests and self.success:
                self.errors.append((test_case, None))
        finally:
            if error_stage and (self.success == self.expecting_failure):
                self.error_stages.append(error_stage)
            self.success = self.success and old_success


# 重写testcase
class TestCase(TestCaseSrc):
    def _callSetUp(self):
        # self._miniSetUp()
        self.setUp()

    def _miniSetUp(self):
        pass

    def _callTearDown(self):
        # self._miniTearDown()
        self.tearDown()

    def _miniTearDown(self):
        pass

    def run(self, result=None):
        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, "startTestRun", None)
            if startTestRun is not None:
                startTestRun()

        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        if getattr(self.__class__, "__unittest_skip__", False) or getattr(
            testMethod, "__unittest_skip__", False
        ):
            # If the class or method was skipped.
            try:
                skip_why = getattr(
                    self.__class__, "__unittest_skip_why__", ""
                ) or getattr(testMethod, "__unittest_skip_why__", "")
                self._addSkip(result, self, skip_why)
            finally:
                result.stopTest(self)
            return

        expecting_failure_method = getattr(
            testMethod, "__unittest_expecting_failure__", False
        )
        expecting_failure_class = getattr(self, "__unittest_expecting_failure__", False)
        expecting_failure = expecting_failure_class or expecting_failure_method
        outcome = Outcome(result)
        try:
            self._outcome = outcome

            with outcome.testPartExecutor(self, error_stage="_miniSetUp"):
                self._miniSetUp()
            if outcome.success:
                with outcome.testPartExecutor(self, error_stage="setUp"):
                    self._callSetUp()
                if outcome.success:
                    outcome.expecting_failure = expecting_failure
                    with outcome.testPartExecutor(
                        self, isTest=True, error_stage="testMethod"
                    ):
                        self._callTestMethod(testMethod)
                    outcome.expecting_failure = False
                    with outcome.testPartExecutor(self, error_stage="tearDown"):
                        self._callTearDown()
            outcome.expecting_failure = False
            with outcome.testPartExecutor(self, error_stage="_miniTearDown"):
                self._miniTearDown()

            self.doCleanups()
            for test, reason in outcome.skipped:
                self._addSkip(result, test, reason)
            self._feedErrorsToResult(result, outcome.errors)
            if outcome.success:
                if expecting_failure:
                    if outcome.expectedFailure:
                        self._addExpectedFailure(result, outcome.expectedFailure)
                    else:
                        self._addUnexpectedSuccess(result)
                else:
                    result.addSuccess(self)
            return result
        finally:
            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, "stopTestRun", None)
                if stopTestRun is not None:
                    stopTestRun()

            # explicitly break reference cycles:
            # outcome.errors -> frame -> outcome -> outcome.errors
            # outcome.expectedFailure -> frame -> outcome -> outcome.expectedFailure
            outcome.errors.clear()
            outcome.expectedFailure = None

            # clear the outcome, no more needed
            self._outcome = None

    def assertSetContainsSubset(self, subset: set, superset: set, msg=None):
        """Checks whether superset is a superset of subset."""
        warnings.warn("assertSetContainsSubset is deprecated", DeprecationWarning)
        missing = []
        for item in subset:
            if item not in superset:
                missing.append(item)

        if not missing:
            return

        standardMsg = ""
        if missing:
            standardMsg = "Missing: %s" % ",".join(safe_repr(m) for m in missing)

        self.fail(self._formatMessage(msg, standardMsg))
