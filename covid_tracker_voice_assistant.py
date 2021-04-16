'''COVID-19 tracker and Voice assistant 
This script allows the user to get all the details of the COVID-19 using a voice interface.
The script updates the database on a auditory update command and respond to a plethora of voice commands. 
The response of the requests is given in a auditory fashion 

The scripts has some dependecies which have been clearly mentioned in the file requirements.txt of the repository 

Author : Srinjoy Bhuiya 
'''
#The necessary libraries are imported 
import  requests
import json
import speech_recognition as sr
import re
import pyttsx3
import threading 
import time

#parsehub API details
API_KEY="to6kYDpbCSVM"
PROJECT_TOKEN="tYMnxnFOCcEX"
RUN_TOKEN="txmvqfs6M1Wa"



class Data:
    """
        Handles all the API calls and searches through the JSON API result to retrun the appropiate value requested.
        Has functions which search and return the:
            1.Total Active Cases on that day.
            2.Total Deaths in a day.
            3.Total Recoveries in a day.
            4.Total mild cases active .
            5.Total serious cases active.
            6.Total cases in a a particular country.
        Also defines a function which creates a thread and keeps polling the thread untill it get some updated data from the API   

        ...

        Attributes
        ----------
        api_key : str
            an API KEY used to call the parsehub API .
               
        project_token : str
            a project token sued to call the parsehub API .
                 
        params : dict
            a dictionary of the parameters required for the API call .
               

        Methods
        -------
        get_data()
            Calls the parsehub API and retruns the most recent data stored in the API.
        
        get_total_cases()
            returns the value of the total coronavirus cases in the world.

        get_total_recovered()
            returns the value of the total recovered cases in the world

        get_total_death()
            returns the total number of deaths in the world due to coranavirus         

        get_country_data()
            retruns the number of cases in a particular country

        get_list_country_data()
            retruns a list of countries affected with the coranavirus
            
        
    """
    
    def __init__(self,api_key,project_token):
        """
        Attributes
        ----------
        api_key : str
            an API KEY used to call the parsehub API .

        project_token : str
            a project token sued to call the parsehub API .
                
        params : dict
            a dictionary of the parameters required for the API call .
               
        """
        self.api_key=api_key
        self.project_token=project_token
        self.params={
            "api_key":self.api_key
        }
        
        self.data=self.get_data()
        
    def get_data(self):
        """
        Fetches the data from the parsehub API
        ...

        Attributes
        ----------
        none
        
        Raises
        -------
        none
        
        Returns
        -------
        
        The data which is fetched by the API call 
        """
        
        response=requests.get(f"https://parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data",params={"api_key":API_KEY})    
        data=json.loads(response.text)
        return data
    def get_total_cases(self):
        """
        The total number of coronavirus cases in the world
        ...

        Attributes
        ----------
        none

        Raises
        -------
        
        none
        
        Returns
        -------
        The value of the total coronavirus cases in the world 
        """
        data= self.data['total']
        for content in data:
            if content['name']=="Coronavirus Cases:":
                return content['value']
        
        
        return "0"
    def get_total_deaths(self):
        """
        The total number of coronavirus releated deaths in the world
        ...

        Attributes
        ----------
        none

        Raises
        -------
        none 
        
        Returns
        -------
        The value of the total coronavirus deaths in the world 
        """
        data= self.data['total']
        for content in data:
            if content['name']=="Deaths:":
                return content['value']
        
        
        return "0"
    def get_total_recovered(self):
        """
        The total number patients recovered from coronavirus in thw world
        ...

        Attributes
        ----------
        none

        Raises
        -------
        none 
        Returns
        -------
        The value of total number patients recovered from coronavirus in thw world
        """
        data= self.data['total']
        for content in data:
            if content['name']=="Recovered:":
                return content['value']
        
        
        return "0"
    
    
    def get_country_data(self,country):
        """
        The total number of coronavirus cases in thw world
        ...

        Attributes
        ----------
        country: str
            the country whoses data we are requesting 

        Raises
        -------
        none 
        
        Returns
        -------
        The value of the total coronavirus cases in a particular country   
        """
        data=self.data['Country']
        
        for content in data:
            if content['name'].lower()==country.lower():
                return content          
        
        
        return "0"
    def get_list_country_data(self):
        """
        generates a list of the countries which have been affected by the cornavirus pandemic 
        ...

        Attributes
        ----------
        none

        Raises
        -------
        none
        
        Returns
        -------
        a list of all the countries which have been affected by the coronavirus pandemic   
        """
        countries=[]
        for country in self.data['Country']:
               countries.append(country['name'].lower())
        return countries            

    def update_data(self):
        """
        Updates the data generated in the API call wit hthe most recent data avaliable 
        ...

        Attributes
        ----------
        
        none

        Raises
        -------
        
        none
        
        Returns
        -------
        
        none
        
        """
        response=requests.post(f"https://parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run",params=self.params)
        
        
        # Creates a thread and keep polling it untill we get updated data
        def poll():
            time.sleep(0.1)
            old_data=self.data
            while True:
                new_data=self.get_data()
                if new_data!= old_data:
                    self.data=new_data
                    print("Data Updated")   
                    break
                time.sleep(5)
                
                
        t=threading.Thread(target=poll)
        t.start()

    
    
