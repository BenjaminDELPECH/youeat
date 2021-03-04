FROM golang:1.14

ARG API_PORT

WORKDIR /build



COPY go.mod .
COPY go.sum .
RUN go mod download

COPY . .

RUN go build -o main .

WORKDIR /dist

RUN cp /build/main .



CMD ["/dist/main"]




COPY cert.pem  /etc/cert.pem
COPY privkey.pem /etc/privkey.pem
