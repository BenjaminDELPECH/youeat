create table foods_mapfoodgroup
(
    id               int auto_increment
        primary key,
    alim_group_level varchar(150) not null,
    grp_code         varchar(150) not null,
    food_group_id    int          not null,
    constraint foods_mapfoodgroup_food_group_id_d302eccb_fk_foods_foodgroup_id
        foreign key (food_group_id) references foods_foodgroup (id)
);

