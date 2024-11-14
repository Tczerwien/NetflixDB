create table netflix_db.seriesgenre_pivot
(
    SID int not null,
    GID int not null,
    primary key (SID, GID)
);

