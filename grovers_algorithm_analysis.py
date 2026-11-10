#!/usr/bin/env python3
"""
Grover's Algorithm Implementation with Quantum Parallelism Analysis
===================================================================

This script implements Grover's quantum search algorithm using Qiskit and
analyzes the concept of quantum parallelism through superposition.

Author: Quantum Computing Implementation
Date: 2026-11-08
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, execute
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.quantum_info import Statevector
import warnings
warnings.filterwarnings('ignore')


class GroversAlgorithm:
    """
    Implementation of Grover's quantum search algorithm.

    Grover's algorithm provides a quadratic speedup for unstructured search
    problems, reducing complexity from O(N) to O(√N).
    """

    def __init__(self, n_qubits=3):
        """
        Initialize Grover's algorithm with specified number of qubits.

        Parameters:
        -----------
        n_qubits : int
            Number of qubits to use (search space size = 2^n_qubits)
        """
        self.n_qubits = n_qubits
        self.search_space_size = 2 ** n_qubits
        self.target_state = None
        self.circuit = None

        # Optimal number of Grover iterations
        self.optimal_iterations = int(np.pi / 4 * np.sqrt(self.search_space_size))

    def create_oracle(self, target_state):
        """
        Create an oracle that marks the target state.

        The oracle is a quantum operation that recognizes the solution
        and flips its phase (phase kickback).

        Parameters:
        -----------
        target_state : int or str
            Target state to mark (e.g., 5 or '101')
        """
        self.target_state = target_state

        # Convert target state to binary string
        if isinstance(target_state, int):
            target_binary = format(target_state, f'0{self.n_qubits}b')
        else:
            target_binary = target_state

        oracle_circuit = QuantumCircuit(self.n_qubits)

        # Mark the target state with a phase flip
        # For simplicity, we'll mark |101⟩ (state 5) for 3-qubit example
        oracle_circuit.name = "Oracle"

        # Apply phase flip to target state using multi-controlled Z gate
        # For a specific target, we use X gates to flip qubits where target has 0
        for i, bit in enumerate(target_binary):
            if bit == '0':
                oracle_circuit.x(i)

        # Apply multi-controlled Z gate (flips phase when all qubits are |1⟩)
        oracle_circuit.h(self.n_qubits - 1)
        oracle_circuit.mcx(list(range(self.n_qubits - 1)), self.n_qubits - 1)
        oracle_circuit.h(self.n_qubits - 1)

        # Undo the X gates
        for i, bit in enumerate(target_binary):
            if bit == '0':
                oracle_circuit.x(i)

        return oracle_circuit

    def create_diffusion_operator(self):
        """
        Create the diffusion operator (Grover diffusion operator).

        The diffusion operator amplifies the amplitude of the marked state
        and reduces amplitudes of other states.
        """
        diffusion_circuit = QuantumCircuit(self.n_qubits)
        diffusion_circuit.name = "Diffusion"

        # Apply Hadamard gates to all qubits
        diffusion_circuit.h(range(self.n_qubits))

        # Apply X gates to all qubits
        diffusion_circuit.x(range(self.n_qubits))

        # Apply multi-controlled Z gate
        diffusion_circuit.h(self.n_qubits - 1)
        diffusion_circuit.mcx(list(range(self.n_qubits - 1)), self.n_qubits - 1)
        diffusion_circuit.h(self.n_qubits - 1)

        # Apply X gates again
        diffusion_circuit.x(range(self.n_qubits))

        # Apply Hadamard gates again
        diffusion_circuit.h(range(self.n_qubits))

        return diffusion_circuit

    def build_circuit(self, target_state=5, iterations=None):
        """
        Build the complete Grover's algorithm circuit.

        Parameters:
        -----------
        target_state : int
            Target state to search for
        iterations : int
            Number of Grover iterations (uses optimal if None)
        """
        if iterations is None:
            iterations = self.optimal_iterations

        self.circuit = QuantumCircuit(self.n_qubits, self.n_qubits)

        # Step 1: Initialize superposition
        print(f"Step 1: Creating superposition of {self.search_space_size} states")
        self.circuit.h(range(self.n_qubits))

        # Step 2: Apply Grover iterations
        oracle = self.create_oracle(target_state)
        diffusion = self.create_diffusion_operator()

        print(f"Step 2: Applying {iterations} Grover iterations")
        for i in range(iterations):
            # Append oracle
            self.circuit.append(oracle, range(self.n_qubits))
            # Append diffusion operator
            self.circuit.append(diffusion, range(self.n_qubits))

            # Optional: Add barriers for visualization
            if i < iterations - 1:
                self.circuit.barrier()

        # Step 3: Measure
        print("Step 3: Measuring results")
        self.circuit.measure(range(self.n_qubits), range(self.n_qubits))

        return self.circuit

    def execute_circuit(self, shots=1024):
        """
        Execute the Grover's algorithm circuit.

        Parameters:
        -----------
        shots : int
            Number of measurement shots
        """
        if self.circuit is None:
            raise ValueError("Circuit not built. Call build_circuit() first.")

        simulator = Aer.get_backend('qasm_simulator')
        job = execute(self.circuit, simulator, shots=shots)
        result = job.result()
        counts = result.get_counts(self.circuit)

        return counts

    def analyze_quantum_parallelism(self):
        """
        Analyze quantum parallelism in Grover's algorithm.

        This function demonstrates how superposition enables parallel
        evaluation of multiple states simultaneously.
        """
        print("\n" + "="*60)
        print("QUANTUM PARALLELISM ANALYSIS")
        print("="*60)

        # Create a simple circuit to demonstrate superposition
        demo_circuit = QuantumCircuit(self.n_qubits)
        demo_circuit.h(0)  # Create superposition on first qubit

        if self.n_qubits > 1:
            demo_circuit.h(1)  # Create entanglement for larger systems

        print(f"\n1. Superposition creates {2**self.n_qubits} parallel states:")
        print(f"   |ψ⟩ = 1/√{2**self.n_qubits} * (|00...0⟩ + |00...1⟩ + ... + |11...1⟩)")

        # Calculate statevector
        simulator = Aer.get_backend('statevector_simulator')
        job = execute(demo_circuit, simulator)
        result = job.result()
        statevector = result.get_statevector()

        print(f"\n2. Statevector coefficients (amplitudes):")
        for i, amplitude in enumerate(statevector):
            basis_state = format(i, f'0{self.n_qubits}b')
            print(f"   |{basis_state}⟩: {amplitude.real:.3f} + {amplitude.imag:.3f}i")

        print(f"\n3. Quantum Parallelism in Grover's Algorithm:")
        print(f"   • Oracle evaluates all {self.search_space_size} states simultaneously")
        print(f"   • Single quantum operation processes entire search space")
        print(f"   • Classical equivalent requires {self.search_space_size} operations")
        print(f"   • Speedup factor: O(√N) vs O(N) for classical search")

        # Calculate speedup
        classical_ops = self.search_space_size
        quantum_ops = self.optimal_iterations * 2  # Oracle + Diffusion per iteration
        speedup = classical_ops / quantum_ops

        print(f"\n4. Theoretical Speedup for N={self.search_space_size}:")
        print(f"   • Classical operations needed: {classical_ops}")
        print(f"   • Quantum operations needed: ~{quantum_ops}")
        print(f"   • Speedup factor: ~{speedup:.2f}x")

        return statevector


def visualize_superposition_effects():
    """
    Visualize the effects of superposition and amplitude amplification.
    """
    print("\n" + "="*60)
    print("VISUALIZING SUPERPOSITION EFFECTS")
    print("="*60)

    # Create simple superposition states
    circuits = []

    # |+⟩ state
    circuit_plus = QuantumCircuit(1)
    circuit_plus.h(0)
    circuits.append(("|+⟩ State", circuit_plus))

    # |-⟩ state
    circuit_minus = QuantumCircuit(1)
    circuit_minus.x(0)
    circuit_minus.h(0)
    circuits.append(("|-⟩ State", circuit_minus))

    # Bell state (maximally entangled)
    circuit_bell = QuantumCircuit(2)
    circuit_bell.h(0)
    circuit_bell.cx(0, 1)
    circuits.append(("Bell State", circuit_bell))

    print("\nQuantum State Visualizations:")
    print("-" * 40)

    simulator = Aer.get_backend('statevector_simulator')

    for name, circuit in circuits:
        print(f"\n{name}:")
        job = execute(circuit, simulator)
        result = job.result()
        statevector = result.get_statevector()

        # Print statevector
        print(f"  Statevector: {statevector}")

        # Calculate probabilities
        print(f"  Probabilities: {np.abs(statevector)**2}")


def main():
    """
    Main function to run Grover's algorithm and analyze quantum parallelism.
    """
    print("="*70)
    print("GROVER'S ALGORITHM IMPLEMENTATION WITH QUANTUM PARALLELISM ANALYSIS")
    print("="*70)

    try:
        # Test if Qiskit is available
        import qiskit
        print(f"\n✓ Qiskit version: {qiskit.__version__}")
    except ImportError:
        print("\n⚠ Qiskit not installed. Please install with: pip install qiskit")
        print("Continuing with theoretical analysis...\n")

    # Create Grover's algorithm instance
    n_qubits = 3
    grover = GroversAlgorithm(n_qubits=n_qubits)

    print(f"\nSearch Space Configuration:")
    print(f"- Number of qubits: {n_qubits}")
    print(f"- Search space size: {grover.search_space_size} states")
    print(f"- Optimal Grover iterations: {grover.optimal_iterations}")

    # Analyze quantum parallelism
    print("\n" + "-"*60)
    statevector = grover.analyze_quantum_parallelism()

    # Build and execute Grover's circuit
    print("\n" + "-"*60)
    print("EXECUTING GROVER'S ALGORITHM")
    print("-"*60)

    target_state = 5  # |101⟩
    print(f"\nSearching for target state |{format(target_state, f'0{n_qubits}b')}⟩ (state {target_state})")

    circuit = grover.build_circuit(target_state=target_state, iterations=1)

    print(f"\nCircuit depth: {circuit.depth()}")
    print(f"Number of gates: {circuit.size()}")

    # Execute circuit
    print("\nExecuting quantum circuit...")
    counts = grover.execute_circuit(shots=1024)

    print(f"\nMeasurement results:")
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    for state, count in sorted_counts:
        probability = count / 1024 * 100
        arrow = " ← TARGET" if int(state, 2) == target_state else ""
        print(f"  |{state}⟩: {count} measurements ({probability:.1f}%){arrow}")

    # Calculate success probability
    target_count = counts.get(format(target_state, f'0{n_qubits}b'), 0)
    success_probability = target_count / 1024 * 100
    print(f"\nSuccess probability: {success_probability:.1f}%")

    # Visualize superposition effects
    visualize_superposition_effects()

    # Theoretical analysis
    print("\n" + "="*60)
    print("THEORETICAL ANALYSIS OF QUANTUM PARALLELISM")
    print("="*60)

    print("\n1. Superposition Principle:")
    print("   • Quantum bits can exist in superposition of |0⟩ and |1⟩")
    print("   • n qubits can represent 2^n states simultaneously")
    print("   • Enables parallel computation on all possible inputs")

    print("\n2. Quantum Parallelism in Grover's Algorithm:")
    print("   • Oracle applies function f(x) to all states in superposition")
    print("   • Single quantum operation evaluates f(x) for all x ∈ {0,1}^n")
    print("   • Classical computer needs 2^n sequential evaluations")

    print("\n3. Amplitude Amplification:")
    print("   • Grover iteration amplifies amplitude of target state")
    print("   • Reduces amplitudes of non-target states")
    print("   • After O(√N) iterations, target state has high probability")

    print("\n4. Quantum Advantage:")
    print(f"   • Classical search: O(N) = O({grover.search_space_size}) operations")
    print(f"   • Quantum search: O(√N) = O({grover.optimal_iterations}) iterations")
    print(f"   • Quadratic speedup: √{grover.search_space_size} = {np.sqrt(grover.search_space_size):.1f}x faster")

    print("\n" + "="*60)
    print("CONCLUSION")
    print("="*60)

    print("\nGrover's algorithm demonstrates the power of quantum parallelism:")
    print("✓ Superposition enables parallel evaluation of all states")
    print("✓ Quantum interference amplifies the correct solution")
    print("✓ Quadratic speedup over classical unstructured search")
    print("✓ Foundation for more advanced quantum algorithms")

    print("\n" + "="*70)
    print("Implementation completed successfully!")
    print("="*70)


if __name__ == "__main__":
    main()