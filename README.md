# spot-on
Cli tool for downloading spotify tracks from youtube<br>
As of now, supports playlist & album downloads<br>
Results may be invalid, make sure to double check downloads(currently works for most genres, although classical music results are bad)<br>


# Installation
```
git clone https://github.com/wdmvv/spot-on
cd spot-on
pip install -r requirements.txt
```

# Usage:
python3.11 main.py [type] link [download_path]<br>
<ul>
  <li>type - defines what should it download - album or playlist, playlist by default</li>
  <li>link - download link - can be either full path link or just id</li>
  <li>download_path - where should downloads be stored - by default creates 'Downloads' dir in workdir</li>
</ul>

# TBD
<ul>
  <li>Add precision search based on duration</li>
</ul>

# Known problem(s)
<ul>
  <li>Sometimes download may fail with following error: `[download] Got error: HTTP Error 403: Forbidden ytdlp`. I assume this is related to youtube doing something on their side since it used to work previously</li>
  <li>Some songs have entire album inside instead of single song - I will try to fix this in future (given that I dont forget about this project)</li>
</ul>