from pytube import YouTube # interaction with YouTube
from pytube.cli import on_progress # built in progress bar.
import argparse # for argument parsing

"""
Sample usage
FILE LOCATION MATTERS!!!

python extractmedia.py <youtube_link>

-u --> https://stackoverflow.com/questions/14258500/python-significance-of-u-option

webm works fine

"""

class YouTube_DL:
    def __init__(self):
        self.args = self.parse_arguments()
        self.url = YouTube(self.args.link, on_progress_callback = on_progress)
        self.filtered_streams_selection = []

    # Parse arguments
    def parse_arguments(self):
        """
        Parses arguments

        <param> url : a YouTube object
        ---
        <Dict> arg: Mapping of each arg to it's value
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('link', type=str, help="Must include YouTube link") # required arg
        parser.add_argument('--list', '-l', action="store_true", help="Lists all streams for this YouTube video.") # optional arg
        parser.add_argument('--withvideo', '-wv', action="store_true", help="Specifies to download any stream with video. Starts at 720p then looks for 480p.") # optional arg
        # Note Progressive only starts at 720p. We need a Stream with both the audio and video. Read more into it here: https://pytube.io/en/latest/user/streams.html#dash-vs-progressive-streams
        parser.add_argument('--format', '-f', type=str, help="Format for either audio or video you input then downloads it.") # optional arg

        args = parser.parse_args()  
        return args
    
    def process_video(self):
        # Only 1 action that can be taken
        if self.args.list:
            self.list_streams()
            return
        
        # Handle video selection
        if self.args.withvideo:
            # Filters for only streams with video
            self.filtered_streams_selection = self.get_list_of_streams_with_video()
        elif self.args.format != None:
            self.filtered_streams_selection = self.get_specific_formatted_videos()
        else:
            # Default option  
            # Results in black screen
            self.filtered_streams_selection = self.url.streams.filter(mime_type="audio/mp4").desc()
        
        self.download_process()
    
    def list_streams(self):
        """
        Prints all the streams on a separate line for a given url in descending order.

        <param> url : a YouTube object
        ---
        <None> 
        """
        print(f"Here are the available streams for '{self.url.title}'...")
        audio_stream = self.url.streams.desc()
        for stream in audio_stream:
            print(stream)
        print("====================================")

    ## Utility Functions ##
    # Get File size
    def get_file_size(self, stream):
        """
        Returns approx file size of a specific stream in MB.

        <param> stream : Stream Object
        """
        return stream.filesize_approx / 10**6

    # Start the download process
    def download_process(self):
        if (len(self.filtered_streams_selection) > 0):
            print("Downloading... ", self.filtered_streams_selection[0])
            self.download_stream(self.filtered_streams_selection[0])
        else:
            print("There were no streams found for your current arguments. Unable to download. Try running... 'python youtube_dl.py " + self.args.link + " -l' to take a look at the available streams for this video.")

    # Download a specifc stream
    def download_stream(self, stream):
        """
        Downloads a specific stream to the specified folder.

        <param> stream: Stream Object
        """
        # Get file size
        print(f"The approx file size is: {self.get_file_size(stream)} mb")
        # Download
        print("Downloading...")
        stream.download()
        print(f"Your video: '{self.url.title}' has downloaded. 🎉")
    
    # Filters list of streams only if they contain mp4 videos
    def get_list_of_streams_with_video(self):
        """
        Returns a list of streams that contain video

        <param> stream: Stream Object
        """
        list_of_videos_mp4 = self.url.streams.filter(mime_type="video/mp4", progressive="True").desc()
        # Only mp4 because... 
        return list_of_videos_mp4

    # Filters for specific formatted video
    def get_specific_formatted_videos(self):
        # Get specific video resolution
        if "0p" in self.args.format:
            return self.url.streams.filter(mime_type="video/mp4", res=self.args.format, progressive="True").desc()
        # Get specific audio resolution
        elif "kbps" in self.args.format:
            return self.url.streams.filter(mime_type="audio/mp4", abr=self.args.format).desc()

youtube_dl = YouTube_DL()
youtube_dl.process_video()