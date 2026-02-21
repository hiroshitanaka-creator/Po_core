Output & Rendering

This folder contains design documents related to formatting and outputting inference results.

📋 Overview

This module provides functions to convert Po_core’s inference results into human-readable formats and output them in various formats.

🎯 Main Features
Po_core_output

Basic output functions for inference results

Output in text format

Generation of structured data

Attaching metadata

Po_core_output_renderer

Advanced rendering functions

HTML rendering

Markdown conversion

Support for custom templates

Po_core_renderer + auto_log_writer

Integrated renderer including automatic log recording

Real-time rendering

Automatic log generation

Asynchronous processing support

🔧 Rendering Pipeline
Reasoning Results
    ↓
Format Selection
    ↓
Template Application
    ↓
Content Rendering
    ↓
Output Generation
    ↓
Auto Logging

📝 Supported Output Formats
Text Formats

Plain text

Markdown

JSON

YAML

Rich Formats

HTML (styled)

PDF (planned for future)

Interactive viewer

Data Formats

Structured JSON

RDF/Turtle (Semantic Web support)

CSV (for analysis)

🎨 Template System
Customizable Elements

Layout structure

Styling

Display order of content

Display/hide metadata

Template Language

Uses a Jinja2-based template engine

🔗 Related Components

Inference Logs: ../reason_log/

Visualization: ../viewer/

Event Logging: ../po_trace/

💡 Implementation Notes
Performance

For large outputs, streaming processing is recommended

Utilize template caching

Consider asynchronous rendering

Error Handling

Fallback on rendering failure

Detection of invalid templates

Graceful degradation

Internationalization

Multilingual support

Output according to locale

Proper character encoding handling

📚 Documentation Structure

Each design document includes:

Rendering algorithms

Template specifications

Output examples

Customization methods

🔄 Processing Flow

Input Reception: Receiving inference results

Format Selection: Deciding output format

Data Conversion: Transforming from internal representation to output format

Template Application: Formatting and styling

Output Generation: Creating the final output

Log Recording: Writing automatic logs

🌟 Notable Features
auto_log_writer

Automatically records the entire process as logs during rendering, ensuring traceability and reproducibility.

Flexible Templates

Users can define their own templates, supporting output formats specific to their organization or project.

Streaming Support

Supports streaming rendering, allowing memory-efficient processing even for large outputs.
