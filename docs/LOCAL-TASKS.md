# Tasks for a local session

Work that a cloud session cannot do, for a local Claude Code session to do under
supervision. A cloud session adds a row when it hits such a task; the local session
fills in the status and the date. Delete nothing: a done row is the record.

| Added | Task | Why not from the cloud | Status |
|---|---|---|---|
| 2026-10-17 | Delete the branch `claude-access-check-delete-me` in chrisjbillington/zprocess and in labscript-suite/labscript-utils (created to test push access; each points at the then-current master commit) | the session's proxy refuses branch deletion over git and the REST API | open |
