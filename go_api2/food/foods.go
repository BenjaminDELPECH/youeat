package food

import (
	"database/sql"
	"encoding/json"
	"github.com/gin-gonic/gin"
	"github.com/go_api2/database"
	"github.com/go_api2/utils"
	"log"
	"net/http"
	"sort"
	"strconv"
)

type Food struct {
	ID              uint64
	NameFr          string
	nb_of_selection uint64
	ConvFactorNb uint8
}

type ObjFoodScore struct {
	Food  Food
	Score uint64
	ConvFactorNb uint8
}
type foodScoresList []*ObjFoodScore
type ByFoodScore struct {
	foodScoresList
}

func (obj foodScoresList) Len() int {
	return len(obj)
}
func (obj ByFoodScore) Less(i, j int) bool {
	return obj.foodScoresList[i].Score > obj.foodScoresList[j].Score
}
func (list foodScoresList) Swap(i, j int) {
	list[i], list[j] = list[j], list[i]
}

func GetFoodScores(searchText *string, foodGroupID *int) []*ObjFoodScore {
	sqlBase := "SELECT id, name_fr, nb_of_selection ,(Select count(id) From foods_conversionfactor where food_id = f.id) as conFactorNb FROM simplenutrition.foods_food as f;"
	if foodGroupID != nil {
		nutrientGroupId := int64(*foodGroupID)
		sqlBase += " WHERE foodGroup_id = " + strconv.FormatInt(nutrientGroupId, 10)
	}
	statement, err := database.Database.Prepare(sqlBase)
	if err != nil {
		log.Fatal(err)
	}
	defer statement.Close()
	rows, err := statement.Query()
	defer rows.Close()

	foods := []Food{}
	var objScoreList []*ObjFoodScore

	for rows.Next() {
		objScoreList, foods = manageFoodRow(searchText, rows, objScoreList, foods)
	}
	if err = rows.Err(); err != nil {
		log.Fatal(err)
	}

	sort.Slice(objScoreList, func(i, j int) bool {
		return objScoreList[i].Score > objScoreList[j].Score
	})

	return objScoreList
}

func SearchFoods(c *gin.Context) {
	foodsScore := GetFoodsScores(c)
	var foods []*Food
	for i := 0; i < 100; i++ {
		foods = append(foods, &foodsScore[i].Food)
	}

	jsonData, err := json.Marshal(foods)
	utils.ThrowError(err)
	c.String(200, string(jsonData))
}

func manageFoodRow(searchText *string, rows *sql.Rows, objScoreList []*ObjFoodScore, foods []Food) ([]*ObjFoodScore, []Food) {
	var food Food
	err := rows.Scan(&food.ID, &food.NameFr, &food.nb_of_selection, &food.ConvFactorNb)
	var objScore ObjFoodScore
	if *searchText != "" {
		similarity_score := utils.CalculateSimilarityStringScores(&food.NameFr, *searchText)
		objScore = ObjFoodScore{
			Food:  food,
			Score: *similarity_score,
			ConvFactorNb: food.ConvFactorNb,
		}
	} else {
		objScore = ObjFoodScore{
			Food:  food,
			Score: food.nb_of_selection,
		}
	}
	objScoreList = append(objScoreList, &objScore)
	if err != nil {
		log.Fatal(err)
	}
	return objScoreList, foods
}

func GetMostSimilarFoodName(c *gin.Context) {
	foodsAndScore := GetFoodsScores(c)
	foodsAndScore = foodsAndScore[:250]
	var foodIdList []uint64
	for i := 0; i < len(foodsAndScore); i++ {
		foodIdList = append(foodIdList, foodsAndScore[i].Food.ID)
	}
	firstResultStr := strconv.Itoa(int(foodIdList[0]))
	c.String(http.StatusOK, firstResultStr)
}

func GetFoodsScores(c *gin.Context) []*ObjFoodScore {
	q := c.Query("q")
	return GetFoodScores(&q, nil)
}

var QueryLNF = "Select * from nutrients_linknutrientfood where food_id = ?;"
func GetLNFByFoodId(c *gin.Context) {
	q := c.Query("foodId")
	mealId := utils.GetIntFromParam(q)
	query := utils.GetStmtFromStr(QueryLNF)
	rows, err := query.Query(mealId)
	utils.ThrowError(err)
	utils.RowsToJson(c, rows)
}
