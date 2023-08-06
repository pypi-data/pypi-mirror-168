# JKDownload
Collect information about your favorite anime from the jkanime.net website.

![](https://img.shields.io/static/v1?label=python&message=3.9%20|%203.10&color=informational&style=plastic&logo=python)
![](https://img.shields.io/static/v1?label=selenium&message=4.4&color=informational&style=plastic&logo=selenium)
[![](https://img.shields.io/static/v1?label=pypi%20package&message=v0.0.2&color=%2334D058&style=plastic&logo=pypi)](https://pypi.org/project/jkdownload/)
![](https://img.shields.io/static/v1?label=test&message=pending&color=yellow&style=plastic)


## Description
This module makes use of the Selenium library for python to collect information of your favorite anime, such as anime name, description, number of episodes, year of broadcast, and it does have a download option.

## Installation
You must have Chrome or Chromium browser installed. You must also install the browser driver that will communicate with Selenium. In this case you must download `chromedriver`, as indicated in the [official documentation](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/).

If you are a Linux user of the Ubuntu-Debian family, you can install the driver directly from the repositories as follows:

```console
$ sudo apt install chromium-chromedriver
```

Finally to install this module, create a python virtual environment, either with venv or conda, and run the following:

```console
$ python -m pip install jkdownload
```

You are now ready to use jkdownload module.