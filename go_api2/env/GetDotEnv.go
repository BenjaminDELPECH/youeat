package env

import (
	"github.com/joho/godotenv"
	"log"
	"os"
)

func GetDotEnvVariable(key string) string {
	value := os.Getenv(key)
	if value == "" {
		if err := godotenv.Load("../.env"); err != nil {
			log.Println(err)
		}
		return GetDotEnvVariable(key)
	}
	return os.Getenv(key)
}
