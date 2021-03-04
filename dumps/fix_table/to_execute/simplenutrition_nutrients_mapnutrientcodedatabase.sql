create table nutrients_mapnutrientcodedatabase
(
    id            int auto_increment
        primary key,
    nutrient_code int not null,
    database_id   int null,
    nutrient_id   int not null,
    constraint nutrients_mapnutrien_database_id_5c090155_fk_nutrients
        foreign key (database_id) references nutrients_database (id),
    constraint nutrients_mapnutrien_nutrient_id_1a4bcaf1_fk_nutrients
        foreign key (nutrient_id) references nutrients_nutrient (id)
);

INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (1, 25000, 1, 203);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (2, 40000, 1, 204);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (3, 31000, 1, 205);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (4, 333, 1, 208);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (5, 32250, 1, 211);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (6, 32210, 1, 212);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (7, 32220, 1, 213);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (8, 32430, 1, 214);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (9, 60000, 1, 221);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (10, 400, 1, 255);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (11, 32000, 1, 269);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (12, 32220, 1, 287);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (13, 34100, 1, 291);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (14, 10200, 1, 301);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (15, 10260, 1, 303);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (16, 10120, 1, 304);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (17, 10150, 1, 305);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (18, 10190, 1, 306);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (19, 10110, 1, 307);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (20, 10300, 1, 309);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (21, 10290, 1, 312);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (22, 10251, 1, 315);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (23, 10340, 1, 317);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (24, 51200, 1, 319);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (25, 51330, 1, 321);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (26, 52100, 1, 339);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (27, 55100, 1, 401);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (28, 56100, 1, 404);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (29, 56200, 1, 405);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (30, 56310, 1, 406);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (31, 56400, 1, 410);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (32, 56500, 1, 415);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (33, 56700, 1, 417);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (34, 56600, 1, 418);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (35, 75100, 1, 601);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (36, 40302, 1, 606);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (37, 40303, 1, 645);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (38, 40304, 1, 646);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (39, 40400, 1, 607);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (40, 40600, 1, 608);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (41, 40800, 1, 609);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (42, 41000, 1, 610);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (43, 41200, 1, 611);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (44, 41400, 1, 612);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (45, 41600, 1, 613);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (46, 41800, 1, 614);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (52, 41819, 1, 824);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (53, 41826, 1, 825);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (54, 41833, 1, 831);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (55, 42046, 1, 855);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (56, 42053, 1, 629);
INSERT INTO simplenutrition.nutrients_mapnutrientcodedatabase (id, nutrient_code, database_id, nutrient_id) VALUES (57, 42263, 1, 621);