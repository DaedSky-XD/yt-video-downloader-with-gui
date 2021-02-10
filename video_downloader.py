from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from pytube import YouTube
from pytube import Playlist
from kivy.uix.screenmanager import Screen

video_url_code = """
MDTextField:
    hint_text: "Enter video url"
    helper_text: "or enter the playlist url"
    helper_text_mode: "on_focus"
    icon_right: "language-python"
    icon_right_color: app.theme_cls.primary_color
    pos_hint: {'center_x': 0.5, 'center_y':0.5}
    size_hint_x:None
    width:300
"""


class YoutubeDownloader(MDApp):
    def build(self):
        # setting up theme
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"

        screen = MDScreen()

        # loading the above code for text field
        self.url = Builder.load_string(video_url_code)
        screen.add_widget(self.url)

        # adding download button
        download_button = MDRectangleFlatButton(text="Download",
                                                pos_hint={'center_x': 0.5, 'center_y': 0.4},
                                                on_press=self.download)
        screen.add_widget(download_button)
        return screen

    # download button function
    def download(self, obj):

        # if the url is blank
        if self.url.text == "":
            close_btn = MDRectangleFlatButton(text='close', on_press=self.close_dialog)

            self.downloading_message = MDDialog(title="bhosdike",
                                                text="a madarchod yt video ka url daalna",
                                                size_hint=(0.7, 1),
                                                buttons=[close_btn])
            self.downloading_message.open()

        # if the url is youtube video url
        elif self.url.text.startswith('https://youtu.be/'):
            audio_btn = MDRectangleFlatButton(text="audio", on_press=self.download_audio)
            video_btn = MDRectangleFlatButton(text="video", on_press=self.download_video)
            close_btn = MDRectangleFlatButton(text="close", on_press=self.close_dialog)

            self.downloading_message = MDDialog(title="Choice",
                                                text=f"what do you want to download?",
                                                size_hint=(0.7, 1),
                                                buttons=[audio_btn, video_btn, close_btn])
            self.downloading_message.open()

        # if the url is a playlist url of youtube
        elif self.url.text.startswith("https://youtube.com/playlist?list="):
            audio_btn = MDRectangleFlatButton(text="audio", on_press=self.download_audio_playlist)
            video_btn = MDRectangleFlatButton(text="video", on_press=self.download_video_playlist)
            close_btn = MDRectangleFlatButton(text="close", on_press=self.close_dialog)

            self.downloading_message = MDDialog(title="Choice",
                                                text=f"what do you want to download?",
                                                size_hint=(0.7, 1),
                                                buttons=[audio_btn, video_btn, close_btn])
            self.downloading_message.open()

        # if the url is not from youtube
        else:
            close_btn = MDRectangleFlatButton(text="close", on_press=self.close_dialog)
            self.downloading_message = MDDialog(title="Invalid url",
                                                text="abe laude, please enter a valid yt video url",
                                                size_hint=(0.7, 1),
                                                buttons=[close_btn])
            self.downloading_message.open()

    # closing the dialogue with close button
    def close_dialog(self, obj):
        self.downloading_message.dismiss()

    # video downloader function of video button
    def download_video(self, obj):
        url = self.url.text
        self.yt = YouTube(url)
        self.downloading_message.dismiss()

        self.downloading_message = MDDialog(title="Downloading...",
                                            text=f"Downloading.. {self.yt.title}")
        self.downloading_message.open()

        self.yt.streams.filter(progressive=True).get_highest_resolution().download(r"c:\video_downloader/videos")
        self.downloading_message.dismiss()

        download_location = r"c:\video_downloader/videos"
        close_btn = MDRectangleFlatButton(text="close", on_press=self.close_dialog)

        self.downloading_message = MDDialog(title="Download completed",
                                            text=f"successfully downloaded {self.yt.title} at {download_location}",
                                            buttons=[close_btn])
        self.downloading_message.open()

    # audio downloader button of audio button
    def download_audio(self, obj):
        url = self.url.text
        self.yt = YouTube(url)
        self.downloading_message.dismiss()

        self.downloading_message = MDDialog(title="Downloading...",
                                            text=f"Downloading.. {self.yt.title}")
        self.downloading_message.open()

        self.yt.streams.get_audio_only(subtype="mp4").download(r"c:\video_downloader/audios")
        self.downloading_message.dismiss()

        download_location = r"c:\video_downloader/audios"
        close_btn = MDRectangleFlatButton(text="close", on_press=self.close_dialog)

        self.downloading_message = MDDialog(title="Download completed",
                                            text=f"successfully downloaded {self.yt.title} at {download_location}",
                                            buttons=[close_btn])
        self.downloading_message.open()

    # video playlist downloader for video button
    def download_video_playlist(self, obj):
        url = self.url.text
        self.pl = Playlist(url)
        self.downloading_message.dismiss()

        self.downloading_message = MDDialog(title="Downloading...",
                                            text=f"Downloading.. {self.pl.title}")
        self.downloading_message.open()

        for vids in self.pl.videos:
            vids.streams.filter(progressive=True).get_highest_resolution().download(
                r"c:\video_downloader/videos/playlists/" + self.pl.title)

        self.downloading_message.dismiss()

        download_location = r"c:\video_downloader/videos/playlists/" + self.pl.title
        close_btn = MDRectangleFlatButton(text="close", on_press=self.close_dialog)

        self.downloading_message = MDDialog(title="Download completed",
                                            text=f"successfully downloaded {self.pl.title} at {download_location}",
                                            buttons=[close_btn])
        self.downloading_message.open()

    # audio playlist downloader for audio button
    def download_audio_playlist(self, obj):
        url = self.url.text
        self.pl = Playlist(url)
        self.downloading_message.dismiss()

        self.downloading_message = MDDialog(title="Downloading...",
                                            text=f"Downloading.. {self.pl.title}")
        self.downloading_message.open()

        for songs in self.pl.videos:
            songs.streams.get_audio_only(subtype="mp4").download(
                r"c:\video_downloader/audios/playlists/" + self.pl.title)

        self.downloading_message.dismiss()

        download_location = r"c:\video_downloader/audios/playlists/" + self.pl.title
        close_btn = MDRectangleFlatButton(text="close", on_press=self.close_dialog)

        self.downloading_message = MDDialog(title="Download completed",
                                            text=f"successfully downloaded {self.pl.title} at {download_location}",
                                            buttons=[close_btn])
        self.downloading_message.open()


# running the mainloop
YoutubeDownloader().run()
