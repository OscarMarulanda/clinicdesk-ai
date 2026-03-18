-- Real users
INSERT INTO users (email, name, role, password_hash) VALUES
    ('odmarulandab@unal.edu.co', 'Oscar Marulanda', 'admin',
     '$2b$12$30TjmSniInCdNnQwVbgpRewZnEuSEmqKaoHe1sgUyqjoiUm37andW'),
    ('oscar.marulanda.2823513@gmail.com', 'Oscar Marulanda', 'staff',
     '$2b$12$30TjmSniInCdNnQwVbgpRewZnEuSEmqKaoHe1sgUyqjoiUm37andW')
ON CONFLICT (email) DO NOTHING;
