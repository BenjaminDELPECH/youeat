create table meal_object_type
(
    id   int auto_increment
        primary key,
    name varchar(255) not null
);

INSERT INTO simplenutrition.meal_object_type (id, name) VALUES (1, 'routines');
INSERT INTO simplenutrition.meal_object_type (id, name) VALUES (2, 'meals');