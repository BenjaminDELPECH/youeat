package meals

import (
	"encoding/json"
	"github.com/gin-gonic/gin"
	"github.com/go_api2/food"
	"github.com/go_api2/utils"
	"sort"
	"strconv"
)

var QueryMeals = "SELECT * FROM simplenutrition.meal_meal"
var QueryMealsWithUserId = "SELECT * FROM simplenutrition.meal_meal where author_id = ?"
var QueryLinkMealFoods = "Select * FROM simplenutrition.nutrients_linknutrientfood where food_id < 100"
var QueryLMF = "Select lmf.id, lmf.meal_id , lmf.food_id, fc.conversion_factor, lmf.conversion_factor_id,\n       lmf.quantity,\n       fm.nameFr as measureNameFr,\n       foods_food.name_fr as foodNameFr\nfrom meal_link_meal_food lmf\n         inner join foods_food on lmf.food_id = foods_food.id\n         inner join meal_meal on lmf.meal_id = meal_meal.id\n         inner join foods_conversionfactor fc on lmf.conversion_factor_id = fc.id\n         inner join foods_measure fm on fc.measure_id = fm.id\nwhere meal_id = ?;"
var QueryLNF = "Select lnf.food_id, nutrient_id, value\nfrom simplenutrition.nutrients_linknutrientfood lnf\ninner join nutrients_nutrient nn on lnf.nutrient_id = nn.id\nwhere lnf.food_id in\n      (Select food_id\n       from simplenutrition.meal_link_meal_food\n       where meal_id = ? \n      )\nand nn.nutrientGroup_id is not null;\n"
var QueryProfile = "Select * from users_profile where user_id = ?"


type LinkMealFood struct {
	FoodId uint64
	MealId uint64
}

type Meal struct {
	Id            uint64
	Name          string
	ImgUrl        string
	QueryScore    uint64
	LinkMealFoods []*LinkMealFood
	Score         string
	Calorie       uint64
}

var QueryMeal = "Select m.*,user.username  from simplenutrition.meal_meal as m join auth_user as user on m.author_id = user.id where m.id = ? "

func GetProfile(c* gin.Context){
	utils.SqlToJSONWithOneColSelector(c, QueryProfile, "user_id")
}

func GetMeal(c *gin.Context) {
	q := c.Query("mealId")
	mealId := utils.GetIntFromParam(q)
	query := utils.GetStmtFromStr(QueryMeal)
	rows, err := query.Query(mealId)
	utils.ThrowError(err)
	utils.RowsToJson(c, rows)
}

func GetLNF(c *gin.Context) {
	q := c.Query("mealId")
	mealId := utils.GetIntFromParam(q)
	query := utils.GetStmtFromStr(QueryLNF)
	rows, err := query.Query(mealId)
	utils.ThrowError(err)
	utils.RowsToJson(c, rows)
}

func GetLMF(c *gin.Context) {
	q := c.Query("mealId")
	mealId, err := strconv.ParseInt(q, 10, 32)
	utils.ThrowError(err)
	query := utils.GetStmtFromStr(QueryLMF)
	rows, err := query.Query(mealId)
	utils.RowsToJson(c, rows)
}

func GetMeals(c *gin.Context) {
	userId := c.Query("userId")
	if userId != "" {
		userId := utils.GetIntFromParam(userId)
		query := utils.GetStmtFromStr(QueryMealsWithUserId)
		rows, err := query.Query(userId)
		utils.ThrowError(err)
		utils.RowsToJson(c, rows)
	} else {
		utils.SqlToJson(c, QueryMeals)
	}

}

func GetLinkMealFoos(c *gin.Context) {
	utils.SqlToJson(c, QueryLinkMealFoods)
}

func SearchMeals(c *gin.Context) {
	q := c.Query("q")
	if q == "" {
		utils.SqlToJson(c, QueryMeals)
	} else {
		foodsAndScore := food.GetFoodsScores(c)

		var foodIdList []uint64
		for i := 0; i < len(foodsAndScore); i++ {
			foodIdList = append(foodIdList, foodsAndScore[i].Food.ID)
		}

		//STEP 2
		stmt := utils.GetSQLListId(foodIdList)
		stmt_main :=
			"Select meal.*, lmf.food_id , ROUND(lmf.quantity * fc.conversion_factor * nlnf.value) as calorie FROM meal_meal as meal " +
				"inner join meal_link_meal_food as lmf  ON meal.id = lmf.meal_id " +
				" inner join nutrients_linknutrientfood nlnf ON nlnf.food_id = lmf.food_id " +
				" inner join foods_conversionfactor fc on lmf.conversion_factor_id = fc.id " +
				"where " +
				"nlnf.nutrient_id = 208 " +
				"and meal.id in " +
				"(Select meal_id from meal_link_meal_food where food_id in " +
				stmt +
				");"

		tableData, err := utils.QueryToTableData(stmt_main)
		utils.ThrowError(err)
		print(tableData)

		var meals []*Meal
		for _, e := range tableData {
			mealId := *getValueFromTableTada(e, "id")
			indexMeal := getMealIndex(meals, mealId)
			if indexMeal != -1 {
				meal := meals[indexMeal]
				meal = addLinkMealFoodAndScore(e, foodsAndScore, mealId, meal)
			} else {

				utils.ThrowError(err)
				meal := Meal{
					Id:            mealId,
					Name:          e["name"].(string),
					ImgUrl:        e["imgUrl"].(string),
					LinkMealFoods: []*LinkMealFood{},
					Calorie:       *getValueFromTableTada(e, "calorie"),
				}
				meal = *addLinkMealFoodAndScore(e, foodsAndScore, mealId, &meal)
				meals = append(meals, &meal)
			}
		}

		sort.Slice(meals, func(i, j int) bool {
			return meals[i].QueryScore > meals[j].QueryScore
		})
		jsonData, err := json.Marshal(meals)

		c.String(200, string(jsonData))
	}
}

func addLinkMealFoodAndScore(e map[string]interface{}, foodsAndScore []*food.ObjFoodScore, mealId uint64, meal *Meal) *Meal {
	calorie := *getValueFromTableTada(e, "calorie")
	foodId := *getValueFromTableTada(e, "food_id")
	var foodIdScore uint64
	foodIdScore = *getFoodIdScore(foodsAndScore, foodId)
	lmf := LinkMealFood{
		FoodId: foodId,
		MealId: mealId,
	}
	meal.LinkMealFoods = append(meal.LinkMealFoods, &lmf)
	meal.QueryScore += foodIdScore
	meal.Calorie += calorie
	return meal
}

func getFoodIdScore(foodsAndScore []*food.ObjFoodScore, foodId uint64) *uint64 {
	for _, e := range foodsAndScore {

		elemFoodId := e.Food.ID
		if elemFoodId == foodId {
			return &e.Score
		}
	}
	return nil
}

/*	rows, error := database.Database.Query(stmt_main)
	utils.ThrowError(error)
	defer rows.Close()
	columns, err := rows.Columns()
	for rows.Next(){

	}*/

func getMealIndex(meals []*Meal, mealId uint64) int {
	indexMeal := -1

	for i2, e2 := range meals {
		if e2.Id == mealId {
			indexMeal = i2
			break
		}
	}
	return indexMeal
}

func getValueFromTableTada(strInterface map[string]interface{}, colName string) *uint64 {
	foodIdTestExist := strInterface[colName]
	if foodIdTestExist != nil {
		foodId, err := strconv.ParseUint(strInterface[colName].(string), 10, 64)
		utils.ThrowError(err)
		return &foodId
	}
	return nil
}
