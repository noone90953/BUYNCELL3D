# Website version history

Local Git version control was set up on 23 October 2026. Nothing has been uploaded or published.

| Version | Git branch | Permanent checkpoint | Contents |
| --- | --- | --- | --- |
| Previous | `previous` | `v1-before-scene-fixes` | The scene before the eight fixes, restored from `qa/review-2026-10-22/before.html`, with the shared local assets and libraries. |
| Before the globe | `before-world` | `v2-scene-fixes`, `v2-before-world-finale` | The five-moment scene with grounding, orange container, truck, warehouse, hero camera, wake, hidden cutouts and surface/shadow fixes. |
| Current | `main` | `v3-world-finale` | Six moments, with the original journey scaled to 0–0.8 and a Natural Earth dotted globe, nine Dubai routes and the World quote CTA. |

## Switch with a double-click

- **Use previous version.cmd** switches to the pre-fix scene.
- **Use current version.cmd** returns to the latest saved `main` version.

Then open `index.html` or refresh your existing preview. The shortcuts stop if tracked files contain uncommitted edits. Git also protects untracked files that a switch would overwrite. Nothing is reset, cleaned or discarded.

From a terminal in this folder, the equivalent commands are `git switch previous` and `git switch main`.

To compare the latest globe update with the version immediately before it, run `git switch before-world`. Return with `git switch main`. The original `previous` branch and both double-click shortcuts retain their established meanings.

## Future changes

Before new website changes, save the current work as a Git commit. Make new changes on `main` and save another commit after checking them. Keep named tags for versions you want to return to. You can ask Codex to create a checkpoint, compare versions, or restore a saved version.

The `previous` branch stays at the original pre-fix scene. The `main` branch can advance with future changes; the named version tags permanently identify each saved checkpoint. Git commits record the setup date, not an invented historical author/date for the restored snapshot.

The original pre-fix source is recovered exactly; a complete historical copy of every ancillary file was not available. Both versions share the current local assets, helper tools and documentation. The `qa/` screenshots stay on disk and are ignored by Git so switching branches does not remove the review archive.

This repository is local version history, not an off-device backup. Keep the hidden `.git` folder when copying or backing up the project.
