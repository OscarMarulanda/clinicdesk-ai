-- Add user_email to escalations table
ALTER TABLE escalations ADD COLUMN IF NOT EXISTS user_email VARCHAR(255);
