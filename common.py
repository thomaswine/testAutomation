
import functools
import inspect
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
from os.path import exists

class TestCommon():

    driver = None

    @classmethod
    def get_driver(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        return driver

class ellenorzes():
    def __init__(self, func_name, *args, **kwargs):
        if hasattr(self, func_name) and func_name != '__call__':
            self.func = getattr(self, func_name)
        self.driver = None
        self.test_func = None

    def __call__(self, *args, **kwargs):
        if inspect.ismethod(args[0]) or inspect.isfunction(args[0]):
            self.test_func = args[0]
            return self

        args_list = list(args)
        test_obj = args_list.pop(0)
        args = tuple(args_list)
        self.driver = test_obj.driver
        return self.func(test_obj, *args, **kwargs)

    def bejelentkezes(self, test_obj, *args, **kwargs):
        try:
            self.test_func(test_obj, *args, **kwargs)
        except Exception as e:
            print(e)

        no_exception = True
        try:
            WebDriverWait(self.driver, 1).until_not(EC.visibility_of_element_located((By.XPATH, "//strong[.='These credentials do not match our records.']")))
        except TimeoutException:
            print(" -- Rossz hitelesitok lettek megadva --")
            no_exception = False
        try:
            WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".page-header")))
        except TimeoutException:
            print(" -- Nem jelent meg a Dashboard --")
            no_exception = False

        if not no_exception:
            print(" -- Hibas Bejelentkezes teszt --\n")
        else:
            print(" -- Helyes Bejelentkezes teszt (1/5) -- \n")

    def navigalas_work_itemsre( self, test_obj, *args, **kwargs):
        try:
            self.test_func(test_obj, *args, **kwargs)
        except Exception as e:
            print(e)
        no_exception = True
        try:
            WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(.,'Work Items')]")))
        except TimeoutException:
            print(" -- A Work Items oldal nem jelent meg --")
            no_exception = False
        rows = self.driver.find_elements(By.TAG_NAME, 'tr')
        if len(rows) < 2:
            print(" -- Reset Data nem történt meg -- ")
            no_exception = False
        if not no_exception:
            print(" -- Hibas Navigalas teszt --\n")
        else:
            print(" -- Helyes Navigalas teszt (2/5) -- \n")

    def feladatlista_kigyujtes( self, test_obj, *args, **kwargs):
        try:
            self.test_func(test_obj, *args, **kwargs)
        except Exception as e:
            print(e)
        no_exception = True
        try:
            WebDriverWait(self.driver, 1).until_not(EC.visibility_of_element_located((By.XPATH, "//a[.='>']")))
        except TimeoutException:
            print(" -- Nem ert el a tablazat vegere --")
            no_exception = False
        
        if not len(test_obj.szurt_tablazat):
            print(" -- Nem kerult feltoltesre a 'szurt_tablazat' valtozo a kigyujtott ertekekkel -- ")
            no_exception = False

        if not no_exception:
            print(" -- Hibas Kigyujtes teszt --\n")
        else:
            print(" -- Helyes Kigyujtes teszt (3/5) -- \n")

    def fajlba_iras( self, test_obj, *args, **kwargs):
        try:
            self.test_func(test_obj, *args, **kwargs)
        except Exception as e:
            print(e)
        no_exception = True

        if exists(test_obj.filename):
            with open(test_obj.filename, 'r') as f:
                file = f.read()
                if len(test_obj.szurt_tablazat) != file.count(test_obj.tipus):
                    print(f" -- A kigyujtott es fajlba irt sorok szama nem egyezik; lista: {len(test_obj.szurt_tablazat)} db, fajl: {test_obj.tipus} db --")
                    no_exception = False
        else:
            print(f" -- Nem készült el a fajl {test_obj.filename} neven a futtato mappaban --")
            no_exception = False

        if not no_exception:
            print(" -- Hibas Fajlba iras teszt --\n")
        else:
            print(" -- Helyes Fajlba iras teszt (4/5) -- \n")

    def kijelentkezes( self, test_obj, *args, **kwargs):
        try:
            self.test_func(test_obj, *args, **kwargs)
        except Exception as e:
            print(e)
        no_exception = True

        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(.,'Login')]")))
        except TimeoutException:
            print(" -- Nem sikerult kijelentkezni --")
            no_exception = False

        if not no_exception:
            print(" -- Hibas Kijelentkezes teszt --\n")
        else:
            print(" -- Helyes Kijelentkezes teszt (5/5) -- \n")
        
    def __get__(self, instance, instancetype):
        return functools.partial(self.__call__, instance)
    

