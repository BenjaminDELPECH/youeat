package controller

import (
	"github.com/gin-gonic/gin"
	"github.com/go_api2/food"
	"github.com/go_api2/meals"
	"github.com/go_api2/nutrients"
)

func HttpToView(router *gin.Engine) {

	//meals
	router.GET("/getMeal", meals.GetMeal)
	router.GET("/searchMeals", meals.SearchMeals)
	router.GET("/meals", meals.GetMeals)
	router.GET("/linkMealFoods", meals.GetLinkMealFoos)
	router.GET("/getMostSimilarFoodName", food.GetMostSimilarFoodName)
	router.GET("/getLMF", meals.GetLMF)
	router.GET("/getLNF", meals.GetLNF)

	//nutrients
	router.GET("/getNutrients", nutrients.GetNutrients)
	router.GET("/getNutrientGroups", nutrients.GetNutrientGroups)

	//foods
	router.GET("/searchFoods", food.SearchFoods)
	router.GET("/getConversionFactors", food.GetConversionFactors)
	router.GET("/getLNFByFoodId", food.GetLNFByFoodId)
	router.GET("/getFood", food.GetFood)

	//user
	router.GET("/getProfile", meals.GetProfile)

}
