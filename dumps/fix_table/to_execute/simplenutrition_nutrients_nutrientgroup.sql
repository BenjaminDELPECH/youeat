create table nutrients_nutrientgroup
(
    id               int auto_increment
        primary key,
    nameFr           varchar(255) not null,
    nameEn           varchar(255) not null,
    deployed_default tinyint(1)   not null,
    position         int          not null
);

INSERT INTO simplenutrition.nutrients_nutrientgroup (id, nameFr, nameEn, deployed_default, position) VALUES (1, 'Glucide', 'Carbohydrate', 0, 1);
INSERT INTO simplenutrition.nutrients_nutrientgroup (id, nameFr, nameEn, deployed_default, position) VALUES (2, 'Lipide', 'Lipid', 0, 2);
INSERT INTO simplenutrition.nutrients_nutrientgroup (id, nameFr, nameEn, deployed_default, position) VALUES (3, 'Protéines', 'Protein', 0, 3);
INSERT INTO simplenutrition.nutrients_nutrientgroup (id, nameFr, nameEn, deployed_default, position) VALUES (4, 'Vitamines', 'Vitamins', 1, 5);
INSERT INTO simplenutrition.nutrients_nutrientgroup (id, nameFr, nameEn, deployed_default, position) VALUES (5, 'Minéraux', 'Minerals', 0, 6);
INSERT INTO simplenutrition.nutrients_nutrientgroup (id, nameFr, nameEn, deployed_default, position) VALUES (8, 'Fibres', 'Fibers', 0, 4);
INSERT INTO simplenutrition.nutrients_nutrientgroup (id, nameFr, nameEn, deployed_default, position) VALUES (9, 'Calorie', 'Calory', 0, 0);