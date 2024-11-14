create table netflix_db.series
(
    SID          int auto_increment
        primary key,
    SName        varchar(50) not null,
    SReleaseDate int         not null,
    SEnd         int         null
);

