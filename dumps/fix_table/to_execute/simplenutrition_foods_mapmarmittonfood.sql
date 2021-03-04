create table foods_mapmarmittonfood
(
    marmitton_food_name varchar(250) not null
        primary key,
    recurrence          int          not null,
    negligable          tinyint(1)   not null,
    food_id             int          null,
    constraint foods_mapmarmittonfood_food_id_7016e012_fk_foods_food_id
        foreign key (food_id) references foods_food (id)
);

