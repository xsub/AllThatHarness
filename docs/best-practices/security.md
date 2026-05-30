# Security Review Gates

For every state-changing or externally-fed operation:

- classify input source
- validate type, range, format, length, and business state
- reject unexpected content
- separate authentication from authorization
- parameterize SQL
- prevent path traversal
- prevent unsafe deserialization
- avoid logging secrets or personal data unnecessarily
- define trust boundary for tool/LLM output
- add tests for rejection paths

LLM/tool output is untrusted input.
