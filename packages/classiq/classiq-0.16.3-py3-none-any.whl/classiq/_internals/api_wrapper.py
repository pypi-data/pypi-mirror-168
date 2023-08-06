import json
from typing import Dict, Optional, Type, TypeVar

import pydantic
from typing_extensions import Protocol

from classiq.interface.analyzer import analysis_params, result as analysis_result
from classiq.interface.analyzer.analysis_params import AnalysisRBParams
from classiq.interface.applications.qsvm import (
    QSVMData,
    QSVMPredictResult,
    QSVMResult,
    QSVMResultStatus,
    QSVMTestResult,
    QSVMTrainResult,
)
from classiq.interface.chemistry import (
    ground_state_problem,
    ground_state_result,
    ground_state_solver,
    operator,
)
from classiq.interface.combinatorial_optimization import (
    optimization_problem,
    result as opt_result,
)
from classiq.interface.combinatorial_optimization.preferences import (
    GASPreferences,
    QAOAPreferences,
)
from classiq.interface.executor import (
    execution_request,
    result as execute_result,
    vqe_result,
)
from classiq.interface.generator import result as generator_result
from classiq.interface.generator.model import Model, ModelResult
from classiq.interface.jobs import AUTH_HEADER, JobDescription, JobStatus, JSONObject
from classiq.interface.server import routes

from classiq._internals.client import client
from classiq._internals.jobs import JobPoller
from classiq.exceptions import ClassiqAPIError, ClassiqQSVMError, ClassiqValueError

_FAIL_FAST_INDICATOR = "{"
ResultType = TypeVar("ResultType", bound=pydantic.BaseModel)


class StatusType(Protocol):
    ERROR: str


def _parse_job_response(
    job_result: JobDescription[JSONObject],
    output_type: Type[ResultType],
) -> ResultType:
    description = job_result.description
    if job_result.status != JobStatus.COMPLETED:
        raise ClassiqAPIError(description["details"])
    return output_type.parse_obj(description)


def _unpack_results(
    result: JobDescription[JSONObject],
    status_type: Type[StatusType],
    result_type: Type[ResultType],
) -> ResultType:
    description = result.description
    if result.status != JobStatus.COMPLETED:
        return result_type(
            status=description.get("status", status_type.ERROR),
            details=description["details"],
        )
    return result_type.parse_obj(result.description)


