-- Seed demo users and providers
-- Passwords are bcrypt hashes of 'demo123'

INSERT INTO users (email, name, role, password_hash) VALUES
    ('admin@clinicdesk.com', 'Admin User', 'admin',
     '$2b$12$HWmTWSZb0LZVo9xIooY0OORnf7QIFrvebcXRejlkWe7ol0TLp8ZNG'),
    ('maria@brightsmile.com', 'Maria Garcia', 'staff',
     '$2b$12$HWmTWSZb0LZVo9xIooY0OORnf7QIFrvebcXRejlkWe7ol0TLp8ZNG'),
    ('james@healthfirst.com', 'James Wilson', 'staff',
     '$2b$12$HWmTWSZb0LZVo9xIooY0OORnf7QIFrvebcXRejlkWe7ol0TLp8ZNG')
ON CONFLICT (email) DO NOTHING;

INSERT INTO providers (name, email, calendar_id, is_available) VALUES
    ('Sarah Chen', 'sarah@clinicdesk.com', 'sarah@clinicdesk.com', true),
    ('Mike Johnson', 'mike@clinicdesk.com', 'mike@clinicdesk.com', true),
    ('Lisa Park', 'lisa@clinicdesk.com', 'lisa@clinicdesk.com', false)
ON CONFLICT (email) DO NOTHING;
