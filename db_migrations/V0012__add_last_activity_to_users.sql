-- Добавить поле last_activity для отслеживания активности пользователя
ALTER TABLE t_p53416936_auxchat_energy_messa.users 
ADD COLUMN IF NOT EXISTS last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Обновить last_activity для существующих пользователей
UPDATE t_p53416936_auxchat_energy_messa.users 
SET last_activity = updated_at 
WHERE last_activity IS NULL;