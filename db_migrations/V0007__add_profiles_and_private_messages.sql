-- Add profile fields to users table
ALTER TABLE t_p53416936_auxchat_energy_messa.users 
ADD COLUMN IF NOT EXISTS bio TEXT,
ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'online';

-- Create user_photos table for photo gallery
CREATE TABLE IF NOT EXISTS t_p53416936_auxchat_energy_messa.user_photos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES t_p53416936_auxchat_energy_messa.users(id),
    photo_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_photos_user_id ON t_p53416936_auxchat_energy_messa.user_photos(user_id);

-- Create private_messages table for direct messages between users
CREATE TABLE IF NOT EXISTS t_p53416936_auxchat_energy_messa.private_messages (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL REFERENCES t_p53416936_auxchat_energy_messa.users(id),
    receiver_id INTEGER NOT NULL REFERENCES t_p53416936_auxchat_energy_messa.users(id),
    text TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_private_messages_sender ON t_p53416936_auxchat_energy_messa.private_messages(sender_id);
CREATE INDEX IF NOT EXISTS idx_private_messages_receiver ON t_p53416936_auxchat_energy_messa.private_messages(receiver_id);
CREATE INDEX IF NOT EXISTS idx_private_messages_conversation ON t_p53416936_auxchat_energy_messa.private_messages(sender_id, receiver_id);