package nutrients

import (
	"github.com/gin-gonic/gin"
	"github.com/go_api2/utils"
)

var QueryNutrients = "Select *  from nutrients_nutrient where nutrientGroup_id is not null;"
var QueryNutrientsGroup = "Select * from nutrients_nutrientgroup;"

func GetNutrients(c *gin.Context){
	utils.SqlToJson(c, QueryNutrients)
}

func GetNutrientGroups(c *gin.Context){
	utils.SqlToJson(c, QueryNutrientsGroup)
}

