# Security Policy

## Supported Versions

This is a new project. Security fixes are handled on the latest released version.

## Reporting A Vulnerability

Please open a GitHub issue with a minimal reproduction unless the report includes sensitive information. Do not paste full diagnostic output if it includes private paths, usernames, tokens, internal hostnames, or other sensitive values.

Use GitHub's private vulnerability reporting feature if it is enabled. If it is not available, open a minimal issue that does not include sensitive details and ask for a private contact path.

## Security Notes

- The CLI is read-only by default.
- It does not collect telemetry.
- It does not send diagnostic results to external services.
- It does not modify shell profiles, registry entries, package manager config, or environment variables.
- It runs version-check commands found on `PATH`. Do not run it in an untrusted shell or with a `PATH` that may point to malicious executables.
- It applies best-effort redaction for user home directories, common token-like values, and URL-embedded credentials before rendering reports.
- Users should still review output before sharing it publicly because local paths, usernames, or tool-specific error messages may remain.
- Future auto-fix behavior, if added, must be opt-in and documented separately.
