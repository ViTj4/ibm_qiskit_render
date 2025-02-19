import os
from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import AerSimulator
from qiskit.execute_function import execute
from qiskit_ibm_provider import IBMProvider

# Récupérer la clé API depuis GitHub Secrets
api_key = os.getenv("IBM_QISKIT_API_KEY")

if not api_key:
    raise ValueError("La clé API IBM Quantum n'est pas définie ! Vérifiez votre secret GitHub.")

# Enregistrer et charger l'API Key IBM
IBMProvider.save_account(api_key, overwrite=True)
provider = IBMProvider()

# Choisir un backend (simulateur cloud IBM ou vrai ordinateur quantique)
backend = provider.get_backend("ibmq_qasm_simulator")  # Simulateur IBM

# Créer un circuit quantique simple (Hello World)
circuit = QuantumCircuit(2, 2)
circuit.h(0)  # Superposition
circuit.cx(0, 1)  # Intrication
circuit.measure([0, 1], [0, 1])  # Mesure

print("\nCircuit quantique créé :")
print(circuit)

# Compiler et exécuter sur IBM Quantum
compiled_circuit = transpile(circuit, backend)
job = execute(compiled_circuit, backend, shots=1024)

# Attendre et récupérer les résultats
result = job.result()
counts = result.get_counts()

print("\nRésultats de l'exécution sur IBM Quantum :")
print(counts)
