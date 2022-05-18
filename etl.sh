# starts mysql
docker-compose up -d 

#builds the python image
docker build . -t etl_process

# runs python image as container and connect to mysql network
docker run -it --rm --network etlprocess_default etl_process