import os
from qiskit import QuantumCircuit, transpile, execute
from qiskit_ibm_provider import IBMProvider

# Récupérer la clé API depuis les variables d'environnement
api_key = os.getenv("IBM_QISKIT_API_KEY")

if not api_key:
    raise ValueError("La clé API IBM Quantum n'est pas définie ! Vérifiez votre secret GitHub ou fichier .env.")

# Enregistrer et charger l'API Key IBM
IBMProvider.save_account(api_key, overwrite=True)
provider = IBMProvider()

backend = provider.get_backend("ibmq_qasm_simulator")  # Simulateur IBM

# Créer un circuit quantique simple (Hello World)
circuit = QuantumCircuit(2, 2)
circuit.h(0)  
circuit.cx(0, 1)  
circuit.measure([0, 1], [0, 1])  

print("\nCircuit quantique créé :")
print(circuit)

compiled_circuit = transpile(circuit, backend)
job = execute(compiled_circuit, backend, shots=1024)

result = job.result()
counts = result.get_counts()

print("\nRésultats de l'exécution sur IBM Quantum :")
print(counts)
