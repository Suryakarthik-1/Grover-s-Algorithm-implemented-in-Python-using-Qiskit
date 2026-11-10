#!/usr/bin/env python3
"""
Simple Grover's Algorithm Implementation with Qiskit
Analyzing Quantum Parallelism Using Superposition

This is a simplified implementation that works with Qiskit 2.6.2
"""

import numpy as np
import matplotlib.pyplot as plt

print("="*70)
print("GROVER'S ALGORITHM WITH QUANTUM PARALLELISM ANALYSIS")
print("="*70)

# First, let's understand the theoretical concepts
n_qubits = 3
search_space_size = 2 ** n_qubits

print(f"\nTHEORETICAL FOUNDATION")
print("-"*40)
print(f"Number of qubits: {n_qubits}")
print(f"Search space size: {search_space_size} states")
print(f"Optimal Grover iterations: ~{int(np.pi/4 * np.sqrt(search_space_size))}")

print(f"\n1. SUPERPOSITION AND QUANTUM PARALLELISM")
print("-"*40)
print(f"• A single qubit: |ψ⟩ = α|0⟩ + β|1⟩")
print(f"• {n_qubits} qubits: |ψ⟩ = Σ_i c_i|i⟩, i from 0 to {search_space_size-1}")
print(f"• Superposition enables parallel evaluation of all {search_space_size} states")
print(f"• Classical equivalent requires {search_space_size} sequential operations")

print(f"\n2. GROVER'S ALGORITHM STEPS")
print("-"*40)
print("Step 1: Initialize superposition (Hadamard gates)")
print("        |ψ⟩ = 1/√N Σ_x |x⟩")
print(f"        Creates equal superposition of {search_space_size} states")

print("\nStep 2: Oracle application (marks solution)")
print("        Oracle: |x⟩ → (-1)^{f(x)}|x⟩")
print("        f(x) = 1 if x is solution, 0 otherwise")
print("        Phase kickback marks the solution")

print("\nStep 3: Diffusion operator (amplitude amplification)")
print("        Inverts all amplitudes about the mean")
print("        Amplifies amplitude of marked state")
print("        Reduces amplitudes of other states")

print(f"\n3. QUANTUM ADVANTAGE ANALYSIS")
print("-"*40)
classical_ops = search_space_size
quantum_ops = int(np.pi/4 * np.sqrt(search_space_size)) * 2  # Oracle + Diffusion
speedup = classical_ops / quantum_ops

print(f"• Classical unstructured search: O(N) = O({search_space_size}) operations")
print(f"• Grover's quantum search: O(√N) = O({int(np.sqrt(search_space_size))}) iterations")
print(f"• Each iteration: 1 oracle + 1 diffusion = 2 operations")
print(f"• Total quantum operations: ~{quantum_ops}")
print(f"• Speedup factor: ~{speedup:.1f}x")

# Now let's implement it with Qiskit
print(f"\n" + "="*70)
print("IMPLEMENTATION WITH QISKIT")
print("="*70)

