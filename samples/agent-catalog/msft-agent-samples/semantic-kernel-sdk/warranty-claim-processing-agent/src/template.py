import asyncio

from semantic_kernel import Kernel
from semantic_kernel.processes import ProcessBuilder
from semantic_kernel.processes.kernel_process import KernelProcessEvent
from semantic_kernel.processes.local_runtime.local_kernel_process import start

from steps.audit_database_step import MockAuditDatabaseStep
from steps.document_intelligence_step import (DocumentIntelligenceStep,
                                                MockDocumentIntelligenceStep)
from steps.pii_redaction_step import MockPiiRedactionStep, PiiRedactionStep
from steps.quick_access_database_step import MockQuickAccessDatabaseStep
from steps.claim_analysis_agent_step import (MockClaimAnalysisAgentStep,
                                          ClaimAnalysisAgentStep)
from config.config import *


# Main function to process the insurance claim using Semantic Kernel
async def build_and_run_semantic_kernel_process(document_path):
    
    # Create the process builder
    process_builder = ProcessBuilder(name="WarrantyClaimWorkflow")

    # Add the agents for each step of the process
    # If mocking is enabled (and it is enabled by default), use mock agents instead. Mock agents don't call the backend AI services; instead they operate on hardcoded data. This allows you to save the cost or reduce the latency when debugging.
    form_extraction_step = process_builder.add_step(MockDocumentIntelligenceStep if MOCK_DOC_INTELLIGENCE_STEP else DocumentIntelligenceStep)
    pii_redaction_step = process_builder.add_step(MockPiiRedactionStep if MOCK_PII_REDACTION_STEP else PiiRedactionStep)
    claims_analysis_step = process_builder.add_step(MockClaimAnalysisAgentStep if MOCK_CLAIMS_ANALYSIS_STEP else ClaimAnalysisAgentStep)
    audit_database_step = process_builder.add_step(MockAuditDatabaseStep)
    quick_access_database_step = process_builder.add_step(MockQuickAccessDatabaseStep)

    # Orchestrate the agents by assigning them to the steps of the process
    process_builder.on_input_event("Start").send_event_to(
        target=form_extraction_step, function_name="execute", parameter_name="document_path"
    )

    form_extraction_step.on_function_result("execute").send_event_to(
        target=pii_redaction_step, function_name="execute", parameter_name="data_to_redact"
    )

    form_extraction_step.on_function_result("execute").send_event_to(
        target=audit_database_step, function_name="execute", parameter_name="unredacted_data"
    )

    pii_redaction_step.on_function_result("execute").send_event_to(
        target=claims_analysis_step, function_name="execute", parameter_name="claim_data_to_analyze"
    )

    claims_analysis_step.on_function_result("execute").send_event_to(
        target=quick_access_database_step, function_name="execute", parameter_name="redacted_data"
    )

    # Create a Semantic Kernel kernel
    kernel = Kernel()

    # Build the process
    kernel_process = process_builder.build()

    # Start the process
    async with await start(
        process=kernel_process,
        kernel=kernel,
        initial_event=KernelProcessEvent(id="Start", data=document_path),
    ) as process_context:
        _ = await process_context.get_state()

if __name__ == "__main__":
    asyncio.run(build_and_run_semantic_kernel_process(INPUT_DOCUMENT_PATH))