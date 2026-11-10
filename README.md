# Grover's Quantum Search Algorithm & Parallelism Analysis

Welcome to this beginner-friendly repository for **Grover's Algorithm implemented in Python using Qiskit**. 

This project was built as part of the **BCA 703A – Cryptography and Quantum Computing with AI** coursework (Dayananda Sagar Academy of Technology & Management). It demonstrates how quantum computers achieve a quadratic speedup over classical computers when searching through unorganized databases, and explains the core quantum mechanical principles behind it.

---

## 📚 Table of Contents
1. [What is Grover's Algorithm? (The Big Picture)](#-what-is-grovers-algorithm-the-big-picture)
2. [Key Quantum Concepts Explained for Beginners](#-key-quantum-concepts-explained-for-beginners)
3. [How Grover's Algorithm Works (Step-by-Step)](#-how-grovers-algorithm-works-step-by-step)
4. [Repository Structure & Files](#-repository-structure--files)
5. [Prerequisites & Installation](#-prerequisites--installation)
6. [How to Run the Code](#-how-to-run-the-code)
7. [Understanding the Output](#-understanding-the-output)

---

## 🔍 What is Grover's Algorithm?

Imagine you have a phone book with **1 million names**, arranged completely at random. You are looking for one specific person's phone number. 

* **Classical Computer:** On average, you would have to check **500,000 names** (and in the worst case, all **1,000,000 names**) one by one. This is called **$O(N)$ linear search time**.
* **Quantum Computer (Grover's Algorithm):** By exploiting the laws of quantum mechanics, a quantum computer can find the exact entry in just about **1,000 steps** ($\sqrt{1,000,000} = 1,000$). This is a **quadratic speedup**, or **$O(\sqrt{N})$ search time**.

---

## ⚛️ Key Quantum Concepts Explained for Beginners

### 1. Bits vs. Qubits
* **Classical Bit:** Can be either `0` or `1` (like a light switch).
* **Qubit (Quantum Bit):** Can be `0`, `1`, or **both at the same time**. This is called **Superposition**.

### 2. Quantum Parallelism
If you have 3 classical bits, you can store *one* number between 0 and 7 at any given moment. 
With **3 qubits** in superposition, your quantum system represents **all 8 states simultaneously** ($000, 001, 010, 011, 100, 101, 110, 111$) in a single wave function. 

---

## ⚙️ How Grover's Algorithm Works (Step-by-Step)

The algorithm consists of four main phases:

1. **Superposition Initialization:** Apply Hadamard ($H$) gates to all qubits. This puts the quantum register into an equal superposition of all possible states.
2. **The Oracle ($U_\omega$):** A special quantum subroutine that "recognizes" the correct answer and flips its phase (multiplies its amplitude by $-1$). This is known as **Phase Kickback**.
3. **The Diffusion Operator ($D$):** Also known as *Amplitude Amplification*. This operator reflects all the state amplitudes about their average value. Because the correct answer's phase was flipped negative, reflecting it about the average **boosts its probability** while shrinking the probabilities of all wrong answers.
4. **Measurement:** After repeating steps 2 and 3 the optimal number of times ($k \approx \frac{\pi}{4}\sqrt{N}$), measuring the qubits collapses the superposition, yielding the correct target state with very high probability.

---

## 🗂️ Repository Structure & Files

| File | Description |
|------|-------------|
| [grovers_simple.py](grovers_simple.py) | **The primary reference script.** Self-contained Qiskit implementation simulating 3 qubits, searching for state `5` (`|101⟩`), printing the circuit diagram, and analyzing probabilities. |
| [grovers_algorithm_analysis.py](grovers_algorithm_analysis.py) | A modular, class-based implementation (`GroversAlgorithm`) demonstrating custom oracle construction and diffusion operators. |
| [grovers_comprehensive.py](grovers_comprehensive.py) | A pure mathematical/numerical script using `NumPy` and `Matplotlib` to model amplitude amplification and complexity curves. |
| [quantum_parallelism_analysis.png](quantum_parallelism_analysis.png) | A pre-rendered 4-panel visual chart comparing classical vs. quantum operations and illustrating amplitude growth. |

---

## 🛠️ Prerequisites & Installation

Make sure Python 3 and the required quantum libraries are installed on your machine.

### 1. Install Dependencies
```bash
pip install qiskit qiskit-aer numpy matplotlib
```

### 2. Verify Installation
You can check your installed Qiskit version with:
```bash
python3 -c "import qiskit; print('Qiskit version:', qiskit.__version__)"
```

---

## 🚀 How to Run the Code

All scripts are standalone and run directly from your terminal.

### Run the Main Reference Script
```bash
python3 grovers_simple.py
```

### Run the Class-Based Analyzer
```bash
python3 grovers_algorithm_analysis.py
```

### Run the Numerical & Chart Generator
```bash
python3 grovers_comprehensive.py
```

---

## 📊 Understanding the Output

When you run [grovers_simple.py](grovers_simple.py), you will see:
1. **The Circuit Diagram:** ASCII art showing the Hadamard gates, Oracle, Diffusion operator, and Measurement meters.
2. **Measurement Results (1024 shots):** A frequency distribution showing how often each binary state was measured by the simulator.
   * Example: `|101⟩: 786 (76.8%) ← TARGET STATE`
3. **Amplification Analysis:** Demonstrating how the target state probability jumped from a uniform baseline of `12.5%` up to `~76.8%` (an amplification factor of over `6x`).

---
*Created for BCA 703A Cryptography & Quantum Computing with AI.*
