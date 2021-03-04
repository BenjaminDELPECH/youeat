package cors

import (
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"time"
)

func UseCors(router *gin.Engine) *gin.Engine{
	router.Use(cors.New(cors.Config{
		AllowAllOrigins: true,
		AllowMethods:           []string{"GET"},
		AllowHeaders:           []string{"*"},
		AllowCredentials:       true,
		ExposeHeaders:          []string{"Content-Length"},
		MaxAge:                 12 * time.Hour,
		AllowWildcard:          false,
		AllowBrowserExtensions: false,
		AllowWebSockets:        false,
		AllowFiles:             false,
	}))
	return router
}