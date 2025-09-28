import tkinter as tk

from tkintermapview import TkinterMapView as TMV
import requests



class Weather:
    def __init__(self):
        self.window=tk.Tk()
        self.window.title("погода")
        self.window.geometry("800x600")
        self.lat,self.lon=55.7536753,37.6208217
        self.API_KEY="859dca7ca2a5fc021784c5c473f376a4"
        self.info=None

        self.frame=tk.Frame(self.window,height=100)
        self.frame.pack(fill="x",padx=5,pady=5)

        self.label1=tk.Label(self.frame,text="Выберите город:",font=('Arial',14))
        self.label1.grid(row=0,column=0,padx=5,pady=5)

        self.entry=tk.Entry(self.frame,width=30,font=('Arial',14))
        self.entry.grid(row=0,column=1,padx=5,pady=5)

        self.button=tk.Button(self.frame,text="Поиск",font=('Arial',14),command=self.search_city)
        self.button.grid(row=0,column=2,padx=5,pady=5)

        self.label_info=tk.Label(self.frame,text="Информация о погоде",font=('Arial',14))
        self.label_info.grid(row=1,column=0,columnspan=3,padx=5,pady=5)

        self.map=TMV(self.window,width=800,height=600)
        self.map.pack(fill="both",expand=True,padx=5,pady=5)
        self.map.set_position(self.lat,self.lon)
        self.map.set_zoom(10)
        self.map.add_left_click_map_command(self.search_click)

    def search_city(self):
        city=self.entry.get()
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API_KEY}&units=metric&lang=ru"
            self.search(url)

    def search_click(self,coords):
        self.lat,self.lon=coords
        url = (f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.API_KEY}"
               f"&units=metric&lang=ru")
        self.search(url)



    def search(self,url):
        try:
            r = requests.get(url)
            data = r.json()
            print(data)
            self.info={
                "name": data["name"] if data["name"] else 'unknown',
                "temp": round(data["main"]["temp"]),
                "desc": data['weather'][0]["description"]
            }
            self.lat,self.lon=data["coord"]["lat"],data["coord"]["lon"]
            self.map.set_position(self.lat,self.lon)
            self.label_info.config(text=f"{self.info['name']}: {self.info['temp']} ℃, {self.info['desc']}")
        except:
            self.label_info.config(text="ошибка получения данных")

    def run(self):
        self.window.mainloop()


app=Weather()
app.run()
print("тестовая строка")