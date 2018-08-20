-- Parents and doctors are in the people table, and they sign in to the
-- app.

-- Patients, meanwhile, are children, and they don't sign in.
create table patients
(

    -- postgresql sequences start with 1, so unless I do something
    -- elaborate,there's not gonna be a "patient zero", which is fine,
    -- because I don't care enough about making a stupid "patient zero"
    -- joke to do all that work.
    patient_number serial primary key,
    display_name citext,
    extra_notes text,
    extra_data json,
    inserted timestamptz not null default now(),
    updated timestamptz
);

create trigger patients_set_updated_column
before update
on patients
for each row
execute procedure set_updated_column();

create table provider_patient_links (

    provider uuid not null references people (person_uuid)
    on delete cascade,

    patient_number integer not null references patients (patient_number),

    primary key (provider, patient_number),

    extra_notes text,
    extra_data json,

    inserted timestamptz not null default now(),
    updated timestamptz

);

create trigger provider_patient_links_set_updated_column
before update
on provider_patient_links
for each row
execute procedure set_updated_column();

create table patient_caretakers (

    caretaker uuid not null references people (person_uuid)
    on delete cascade,

    patient_number integer not null references patients (patient_number),

    primary key (caretaker, patient_number),

    extra_notes text,
    extra_data json,

    inserted timestamptz not null default now(),
    updated timestamptz

);

create trigger patient_caretakers_set_updated_column
before update
on patient_caretakers
for each row
execute procedure set_updated_column();

create table patient_events
(
    patient_number integer not null references patients
    on delete cascade,

    extra_notes text,
    extra_data json,

    -- this is when the poop happened, not when the record was stored in
    -- our system.
    event_timestamp timestamptz not null default now(),

    inserted timestamptz not null default now(),
    updated timestamptz
);

create trigger patient_events_set_updated_column
before update
on patient_events
for each row
execute procedure set_updated_column();
