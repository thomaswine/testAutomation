from selenium.webdriver.common.by import By

class Login:
    
    def __init__(self,driver):
        self.driver=driver
        self.textbox_email_id = "email"
        self.textbox_password_id = "password"
        self.login_button = "/html/body/div[1]/div[2]/div/div/div/form/button"
        self.logout_button = '//*[@id="bs-example-navbar-collapse-1"]/ul/li[3]/a'
    
    def setEmail(self, email):
        self.driver.find_element(By.ID, self.textbox_email_id).clear()
        self.driver.find_element(By.ID, self.textbox_email_id).send_keys(email)
    
    def setPassword(self, password):
        self.driver.find_element(By.ID, self.textbox_password_id).clear()
        self.driver.find_element(By.ID, self.textbox_password_id).send_keys(password)
        
    def clickLogin(self):
        self.driver.find_element(By.XPATH, self.login_button).click()
    
    def clickLogout(self):
        self.driver.find_element(By.XPATH, self.logout_button).click()

class Navigation:
     
    def __init__(self,driver):
        self.driver=driver
        self.workItemBtn = '//*[@id="dashmenu"]/div[2]/a/button'
        self.url = "https://acme-test.uipath.com/login"
        
    def navigationToWorkItem(self):
        self.driver.find_element(By.XPATH, self.workItemBtn).click()
    
    def openPage(self):
        self.driver.get(self.url)


