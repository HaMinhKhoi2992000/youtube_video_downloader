import customtkinter
import tkinter
import tkinter.messagebox
import customtkinter
from tkinter.filedialog import askdirectory
from youtubeDowloader import YoutubeDownloader

customtkinter.set_appearance_mode("dark")
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Youtube Video Downloader Tool")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1), weight=0)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        #self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        #self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        #***
        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Youtube link go here")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.getLinkButton = customtkinter.CTkButton(master=self, command=lambda: self.getYoutubeLink(self.entry.get()), fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Get")
        self.getLinkButton.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create Thumbnail image label
        self.thumbnail_image_label = customtkinter.CTkLabel(self, height=400, width=600, text='Thumbnail Image')
        self.thumbnail_image_label.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Download")

        self.tabview.tab("Download").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        #self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)


        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Download"), text="Download Video",                                       command=self.open_file_chooser_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkScrollableFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")


        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def delete_radiobutton_group(self, radioButtons):
        for button in radioButtons:
            button.destroy()

    def setRadioButtons(self, listResolution, listvideoType):


        for widget in self.radiobutton_frame.winfo_children():
            widget.destroy()

        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Resolutions:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        for i in range(len(listResolution)):
            self.radio_button = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var,
                                                               value=i, text=listResolution[i] + " " + listvideoType[i])
            self.radio_button.grid(row=i+1, column=2, pady=10, padx=20, sticky="n")
            #App.holder.append(self.radio_button)


    def getYoutubeLink(self, url):
        resolutions, mimetypes, videos = YoutubeDownloader.sort_resolutions(url)
        print(resolutions, mimetypes)
        self.setRadioButtons(resolutions, mimetypes)
        self.setThumbnail()

    def setThumbnail(self):
        if YoutubeDownloader.thumbnail_img:
            self.thumbnail_image_label.configure(self, text=YoutubeDownloader.video_title, height=400, width=600, image=YoutubeDownloader.thumbnail_img, compound = "top")

    def open_file_chooser_event(self,):
        print(self.radio_var.get())
        path = askdirectory(title='Select Download Folder')
        YoutubeDownloader.download(self.radio_var.get(), YoutubeDownloader.videos, path)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def combine_to_dictionary(keyList, valueList):
        res = {}
        for key in keyList:
            for value in valueList:
                res[key] = value
                valueList.remove(value)
                break


if __name__ == "__main__":
    app = App()
    app.mainloop()