create table nutrients_database
(
    id   int auto_increment
        primary key,
    name varchar(255) not null
);

INSERT INTO simplenutrition.nutrients_database (id, name) VALUES (1, 'cliqual');