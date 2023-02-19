CREATE TABLE UserAccess (
  UserAccess TEXT PRIMARY KEY,
  PassAccess TEXT NOT NULL,
  TokenAccess TEXT NOT NULL,
  ExpirationAcess DATETIME NOT NULL
);

INSERT INTO UserAccess (UserAccess, PassAccess, TokenAccess, ExpirationAcess)
VALUES ('testuser', 'testpass', 'xxx-xxx-xxx-xxx', datetime('now', '+1 hour'));
