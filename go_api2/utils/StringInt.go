package utils

import "strconv"

func GetIntFromParam(q string) int64 {
	myInt, err := strconv.ParseInt(q, 10, 32)
	ThrowError(err)
	return myInt
}