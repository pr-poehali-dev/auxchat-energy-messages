-- Add voice_url column to private_messages for voice messages
ALTER TABLE t_p53416936_auxchat_energy_messa.private_messages 
ADD COLUMN voice_url TEXT NULL;

-- Add voice_duration column to store duration in seconds
ALTER TABLE t_p53416936_auxchat_energy_messa.private_messages 
ADD COLUMN voice_duration INTEGER NULL;
