del "constants_dump.sql" >nul 2>&1
del "info*" >nul 2>&1
ECHO SET FOREIGN_KEY_CHECKS = 0; > constants_dump.sql
mysqldump -u root -pennov simplenutrition foods_conversionfactor foods_food foods_foodgroup foods_mapfoodgroup foods_mapmarmittonfood foods_measure meal_link_object_page meal_object_type nutrients_database nutrients_linknutrientfood nutrients_linknutrientnutrient nutrients_mapnutrientcodedatabase nutrients_nutrient nutrients_nutrientcategoryrole nutrients_nutrientcategory  nutrients_nutrientgroup nutrients_nutrientneeds  >> constants_dump.sql --force --disable-keys --replace
ECHO SET FOREIGN_KEY_CHECKS = 1; >> constants_dump.sql