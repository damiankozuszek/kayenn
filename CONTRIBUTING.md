# Contributing to KAYENN

Thank you for your interest! KAYENN is developed mostly by one person, so every test and every report helps.

## The easiest way to help: test and report

1. Use the program on your own (real or imaginary) projects.
2. Compare the results with the code or with a hand calculation.
3. Open an [issue](../../issues/new/choose) – wrong result, crash, confusing behaviour, missing feature.

A good report contains: the program version (O programie), your system, the steps to reproduce, what you expected
and what you got. Attach the `.kayenn` project file if you can (remove confidential data) and a screenshot.
**Calculation errors are the most important** – please quote the clause or table of the code.

## Code contributions

- The project language is **English** (code, comments, documentation, commit messages). The **program interface
  stays Polish**. Keys of the `.kayenn` file format are Polish and must not be renamed (compatibility).
- Before you start, read [DEVELOPMENT.md](DEVELOPMENT.md) (running from source, packages). For a bigger
  change open an issue first.
- Every change must work on **Windows, macOS and Linux**.
- Check that the program starts and that your change works (describe how you checked it in the pull request).
- A new function of the program needs a console command (`@command(...)` in `kayenn.pyw`).
- Keep pull requests small and focused; describe what changed and why.

## Licence of contributions

By sending a contribution you agree that it is released under the [MIT licence](LICENSE) of the project.
Do not submit text or data copied from copyrighted sources (standards, books, manufacturers' catalogues)
other than short numerical values with the source named.

## Behaviour

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md). Security problems: see [SECURITY.md](SECURITY.md).
