import os
import shutil
import time
from tkinter.messagebox import NO
from moviepy.editor import TextClip, AudioFileClip, VideoFileClip, CompositeVideoClip


class MakeSubtitle():
    """该工具用来给视频添加字幕

    Returns:
        MakeSubtitle: 对象
    """

    def __init__(self, video: str, fps: int = 5, width=480, threads=8, tts="pyttsx3", inf: dict = None) -> None:
        """该工具用来给视频添加字幕

        Args:
            video (str): 源视频
            fps (int, optional): 输出视频fps. Defaults to 5.
            width (int, optional): 输出视频宽度. Defaults to 480.
            threads (int, optional): 输出视频渲染用线程数. Defaults to 8.
            tts (str, optional): 使用tts种类,可选有pyttsx3和baidu。 Defaults to pyttsx3.
            info (dict, optional): 当使用baidu tts时,需要填入的信息
                {
                    "app_id":"",
                    "api_key":"",
                    "secret_key":"",
                    "spd":5, #语速,0-9
                    "pit":5, #语调,0-9
                    "vol":5, #音量,0-15 
                    "per":5118 #发音人
                }
        """
        # 临时存储目录名称
        self.__temp_dir_name = 'temp'
        # 取得当前的执行目录
        self.__cwd = os.getcwd()
        # 建立当前临时存储目录
        self.__temp_dir = self.__make_temp_dir()
        # 源视频
        self.__src_video_path = video
        # 读取源视频
        self.__src_video = None
        self.__src_video_width = None
        self.__src_video_height = None
        self.__src_duration = None
        # 取得源视频属性
        self.__get_propertes()
        # 字幕列表
        self.__subtitle_list = list()
        # 渲染设置
        self.__render_fps = fps
        self.__render_threads = threads
        self.__render_preset = "ultrafast"
        self.__render_width = width
        # 字幕设置
        self.__subtitle_dispaly_intermission_time = 0.2
        if os.name == "nt":
            self.__subtitle_font = 'SimHei'
        else:
            self.__subtitle_font = 'CESI黑体-GB13000'
        self.__subtitle_font_size = 70
        self.__subtitle_align = 'center'
        self.__subtitle_color = 'red'
        self.__subtitle_bg_color = 'gray85'
        self.__subtitle_position_y = 0.7
        # 文字转语音设置
        self.__tts_type = tts
        self.__tts_inf = inf

    def __get_propertes(self):
        self.__src_video = VideoFileClip(self.__src_video_path)
        self.__src_video_width = self.__src_video.w
        self.__src_video_height = self.__src_video.h
        self.__src_duration = self.__src_video.duration

    def __make_temp_dir(self):
        cwd = self.__cwd
        temp_path = os.path.join(cwd, self.__temp_dir_name)
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        os.makedirs(temp_path)
        return temp_path

    def __mixing_by_pyttsx3(self, text) -> AudioFileClip:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("voice", "zh")
        t = str(time.time()).replace(".", "")
        name_by_aiff = "{}{}".format(t, ".aiff")
        file_name_by_aiff = os.path.join(self.__temp_dir, name_by_aiff)
        engine.save_to_file(text, file_name_by_aiff)
        engine.runAndWait()
        if not os.path.exists(file_name_by_aiff):
            time.sleep(1)
        return AudioFileClip(file_name_by_aiff)

    def __mixing_by_baidu(self, text) -> AudioFileClip:
        from aip import AipSpeech
        # {
        #             "app_id":"",
        #             "api_key":"",
        #             "secret_key":"",
        #             "spd":5, #语速,0-9
        #             "pit":5, #语调,0-9
        #             "vol":5, #音量,0-15
        #             "per":5118 #发音人
        #  }
        if self.__tts_inf is None:
            raise Exception("使用tts:baidu时,必须传入相关接入信息")
        inf = self.__tts_inf
        app_id = inf.get("app_id")
        api_key = inf.get("api_key")
        secret_key = inf.get("secret_key")
        if app_id == None or api_key == None or secret_key == None:
            raise Exception("使用tts:baidu时,必须传入app_id,api_key,secret_key信息")
        spd = 5 if inf.get("spd") == None else inf.get("spd")
        pit = 5 if inf.get("pit") == None else inf.get("pit")
        vol = 5 if inf.get("vol") == None else inf.get("vol")
        per = 5118 if inf.get("per") == None else inf.get("per")
        client = AipSpeech(app_id, api_key, secret_key)
        result = client.synthesis(text, 'zh', 1, {
            'spd': spd,
            'pit': pit,
            'vol': vol,
            'per': per
        })
        t = str(time.time()).replace(".", "")
        name_by_mp3 = "{}{}".format(t, ".mp3")
        file_name_by_mp3 = os.path.join(self.__temp_dir, name_by_mp3)
        if not isinstance(result, dict):
            with open(file_name_by_mp3, 'wb') as f:
                f.write(result)
            if not os.path.exists(file_name_by_mp3):
                time.sleep(1)
            return AudioFileClip(file_name_by_mp3)

    def __mixing(self, text) -> AudioFileClip:
        if self.__tts_type == 'pyttsx3':
            return self.__mixing_by_pyttsx3(text)
        elif self.__tts_type == 'baidu':
            return self.__mixing_by_baidu(text)
        else:
            raise Exception("仅支持tts:pyttsx3和baidu")

    def add_subtitle(self, subtitle: str, start: int, end: int, mixing: bool = True):
        """添加单句字幕
        Args:
            subtitle (str): 要添加的字幕
            start (int): 添加到视频的开始时间
            end (int): 添加到视频的结束时间
            mixing (bool, optional): 是否配音. Defaults to True.
        """
        clip = TextClip(subtitle,
                        fontsize=self.__subtitle_font_size,
                        font=self.__subtitle_font,
                        align=self.__subtitle_align,
                        color=self.__subtitle_color,
                        bg_color=self.__subtitle_bg_color)
        position_x = 0.5-(float(clip.w)/float(self.__src_video_width))*0.5
        clip = clip.set_position(
            (position_x, self.__subtitle_position_y), relative=True)
        clip = clip.set_start(start)
        duration = end-start
        if duration > self.__subtitle_dispaly_intermission_time*2:
            duration = duration-self.__subtitle_dispaly_intermission_time
        clip = clip.set_duration(duration)
        self.__subtitle_list.append((clip, subtitle, start, mixing))

    def add_subtitles(self, subtitles: list, start: list, end: int = None, mixing: bool = True):
        """添加多句字幕

        Args:
            subtitles (list): 要添加的字幕集合
            start (list): 每条字幕在视频中出现的时间
            end (int, optional): 最后一条字幕消失的时间，默认不设置是视频结束. Defaults to None.
            mixing (bool, optional): 是否配音. Defaults to True.
        """
        if end == None:
            end = self.__src_duration
        start.append(end)
        for s, subtitle in enumerate(subtitles):
            self.add_subtitle(subtitle, start[s], start[s+1], mixing)

    def export_to_file(self, file_path: str):
        """导出到文件
        Args:
            file_path (str): 文件路径
        """
        video = self.__src_video
        clip = list()
        for subtitle_clip, subtitle, start, mixing in self.__subtitle_list:
            if mixing:
                audio_clip = self.__mixing(subtitle)
                if audio_clip is not None:
                    audio_clip = audio_clip.set_start(start)
                    subtitle_clip = subtitle_clip.set_audio(audio_clip)
            clip.append(subtitle_clip)
        video = CompositeVideoClip([video, *clip])
        video = video.resize(width=self.__render_width)
        video.write_videofile(file_path, threads=self.__render_threads,
                              preset=self.__render_preset, fps=self.__render_fps, audio_codec="aac")


