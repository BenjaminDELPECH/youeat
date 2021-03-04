package utils

import (
	"database/sql"
	"encoding/json"
	"github.com/gin-gonic/gin"
)


func SqlToJson(c *gin.Context, string string) {
	response := GetJSONFromSqlReq(string)
	c.String(200, response)
}

func GetJSONFromSqlReq(sqlString string) (string) {
	tableData, err := QueryToTableData(sqlString)
	ThrowError(err)
	return GetJSONFromTableData(tableData)
}

func GetJSONFromTableData(tableData []map[string]interface{}) (string) {
	jsonData, err := json.Marshal(tableData)
	ThrowError(err)
	return string(jsonData)
}

func RowsToJson(c *gin.Context, rows *sql.Rows) {
	response, err := SqlRowsToTableData(rows)
	ThrowError(err)
	c.String(200, GetJSONFromTableData(response))
}



