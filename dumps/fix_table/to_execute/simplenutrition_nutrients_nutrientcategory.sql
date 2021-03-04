create table nutrients_nutrientcategory
(
    id               int auto_increment
        primary key,
    icon_name        varchar(255) not null,
    category_name_fr varchar(255) not null,
    category_name_en varchar(255) not null,
    activated        tinyint(1)   not null
);

INSERT INTO simplenutrition.nutrients_nutrientcategory (id, icon_name, category_name_fr, category_name_en, activated) VALUES (1, 'img:https://img.icons8.com/material/24/000000/coronavirus.png', 'santé', 'immunity', 1);
INSERT INTO simplenutrition.nutrients_nutrientcategory (id, icon_name, category_name_fr, category_name_en, activated) VALUES (2, 'img:https://img.icons8.com/ios/50/000000/brain--v1.png', 'cerveau', 'cerveau', 1);
INSERT INTO simplenutrition.nutrients_nutrientcategory (id, icon_name, category_name_fr, category_name_en, activated) VALUES (3, 'img:https://img.icons8.com/metro/26/000000/dumbbell.png', 'force', 'strength', 1);
INSERT INTO simplenutrition.nutrients_nutrientcategory (id, icon_name, category_name_fr, category_name_en, activated) VALUES (4, 'icons/keto.png', 'keto', 'keto', 0);
INSERT INTO simplenutrition.nutrients_nutrientcategory (id, icon_name, category_name_fr, category_name_en, activated) VALUES (5, 'img:https://www.flaticon.com/svg/static/icons/svg/846/846559.svg', 'vegan', 'vegan', 0);