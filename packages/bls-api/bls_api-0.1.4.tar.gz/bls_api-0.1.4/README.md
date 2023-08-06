# BLS_API PACKAGE
## Introduction:
    - This package is design to get aggregated data from Bureau Labor of Statistics
    rather than specifying the Series Id.
    - The package already have the series scraped and defined.
## Installation:
### Pip:
You can use pip to install this package
```bash
pip install bls_api
```
## Usage:
### Labor Force data:
Let's first interact with Labor Force data in BLS
```python
from bls_api import labor_force

### Initiate the instance
instance=labor_force()
### if you have the token from BLS you can set it up if not it is not the problem.
instance.token="<Your Token>"

"""
Let's assume we have 2 series LAUMT531338000000006 and LAUMT531338000000005
We want to get data from these 2 series.
These series belongs to labor_force_participation_data
Let's these 2 series to the instance
"""
custom_series=instance.add_custom_series(["LAUMT531338000000006","LAUMT531338000000005"])

### add_custom_series returns a series_object class
### Now we can set the _from and _to to this object class
custom_series._from=2017
custom_series._to=2018
### now we can loop through the custom series to get the data:
### This will return 3 types series_data, catalog, and data type
for series_data,catalog,type_ in custom_series:
    print(series_data)
    print(catalog)
    print(type_)
"""
Output
{'year': '2019', 'period': 'M12', 'value': '118566', 'periodName': 'December'}
{'series_id': 'LAUMT531338000000006', 'series_title': 'Labor Force: Bellingham, WA Metropolitan Statistical Area (U)', 'seasonality': 'Not Seasonally Adjusted', 'survey_name': 'Local Area Unemployment Statistics', 'survey_abbreviation': 'LA', 'measure_data_type': 'l
abor force', 'area': 'Bellingham, WA Metropolitan Statistical Area', 'area_type': 'Metropolitan areas'}
{'data_type': None}
{'year': '2019', 'period': 'M11', 'value': '118456', 'periodName': 'November'}
{'series_id': 'LAUMT531338000000006', 'series_title': 'Labor Force: Bellingham, WA Metropolitan Statistical Area (U)', 'seasonality': 'Not Seasonally Adjusted', 'survey_name': 'Local Area Unemployment Statistics', 'survey_abbreviation': 'LA', 'measure_data_type': 'l
abor force', 'area': 'Bellingham, WA Metropolitan Statistical Area', 'area_type': 'Metropolitan areas'}
{'data_type': None}
{'year': '2019', 'period': 'M10', 'value': '117918', 'periodName': 'October'}
{'series_id': 'LAUMT531338000000006', 'series_title': 'Labor Force: Bellingham, WA Metropolitan Statistical Area (U)', 'seasonality': 'Not Seasonally Adjusted', 'survey_name': 'Local Area Unemployment Statistics', 'survey_abbreviation': 'LA', 'measure_data_type': 'l
abor force', 'area': 'Bellingham, WA Metropolitan Statistical Area', 'area_type': 'Metropolitan areas'}
{'data_type': None}
{'year': '2019', 'period': 'M09', 'value': '115242', 'periodName': 'September'}
{'series_id': 'LAUMT531338000000006', 'series_title': 'Labor Force: Bellingham, WA Metropolitan Statistical Area (U)', 'seasonality': 'Not Seasonally Adjusted', 'survey_name': 'Local Area Unemployment Statistics', 'survey_abbreviation': 'LA', 'measure_data_type': 'l
abor force', 'area': 'Bellingham, WA Metropolitan Statistical Area', 'area_type': 'Metropolitan areas'}
{'data_type': None}
{'year': '2019', 'period': 'M08', 'value': '115526', 'periodName': 'August'}
{'series_id': 'LAUMT531338000000006', 'series_title': 'Labor Force: Bellingham, WA Metropolitan Statistical Area (U)', 'seasonality': 'Not Seasonally Adjusted', 'survey_name': 'Local Area Unemployment Statistics', 'survey_abbreviation': 'LA', 'measure_data_type': 'l
abor force', 'area': 'Bellingham, WA Metropolitan Statistical Area', 'area_type': 'Metropolitan areas'}
{'data_type': None}
{'year': '2019', 'period': 'M07', 'value': '116541', 'periodName': 'July'}
{'series_id': 'LAUMT531338000000006', 'series_title': 'Labor Force: Bellingham, WA Metropolitan Statistical Area (U)', 'seasonality': 'Not Seasonally Adjusted', 'survey_name': 'Local Area Unemployment Statistics', 'survey_abbreviation': 'LA', 'measure_data_type': 'l
abor force', 'area': 'Bellingham, WA Metropolitan Statistical Area', 'area_type': 'Metropolitan areas'}
{'data_type': None}
{'year': '2019', 'period': 'M06', 'value': '116374', 'periodName': 'June'}
{'series_id': 'LAUMT531338000000006', 'series_title': 'Labor Force: Bellingham, WA Metropolitan Statistical Area (U)', 'seasonality': 'Not Seasonally Adjusted', 'survey_name': 'Local Area Unemployment Statistics', 'survey_abbreviation': 'LA', 'measure_data_type': 'l
abor force', 'area': 'Bellingham, WA Metropolitan Statistical Area', 'area_type': 'Metropolitan areas'}
{'data_type': None}
{'year': '2019', 'period': 'M05', 'value': '115558', 'periodName': 'May'}
{'series_id': 'LAUMT531338000000006', 'series_title': 'Labor Force: Bellingham, WA Metropolitan Statistical Area (U)', 'seasonality': 'Not Seasonally Adjusted', 'survey_name': 'Local Area Unemployment Statistics', 'survey_abbreviation': 'LA', 'measure_data_type': 'l
abor force', 'area': 'Bellingham, WA Metropolitan Statistical Area', 'area_type': 'Metropolitan areas'}
{'data_type': None}
"""

### If you  want to get all the available series in Labor_Force
all_series=instance.add_all_series()
all_series._from=2017
all_series._to=2018

for series_data,catalog,type_ in all_series:
    print(series_data)
    print(catalog)
    print(type_)


```
## License 
MIT License

Copyright (c) 2022 Tien Nguyen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
