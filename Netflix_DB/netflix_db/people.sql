create table netflix_db.people
(
    PID        int auto_increment
        primary key,
    PName      varchar(50) not null,
    DOB        date        not null,
    IsActor    bit         null,
    IsDirector bit         null,
    IsWriter   bit         null
);

