create table foods_googlefoodslabels
(
    id      int auto_increment
        primary key,
    img_url varchar(500) not null,
    label   varchar(250) not null,
    food_id int          not null,
    constraint foods_googlefoodslabels_food_id_b38c3589_fk_foods_food_id
        foreign key (food_id) references foods_food (id)
);

