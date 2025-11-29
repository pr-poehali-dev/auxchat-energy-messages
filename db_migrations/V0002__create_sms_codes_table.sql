-- Таблица для хранения SMS-кодов верификации
CREATE TABLE IF NOT EXISTS sms_codes (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) NOT NULL,
    code VARCHAR(4) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    verified BOOLEAN DEFAULT FALSE
);

-- Индекс для быстрого поиска по телефону
CREATE INDEX idx_sms_codes_phone ON sms_codes(phone);

-- Индекс для очистки старых кодов
CREATE INDEX idx_sms_codes_expires_at ON sms_codes(expires_at);
