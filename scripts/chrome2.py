try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import json
    descargas=GetVar ('descargas')
    base_path = tmp_global_obj["basepath"]
    web = GetGlobals("web")
    chromedriver = os.path.join(base_path, os.path.normpath(r"drivers\win\chrome"), "chromedriver.exe")
    chrome_options = webdriver.ChromeOptions()
    settings = {
       "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }
    # this is the preference we're passing
    prefs = {'profile.default_content_setting_values.automatic_downloads': 1,"download.default_directory": descargas,'savefile.default_directory': descargas,'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--kiosk-printing')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--dns-prefetch-disable')
    web.driver_list[web.driver_actual_id] = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver)
    
    web.driver_list[web.driver_actual_id].get("http://apps.supernet.bo/IC/Autentication.aspx")
    #driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver)
    #driver.get("http://apps.supernet.bo/IC/Autentication.aspx")
    #driver.execute_script('window.print();')
    #driver.quit()
except Exception as e:
    PrintException()
    raise e