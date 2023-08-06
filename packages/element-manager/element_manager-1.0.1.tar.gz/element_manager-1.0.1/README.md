### Installation
```sh
pip install element-manager
```

### Import
```sh
from element_manager import get_xpath
```


### Example
Below script searches given keyword on google & scrapes result count
```sh
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from element_manager import get_xpath

driver = webdriver.Chrome("chromedriver.exe")

# Open URL
driver.get('https://www.google.com/')

xpath=get_xpath(driver,'QYQyyPtidm5_xqG')
driver.find_element_by_xpath(xpath).click()

# Type in search bar
driver.switch_to.active_element.send_keys('shoes\n')

# Advanced method to scrape result count
xpath=get_xpath(driver,'z6XMV66vxokYpfn')
result_count=driver.find_element_by_xpath(xpath).text
print('result_count ',result_count)
driver.quit()

```


### Contact Us
* [Telegram](https://t.me/datakund)