from common import *
from pageObject import *
import os


class BCATesting:

    def __init__(self):
        self.driver = TestCommon.get_driver()
        self.loginPage = Login(self.driver)
        self.navigationPage = Navigation(self.driver)
        self.szurt_tablazat = []
        self.filename = "result.txt"
        self.tipus = "WI4"

    @ellenorzes('bejelentkezes')
    def bejelentkezes(self, email, password):
        self.navigationPage.openPage()
        
        act_title = self.driver.title
        assert act_title == "ACME System 1 - Log In", "Error - Wrong Title Name"
        
        self.loginPage.setEmail(email)
        self.loginPage.setPassword(password)
        self.loginPage.clickLogin()
        
        act_title = self.driver.title
        assert act_title == "ACME System 1 - Dashboard", "Error - Wrong Title Name"

    @ellenorzes('navigalas_work_itemsre')
    def navigalas_work_itemsre( self ):
        self.navigationPage.navigationToWorkItem()
        
        act_title = self.driver.title
        assert act_title == "ACME System 1 - Work Items", "Error - Wrong Title Name"

    @ellenorzes('feladatlista_kigyujtes')
    def feladatlista_kigyujtes(self):
        pages = self.driver.find_elements_by_class_name("page-numbers")
        page_count = len(pages)-1
            
        for number in range(2, page_count):
            
            table = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/table")
            rows = table.find_elements_by_tag_name("tr")
        
            for row in rows:
                self.szurt_tablazat.append(row.text)
        
            element = self.driver.find_element_by_xpath(f"//*[text()='{str(number)}']")
            element.click()
    
    @ellenorzes('fajlba_iras')
    def fajlba_iras(self):
        self.testList = []
        
        with open(self.filename, "w") as file:
            for element in self.szurt_tablazat:
                if self.tipus in element:
                    file.write(str(element) + '\n')
                    self.testList.append(element)
        
        self.szurt_tablazat = self.testList

    @ellenorzes('kijelentkezes')
    def kijelentkezes(self):  
        self.loginPage.clickLogout()
        
        act_title = self.driver.title
        assert act_title == "ACME System 1 - Log In", "Error - Wrong Title Name"

    def teszt_ellenorzes(self):
        assert len(self.szurt_tablazat) > 13, "The number of WI4 elements are not greather than 13."

    def run(self):
        self.bejelentkezes("email", "password")
        self.navigalas_work_itemsre()
        self.feladatlista_kigyujtes()
        self.fajlba_iras()
        self.kijelentkezes()
        self.teszt_ellenorzes()

BCATesting().run()
