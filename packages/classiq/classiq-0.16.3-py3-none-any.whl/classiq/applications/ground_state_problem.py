from classiq.interface.chemistry import ground_state_problem, operator
from classiq.interface.chemistry.operator import PauliOperator

from classiq._internals import async_utils
from classiq._internals.api_wrapper import ApiWrapper
from classiq.exceptions import ClassiqGenerationError


async def generate_hamiltonian_async(
    gs_problem: ground_state_problem.CHEMISTRY_PROBLEMS_TYPE,
) -> PauliOperator:
    result = await ApiWrapper.call_generate_hamiltonian_task(problem=gs_problem)

    if result.status != operator.OperatorStatus.SUCCESS:
        raise ClassiqGenerationError(f"Generate Hamiltonian failed: {result.details}")

    return result.details


ground_state_problem.GroundStateProblem.generate_hamiltonian = async_utils.syncify_function(generate_hamiltonian_async)  # type: ignore[attr-defined]
ground_state_problem.GroundStateProblem.generate_hamiltonian_async = generate_hamiltonian_async  # type: ignore[attr-defined]
