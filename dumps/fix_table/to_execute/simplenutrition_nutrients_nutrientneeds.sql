create table nutrients_nutrientneeds
(
    id          int auto_increment
        primary key,
    sex         int          not null,
    need        double       not null,
    nutrient_id int          not null,
    code        varchar(255) null,
    constraint nutrients_nutrientne_nutrient_id_c59288d3_fk_nutrients
        foreign key (nutrient_id) references nutrients_nutrient (id)
);

INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (1, 1, 800, 301, '');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (2, 0, 1200, 301, '');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (3, 1, 1.7, 312, '');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (4, 0, 1.2, 312, '');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (5, -1, 2500, 301, 'MAX');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (6, -1, 40, 312, 'MAX');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (7, 1, 9, 303, ' ');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (8, 0, 15, 303, ' ');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (9, -1, 100, 303, 'MAX');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (10, 1, 420, 304, ' ');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (11, 0, 360, 304, ' ');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (12, -1, 3000, 304, 'MAX');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (16, 1, 800, 305, null);
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (17, 0, 800, 305, null);
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (18, -1, 2500, 305, 'MAX');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (19, 1, 3500, 306, null);
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (20, 0, 3500, 306, null);
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (21, -1, 6000, 306, 'MAX');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (22, 1, 70, 317, null);
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (23, 0, 70, 317, null);
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (24, -1, 400, 317, 'MAX');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (25, 1, 1500, 307, null);
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (26, 0, 1500, 307, null);
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (27, -1, 14000, 307, 'MAX');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (28, -1, 2500, 307, 'AMT');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (29, -1, 5, 312, 'AMT');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (30, -1, 300, 317, 'AMT');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (31, 1, 15, 309, null);
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (32, 0, 10, 309, null);
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (33, -1, 25, 309, 'AMT');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (34, -1, 200, 309, 'MAX');
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (35, 1, 3, 315, null);
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (36, 0, 3, 315, null);
INSERT INTO simplenutrition.nutrients_nutrientneeds (id, sex, need, nutrient_id, code) VALUES (37, -1, 50, 315, 'MAX');