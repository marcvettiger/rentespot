# Rentepoint
probably b'cause we rip
## Requirements
* python 2.7.12
* pip

## Setup

~~~
pip install -r requirements.txt
~~~

## Basic Usage
Import Spots from the package
~~~
from rentepoint import Spots
~~~

Get a Panda Data Frame holding all the Spots Data and their actual Forecast:
~~~
spotsDF = Spots().get_pandaDF(source="RentepointDB")
~~~

Play with it 
~~~
spotsDF.head()
~~~

Print top 20 Spots sorted by best surf ratings
~~~
dates = spotsDF.columns[7:].tolist()
spotsDF.sort_values(dates,ascending=False).head(20)
~~~

Get top 20 Spots of a Portugal
~~~
portugal_spotsDF = spotsDF.loc[spotsDF["country"]=='pt']
portugal_spotsDF.sort_values(dates,ascending=False).head(20)
~~~

Get a list of all countries
~~~
spotsDF.country.unique()
~~~




## Detailed usage 
####Load Spot data 
Get a Spots() object which holds all reference data in a dict
~~~
s = Spots()
~~~
and therefrom get a pandas DataFrame with all spots. 
This Data Frame does not contain any forecast data yet.
It contains only the persistent spot data like name, location, region, etc.
~~~
spots_df = s.get_pandaDF()
~~~

#### Load Forecast data

Load forecast data from our spreadsheet
~~~
data_set = spread.get_data("RentepointDB")
~~~
and pass it to DataEngine to get it in a new separate Data Frame
~~~
ratings_df = DataEngine.get_pandaDF(data_set)
~~~

#### Compine Spot and Forecast data 

Merge them as following. Spots DF will now hold all Spot and Forecast Data
~~~
spotsDF = spots_df.merge(ratings_df, on='_id')
~~~




Links:
https://www.surfline.com/surfology/surfology_glossary_index.cfm
