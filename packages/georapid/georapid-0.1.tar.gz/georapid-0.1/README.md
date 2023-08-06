# georapid-py
Query broadcasted news worldwide and visualize them using spatial aggregations. This python modules represents an idiomatic client accessing the [Geospatial Knowledge APIs](https://geospatial-ai.de/?rara_portfolio_categories=api-services) being hosted on [Rapid API Hub](https://rapidapi.com/hub). Please, check out the [RapidAPI Account Creation and Management Guide](https://docs.rapidapi.com/docs/account-creation-and-settings).

## Features
### [geoprotests API](https://rapidapi.com/gisfromscratch/api/geoprotests/)
*Query protests worldwide and visualize them using spatial aggregations.*
### [geofires API](https://rapidapi.com/gisfromscratch/api/geofires/)
*Query wildfires worldwide and visualize them using spatial aggregations.*
### [geojoins API](https://rapidapi.com/gisfromscratch/api/geojoins/)
*Joins two spatially enabled feature collections based on their relative spatial locations.*
### [geodetic API](https://rapidapi.com/gisfromscratch/api/geodetic/)
*Enables various geodetic functions like buffers, points from distance and direction, points along path and wedge construction.*

## Ready to use
The geoprotests and geofires services offer ready-to-use geospatial features representing broadcasted news related to various themes. You can use these geospatial features to build various mapping and geospatial applications. The underlying serverless cloud-backend analyses raw geospatial locations of news articles provided by the Global Database of Events, Language and Tone (GDELT) Project (https://www.gdeltproject.org/).

Every geospatial result support the GeoJSON and Esri FeatureSet format out of the box. All endpoints support a date parameter for filtering the geospatial features. For best sustainability, the serverless cloud-backend queries the articles from the knowledge graph and calculates the geospatial features on-the-fly.
