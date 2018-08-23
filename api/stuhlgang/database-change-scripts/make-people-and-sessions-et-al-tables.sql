create table person_statuses
(
    title citext primary key,
    description text,
    inserted timestamptz not null default now(),
    updated timestamptz
);

create trigger person_statuses_set_updated_column
before update
on person_statuses
for each row
execute procedure set_updated_column();

insert into person_statuses
(title)
values
('started registration'),
('confirmed'),
('deactivated'),
('canceled registration');

create domain email_address_type as citext check(value ~ E'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+$');

CREATE OR REPLACE FUNCTION random_between(low INT ,high INT)
    RETURNS INT AS
    $$
    BEGIN
        RETURN floor(random()* (high-low + 1) + low);
    END;
$$ language 'plpgsql' STRICT;

create table people
(
    person_uuid uuid primary key default uuid_generate_v4(),
    email_address email_address_type not null unique,

    salted_hashed_password text,

    person_status citext not null default 'started registration'
    references person_statuses (title)
    on delete cascade
    on update cascade,

    display_name citext,

    -- super users are different than just local administrators.
    is_superuser boolean not null default false,

    -- Use this for whatever you want, for example, when you send an
    -- "confirm signup" email or SMS message.
    -- This will automatically get a random 4-digit code.
     confirmation_code text default to_char(random_between(1, 9999), 'fm0000'),

    -- I'm storing WHEN they agreed with the TOS.  A NULL value means
    -- they haven't yet agreed.
    agreed_with_TOS timestamptz,

    inserted timestamptz not null default now(),
    updated timestamptz

);

create trigger people_set_updated_column
before update
on people
for each row
execute procedure set_updated_column();

-- The only thing that goes in the cookie should be the session UUID and
-- the signature.  Everything else goes in here.  Deal with it.
create table webapp_sessions
(
    session_uuid uuid primary key default uuid_generate_v4(),
    expires timestamptz not null default now() + interval '1 year',

    person_uuid uuid
    references people (person_uuid)
    on delete cascade
    on update cascade,

    inserted timestamptz not null default now(),
    updated timestamptz
);

create trigger webapp_sessions_set_updated_column
before update
on webapp_sessions
for each row
execute procedure set_updated_column();

create table webapp_session_data
(
    session_uuid uuid not null
    references webapp_sessions (session_uuid)
    on delete cascade
    on update cascade,

    -- namespace is a crappy name and when I figure out a better name,
    -- I'll rename this column.

    -- The point is to allow you to separate data into separate
    -- categories.

    -- For example, each HTML form could store the user's submitted data
    -- (for redrawing later) in a separate namespace.

    namespace citext not null,

    primary key (session_uuid, namespace),
    session_data hstore,
    inserted timestamptz not null default now(),
    updated timestamptz
);

create trigger webapp_session_data_set_updated_column
before update
on webapp_session_data
for each row
execute procedure set_updated_column();

create table message_types
(
    title citext primary key,
    description text,
    inserted timestamptz not null default now(),
    updated timestamptz
);

create trigger message_types_set_updated_column
before update
on message_types
for each row
execute procedure set_updated_column();

insert into message_types
(title)
values
('registration'),
('forgot password')
;


-- Put rows in here to send emails.
create table email_message_queue
(
    email_message_queue_id serial primary key,
    nonce uuid not null default uuid_generate_v4(),

    -- the redeemed columns tracks if this message has already been
    -- redeemed.  if "redeemed" sounds goofy, think of it as when the
    -- user used this message to do something.
    redeemed timestamptz,

    recipient_email_address email_address_type
    not null references people (email_address)
    on delete cascade
    on update cascade,

    message_type citext not null references message_types (title)
    on delete cascade
    on update cascade,

    selected_for_delivery timestamptz,

    -- Right now, python passes in these values.  I bet there's some
    -- cool way to grab these out of some environmental variables.
    selector_pid int,
    selector_host text,

    sent timestamptz,

    inserted timestamptz not null default now(),
    updated timestamptz
);

-- I just learned about this "comment" feature.
-- After you set these comments, then when you do \d
-- email_message_queue, this text is now part of the table definition.
-- It seems like a good way to help explain stuff.
comment on column email_message_queue.sent is
E'A NULL value means that the message has not been sent yet, while a
timestamptz value shows the moment when it was sent.';

comment on column email_message_queue.selected_for_delivery is
E'A NULL value means no script is processing this row.  A timestamptz
is the date when the script began processing this row.  Also look at
selector_pid and selector_host for more information';

create trigger email_message_queue_set_updated_column
before update
on email_message_queue
for each row
execute procedure set_updated_column();
