create table users (
    id integer primary key autoincrement,
    username text not null,
    email text not null,
    password text not null,
    client boolean not null,
    talent boolean not null,
    admin boolean not null
);


create table talent_profile (
    id integer primary key autoincrement,
    talent_user_id integer not null,
    profession text not null,
    years_experience integer not null,
    first_name text not null,
    last_name text not null
);