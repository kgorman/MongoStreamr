# MongoStreamr
Mongodb change stream to Eventador.io agent

## install

### Clone this repo
Open a terminal window and run the following commands from a convenient directory on your machine:

```
git clone git@github.com:kgorman/MongoStreamr.git
cd MongoStreamr
```

### Create an environment file
In the same terminal window and directory, create an .env file with your login credentials and some configuration information. This example uses the sample data called MongoWeather.
```
echo "TOPIC=xx" > mongostreamr.env
echo "URL=<rest url>" >> mongostreamr.env
echo "API_KEY=<api key>" >>mongostreamr.env
echo "MONGOSTR=<string from mongo atlas>" >>mongostreamr.env
echo "MONGODB=sample_weatherdata" >>mongostreamr.env
echo "MONGOCOL=data" >>mongostreamr.env
```
### Populate Eventador Kafka topic with data
```
docker build . -t streamr
docker -it -d --env-file mongostreamr.env streamr
```
