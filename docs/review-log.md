# Review Log

This file records pre-application review work for the initial public repository.

## 2026-06-01

### Internal Sub-Agent Review

Three independent internal sub-agent reviews were run before publication:

- Implementation and tests
- Documentation and application wording
- Security, privacy, and packaging

Issues addressed from those reviews:

- Fixed `PATH` check environment injection so `environ={}` does not fall back to the real process environment.
- Changed empty version output from `OK` to `WARNING`.
- Added tests for timeout, non-zero, empty-version, empty-`PATH`, generic home path redaction, bearer tokens, URL credentials, GitLab/npm/AWS-style tokens, and `KEY: value` secrets.
- Added `MANIFEST.in` so sdist includes docs, examples, tests, and GitHub metadata.
- Added `twine check` and built-wheel smoke checks to CI.
- Clarified `--strict` behavior for optional tools in `README.md`.
- Documented the risk that version checks execute commands found on `PATH`.
- Improved `SECURITY.md` and the bug report template to reduce accidental sharing of sensitive diagnostic output.

### Chrome GPT Pro Extend Review Attempt

A Chrome ChatGPT Pro review request was sent with a concise repository summary and explicit honesty constraints. The long full-repository prompt and the shorter follow-up both entered a long "thinking/finalizing" state during this run, and the final assistant review text could not be retrieved through the browser automation before timeout.

No application or README claim is based on an unretrieved external review. The concrete changes above are based on locally verified code review findings and validation results.
