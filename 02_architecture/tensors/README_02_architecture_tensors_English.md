ensor Definitions

This folder contains documents that mathematically express philosophical concepts as tensors.

📋 Overview

This includes definitions and specifications related to the “tensor representation of philosophical concepts,” which is the core technology of Po_core. It serves as the design documentation for converting each philosopher’s theory into a mathematical tensor structure and implementing it in a computable format.

🔢 What is a Tensor?

A tensor in Po_core is a mathematical structure with the following characteristics:

Multidimensional Array: Represents philosophical concepts in a multidimensional space.

Dynamic Interactions: New meanings are generated through operations between tensors.

Pressure Field: Expresses the balance of degrees of freedom and constraints.

📄 Key Tensor Definitions
Freedom Pressure Tensor

A tensor representation based on Sartre’s theory of freedom.

Quantifies existential degrees of freedom

Calculates the weight of choices

Models the pressure field of responsibility

Other Tensors

Shadow Integration Tensor: Jung’s integration of the shadow

Trace Tensor: Derrida’s theory of trace

Betweenness Tensor: Watsuji Tetsurō’s theory of betweenness

Conatus Tensor: Spinoza’s conatus

🎯 Role of Tensors

Computation of Meaning: Express philosophical concepts in a computable form

Dynamic Integration: Mathematically integrate multiple perspectives

Visualization: Make abstract concepts visually representable

📐 Mathematical Notation

Vector notation: v = (v₁, v₂, ..., vₙ)

Tensor product: T ⊗ S

Inner product: T · S

Norm: ||T||

🔗 Related Documents

Philosophical Background: ../philosophy/

API Implementation: ../../03_api/

Visualization in Viewer: ../../04_modules/viewer/

📚 Version Control

Tensor definitions are refined in stages:

Ver1: Basic definitions

Ver2: Refined definitions

Ver3: Implementation-optimized version

It is recommended to use the latest version, but previous versions are also valuable for understanding the theoretical background.

💡 Implementation Notes

Tensor operations should be implemented with NumPy or PyTorch

Consider the balance between computational efficiency and interpretability

Pay attention to numerical stability