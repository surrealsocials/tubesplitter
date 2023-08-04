from tkinter import Tk,Label,PhotoImage

class LoadingScreen:
    def __init__(self):
        self.root = Tk()
        self.root.overrideredirect(True)  # Hide title bar and borders
        self.root.attributes('-topmost', True)  # Keep the window on top
        self.loading_image = PhotoImage(file="images/LOADING2.png")  # Replace with your image file path
        self.loading_image = self.loading_image.subsample(2)  # Adjust subsample factor as needed
        self.label = Label(self.root, image=self.loading_image)
        self.label.pack()
        self.center_window()
        self.root.after(4000, self.close_loading_screen)  # Close after 3000ms (3 seconds)

    def center_window(self):
        self.root.update_idletasks()
        width = self.loading_image.width()
        height = self.loading_image.height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def close_loading_screen(self):
        self.root.destroy()

def run():
    loading_app = LoadingScreen()
    loading_app.root.mainloop()

run()

