import subprocess
import os
result = subprocess.Popen("python splash.py")
import customtkinter
from Toolz import vlc
import Toolz.main as videotool
import tkinter as tk
import math,time
from tkinter import PhotoImage,messagebox
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class MyApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        if not os.path.exists('content'):os.mkdir('content')
        if not os.path.exists('compas'):os.mkdir('compas')
        self.file1,self.file2,self.file3,self.file4='','','',''
        self.directory='content'

        # configure window
        self.title("TupeSplitter")
        self.attributes('-topmost', True)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.center_window()

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="TUBE-SPLITTER",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=5, pady=(5, 5))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Url")
        self.entry.grid(row=3, column=1, padx=(0, 0), pady=(5, 5),sticky='ew')

        self.main_button_1 = customtkinter.CTkButton(master=self,text="Download",command=self.downloadvideo, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=2, padx=(20, 20), pady=(6, 6), sticky="n")
        self.add_compas_button = customtkinter.CTkButton(master=self,text="Add Compas",command=self.downloadvideo, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.add_compas_button.grid(row=3, column=2, padx=(20, 20), pady=(6, 6), sticky="s")

        self.finish_button = customtkinter.CTkButton(master=self,width=150,text="Close",command=self.finish, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.finish_button.grid(row=3,columnspan=2, column=3, padx=(20, 40), pady=(20, 20), sticky="e")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self.sidebar_frame, width=200,height=700)
        self.tabview.grid(row=1,rowspan=3,column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
        self.tabview.add("Videos")
        self.tabview.add("Compas")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(5):
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()

        # create checkbox and switch frame
        checkbox_value1 = tk.BooleanVar()
        checkbox_value2 = tk.BooleanVar()
        checkbox_value3 = tk.BooleanVar()
        checkbox_value4 = tk.BooleanVar()
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=0,column=4, padx=(20, 20), pady=(40, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,variable=checkbox_value1)
        self.checkbox_1.configure(command=self.onguitarcheck,text="Guitar")
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="nw")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,variable=checkbox_value2)
        self.checkbox_2.configure(command=self.onvocalscheck,text="Vocals")
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="nw")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,variable=checkbox_value3)
        self.checkbox_3.configure(command=self.ondrumscheck,text="Drums")
        self.checkbox_3.grid(row=3, column=0, pady=(20, 0), padx=20, sticky="nw")
        self.checkbox_4 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame,variable=checkbox_value4)
        self.checkbox_4.configure(command=self.onbasscheck,text="Bass")
        self.checkbox_4.grid(row=4, column=0, pady=(20, 0), padx=20, sticky="nw")
        self.checkbox_1.select()
        self.checkbox_2.select()
        self.checkbox_3.select()
        self.checkbox_4.select()

        # play button
        self.play_button = customtkinter.CTkButton(master=self.checkbox_slider_frame,text="Play",command=self.playvid, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.play_button.grid(row=5, column=0, padx=(20, 20), pady=(20, 5), sticky="SW")
        self.stop_button = customtkinter.CTkButton(master=self.checkbox_slider_frame,text="Stop",command=self.stopvid, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.stop_button.grid(row=6, column=0, padx=(20, 20), pady=(5, 5), sticky="SW")

        # open youtube button
        self.tube_button = customtkinter.CTkButton(master=self.checkbox_slider_frame,text="youtube",command=self.openyoutube, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.tube_button.grid(row=8, column=0, padx=(20, 20), pady=(5, 5), sticky="SW")

        self.text_box = customtkinter.CTkTextbox(master=self.checkbox_slider_frame,height=300,width=170)
        self.text_box.grid(row=9,column=0, padx=(10, 10), pady=(10, 10), sticky="NESW")

        # Create a VLC player instance and load the video file
        self.instance = vlc.Instance("--no-xlib")
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new("rainbow.jpg")
        self.player.set_media(self.media)
        
        # Create the listbox widget
        self.listbox = tk.Listbox(self.tabview.tab("Videos"), width=30,height=50,bg='#333', fg='white', bd=0, highlightthickness=0, font=('Helvetica', 12), selectbackground='#111', selectforeground='white', borderwidth=0, highlightcolor='#333')
        self.listbox.grid(row=0,column=0,sticky="ns", padx=5, pady=10)

        self.compaslist = tk.Listbox(self.tabview.tab("Compas"),width=30, height=50,bg='#333', fg='white', bd=0, highlightthickness=0, font=('Helvetica', 12), selectbackground='#111', selectforeground='white', borderwidth=0, highlightcolor='#333')
        self.compaslist.grid(row=0,column=0,sticky="ns", padx=5, pady=10)

        # Update the listbox with the folder names
        self.update_listbox(self.directory)

        # Get the handle to the Tkinter window
        self.window_handle = self.winfo_id()

        # Create a VLC instance and player
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()

        # Set the VLC player to use the handle of the Tkinter window as its parent
        self.player.set_hwnd(self.window_handle)

        # Create a frame to hold the video
        self.video_frame = tk.Frame()
        self.video_frame.grid(row=0, column=1,columnspan=2,sticky="NSEW")
        self.video_frame.configure(bg="black",padx=5, pady=10)

        self.image = PhotoImage(file="images/logo3.png")  # Replace "your_image.png" with your actual image file path
        self.video_label = tk.Label(self.video_frame,image=self.image,bg="#111")
        self.video_label.grid(row=0, column=0, sticky="news")
        
        self.video_frame.grid_rowconfigure(0, weight=1)
        self.video_frame.grid_columnconfigure(0, weight=1)

        # Get the handle to the label widget
        self.video_handle = self.video_label.winfo_id()

        # Set the VLC player to use the handle of the label widget as its parent
        self.player.set_hwnd(self.video_handle)
        self.player.play()    

        self.listbox.bind('<<ListboxSelect>>', self.saveselected)
        self.compaslist.bind('<<ListboxSelect>>', self.saveselected)
    
        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self.video_frame, fg_color="transparent",height=40)
        self.slider_progressbar_frame.grid(row=2, column=0, padx=(10, 10), pady=(0, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(0, weight=1)

        self.volume = customtkinter.CTkSlider(self,from_=0, to=100, number_of_steps=100, orientation="vertical")
        self.volume.grid(row=0, column=3, rowspan=1, padx=(10, 10), pady=(500, 10), sticky="s")
        self.volume.set(100)

        self.scan = customtkinter.CTkSlider(self.video_frame,from_=0, to=100, number_of_steps=100,height=20)
        self.scan.grid(row=2, column=0,columnspan=2, padx=(10, 10), pady=(0,0 ), sticky="ew")
        self.scan.bind("<ButtonRelease-1>", self.settrackpos)
        self.volume.configure(command=self.setvolume)
        self.scan.set(0.1)

        self.mainvid_button = customtkinter.CTkButton(master=self.checkbox_slider_frame,text="Main Mute",command=self.player.audio_toggle_mute, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.mainvid_button.grid(row=7, column=0, padx=(20, 20), pady=(5, 5), sticky="SW")

        self.attributes('-topmost', False)

    def finish(self):
        self.destroy()
        exit()

    def center_window(self):
        self.update_idletasks()  # Update widget dimensions
        width = 2100
        height = 1180
        x = (self.winfo_screenwidth() // 2) - (width // 3)
        y = (self.winfo_screenheight() // 2) - (height // 3)
        self.wm_geometry(f'{width}x{height}+{x}+{y}')

    # Define a function to get the list of folder names in a directory
    def get_folder_names(self, directory):
        folder_names = []
        for item in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, item)):
                folder_names.append(item)
        return folder_names

    # Define a function to update the listbox with folder names
    def update_listbox(self, directory):
        folder_names = self.get_folder_names(directory)
        self.listbox.delete(0, tk.END)
        for i,folder_name in enumerate(folder_names):
            self.listbox.insert(tk.END, folder_name)
        folder_names = self.get_folder_names("./compas")
        self.compaslist.delete(0, tk.END)
        for i,folder_name in enumerate(folder_names):
            self.compaslist.insert(tk.END, folder_name)

    def swap_audio(self,aud,newvideoname):
        # load the video and audio files
        video = VideoFileClip(f"{self.folder_path}/video.mp4")
        new_audio = AudioFileClip(aud)

        # replace the video's audio with the new audio
        new_video = video.set_audio(new_audio)

        # save the new video file
        new_video.write_videofile(f"{self.folder_path}/{newvideoname}.mp4")

    def play_video(self):
        self.my_media.stop()
        audio_directory=self.splits_folder_path
        selected_audio = self.files_listbox.get(tk.ACTIVE)
        selected_audio_path = os.path.join(audio_directory, f'{self.selected_folder}/{selected_audio}')
        print(selected_audio_path)

        newvideoname = simpledialog.askstring("Input", "name file without extension",
                                parent=self.master)

        self.swap_audio(selected_audio_path,newvideoname)
        
        try:
            self.my_media = vlc.MediaPlayer(f"{self.folder_path}/{newvideoname}.mp4")
            self.my_media.play()
        except:pass

    def openyoutube(self):
        os.system('start Firefox https://www.youtube.com/results?search_query=flamenco')


# Define a new class that inherits from MyApp
class MyCustomApp(MyApp):

    def __init__(self):
        super().__init__()
        self.current=videotool.Tube()
        print(self.file2)
        print(self.current.title)

    def settrackpos(self,event):
        self.pos = self.scan.get()
        self.player.set_position(self.pos / 100.0)
        self.current.pguitar.set_position(self.pos / 100.0)
        self.current.pdrums.set_position(self.pos / 100.0)
        self.current.pvocals.set_position(self.pos / 100.0)
        self.current.pbass.set_position(self.pos / 100.0)
        self.current.pvideo.set_position(self.pos / 100.0)

    def setvolume(self,event):
        
        self.vol = int(math.ceil(event))
        print(self.vol)
        self.player.audio_set_volume(self.vol)
        self.current.pguitar.audio_set_volume(self.vol)
        self.current.pdrums.audio_set_volume(self.vol)
        self.current.pvocals.audio_set_volume(self.vol)
        self.current.pbass.audio_set_volume(self.vol)
        self.current.pvideo.audio_set_volume(self.vol)

    def loadfromtitle(self,title):
        self.current.title=title
        self.current.loadfromtitle(self.current.title)

    def getvideo(self):
        self.current.url =self.entry.get()
        self.current.getaudio()

    def onguitarcheck(self):
        if self.checkbox_1.get():
            print("Checkbox is checked")
            if self.current.pguitar.is_playing():
                self.current.togglemute("guitar")
                print("guitar is now playing")    
            else:
                print("guitar is playing")             
        else:
            if self.current.pguitar.is_playing():
                self.current.togglemute("guitar")
                print("guitar is now not playing")
            else:
                print("Checkbox is unchecked")

    def onvocalscheck(self):
        if self.checkbox_2.get():
            print("Checkbox is checked")
            if self.current.pvocals.is_playing():
                self.current.togglemute("vocals")
                print("vocals is now playing")    
            else:
                print("vocals is playing")
                
        else:
            if self.current.pvocals.is_playing():
                self.current.togglemute("vocals")
                print("vocals is now not playing")
            else:
                print("Checkbox is unchecked")

    def ondrumscheck(self):
        if self.checkbox_3.get():
            print("Checkbox is checked")
            if self.current.pdrums.is_playing():
                self.current.togglemute("drums")
                print("drums is now playing")    
            else:
                print("drums is playing")
                
        else:
            if self.current.pdrums.is_playing():
                self.current.togglemute("drums")
                print("drums is now not playing")
            else:
                print("Checkbox is unchecked")

    def onbasscheck(self):
        if self.checkbox_4.get():
            print("Checkbox is checked")
            if self.current.pbass.is_playing():
                self.current.togglemute("bass")
                print("bass is now playing")    
            else:
                print("bass is playing")
                
        else:
            if self.current.pbass.is_playing():
                self.current.togglemute("bass")
                print("bass is now not playing")
            else:
                print("Checkbox is unchecked")     
            
    def saveselected(self,event):
        self.current.title=self.listbox.get(self.listbox.curselection())
        print(self.current.title)

    def playvid(self):
        self.checkbox_1.select()
        self.checkbox_2.select()
        self.checkbox_3.select()
        self.checkbox_4.select()
        if self.player.is_playing():
            self.stopvid()

        self.current.loadfromtitle()     
        self.media=self.instance.media_new(self.current.video)
        self.player.set_media(self.media)
        self.player.play()
        self.player.audio_toggle_mute()
        try:
            self.current.play_video()
            self.player.audio_toggle_mute()
        except:
            pass

        print(self.player.audio_get_mute())
        time.sleep(1)
        self.scan.set(1)
        time.sleep(1)
        if int(self.player.audio_get_mute())==0:
            self.player.audio_toggle_mute()

    def stopvid(self):
        self.player.stop()
        self.current.stop_video()

    def update_textbox(self, message):
        #self.video_label.config(image= PhotoImage(file="loading.gif"))
        self.text_box.insert(tk.END, message + '\n')
        self.text_box.see(tk.END)
        self.update_idletasks() 

    def downloadvideo(self):
        import requests
        self.update_textbox("Starting download...")
        if self.player.is_playing():
            self.stopvid()
        self.current.url=self.entry.get()
        self.current.getaudio()
        self.update_textbox(f"title: {self.current.title}")
        self.update_textbox('Getting Audio/Video')
        self.current.getvideo()
        self.update_textbox('Content Downloaded')
        self.update_textbox("Splitting Audio...\nThis will take a minute..")
        self.current.split()
        self.update_textbox("Done!")
        self.update_listbox(self.directory)


if __name__ == "__main__":

    # Create an instance of the custom app class
    my_app = MyCustomApp()

    # Start the main event loop
    my_app.mainloop()

