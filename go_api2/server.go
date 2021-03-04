package main

import (
	"github.com/getsentry/sentry-go"
	sentrygin "github.com/getsentry/sentry-go/gin"
	"github.com/gin-gonic/gin"
	"github.com/go_api2/controller"
	"github.com/go_api2/cors"
	"github.com/go_api2/database"
	"github.com/go_api2/env"
	"log"
	"net/http"
)

func main() {
	err:= sentry.Init(sentry.ClientOptions{
		Dsn: "https://abe0f3d0c6744585b57503c135d42623@o528321.ingest.sentry.io/5647886",
	})
	if err != nil {
		log.Fatalf("sentry.Init: %s", err)
	}
	router := gin.Default()
	cors.UseCors(router)
	/*router.Use(cors.Default())*/
	runWithDocker := env.GetDotEnvVariable("RUN_IN_DOCKER")
	database.InitDB_wih_envs(runWithDocker)
	controller.HttpToView(router)



	router.Use(sentrygin.New(sentrygin.Options{}))

    port := env.GetDotEnvVariable("GO_GIN_PORT")
    ENV_TYPE:= env.GetDotEnvVariable("ENV_TYPE")

	if ENV_TYPE == "0" {
		err := http.ListenAndServe(":"+port, router)
		if err != nil {
			println(err)
		}
	} else if ENV_TYPE == "1" {
		err := http.ListenAndServeTLS(":"+port, "/etc/cert.pem", "/etc/privkey.pem", router)
		if err != nil {
			println(err)
		}
	}
}







