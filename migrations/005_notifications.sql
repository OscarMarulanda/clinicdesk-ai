-- Notifications table for admin dashboard
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL DEFAULT 'escalation',
    title VARCHAR(500) NOT NULL,
    message TEXT NOT NULL,
    reference_id INTEGER,
    reference_type VARCHAR(50),
    is_read BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications (is_read);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications (created_at);
