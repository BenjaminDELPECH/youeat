package utils

import (
	"github.com/gin-gonic/gin"
	"strconv"
	"strings"
)

func SqlToJSONWithOneColSelector(c *gin.Context, querySQL string, colNameSelector string) {
	q := c.Query(colNameSelector)


	if strings.Contains(querySQL, " in ") {
		idList := strings.Split(q, ",")
		var idListUint []uint64
		for _, s := range idList {
			id, err := strconv.ParseUint(s, 10, 64)
			ThrowError(err)
			idListUint = append(idListUint, id)
		}
		paramValue := GetSQLListId(idListUint)
		querySQL += paramValue
		sqlStmt := GetStmtFromStr(querySQL)
		rows, err := sqlStmt.Query()
		ThrowError(err)
		RowsToJson(c, rows)

	}else{
		paramValue := GetIntFromParam(q)
		sqlStmt := GetStmtFromStr(querySQL)
		rows, err := sqlStmt.Query(paramValue)
		ThrowError(err)
		RowsToJson(c, rows)
	}



}