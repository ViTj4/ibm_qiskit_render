import os
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator, QiskitRuntimeService

api_key = os.getenv("IBM_QISKIT_API_KEY")
if not api_key:
    raise ValueError("Clé API IBM Quantum non définie. Vérifiez votre secret GitHub.")

service = QiskitRuntimeService(channel="ibm_quantum", token=api_key)
backend = service.least_busy(simulator=False, operational=True)

circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0, 1)

observables_labels = ["IZ", "IX", "ZI", "XI", "ZZ", "XX"]
observables = [SparsePauliOp(label) for label in observables_labels]

pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=1)
optimized_circuit = pass_manager.run(circuit)

#disable graphic print to fix pipeline : useless in pipeline
#optimized_circuit.draw("mpl", idle_wires=False)

estimator = Estimator(mode=backend)
estimator.options.resilience_level = 1
estimator.options.default_shots = 5000

mapped_observables = [obs.apply_layout(optimized_circuit.layout) for obs in observables]

job = estimator.run([(optimized_circuit, mapped_observables)])

print(f">>> Job ID: {job.job_id()}")
