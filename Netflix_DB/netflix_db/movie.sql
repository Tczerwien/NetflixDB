create table netflix_db.movie
(
    MID          int auto_increment
        primary key,
    MName        varchar(50) not null,
    MReleaseDate int         not null,
    MRuntime     int         not null
);