class ApiWrapper:
    _AUTH_HEADERS = {AUTH_HEADER}

    @classmethod
    async def _call_task(cls, http_method: str, url: str, body: Optional[Dict] = None):
        res = await client().call_api(http_method=http_method, url=url, body=body)
        if not isinstance(res, dict):
            raise ClassiqValueError(f"Unexpected returned value: {res}")
        return res

    @classmethod
    async def call_generation_task(
        cls, model: Model
    ) -> generator_result.GeneratedCircuit:
        poller = JobPoller(base_url=routes.TASKS_GENERATE_FULL_PATH)
        result = await poller.run_pydantic(model, timeout_sec=None)
        return _parse_job_response(result, generator_result.GeneratedCircuit)

    @staticmethod
    def _is_async_execute_task(request: execution_request.ExecutionRequest):
        return (
            isinstance(
                request.execution_payload, execution_request.QuantumProgramExecution
            )
            and request.execution_payload.syntax
            == execution_request.QuantumInstructionSet.IONQ
        )

    @classmethod
    async def call_execute_grover(
        cls, request: execution_request.ExecutionRequest
    ) -> execute_result.GroverSimulationResults:
        poller = JobPoller(base_url=routes.EXECUTE_GROVER_FULL_PATH)
        result = await poller.run_pydantic(request, timeout_sec=None)
        return _parse_job_response(result, execute_result.GroverSimulationResults)

    @classmethod
    async def call_execute_finance(
        cls, request: execution_request.ExecutionRequest
    ) -> execute_result.FinanceSimulationResults:
        poller = JobPoller(base_url=routes.EXECUTE_FINANCE_FULL_PATH)
        result = await poller.run_pydantic(request, timeout_sec=None)
        return _parse_job_response(result, execute_result.FinanceSimulationResults)

    @classmethod
    async def call_execute_vqe(
        cls, request: execution_request.ExecutionRequest
    ) -> vqe_result.VQESolverResult:
        poller = JobPoller(base_url=routes.EXECUTE_VQE_FULL_PATH)
        result = await poller.run_pydantic(request, timeout_sec=None)
        return _parse_job_response(result, vqe_result.VQESolverResult)

    @classmethod
    async def call_execute_quantum_program(
        cls, request: execution_request.ExecutionRequest
    ) -> execute_result.ExecutionDetails:
        if cls._is_async_execute_task(request):
            poller = JobPoller(
                base_url=routes.EXECUTE_ASYNC_TASKS_FULL_PATH,
                required_headers=cls._AUTH_HEADERS,
            )
        else:
            poller = JobPoller(
                base_url=routes.EXECUTE_QUANTUM_PROGRAM_FULL_PATH,
            )
        result = await poller.run_pydantic(request, timeout_sec=None)
        return _parse_job_response(result, execute_result.ExecutionDetails)

    @classmethod
    async def call_analysis_task(
        cls, params: analysis_params.AnalysisParams
    ) -> analysis_result.AnalysisResult:
        # TODO Support smarter json serialization
        params_dict = json.loads(params.json())
        data = await cls._call_task(
            http_method="post",
            url=routes.ANALYZER_FULL_PATH,
            body=params_dict,
        )

        return analysis_result.AnalysisResult.parse_obj(data)

    @classmethod
    async def call_analyzer_app(
        cls, params: generator_result.GeneratedCircuit
    ) -> analysis_result.DataID:
        # TODO Support smarter json serialization
        problem_dict = json.loads(params.json())
        data = await cls._call_task(
            http_method="post",
            url=routes.ANALYZER_DATA_FULL_PATH,
            body=problem_dict,
        )
        return analysis_result.DataID.parse_obj(data)

    @classmethod
    async def get_analyzer_app_data(
        cls, params: analysis_result.DataID
    ) -> generator_result.GeneratedCircuit:
        data = await cls._call_task(
            http_method="get",
            url=f"{routes.ANALYZER_DATA_FULL_PATH}/{params.id}",
        )
        return generator_result.GeneratedCircuit.parse_obj(data)

    @classmethod
    async def call_rb_analysis_task(
        cls, params: AnalysisRBParams
    ) -> analysis_result.RbResults:
        data = await cls._call_task(
            http_method="post",
            url=routes.ANALYZER_RB_FULL_PATH,
            body=params.dict(),
        )

        return analysis_result.RbResults.parse_obj(data)

    @classmethod
    async def call_qubits_connectivity_graphs_task(
        cls, params: analysis_params.AnalysisParams
    ) -> analysis_result.GraphResult:
        # TODO Support smarter json serialization
        params_dict = json.loads(params.json())
        data = await cls._call_task(
            http_method="post",
            url=routes.ANALYZER_QC_GRAPH_FULL_PATH,
            body=params_dict,
        )
        return analysis_result.GraphResult.parse_obj(data)

    @classmethod
    async def call_hardware_connectivity_task(
        cls, params: analysis_params.AnalysisHardwareParams
    ) -> analysis_result.GraphResult:
        # TODO Support smarter json serialization
        params_dict = json.loads(params.json())
        data = await cls._call_task(
            http_method="post",
            url=routes.ANALYZER_HC_GRAPH_FULL_PATH,
            body=params_dict,
        )
        return analysis_result.GraphResult.parse_obj(data)

    @classmethod
    async def call_heatmap_graphs(
        cls, params: analysis_params.AnalysisParams
    ) -> analysis_result.GraphResult:
        # TODO Support smarter json serialization
        params_dict = json.loads(params.json())
        data = await cls._call_task(
            http_method="post",
            url=routes.ANALYZER_HEATMAP_GRAPH_FULL_PATH,
            body=params_dict,
        )
        return analysis_result.GraphResult.parse_obj(data)

    @classmethod
    async def call_table_graphs_task(
        cls,
        params: analysis_params.AnalysisHardwareListParams,
    ) -> analysis_result.GraphResult:
        poller = JobPoller(base_url=routes.ANALYZER_HC_TABLE_GRAPH_FULL_PATH)
        result = await poller.run_pydantic(params, timeout_sec=None)
        return _unpack_results(
            result,
            status_type=analysis_result.GraphStatus,
            result_type=analysis_result.GraphResult,
        )

    @classmethod
    async def call_available_devices_task(
        cls,
        params: analysis_params.AnalysisOptionalDevicesParams,
    ) -> analysis_result.DevicesResult:
        data = await cls._call_task(
            http_method="post",
            url=routes.ANALYZER_OPTIONAL_DEVICES_FULL_PATH,
            body=params.dict(),
        )
        return analysis_result.DevicesResult.parse_obj(data)

    @classmethod
    async def call_gas_circuit_generate_task(
        cls, problem: optimization_problem.OptimizationProblem
    ) -> generator_result.GeneratedCircuit:
        poller = JobPoller(
            base_url=routes.COMBINATORIAL_OPTIMIZATION_GAS_CIRCUIT_FULL_PATH
        )
        result = await poller.run_pydantic(problem, timeout_sec=None)

        return _parse_job_response(result, generator_result.GeneratedCircuit)

    @classmethod
    async def call_combinatorial_optimization_solve_task_gas(
        cls,
        problem: optimization_problem.OptimizationProblem,
    ) -> execute_result.GroverAdaptiveSearchResult:
        if not isinstance(problem.qsolver_preferences, GASPreferences):
            raise ValueError("Must have gas preferences")
        poller = JobPoller(
            base_url=routes.COMBINATORIAL_OPTIMIZATION_SOLVE_GAS_ASYNC_FULL_PATH
        )
        result = await poller.run_pydantic(problem, timeout_sec=None)
        return _parse_job_response(result, execute_result.GroverAdaptiveSearchResult)

    @classmethod
    async def call_combinatorial_optimization_solve_task_vqe(
        cls,
        problem: optimization_problem.OptimizationProblem,
    ) -> vqe_result.OptimizationResult:
        if not isinstance(problem.qsolver_preferences, QAOAPreferences):
            raise ValueError("Must have QAOA preferences")
        poller = JobPoller(
            base_url=routes.COMBINATORIAL_OPTIMIZATION_SOLVE_VQE_ASYNC_FULL_PATH
        )
        result = await poller.run_pydantic(problem, timeout_sec=None)
        return _parse_job_response(result, vqe_result.OptimizationResult)

    @classmethod
    async def call_combinatorial_optimization_solve_classically_task(
        cls, problem: optimization_problem.OptimizationProblem
    ) -> vqe_result.SolverResult:
        problem_dict = json.loads(problem.json())
        data = await cls._call_task(
            http_method="post",
            url=routes.COMBINATORIAL_OPTIMIZATION_SOLVE_CLASSICALLY_FULL_PATH,
            body=problem_dict,
        )

        return vqe_result.SolverResult.parse_obj(data)

    @classmethod
    async def call_combinatorial_optimization_model_task(
        cls, problem: optimization_problem.OptimizationProblem
    ) -> ModelResult:
        problem_dict = json.loads(problem.json())
        data = await cls._call_task(
            http_method="post",
            url=routes.COMBINATORIAL_OPTIMIZATION_MODEL_FULL_PATH,
            body=problem_dict,
        )

        return ModelResult.parse_obj(data)

    @classmethod
    async def call_combinatorial_optimization_operator_task(
        cls, problem: optimization_problem.OptimizationProblem
    ) -> operator.OperatorResult:
        problem_dict = json.loads(problem.json())
        data = await cls._call_task(
            http_method="post",
            url=routes.COMBINATORIAL_OPTIMIZATION_OPERATOR_FULL_PATH,
            body=problem_dict,
        )

        return operator.OperatorResult.parse_obj(data)

    @classmethod
    async def call_combinatorial_optimization_objective_task(
        cls, problem: optimization_problem.OptimizationProblem
    ) -> opt_result.PyomoObjectResult:
        problem_dict = json.loads(problem.json())
        data = await cls._call_task(
            http_method="post",
            url=routes.COMBINATORIAL_OPTIMIZATION_OBJECTIVE_FULL_PATH,
            body=problem_dict,
        )

        return opt_result.PyomoObjectResult.parse_obj(data)

    @classmethod
    async def call_combinatorial_optimization_initial_point_task(
        cls, problem: optimization_problem.OptimizationProblem
    ) -> opt_result.AnglesResult:
        # This was added because JSON serializer doesn't serialize complex type, and pydantic does.
        # TODO Support smarter json serialization
        problem_dict = json.loads(problem.json())
        data = await cls._call_task(
            http_method="post",
            url=routes.COMBINATORIAL_OPTIMIZATION_INITIAL_POINT_FULL_PATH,
            body=problem_dict,
        )

        return opt_result.AnglesResult.parse_obj(data)

    @classmethod
    async def call_qsvm_train(cls, qsvm_data: QSVMData) -> QSVMTrainResult:
        data = await cls._call_task(
            http_method="post",
            url=routes.QSVM_TRAIN,
            body=qsvm_data.dict(),
        )

        result = QSVMResult.parse_obj(data)

        if result.status != QSVMResultStatus.SUCCESS:
            raise ClassiqQSVMError(f"Training failed: {result.details}")

        if not isinstance(result.result, QSVMTrainResult):
            raise ClassiqQSVMError("Invalid train result")

        return result.result

    @classmethod
    async def call_qsvm_test(cls, qsvm_data: QSVMData) -> QSVMTestResult:
        data = await cls._call_task(
            http_method="post",
            url=routes.QSVM_TEST,
            body=qsvm_data.dict(),
        )

        result = QSVMResult.parse_obj(data)

        if result.status != QSVMResultStatus.SUCCESS:
            raise ClassiqQSVMError(f"Testing failed: {result.details}")

        if not isinstance(result.result, QSVMTestResult):
            raise ClassiqQSVMError("Invalid test result")

        return result.result

    @classmethod
    async def call_qsvm_predict(cls, qsvm_data: QSVMData) -> QSVMPredictResult:
        data = await cls._call_task(
            http_method="post",
            url=routes.QSVM_PREDICT,
            body=qsvm_data.dict(),
        )

        result = QSVMResult.parse_obj(data)

        if result.status != QSVMResultStatus.SUCCESS:
            raise ClassiqQSVMError(f"Predicting failed: {result.details}")

        if not isinstance(result.result, QSVMPredictResult):
            raise ClassiqQSVMError("Invalid predict result")

        return result.result

    @classmethod
    async def call_generate_hamiltonian_task(
        cls, problem: ground_state_problem.CHEMISTRY_PROBLEMS_TYPE
    ) -> operator.OperatorResult:
        poller = JobPoller(base_url=routes.CHEMISTRY_GENERATE_HAMILTONIAN_FULL_PATH)
        result = await poller.run_pydantic(problem, timeout_sec=None)
        return _unpack_results(
            result,
            status_type=operator.OperatorStatus,
            result_type=operator.OperatorResult,
        )

    @classmethod
    async def call_solve_exact_task(
        cls, problem: ground_state_problem.CHEMISTRY_PROBLEMS_TYPE
    ) -> ground_state_result.MoleculeExactResult:
        poller = JobPoller(base_url=routes.CHEMISTRY_SOLVE_EXACT_FULL_PATH)
        result = await poller.run_pydantic(problem, timeout_sec=None)
        return _parse_job_response(result, ground_state_result.MoleculeExactResult)

    @classmethod
    async def call_ground_state_solve_task(
        cls, problem: ground_state_solver.GroundStateSolver
    ) -> ground_state_result.MoleculeResult:
        poller = JobPoller(base_url=routes.CHEMISTRY_SOLVE_FULL_PATH)
        result = await poller.run_pydantic(problem, timeout_sec=None)
        return _parse_job_response(result, ground_state_result.MoleculeResult)
