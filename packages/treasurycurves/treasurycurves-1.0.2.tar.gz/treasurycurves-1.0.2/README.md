# Treasury Curve Data

Using the Developer API found at [treasury.gov](https://home.treasury.gov/developer-notice-xml-changes),
one can find yield curves dating back to the 90's.

&nbsp;

# Selecting and plotting data

Access data for a particular date using ``` curves("2022-08-08") ```.
curves will find the nearest valid date (weekday) and returns a pandas dataframes of all curves
available on that date or nearest to it. calling ``` curves() ``` will use the current date.
Optionally specify ``` curves(allow_missing=True) ``` to keep years with missing data.

Alternatively, you can retrieve all data by calling ``` download() ```.

Once you have the data, it is possible to plot out the yield curves with
``` plot(curves_data, start="2022-01-01", end="2022-05-03", num_years=1) ```.
Specify the number of years, or pick a start and end date to sample from, as the chart would otherwise
become inundated with yield curve data.

Save your data in a spreadsheet using ``` export(curves_data, file_extension="csv") ``` and specify
"csv" or "xlsx" to determine the file type.

&nbsp;

# Using treasurycurves module from the Command Line
```
$ python treasury.py --help
usage: treasury.py [-h] [-a] [-s START] [-e END] [-d DATE] [-y YEARS] [-p] [-o OUTPUT]

treasurycurves - query and analyze US Treasury yield data

optional arguments:
  -h, --help            show this help message and exit
  -a, --allowna         Allow NaN values
  -s START, --start START
                        Year to start analysis
  -e END, --end END     Year to end analysis
  -d DATE, --date DATE  Date in YYYY-MM-DD to analyze
  -y YEARS, --years YEARS
                        Num years before end to analyze
  -p, --plot            Plot yield curves
  -o OUTPUT, --output OUTPUT
                        File extension to save data (csv or xlsx), leave empty to avoid saving file
```

&nbsp;
