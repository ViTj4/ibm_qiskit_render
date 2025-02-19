import os
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator, QiskitRuntimeService

# 🔹 Récupérer la clé API depuis GitHub Secrets
api_key = os.getenv("IBM_QISKIT_API_KEY")

if not api_key:
    raise ValueError("La clé API IBM Quantum n'est pas définie ! Vérifiez votre secret GitHub.")

# 🔹 Authentification avec IBM Quantum
service = QiskitRuntimeService()
backend = service.least_busy(simulator=False, operational=True)

# 🔹 Création du circuit quantique
qc = QuantumCircuit(2)
qc.h(0)  # Hadamard sur le qubit 0
qc.cx(0, 1)  # CNOT entre qubit 0 et 1

# 🔹 Dessiner le circuit (pas nécessaire en mode pipeline, mais utile en local)
qc.draw("mpl")

# 🔹 Définition des observables
observables_labels = ["IZ", "IX", "ZI", "XI", "ZZ", "XX"]
observables = [SparsePauliOp(label) for label in observables_labels]

# 🔹 Convertir en circuit ISA optimisé pour le backend IBM
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)

# 🔹 Dessiner le circuit optimisé (optionnel)
isa_circuit.draw("mpl", idle_wires=False)

# 🔹 Construire l'EstimatorV2 et exécuter
estimator = Estimator(mode=backend)
estimator.options.resilience_level = 1
estimator.options.default_shots = 5000

# 🔹 Mapper les observables avec le circuit
mapped_observables = [
    observable.apply_layout(isa_circuit.layout) for observable in observables
]

# 🔹 Exécuter la tâche sur IBM Quantum
job = estimator.run([(isa_circuit, mapped_observables)])

# 🔹 Afficher l'ID du job pour suivre son état sur IBM Quantum
print(f">>> Job ID: {job.job_id()}")
