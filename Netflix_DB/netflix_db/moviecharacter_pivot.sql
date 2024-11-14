create table netflix_db.moviecharacter_pivot
(
    MID int not null,
    CID int not null,
    primary key (MID, CID)
);

