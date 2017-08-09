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
Imports
~~~
from rentepoint import Spots, DataEngine, spread
~~~
Get a Spots() object which holds all reference data in a dict
~~~
s = rentepoint.Spots()
~~~
and therefrom get a pandas DataFrame with all spots
~~~
spots_df = s.get_pandaDF()
~~~

Load forecast data from our spreadsheet
~~~
data_set = spread.get_data("RentepointDB")
~~~
and pass it to DataEngine to get it in a  panda frame back
~~~
ratings_df = DataEngine.get_pandaDF(data_set)
~~~

Merge them
~~~
spotsDF = spots_df.merge(ratings_df, on='_id')
~~~

Play with it 

~~~
spotsDF.head()
~~~

Links:
https://www.surfline.com/surfology/surfology_glossary_index.cfm
