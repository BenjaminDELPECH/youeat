create table nutrients_linknutrientnutrient
(
    id              int auto_increment
        primary key,
    `order`         int not null,
    mom_nutrient_id int null,
    son_nutrient_id int null,
    constraint nutrients_linknutrie_mom_nutrient_id_3f9be177_fk_nutrients
        foreign key (mom_nutrient_id) references nutrients_nutrient (id),
    constraint nutrients_linknutrie_son_nutrient_id_858bfebe_fk_nutrients
        foreign key (son_nutrient_id) references nutrients_nutrient (id)
);

INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (1, 1, 204, 606);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (2, 3, 204, 861);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (3, 2, 204, 645);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (4, 1, 606, 607);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (5, 2, 606, 608);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (6, 3, 606, 609);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (7, 4, 606, 610);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (8, 5, 606, 611);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (9, 7, 606, 613);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (10, 8, 606, 614);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (11, 9, 606, 615);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (13, 1, 646, 831);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (14, 2, 646, 621);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (15, 3, 646, 629);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (16, 4, 646, 825);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (17, 5, 646, 855);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (18, 6, 606, 612);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (24, 1, 205, 211);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (25, 2, 205, 212);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (26, 3, 205, 213);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (27, 4, 205, 214);
INSERT INTO simplenutrition.nutrients_linknutrientnutrient (id, `order`, mom_nutrient_id, son_nutrient_id) VALUES (28, 5, 205, 221);