try:
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    from qiskit.visualization import plot_histogram

    print("✓ Qiskit imports successful")

    # Create a simple demonstration circuit
    print(f"\nCreating quantum circuit with {n_qubits} qubits...")

    # Initialize circuit
    qc = QuantumCircuit(n_qubits, n_qubits)

    # Step 1: Create superposition
    print("1. Applying Hadamard gates to create superposition...")
    qc.h(range(n_qubits))

    # For demonstration, let's mark |101⟩ (state 5) as solution
    target_state = 5  # Binary: 101
    target_binary = format(target_state, f'0{n_qubits}b')

    print(f"2. Creating oracle to mark |{target_binary}⟩ (state {target_state})...")

    # Simple oracle using X and Z gates
    # Mark |101⟩ by flipping phase when qubits are in |1⟩,|0⟩,|1⟩
    qc.barrier()

    # Apply X to qubits that should be |0⟩ in target
    for i, bit in enumerate(target_binary):
        if bit == '0':
            qc.x(i)

    # Apply controlled-Z (phase flip when all qubits are |1⟩)
    qc.h(n_qubits-1)
    qc.mcx(list(range(n_qubits-1)), n_qubits-1)
    qc.h(n_qubits-1)

    # Undo X gates
    for i, bit in enumerate(target_binary):
        if bit == '0':
            qc.x(i)

    qc.barrier()

    print("3. Applying diffusion operator...")

    # Diffusion operator
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))

    qc.h(n_qubits-1)
    qc.mcx(list(range(n_qubits-1)), n_qubits-1)
    qc.h(n_qubits-1)

    qc.x(range(n_qubits))
    qc.h(range(n_qubits))

    # Measure
    print("4. Measuring results...")
    qc.measure(range(n_qubits), range(n_qubits))

    # Draw circuit
    print(f"\nCircuit diagram:")
    print(qc.draw(output='text'))

    # Simulate
    print(f"\nSimulating quantum circuit...")
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1024)
    result = job.result()
    counts = result.get_counts()

    print(f"\nMeasurement results (1024 shots):")
    print("-" * 30)

    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    for state, count in sorted_counts:
        probability = count / 1024 * 100
        arrow = " ← TARGET STATE" if int(state, 2) == target_state else ""
        print(f"|{state}⟩: {count} ({probability:.1f}%){arrow}")

    # Calculate success rate
    target_count = counts.get(target_binary, 0)
    success_rate = target_count / 1024 * 100

    print(f"\nSuccess rate for |{target_binary}⟩: {success_rate:.1f}%")

    # Analyze state probabilities
    print(f"\nSTATE PROBABILITY ANALYSIS:")
    print("-" * 30)

    total_states = len(counts)
    print(f"Number of states observed: {total_states}")
    print(f"Target state probability: {success_rate:.1f}%")

    if total_states > 0:
        avg_prob = 100 / total_states
        print(f"Average probability per state (if uniform): {avg_prob:.1f}%")
        print(f"Amplification factor: {success_rate/avg_prob:.2f}x")

    # Quantum parallelism demonstration
    print(f"\n" + "="*70)
    print("QUANTUM PARALLELISM DEMONSTRATION")
    print("="*70)

    print(f"\nHow quantum parallelism works in Grover's algorithm:")
    print("1. Superposition creates all {search_space_size} states simultaneously")
    print(f"2. Oracle evaluates f(x) for ALL x ∈ {{0,1}}^{n_qubits} in one operation")
    print(f"3. Classical computer needs {search_space_size} sequential evaluations")
    print(f"4. Speedup: O(√N) vs O(N) → {int(np.sqrt(search_space_size))} vs {search_space_size}")

    print(f"\nMathematical representation:")
    print(f"Initial state: |ψ₀⟩ = 1/√{search_space_size} Σ_x |x⟩")
    print(f"Oracle: U_ω|x⟩ = (-1)^{{f(x)}}|x⟩, f(x)=1 if x=ω, 0 otherwise")
    print(f"Diffusion: D = 2|ψ₀⟩⟨ψ₀| - I")
    print(f"Grover iteration: G = D·U_ω")
    print(f"After k iterations: |ψ_k⟩ = sin((2k+1)θ)|ω⟩ + cos((2k+1)θ)Σ_{{x≠ω}}|x⟩/√(N-1)")
    print(f"where θ = arcsin(1/√N) ≈ {np.arcsin(1/np.sqrt(search_space_size)):.3f}")

    # Visualize the speedup
    print(f"\n" + "="*70)
    print("SPEEDUP VISUALIZATION")
    print("="*70)

    # Compare classical vs quantum for different problem sizes
    problem_sizes = [4, 8, 16, 32, 64, 128, 256]
    classical_ops_list = []
    quantum_ops_list = []

    for N in problem_sizes:
        classical_ops_list.append(N)
        quantum_ops_list.append(int(np.pi/4 * np.sqrt(N)) * 2)

    print(f"\nProblem Size | Classical Ops | Quantum Ops | Speedup")
    print("-" * 50)
    for i, N in enumerate(problem_sizes):
        speedup = classical_ops_list[i] / quantum_ops_list[i]
        print(f"{N:11d} | {classical_ops_list[i]:13d} | {quantum_ops_list[i]:11d} | {speedup:7.1f}x")

    print(f"\n" + "="*70)
    print("CONCLUSION")
    print("="*70)

    print(f"\nKey insights from Grover's algorithm:")
    print("1. Quantum parallelism enables simultaneous evaluation of all states")
    print("2. Superposition is the foundation for exponential parallelism")
    print("3. Interference patterns amplify the correct solution")
    print("4. Quadratic speedup over classical unstructured search")
    print(f"5. Practical applications: database search, optimization, cryptography")

    print(f"\nFor N={search_space_size}:")
    print(f"• Classical: {search_space_size} operations")
    print(f"• Quantum: ~{quantum_ops} operations")
    print(f"• Speedup: ~{speedup:.1f}x")

    print(f"\n" + "="*70)
    print("IMPLEMENTATION COMPLETE")
    print("="*70)

except ImportError as e:
    print(f"\nError: {e}")
    print("\nPlease install Qiskit with: pip install qiskit qiskit-aer")
    print("Then run this script again.")
except Exception as e:
    print(f"\nError during execution: {e}")
    print("\nContinuing with theoretical analysis...")

    # Provide theoretical analysis even if Qiskit fails
    print(f"\nTHEORETICAL GROVER'S ALGORITHM:")
    print("-" * 30)

    print(f"\nFor {n_qubits} qubits (N={search_space_size}):")
    print(f"1. Initialize: |0⟩^⊗{n_qubits}")
    print(f"2. Apply H^⊗{n_qubits}: 1/√{search_space_size} Σ_x |x⟩")
    print(f"3. Repeat ~{int(np.pi/4 * np.sqrt(search_space_size))} times:")
    print(f"   a. Apply oracle U_ω (marks solution)")
    print(f"   b. Apply diffusion operator D")
    print(f"4. Measure: high probability of |ω⟩")

    print(f"\nQuantum Parallelism Analysis:")
    print(f"• Single oracle call evaluates f(x) for all {search_space_size} x")
    print(f"• Classical needs {search_space_size} function evaluations")
    print(f"• Parallelism factor: {search_space_size}x")
    print(f"• Overall speedup: O(√N) = O({int(np.sqrt(search_space_size))}) vs O(N) = O({search_space_size})")