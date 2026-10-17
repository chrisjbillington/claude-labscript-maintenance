# Tasks for a local session

Work that a cloud session cannot do, for a local Claude Code session to do under
supervision. A cloud session adds a row when it hits such a task; the local session
fills in the status and the date. Delete nothing: a done row is the record.

| Added | Task | Why not from the cloud | Status |
|---|---|---|---|
| 2026-10-17 | Delete the branch `claude-access-check-delete-me` in chrisjbillington/zprocess and in labscript-suite/labscript-utils (created to test push access; each points at the then-current master commit) | the session's proxy refuses branch deletion over git and the REST API | done: neither branch existed on 2026-10-17 (`git ls-remote`) |
| 2026-10-17 | Push two tags on one commit to a repository that runs the sandbox release workflow with workflow-sandbox #46 applied (an rc tag, then the final tag), and check that each run builds its own tag's version | the session's proxy refuses tag pushes (HTTP 403); the step was only tested with tags created inside the job (`tag-test.yml` on branch `claude/release-tag-test`) | open |
| 2026-10-17 | Delete the branch `claude/release-tag-test` in this repository once workflow-sandbox #46 is merged | branch deletion is refused by the proxy | open |
