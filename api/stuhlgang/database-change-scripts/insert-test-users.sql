insert into people
(
    email_address,
    display_name,
    salted_hashed_password,
    person_status,
    is_superuser
)
values

(
    'matt@216software.com',
    'Matt Wilson',
    crypt('abc123', gen_salt('bf')),
    'confirmed',
    false
),

(
    'rob@216software.com',
    'Rob Heinen',
    crypt('abc123', gen_salt('bf')),
    'confirmed',
    false
),

(
    'leroy@216software.com',
    'Leroy Jenkins',
    crypt('abc123', gen_salt('bf')),
    'confirmed',
    false
),

(
    'evanmicahstern@gmail.com',
    'Evan Stern',
    crypt('abc123', gen_salt('bf')),
    'confirmed',
    false
)
;
