# robotframework-openweathermap

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![CodeQL](https://github.com/joergschultzelutter/robotframework-openweathermap/actions/workflows/codeql.yml/badge.svg)](https://github.com/joergschultzelutter/robotframework-openweathermap/actions/workflows/codeql.yml) [![PyPi version](https://img.shields.io/pypi/v/robotframework-openweathermap.svg)](https://pypi.python.org/pypi/robotframework-openweathermap)

```robotframework-openweathermap``` is a [Robot Framework](https://www.robotframework.org) keyword collection for the [OpenWeatherMap](https://www.openweathermap.org/api) API.

## Installation

The easiest way is to install this package is from pypi:

    pip install robotframework-openweathermap

## Robot Framework Library Examples

Prerequisites:

The accompanying Robot Framework [test file](https://github.com/joergschultzelutter/robotframework-openweathermap/blob/master/tests/keyword_checks.robot) relies on two requirements: 

- [get an OpenWeatherMap API key](https://home.openweathermap.org/users/sign_up) (it's free)
- create an environment variable ```OWM_API_KEY``` and assign the OpenWeatherMap API key to that variable
- Execute test with ``robot keyword_checks.robot``

## Library usage and supported keywords

### Default settings 

The following rules apply:

- The default value for each parameter is ```None```
- Each parameter supports ```Getter``` and ```Setter``` keywords, e.g, ```Set OpenWeatherMap Latitude```
- Each OpenWeatherMap Keyword also permits the usage of these parameters. Example:

```robot
Get Current Weather   latitude=....
```
- A keyword's parameter value has priority over the ```Setter``` value. This means that if you use ```Set OpenWeathermap Latitude  10``` and ```Get Current Weather  latitude=20```, the value from the OWK Keyword will supersede the ``Setter`` keyword and a value of ```20``` is going to be used.  

### Options for setting the parameter values

You can either specify all parameters during the initial setup of the library or alternatively via separate keywords

#### Option 1 - set as position parameters

```robot
*** Settings ***

Library  OpenWeatherMapLibrary  51.82798  9.4455  ...

*** Test Cases ***
My first test case
```

#### Option 2 - set as named parameters

```robot
*** Settings ***

Library  OpenWeatherMapLibrary  latitude=51.82798  longitude=9.4455  ...

*** Test Cases ***
My first test case
```

#### Option 3 - Use Robot Keywords
```robot
Set OpenWeatherMap Latitude   latitude=51.82798
```

### Generic Getter / Setter Robot Keywords supported by this library

You can use these optional Getter/Setter methods for setting your fixed default values. If you specify the same parameter as part of the actual OpenWeatherMap keyword, the value specified with that API call supersedes these generic Getter/Setter values.


| Keyword                                          | Description                                                                                                                                                           | Arguments         | Valid Values                                                                             |
|--------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|------------------------------------------------------------------------------------------|
| ``Get``/``Set OpenWeatherMap Latitude``          | Gets / Sets the latitude value                                                                                                                                        | ``latitude``      | float value                                                                              |
| ``Get``/``Set OpenWeatherMap Longitude``         | Gets / Sets the longitude value                                                                                                                                       | ``longitude``     | float value                                                                              |
| ``Get``/``Set OpenWeatherMap API Key``           | Gets / Sets the OWM API Key                                                                                                                                           | ``apikey``        | string                                                                                   |
| ``Get``/``Set OpenWeatherMap Number Of Results`` | Gets / Sets the max number of results                                                                                                                                 | ``number``        | integer > 0                                                                              |
| ``Get``/``Set OpenWeatherMap Language``          | Gets / Sets the desired output language                                                                                                                               | ``language``      | see [OpenWeatherMap API](https://openweathermap.org/current#multi)<br />for valid values |
| ``Get``/``Set OpenWeatherMap Excludes``          | Gets / Sets the exclude(s) value.<br /> Separarate multiple values with a comma<br />See [API documentation](https://openweathermap.org/api/one-call-api) for details | ``exclude``       | ``current``<br />``minutely``<br />``hourly``<br />``daily``<br />``alerts``             |
| ``Get``/``Set OpenWeatherMap Output Format``     | Gets / Sets the output format (e.g. ``json``)                                                                                                                         | ``output_format`` | ``json``<br />``xml``<br />``html``                                                      |
| ``Get``/``Set OpenWeatherMap Unit Format``       | Gets / Sets the unit format<br />See [API Documentation](https://openweathermap.org/api/one-call-api#data) for details<br />Format availability depends on API call   | ``unit_format``   | ``standard``<br />``metric``<br >``imperial``                                            |
| ``Get``/``Set OpenWeatherMap Datetime Start``    | Gets / Sets the start datetime for date ranges                                                                                                                        | ``dt_start``      | Unix timestamp                                                                           |
| ``Get``/``Set OpenWeatherMap Datetime End``      | Gets / Sets the end datetime for date ranges                                                                                                                          | ``dt_end``        | Unix timestamp                                                                           |
| ``Get``/``Set OpenWeatherMap Datetime``          | Gets / Sets a single point in time                                                                                                                                    | ``dt``            | Unix Timestamp                                                                           |

## OpenWeatherMap Keywords

Please note that a majority of these keywords requires a paid OpenWeatherMap subscription. You can still try to run the keywords but most of them will fail with a http 4xx error unless you have a valid paid subscription.

Each of the following keywords has a set of mandatory parameters. which means that if you used the setter methods to assign values for ``latitude`` and ``longitude``, for example, you can omit those values for the following keywords. 

| Keyword | Description | Mandatory<br />parameters | Optional<br />parameters | Comments                              |
| ------- | ----------- | -------------------- | ------------------- |---------------------------------------|
| [Get Current Weather](https://openweathermap.org/current) | Access current weather data for any location on<br />Earth including over 200,000 cities | ``latitude``<br />``longitude``<br />``apikey``|``output_format``<br />``unit_format``<br />``language`` |                                       | 
| [Get Hourly Forecast 4 Days](https://openweathermap.org/api/hourly-forecast) | Hourly forecast for 4 days (96 timestamps) | ``latitude``<br />``longitude``<br />``apikey``|``output_format``<br />``number``<br />``language`` | no ``output_format``<br />support for HTML |
| [Get OneCall Forecast](https://openweathermap.org/api/one-call-api) | Current and forecast weather data | ``latitude``<br />``longitude``<br />``apikey``|``exclude``<br />``unit_format``<br />``language`` |                                       |
| [Get Daily Forecasts 16 Days](https://openweathermap.org/forecast16) | Daily Forecast 16 Days is available at any location on the globe. | ``latitude``<br />``longitude``<br />``apikey``|``number``<br />``unit_format``<br />``output_format``<br />``language`` | no ``output_format``<br />support for HTML |
| [Get Climatic Forecasts 30 Days](https://openweathermap.org/forecast30) | Climate Forecast 30 Days allows you to request daily weather data for the next 30 days | ``latitude``<br />``longitude``<br />``apikey``|``number``<br />``unit_format``<br />``output_format``<br />``language`` | no ``output_format``<br />support for HTML |
| [Get Current Solar Radiation](https://openweathermap.org/api/solar-radiation) | Current solar radiation data | ``latitude``<br />``longitude``<br />``apikey``| |                                       |
| [Get Solar Radiation Forecast](https://openweathermap.org/api/solar-radiation) | Forecast solar radiation data | ``latitude``<br />``longitude``<br />``apikey``| |                                       |
| [Get Solar Radiation History](https://openweathermap.org/api/solar-radiation) | Historical solar radiation data<br />for a from-to time span | ``latitude``<br />``longitude``<br />``apikey``<br />``dt_start``<br />``dt_end``| |                                       |
| [Get 5 Day 3 Hour Forecast](https://openweathermap.org/forecast5) | 5 day forecast is available at any location on the globe | ``latitude``<br />``longitude``<br />``apikey``|``number``<br />``unit_format``<br />``output_format``<br />``language`` | no ``output_format``<br />support for HTML |
| [Get Current Air Pollution Radiation](https://openweathermap.org/api/air-pollution) | Current air pollution data | ``latitude``<br />``longitude``<br />``apikey``| |                                       |
| [Get Air Pollution Forecast](https://openweathermap.org/api/air-pollution) | Air pollution data forecast | ``latitude``<br />``longitude``<br />``apikey``| |                                       |
| [Get Air Pollution History](https://openweathermap.org/api/air-pollution) | Historical Air Pollution data<br />for a from-to time span | ``latitude``<br />``longitude``<br />``apikey``<br />``dt_start``<br />``dt_end``| |                                       |
| [Get Road Risk Data](https://openweathermap.org/api/road-risk) | Road Risk API provides weather data<br />and national alerts at the point of<br />destination and along a route | ``latitude``<br />``longitude``<br />``apikey``<br />``dt``| |                                       |


## Known issues

- Not all OpenWeatherMap APIs have been assigned with corresponding Robot Framework keywords. What you see is what you get - at least for this version.
- The ``Get Road Risk Data`` keyword only supports a single set of ``latitude`` and ``longitude`` values (the underlying API supports multiple sets)

