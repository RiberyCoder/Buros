try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    base_path = tmp_global_obj["basepath"]
    web = GetGlobals("web")
    chromedriver = os.path.join(base_path, os.path.normpath(r"drivers\win\chrome"), "chromedriver.exe")
    chrome_options = Options()
    # this is the preference we're passing
    prefs = {'profile.default_content_setting_values.automatic_downloads': 1,"download.default_directory": r"{rutaPadre}descargas"}
    chrome_options.add_experimental_option("prefs", prefs)
    web.driver_list[web.driver_actual_id] = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver)
except Exception as e:
    PrintException()
    raise e