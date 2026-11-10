# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a student CCA activity for BCA 703A – Cryptography and Quantum Computing with AI (Dayananda Sagar Academy of Technology & Management). The assignment: implement Grover's algorithm with Qiskit, analyze quantum parallelism using superposition, and be ready with working code plus output gate diagrams at presentation time. The activity PDF was pasted into the first user turn ("Activity_CCA2.pdf") and covers batches 1–6 (Grover's algorithm) due 11 Nov 2026.

## Environment & commands

**Installed:** Python 3, qiskit 2.6.2, qiskit_aer 0.18.2, numpy 2.5.4, matplotlib 3.11.2.

**Run a script:**
```
python3 grovers_simple.py
python3 grovers_algorithm_analysis.py
python3 grovers_comprehensive.py
```

There is no test suite, no build system, no linter config, and no package manager. If you add code, run the affected script directly to verify it executes. Each script is a self-contained entry point that runs top-to-bottom on execution (no `if __name__ == "__main__"` guard).

**Dependency check:**
```
python3 -c "import qiskit; print(qiskit.__version__)"
python3 -c "import qiskit_aer; print(qiskit_aer.__version__)"
```

## Architecture (big picture)

The repo contains three standalone Python scripts, not a package. No modules import each other.

| File | Role |
|------|------|
| `grovers_simple.py` | Reference implementation the assignment expects. Self-contained Qiskit program: circuit build → simulate on `AerSimulator` → print counts → analyze target-state probability vs average → speedup table. Best starting point for a presentation demo. |
| `grovers_algorithm_analysis.py` | Class-based Qiskit implementation (`GroversAlgorithm`): `create_oracle`, `create_diffusion_operator`, `build_circuit`, `execute_circuit`, `analyze_quantum_parallelism`. More modular; useful if you want to reuse oracle/diffusion pieces. |
| `grovers_comprehensive.py` | Pure numerical/mathematical analysis with `numpy` + `matplotlib` (no Qiskit). Computes optimal iterations, amplitude evolution, classical vs quantum comparison, saves `quantum_parallelism_analysis.png` (already present in repo). |

`quantum_parallelism_analysis.png` is a pre-generated 4-panel visualization: classical vs quantum operations, speedup factor, amplitude amplification (N=16), and parallelism bar chart (8 states).

**Key implementation pattern used across scripts:** an oracle marks the target state by applying `X` gates to qubits where the target bit is `0`, then `H`–`MCX`–`H` on the last qubit (phase flip via multi-controlled Z), then undoing the `X` gates. The diffusion operator is H–X–(H–MCX–H)–X–H. This matches the assignment's "output gate diagrams" requirement — call `qc.draw(output='text')` or save a circuit diagram for the presentation.

## Requirements mapping (from the pasted Activity_CCA2.pdf)

- Implement Grover's algorithm with Qiskit → `grovers_simple.py` (and `grovers_algorithm_analysis.py`)
- Analyze quantum parallelism using superposition → superposition creation via Hadamards + parallelism analysis sections in all three scripts
- Working code + output gate diagrams at presentation → run `grovers_simple.py`; it prints `qc.draw(output='text')` and measurement counts

## Conventions to keep

- Scripts print section headers and progress messages inline; keep that style if extending.
- Qiskit version is 2.6.2 — use `AerSimulator().run(qc, shots=...)` (not the older `execute`/`Aer.get_backend` API used in `grovers_algorithm_analysis.py`).
- No git repository exists in this directory; commits are not part of the workflow here.
