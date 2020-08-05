create table users (
    id integer primary key,
    name text not null,
    password text not null,
    talent boolean not null,
    client boolean not null
);