create table netflix_db.moviegenre_pivot
(
    MID int not null,
    GID int not null,
    primary key (MID, GID)
);

