from semantic_kernel.functions import kernel_function
from semantic_kernel.processes.kernel_process import KernelProcessStep

from config.config import *
from config.config_secrets import *
from utils.logger import Logger


# Non-AI step that saves data with unredacted PII to an audit trail database.
# This class is mocked for the purpose of the sample application.
class MockAuditDatabaseStep(KernelProcessStep):
    _agentName = "MockAuditDatabaseStep"

    @kernel_function
    def execute(self, unredacted_data):
        Logger.log_step_start(self._agentName)

        Logger.log_step_result("Saved unredacted data to the audit trail database.")
        Logger.log_step_completion(self._agentName)

        return input