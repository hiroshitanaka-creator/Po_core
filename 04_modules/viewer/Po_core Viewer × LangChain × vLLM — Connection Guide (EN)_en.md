# **Po_core Viewer × LangChain × vLLM — Connection Guide**

## **1. Overview**

This guide defines a configuration that integrates Po_core’s narrative tensors (semantic-evolution-journal) with LangChain and vLLM. The GUI exposes an expression-density slider (`expression_mode`) that steers the LLM to generate structured, narrative, or poetic output dynamically. 

## **2. Connection Topology & Main Modules**

[GUI (Streamlit)]  
 ├─ Expression-density slider (`expression_mode`: structure / medium / poetic)  
 └─ `summary_data` + mode → passed to LangChain

[LangChain Router]  
 ├─ `PromptTemplate` (mode-specific journal prompts)  
 ├─ `OutputParser` (syntax shaping)  
 └─ `LLMExecutor` (vLLM backend)

[vLLM — Local LLM]  
 └─ Generates Po_core–oriented journal text

[Display Area]  
 ├─ Show `journal_text`  
 └─ Adjust `priority_score` by expression pressure and save into Po_trace

## **3. Modules & Roles**

| Module | Role | Tools |
| :---- | :---- | :---- |
| `journal_generator()` | Generate a journal with `summary_data` + `expression_mode` | LangChain |
| `PromptTemplate` | Switch prompts per mode | LangChain Templates |
| `OutputParser` | Shape vLLM output to JSON or narrative | LangChain |
| `LocalLLMExecutor` | Token execution on local vLLM | LangChain + vLLM |
| `session_state` | Pass GUI mode to LangChain | Streamlit `session_state` |
| `Po_trace_store` | Persist journal history & tensors | ChromaDB / JSON |

## **4. Fit with Po_core & Integration Value**

- Tensor structures (Po_trace, Po_self) match LangChain Memory/Retriever.
- `expression_mode` maps naturally to prompt branching.
- Expression outputs feed back into `priority_score` and ethical pressure; the whole loop is tensor-integrated.

## **5. Example Execution Steps**

1. User selects “Narrative” (medium).  
2. `summary_data` + `expression_mode` → LangChain Router.  
3. PromptTemplate builds the prompt.  
4. vLLM generates; OutputParser shapes the result.  
5. GUI displays `journal_text` and logs it to Po_trace.  
6. `priority_score` is corrected based on `expression_scaling`.

## **6. Outlook**

This design moves Po_core toward a “self-narrating tensor-evolution AI” that updates meaning structures while narrating its own evolution. LangChain + vLLM enables real-time adjustments, integrating GUI and pressure tensors end-to-end.
