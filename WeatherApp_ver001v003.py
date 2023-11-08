
from tkinter import *
import requests, json

root = Tk()
root.title("Weather App")
root.geometry("430x60")

my_label = Label(root, text="", font=("Helvetica", 14))
my_label.grid(row=1, column=0, columnspan=2)

# crearte zipcode lookup function
def zipLookup():
    
    # clear any existing label & colour before making the api call
    my_label.config(text="", bg=my_label.master.cget('bg'))
    
    # weather api urls: (used multiple zipcodes for testing of different air quality conditions)
    # https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=20002&distance=25&API_KEY=DACC23C2-B201-466A-8637-5C414E43DA8D
    # https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=98362&distance=25&API_KEY=DACC23C2-B201-466A-8637-5C414E43DA8D

    # weather app output (reference)
    # [{"DateObserved":"2023-10-30","HourObserved":5,"LocalTimeZone":"EST","ReportingArea":"Metropolitan Washington","StateCode":"DC","Latitude":38.919,"Longitude":-77.013,"ParameterName":"O3","AQI":6,"Category":{"Number":1,"Name":"Good"}},{"DateObserved":"2023-10-30","HourObserved":5,"LocalTimeZone":"EST","ReportingArea":"Metropolitan Washington","StateCode":"DC","Latitude":38.919,"Longitude":-77.013,"ParameterName":"PM2.5","AQI":33,"Category":{"Number":1,"Name":"Good"}},{"DateObserved":"2023-10-30","HourObserved":5,"LocalTimeZone":"EST","ReportingArea":"Metropolitan Washington","StateCode":"DC","Latitude":38.919,"Longitude":-77.013,"ParameterName":"PM10","AQI":11,"Category":{"Number":1,"Name":"Good"}}]

    try:
        # get the info from the url... we concatenate the given zipcode into the url
        api_req = requests.get("https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=" + zip.get() + "&distance=25&API_KEY=DACC23C2-B201-466A-8637-5C414E43DA8D")
        api = json.loads(api_req.content) # parse / strip out of json and make it usable by python

        # here we are querying the api data - with any api call we need to drill down into the actual data we want to return
        # in this case the api consists of a list of dictionaries; we only care about the 0th dictionary as this contails the ozone data
        # if we wanted pollen (PM) info, we would amend the api list references below
        city = api[0]['ReportingArea']
        print(city)
        category = api[0]['Category']['Name']
        print(category)
        quality = api[0]['AQI']
        print(quality)

        if category == "Good":
            weather_colour = "#00E400"
        elif category == "Moderate":
            weather_colour = "#FFFF00"
        elif category == "Unhealthy for Sensitive Groups":
            weather_colour = "#ff9900"
        elif category == "Unhealthy":
            weather_colour = "#FF0000"
        elif category == "Very Unhealthy":
            weather_colour = "#990066"
        elif category == "Hazardous":
            weather_colour = "#660000"
        #print(weather_colour)

        # re-print the label
        my_label.config(text=city + ': Air Quality = ' + category + ' / ' + str(quality), font=("Helvetica", 14), background=weather_colour)
        my_label.grid(row=1, column=0, columnspan=2)
        root.configure(background=weather_colour)

    except Exception as e:
        api = "error..."


# user zipcode entry
zip = Entry(root)
zip.grid(row=0, column=0, sticky=W+E+N+S)

zipButton = Button(root, text="Lookup Zipcode", command=zipLookup)
zipButton.grid(row=0, column=1, sticky=W+E+N+S)

root.mainloop()