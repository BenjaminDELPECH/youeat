package utils

import (
	"database/sql"
	"github.com/go_api2/database"
	"strconv"
)


func GetStmtFromStr(reqStr string ) *sql.Stmt {
	query, err := database.Database.Prepare(reqStr)
	ThrowError(err)
	return query
}

func GetSQLListId(idList []uint64) string {
	args := []interface{}{}
	var id_list_str string
	for i := 0; i < len(idList); i++ {
		foodId := int(idList[i])
		id_list_str += strconv.Itoa(foodId)
		args = append(args, idList[i])
		if i < len(idList)-1 {
			id_list_str += ","
		}
	}
	return "("+id_list_str+")"
}

func QueryToTableData(sqlString string) ([]map[string]interface{}, error) {
	rows, err := database.Database.Query(sqlString)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	if err != nil {
		return nil, err
	}
	return SqlRowsToTableData( rows)
}

func SqlRowsToTableData(rows *sql.Rows) ([]map[string]interface{}, error) {
	columns, err := rows.Columns()
	ThrowError(err)
	count := len(columns)
	tableData := make([]map[string]interface{}, 0)
	values := make([]interface{}, count)
	valuePtrs := make([]interface{}, count)
	for rows.Next() {
		for i := 0; i < count; i++ {
			valuePtrs[i] = &values[i]
		}
		rows.Scan(valuePtrs...)
		entry := make(map[string]interface{})
		for i, col := range columns {
			var v interface{}
			val := values[i]
			b, ok := val.([]byte)
			if ok {
				v = string(b)
			} else {
				v = val
			}
			entry[col] = v
		}
		tableData = append(tableData, entry)
	}
	return tableData, nil
}