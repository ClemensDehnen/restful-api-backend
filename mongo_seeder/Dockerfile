FROM mongo:4.2
COPY data.json /data.json
CMD mongoimport --host mongo_db --db test --collection testCollection --drop --file /data.json --jsonArray