package database

import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	"github.com/go_api2/env"
	"log"
)

var Database *sql.DB

func InitDB_wih_envs(runWithDocker string) {
	database_name := env.GetDotEnvVariable("DATABASE_NAME")
	database_username := env.GetDotEnvVariable("DATABASE_USERNAME")
	database_password := env.GetDotEnvVariable("DATABASE_PASSWORD")

	// todo check if this is not the name of the container

	var database_host string
	var database_port string
	if runWithDocker == "0" {
		database_host = "localhost"
		database_port = "3306"
	} else {
		database_host = env.GetDotEnvVariable("DATABASE_HOST")
		database_port = env.GetDotEnvVariable("DATABASE_CONTAINER_PORT")
	}

	datasource_name := ""
	datasource_name += database_username
	datasource_name += ":"
	datasource_name += database_password
	datasource_name += "@(" + database_host + ":" + database_port + ")/"
	datasource_name += database_name

	db, err := sql.Open("mysql", datasource_name)
	if err != nil {
		log.Panic(err)
	}

	//if err = db.Ping(); err != nil {
	//	log.Panic(err)
	//}
	Database = db
}