def speak(text):
    """
        Initialises the speech to text module 
        ...

        Attributes
        ----------
        
        none

        Raises
        -------
        
        none
        
        Returns
        -------
        
        none
        
        """
    engine=pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    """
        Initialises the speech API of the system to record the voice of the user 
        ...

        Attributes
        ----------
        
        none

        Raises
        -------
        
        none
        
        Returns
        -------
            the spoken text as a string 
        """
    r=sr.Recognizer()
    with sr.Microphone() as source:
        audio=r.listen(source)
        said=""
        
        try:
            said =r.recognize_google(audio)
            
        except Exception as e:
            print("Exception:",str(e))
    return(said.lower())           

def main():
    """
        The main Funtion which handles the running of the program
        ...

        Attributes
        ----------
        none

        Raises
        -------
        none
        
        Returns
        -------
        none
        
        """
        
    #Start of the program
    
    print("Started Program")
    
    #Define  the end phrase
    END_PHRASE="stop"
    
    data=Data(API_KEY,PROJECT_TOKEN)
    country_list=data.get_list_country_data()
    
    UPDATE_COMMAND={"update",
                    "update_data"
                    }
    TOTAL_PATTERNS={
                    re.compile("[\w\s]+ total [\w\s]+ cases"):data.get_total_cases,
                    re.compile("[\w\s]+ total cases"):data.get_total_cases,
                    re.compile("[\w\s]+ total [\w\s]+ deaths"):data.get_total_deaths,
                    re.compile("[\w\s]+ total deaths"):data.get_total_deaths,
                    re.compile("[\w\s]+ total [\w\s]+ death"):data.get_total_deaths,
                    re.compile("[\w\s]+ total death"):data.get_total_deaths
                }
    
    COUNTRY_PATTERNS={
                    re.compile("[\w\s]+ cases [\w\s]"): lambda country: data.get_country_data(country)['total_cases'],
                    re.compile("[\w\s]+ deaths [\w\s]"): lambda country: data.get_country_data(country)['total_deaths'],
                    re.compile("[\w\s]+ death [\w\s]"): lambda country: data.get_country_data(country)['total_deaths']
                    
                }
    
    while True:
        print("Listening")
        text=get_audio()
        print(text)
        result=None
        
        for pattern,func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words=set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result= func(country)
                        break
            
        for pattern,func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result= func()
                break
        
        if text in UPDATE_COMMAND:
            data.update_data()
            result="Data Updating. This may take a moment"
            speak(result)
            
        if result:
            speak(result)    

        if(text.find(END_PHRASE)!=-1):
            print("Exit")
            break
        
#Calling main         
main()        