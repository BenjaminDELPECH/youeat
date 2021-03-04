package food

import (
	"github.com/gin-gonic/gin"
	"github.com/go_api2/utils"
)


var QueryConversionFactor = " Select cf.id as conversion_factor_id,\n       cf.food_id as food_id,\n       cf.measure_id as measure_id,\n       cf.conversion_factor as conversion_factor,\n       fm.nameFr as nameFr from simplenutrition.foods_conversionfactor cf\n    join foods_measure fm on fm.id = cf.measure_id where food_id in "

var QueryFood = "Select * from foods_food where id = ?;"

func GetConversionFactors(c* gin.Context){
	utils.SqlToJSONWithOneColSelector(c, QueryConversionFactor, "food_id_list")
}

func GetFood(c* gin.Context){
	utils.SqlToJSONWithOneColSelector(c, QueryFood, "food_id")
}
