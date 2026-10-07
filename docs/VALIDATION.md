# SupportLens validation

Verified on 7 October 2026, Windows, Python 3.12.14.

## Automated checks

`python -m pytest`: **14 passed**, exit code 0. Tests cover actual Chroma indexing/retrieval with deterministic test vectors, Word table extraction, invalid document rejection, constrained GitHub identifiers, draft-only tickets, grouped citation checks, support tool-message execution, retrieval retry/escalation, invented evidence IDs and UI validation before indexing.

The execution sandbox emitted temporary-directory cleanup permission errors at interpreter shutdown after successful tests. These did not affect test assertions or the command's exit code.

## Live RAG verification

Production indexing used `gemini-embedding-001` through Google's API and stored seven chunks from the sample manuals in Chroma. Both complete requests below used actual `gemini-3.5-flash-lite` model calls.

| Case | Observed workflow | Result |
|---|---|---|
| DeskSync E104 and files not syncing | classify → retrieve → assess → respond → finish → validate | Evidence sufficient; no retrieval retry; three valid source IDs; citation check passed |
| Unrelated printer paper jam | classify → retrieve → assess → rewrite → retrieve → assess → escalate → validate | Evidence insufficient; one retry; local draft ticket; two valid source IDs; citation check passed |

Actual responses and JSON traces are in `examples/resolved-live.*` and `examples/escalation-live.*`. These contain retrieved document passages, evidence assessments, graph actions and outputs. Production never substitutes deterministic test embeddings or model fixtures for Gemini.

The separate GitHub known-issue integration was also called against `pallets/flask` with a timeout query and succeeded. Its result is in `examples/github-api-check.json`. The fictional DeskSync demo is not represented as Flask or another real product.

## Delivery scope

Source code, local hardcoded configuration, independent Git repository, UI, tests, sample manuals, launcher, Dockerfile and hosting instructions are present. The local configuration containing the key is ignored by Git and Docker. Deployment and Docker image build have not been performed. A voice demo has not been recorded.

RAG relevance assessment is an LLM judgement. Citation validation checks IDs and presence, not entailment. A draft ticket is never externally submitted. Session indexes are in-memory and require rebuilding after a server/session restart.

## Browser verification

The actual local interface indexed seven chunks with Gemini, then displayed a grounded live response with five retrieved passages, zero retries and a passing citation check.
