import os, glob, re, random, time, json
from time import sleep

class Setup:

    images_path = 'images/'
    local_appdata_path = os.getenv('LOCALAPPDATA')
    terminal_path = glob.glob(rf'{local_appdata_path}\Packages\Microsoft.WindowsTerminal*')[0]
    settings_path = rf'{terminal_path}\LocalState\settings.json'

    settings_to_add = { "backgroundImage" : "", 
                        "backgroundImageAlignment": "center", 
                        "backgroundImageStretchMode": "uniformToFill", 
                        "backgroundImageOpacity": 0.2 }

    re_comments = re.compile(r"([^:]//.+|^//.+)")

    def addSetting(self, settings : dict, setting_name : str, setting_value):
        if not settings.__contains__(setting_name):
            settings[setting_name] = setting_value
        
        return settings

    def setup(self):
        data = {}
        with open(self.settings_path, 'rt') as read_file:
            json_string = read_file.read()

            line = self.re_comments.sub("", json_string)
            data = json.loads(line)
            defaults = data["profiles"]["defaults"]

            for k, v in self.settings_to_add.items():
                defaults = self.addSetting(defaults, k, v)

        with open(self.settings_path, 'wt') as f:
            f.write(json.dumps(data, indent="    "))

class ImageHandler:

    images_path = 'images/'
    local_appdata_path = os.getenv('LOCALAPPDATA')
    terminal_path = glob.glob(rf'{local_appdata_path}\Packages\Microsoft.WindowsTerminal*')[0]
    settings_path = rf'{terminal_path}\LocalState\settings.json'

    last_image_index = 0

    def start(self):
        initializer = Setup()
        initializer.setup()
        self.changeImage()

    def getRandomIndex(self, start : int, stop: int):
        res = random.randint(start, stop)
        if res == self.last_image_index:
            return self.getRandomIndex(start, stop)
        else:
            self.last_image_index = res
            return res
    
    def changeImage(self):
        files = os.listdir(self.images_path)
        imageIndex = self.getRandomIndex(0, files.__len__() - 1)
        newImage = os.path.abspath(f'images/{files[imageIndex]}')
        newImage = newImage.replace('\\', '/')
        
        with open(self.settings_path, 'rt') as f:
            src = f.read()
            match = re.search(r'"backgroundImage": "([\w.:/]+)"', src)
            replace = src.replace(match.group(1), newImage)
        
        with open(self.settings_path, 'wt') as f:
            f.write(replace)
        
        sleep(650)
        self.changeImage()

changer = ImageHandler()
changer.start()
