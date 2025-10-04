-- Agent Constitution Compliance Database Schema v1.0

-- Track every agent session
CREATE TABLE IF NOT EXISTS agent_sessions (
    session_id TEXT PRIMARY KEY,
    agent_type TEXT NOT NULL,
    launched_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    acknowledged BOOLEAN DEFAULT 0,
    task_summary TEXT,
    status TEXT  -- 'running', 'completed', 'failed'
);

-- Track violations
CREATE TABLE IF NOT EXISTS violations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    violation_type TEXT NOT NULL,  -- 'no_acknowledgment', 'concurrency', 'tool_misuse'
    severity TEXT DEFAULT 'warning',  -- 'critical', 'warning', 'info'
    details TEXT,
    detected_at TIMESTAMP NOT NULL,
    FOREIGN KEY (session_id) REFERENCES agent_sessions(session_id)
);

-- Track constitution versions
CREATE TABLE IF NOT EXISTS constitution_versions (
    version TEXT PRIMARY KEY,
    released_at TIMESTAMP NOT NULL,
    active BOOLEAN DEFAULT 1
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_sessions_launched ON agent_sessions(launched_at);
CREATE INDEX IF NOT EXISTS idx_sessions_agent_type ON agent_sessions(agent_type);
CREATE INDEX IF NOT EXISTS idx_violations_session ON violations(session_id);
CREATE INDEX IF NOT EXISTS idx_violations_detected ON violations(detected_at);

-- Initialize with v1.0
INSERT OR IGNORE INTO constitution_versions (version, released_at, active)
VALUES ('1.0', datetime('now'), 1);