class SubtitleFactary():

    interface = None

    def __init__(self) -> None:
        self.__video_path = None
        self.__start_time = None
        self.__end_time = None
        self.__subtitles = list()
        self.__time = list()

    @classmethod
    def create(cls, init=True):
        """创建一个字幕工厂实例

        Args:
            init (bool, optional): 是否初始化. Defaults to True.
        """
        cls.instance = SubtitleFactary()
        if init:
            cls.instance.start()

    @classmethod
    def get_instance(cls):
        """取到当前字幕工厂实例

        Returns:
            SubtitleFactary: 字幕工厂实例
        """
        if not hasattr(cls, "instance"):
            cls.create()
        instance: SubtitleFactary = cls.instance
        return instance

    @classmethod
    def make(cls, src_movie: str, dst_movie: str, offset: int = 0, fps: int = 5, width=480, threads=8, mixing: bool = True, tts="pyttsx3", inf: dict = None):
        """合成字幕

        Args:
            src_movie (str): 源视频
            dst_movie (str): 合成视频路径
            offset (int, optional): 整体字幕时间偏移量. Defaults to 0.
            fps (int, optional): 输出视频fps. Defaults to 5.
            width (int, optional): 输出视频宽度. Defaults to 480.
            threads (int, optional): 输出视频渲染用线程数. Defaults to 8.
            mixing (bool, optional): 是否配音. Defaults to True.
            tts (str, optional): 使用tts种类,可选有pyttsx3和baidu。 Defaults to pyttsx3.
            info (dict, optional): 当使用baidu tts时,需要填入的信息
                {
                    "app_id":"",
                    "api_key":"",
                    "secret_key":"",
                    "spd":5, #语速,0-9
                    "pit":5, #语调,0-9
                    "vol":5, #音量,0-15 
                    "per":5118 #发音人
                }
        Raises:
            Exception: Exception("未初始化工厂")
        """
        if not hasattr(cls, "instance"):
            raise Exception("未初始化工厂")
        t = list()
        for _i in cls.instance.time:
            _t = _i-cls.instance.start_time
            t.append(int(_t)+offset)
        make_subtitle = MakeSubtitle(
            src_movie, fps=fps, width=width, threads=threads, tts=tts, inf=inf)
        make_subtitle.add_subtitles(cls.instance.subtitles, t, mixing=mixing)
        make_subtitle.export_to_file(dst_movie)

    @property
    def video(self):
        return self.__video_path

    @video.setter
    def video(self, video):
        self.__video_path = video

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
        self.__start_time = time.time()

    def subtitle(self, text: str, offset: int = 0):
        """增加一条字幕

        Args:
            text (str): 要增加的字幕
            offset (int, optional): 需要增加的偏移量，正数代表延后，负数代表提前. Defaults to 0.
        """
        self.__subtitles.append(text)
        self.__time.append(time.time()+offset)
