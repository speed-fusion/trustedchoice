import json
import time
from playwright_driver import PlaywrightDriver


driver = PlaywrightDriver()

driver.start()


states = [
        'ny',
        'me',
        'ma',
        'ct',
        'pa',
        'nj',
        'md',
        'de',
        'va',
        'nc',
        'sc',
        'ga',
        'fl',
        'dc',
        'nh',
        'ri',
        'vt'
        ]

base_url = "https://www.trustedchoice.com/agent/"

try:
    data = []
    
    for code in states:
        driver.page.goto(f'https://www.trustedchoice.com/agent/{code}/')
    
        for i in range(0,5):
            driver.page.press("body","Space")
            time.sleep(1)
        
        soup = driver.get_soup()
        
        for link in soup.find_all("a"):
            url = link.get("href")
            if url == None:
                continue
            if not  f'/agent/{code}' in url:
                continue
            name = link.text
            tmp = {
                "city_url":url,
                "city_name":name,
                "state_code":code,
                "state_url":f'https://www.trustedchoice.com/agent/{code}/',
            }
            print(tmp)
            data.append(tmp)
            
        print(f'total : {len(data)}')
    
    with open("trustedchoice.json","w") as f:
        f.write(json.dumps(data))
        
except Exception as e:
    print(f'error : {str(e)}')

driver.stop()