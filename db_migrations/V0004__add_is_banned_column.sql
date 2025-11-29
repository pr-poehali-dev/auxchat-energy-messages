-- Add is_banned column to users table
ALTER TABLE t_p53416936_auxchat_energy_messa.users 
ADD COLUMN IF NOT EXISTS is_banned BOOLEAN DEFAULT FALSE;