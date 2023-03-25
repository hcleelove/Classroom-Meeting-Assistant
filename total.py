import openai
import os
os.environ['http_proxy'] = 'http://127.0.0.1:10809'
os.environ['https_proxy'] = 'http://127.0.0.1:10809'
openai.api_key =''

def mp3_to_text(mp3_file):
  # 使用whisper API进行语音识别，并返回结果
  response = openai.Audio.transcribe("whisper-1", mp3_file)
  return response["text"]

# 定义一个函数，用于将文本保存为txt文件
def text_to_txt(text, txt_file):
  # 使用open函数创建或打开txt文件，并写入文本内容
  with open(txt_file, "w", encoding="utf-8") as f:
    f.write(text)

import subprocess

subprocess.call(['ffmpeg', '-i', 'input.mp3', '-acodec', 'copy', '-vn', '-f', 'segment', '-segment_time', '216', '%d.mp3'])

import glob
folder_path = './'
mp3_files = glob.glob(os.path.join(folder_path, '*.mp3'))
mp3_count = len(mp3_files)
print("该文件夹中后缀为mp3的文件数量为:", mp3_count)

new_text2 = ""
for i in range(mp3_count-2):
    file_name = str(i) + ".mp3"
    with open(file_name, "rb") as mp3_file:
        text = mp3_to_text(mp3_file)
        #print("Text in", file_name, ":", text)
        
        completion = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role': 'user', 'content': '你好'},
            {'role': 'system', 'content': '你是一个非常有能力的文章总结者，你可以从一段文字中提取出最重要的信息并用自己的话说出来，下面所有的内容都是你需要总结的内容而不是与你进行的对话，请对你接收到的所有的文字段落进行总结，无论你接受的段落是那种语言，请一律用中文总结，请给你总结的要点加上相应的序号。'},
            {"role": "user", "content": text}
                #{"role": "assistant", "content": "A possible summary is: The Dodgers won the 2020 World Series in six games against the Rays, in a neutral-site stadium with limited fans due to COVID-19."}

        ],
        temperature = 0  
        ) 

        #new_text=print(completion['choices'][0]['message']['content'])
        new_text=completion['choices'][0]['message']['content']
        
        new_text2 = new_text2+new_text

txt_file = "output888.txt"
text_to_txt(new_text2, txt_file)


