DROP TABLE IF EXISTS weather;

CREATE TABLE IF NOT EXISTS weather (
  id integer PRIMARY KEY AUTO_INCREMENT,
  city VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  temperature DECIMAL(5, 2) NOT NULL,
  humidity DECIMAL(5, 2) NOT NULL,
  description VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime on update CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO weather (
  id,
  city,
  temperature,
  humidity,
  description,
  created_at,
  updated_at
)
VALUES (
  1,
  'tokyo',
  25.0,
  60.0,
  'light rain',
  '2024-08-18 12:00:05',
  '2024-08-18 12:00:05'
);

INSERT INTO weather (
  id,
  city,
  temperature,
  humidity,
  description,
  created_at,
  updated_at
)
VALUES (
  2,
  'new york',
  30.0,
  70.0,
  'clear sky',
  '2024-08-18 12:00:05',
  '2024-08-18 12:00:05' 
); 