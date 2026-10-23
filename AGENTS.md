# Version control for this website

The owner requested recoverable versions so they can return to an earlier design.

- Before changing website files, inspect Git status and save existing website work as a checkpoint commit. Exclude credentials, machine-specific configuration and unrelated files.
- Make new website changes on `main`. If another branch is active, preserve any edits before returning to `main`.
- After implementing and checking a coherent update, commit it with a clear description. Tell the owner which checkpoint can restore the earlier version.
- Preserve `previous`, `v1-before-scene-fixes` and `v2-scene-fixes`; these are named recovery points. New checkpoints should use new names.
- Do not discard uncommitted edits, reset hard, clean files, rewrite checkpoints, or force-push as part of switching versions.
- Keep the two version-switch shortcuts usable. `Use current version.cmd` follows `main`; `Use previous version.cmd` returns to the original pre-fix scene.
- Keep version history local unless the owner asks to add a remote or publish it.
