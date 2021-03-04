# Run zap docker container on port 9090  as a daemon, set the host as localhost and allow all ip address to connect to the api ( api.addrs.addr.name=.* )

docker run -u zap -p 9090:9090 -i owasp/zap2docker-stable zap.sh -daemon -host 0.0.0.0 -port 9090 -config api.disablekey=true -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true

# run zap-cli and perform tests such as a quick scan of a URL that will open and spider the URL, scan recursively, exclude URLs matching a given regex, and only use XSS and SQLi scanners,   -sc for scan then shutdown zap container

zap-cli -p 9090 -sc quick-scan -s xss,sqli --spider -r -e "some_regex_pattern" https://localhost:443
