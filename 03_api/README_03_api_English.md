API Specifications

This folder contains the API specification documents for the Po_core system.

📋 Overview

This folder includes detailed specifications for various APIs in Po_core. It provides interface definitions necessary for system integration, external collaboration, and communication between modules.

🔌 Main APIs
API Chains

APIs for constructing and executing inference chains:

Chain definition in JSON format

Execution order control

Retrieval of intermediate results

Po_trace Event Metadata API

APIs for event logging and metadata management:

Event tracing

Structuring of metadata

Support for version control

📡 API Design Principles
RESTful Design

Resource-oriented endpoints

Proper use of HTTP methods

Stateless communication

JSON Format

Standardized data format

Schema validation

Multilingual support

Versioning

Explicit API versioning

Backward compatibility

Gradual migration support

🎯 API Use Cases
Integration with External Systems

Integration with LangChain

Connection to vLLM

Embedding custom LLMs

Data Input/Output

Submission of inference chains

Retrieval of results

Log reference

Monitoring

System status monitoring

Performance measurement

Error tracking

📖 Structure of API Documentation

Each API specification includes the following information:

Overview: Purpose and role of the API

Endpoints: URL paths and HTTP methods

Request Format: Parameter and body specifications

Response Format: Structure of returned data

Error Handling: Error codes and messages

Sample Code: Implementation examples

🔗 Related Documents

System Specifications: ../01_specifications/

Architecture: ../02_architecture/

Implementation Modules: ../04_modules/

🛠️ Developer Information
Authentication

Authentication is not implemented in the current version. It will be added in future releases.

Rate Limiting

No rate limiting for local execution. To be considered for production environments.

Error Handling

Standard HTTP status codes are used:

200: Success

400: Bad request

404: Resource not found

500: Server error

📚 Recommended Reading Order

First-time Users: Start with the API overview to grasp the big picture

Implementers: Check the detailed specifications for each endpoint

Integrators: Review implementation patterns with sample code

💡 Implementation Tips
Position Completion Expressions

API Chains allow for dynamic position specification within chains using position completion expressions.

Multi-Schema Support

The Event Metadata API supports multiple schema versions, enabling gradual migration.

Multilingual Support

The APIs can record metadata in both Japanese and English.

🔄 Version History

The version history for each API is provided within the respective specification documents.