import os
import shutil
import time
from moviepy.editor import TextClip, AudioFileClip, VideoFileClip, CompositeVideoClip


class MakeSubtitle():
    """该工具用来给视频添加字幕

    Returns:
        MakeSubtitle: 对象
    """

    def __init__(self, video:str,fps:int=5) -> None:
        """该工具用来给视频添加字幕

        Args:
            video (str): 源视频
            fps (int, optional): 输出视频fps. Defaults to 5.
        """
        self.__temp_dir_name = 'temp'
        self.__cwd=os.getcwd()
        self.__temp_dir = self.__make_temp_dir()
        self.__src_video_path = video
        self.__video = VideoFileClip(self.__src_video_path)
        self.__width,self.__height,self.__duration=self.__get_propertes()
        self.__subtitle_list = list()
        #渲染设置
        self.__fps=fps
        self.__threads=16
        # 字幕设置
        self.__dispaly_intermission_time=0.2
        if os.name=="nt":
            self.__font = 'SimHei'
        else:
            self.__font = 'CESI黑体-GB13000'
        self.__font_size = 70
        self.__align = 'center'
        self.__color = 'red'
        self.__bg_color = 'gray85'
        self.__position_y =0.7
    
    def __get_propertes(self):
        video=self.__video
        width=video.w
        height=video.h
        duration=video.duration
        return width,height,duration

    def __make_temp_dir(self):
        cwd = self.__cwd
        temp_path = os.path.join(cwd, self.__temp_dir_name)
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        os.makedirs(temp_path)
        return temp_path

    def __mixing(self, text) -> AudioFileClip:
        import pyttsx3
        # from pydub import AudioSegment
        engine = pyttsx3.init()
        engine.setProperty("voice","zh")
        t=str(time.time()).replace(".", "")
        name_by_aiff="{}{}".format(t,".aiff")
        # name_by_mp3="{}{}".format(t,".mp3")
        file_name_by_aiff = os.path.join(self.__temp_dir,name_by_aiff)
        # file_name_by_mp3=os.path.join(self.__temp_dir,name_by_mp3)
        engine.save_to_file(text, file_name_by_aiff)
        engine.runAndWait()
        if not os.path.exists(file_name_by_aiff):
            time.sleep(1)
        # AudioSegment.from_file(file_name_by_aiff).export(file_name_by_mp3,format="mp3")
        return AudioFileClip(file_name_by_aiff)

    def add_subtitle(self, subtitle:str, start: int, end: int, mixing:bool=True):
        """添加单句字幕
        Args:
            subtitle (str): 要添加的字幕
            start (int): 添加到视频的开始时间
            end (int): 添加到视频的结束时间
            mixing (bool, optional): 是否配音. Defaults to True.
        """
        clip = TextClip(subtitle,
                        fontsize=self.__font_size,
                        font=self.__font,
                        align=self.__align,
                        color=self.__color,
                        bg_color=self.__bg_color)
        position_x=0.5-(float(clip.w)/float(self.__width))*0.5
        clip = clip.set_position((position_x,self.__position_y), relative=True)
        clip = clip.set_start(start)
        duration=end-start
        if duration>self.__dispaly_intermission_time*2:
            duration=duration-self.__dispaly_intermission_time
        clip = clip.set_duration(duration)
        self.__subtitle_list.append((clip, subtitle,start,mixing))

    def add_subtitles(self, subtitles: list, start: list, end:int=None, mixing:bool=True):
        """添加多句字幕

        Args:
            subtitles (list): 要添加的字幕集合
            start (list): 每条字幕在视频中出现的时间
            end (int, optional): 最后一条字幕消失的时间，默认不设置是视频结束. Defaults to None.
            mixing (bool, optional): 是否配音. Defaults to True.
        """
        if end == None:
            end = self.__duration
        start.append(end)
        for s, subtitle in enumerate(subtitles):
            self.add_subtitle(subtitle, start[s], start[s+1], mixing)

    def export_to_file(self, file_path:str):
        """导出到文件
        Args:
            file_path (str): 文件路径
        """
        video = self.__video
        clip = list()
        for subtitle_clip, subtitle, start,mixing in self.__subtitle_list:
            if mixing:
                audio_clip = self.__mixing(subtitle)
                audio_clip=audio_clip.set_start(start)
                subtitle_clip = subtitle_clip.set_audio(audio_clip)
            clip.append(subtitle_clip)
        video = CompositeVideoClip([video, *clip])
        video.write_videofile(file_path,threads=self.__threads,preset='ultrafast',fps=self.__fps, audio_codec="aac")

class SubtitleFactary():
    
    interface=None
    
    def __init__(self) -> None:
        self.__video_path=None
        self.__start_time=None
        self.__end_time=None
        self.__subtitles=list()
        self.__time=list()
        
    
    @classmethod
    def create(cls,init=True):
        """创建一个字幕工厂实例

        Args:
            init (bool, optional): 是否初始化. Defaults to True.
        """
        cls.instance=SubtitleFactary()
        if init:
            cls.instance.start()
        
    @classmethod
    def get_instance(cls):
        """取到当前字幕工厂实例

        Returns:
            SubtitleFactary: 字幕工厂实例
        """
        if not hasattr(cls,"instance"):
            cls.create()
        instance:SubtitleFactary=cls.instance
        return instance
    
    @classmethod
    def make(cls,src_movie:str,dst_movie:str,offset:int=0,mixing:bool=True,fps:int=5):
        """合成字幕

        Args:
            src_movie (str): 源视频
            dst_movie (str): 合成视频路径
            offset (int, optional): 整体字幕时间偏移量. Defaults to 0.
            mixing (bool, optional): 是否配音. Defaults to True.
            fps (int, optional): 输出视频fps. Defaults to 5.

        Raises:
            Exception: Exception("未初始化工厂")
        """
        if not hasattr(cls,"instance"):
            raise Exception("未初始化工厂")
        t=list()
        for _i in cls.instance.time:
            _t=_i-cls.instance.start_time
            t.append(int(_t)+offset)
        make_subtitle = MakeSubtitle(src_movie,fps=fps)
        make_subtitle.add_subtitles(cls.instance.subtitles, t,mixing=mixing)
        make_subtitle.export_to_file(dst_movie)
                
    @property
    def video(self):
        return self.__video_path
    
    @video.setter
    def video(self,video):
        self.__video_path=video
        
    @property
    def start_time(self):
        return self.__start_time
    
    @property
    def end_time(self):
        return self.__end_time
    
    @property
    def time(self):
        return self.__time
    
    @property
    def subtitles(self):
        return self.__subtitles
        
    def start(self):
        self.__start_time=time.time()
    
        
    def subtitle(self,text:str,offset:int=0):
        """增加一条字幕

        Args:
            text (str): 要增加的字幕
            offset (int, optional): 需要增加的偏移量，正数代表延后，负数代表提前. Defaults to 0.
        """
        self.__subtitles.append(text)
        self.__time.append(time.time()+offset)
        
        
    