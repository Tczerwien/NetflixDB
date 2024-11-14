create table netflix_db.rating
(
    RID    int           not null
        primary key,
    Rating decimal(5, 2) null,
    Votes  int           null
);

