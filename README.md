# spot-on
Cli tool for downloading spotify tracks from youtube<br>
As of now, supports playlist & album downloads<br>
Results may be invalid, make sure to double check downloads<br>
Please credit if you so happen to use this somewhere else<br>

# Installation
```
git clone https://github.com/wdmvv/spot-on
cd spot-on
pip install -r requirements.txt
```
You will also have to obtain spotify app client id and secret. To do that go to the [app creation page](https://developer.spotify.com/dashboard) and create new app. Upon creating, click "Settings" button, copy client id & client secret and put both into .env file


# Usage:
```
python3.11 main.py [-h] [--type type] [--path path] [--precise] [--workers number] link
```
<ul>
  <li>-h - program help</li>
  <li>--type - download type, must be either 'album' or 'playlist'</li>
  <li>--path - specify download path, by default creates 'Downloads' dir in workdir</li>
  <li>--precise - enable precise search. It will work slower, but results will be as close to the spotify's ones as possible</li>
  <li>--workers - amount of threads to launch during download, 5 by default</li>
  <li>--sideload - allows you to specify path or link that you want to use instead of yt search - read more about this below<li>
  <li>link - spotify playlist/album link, can be either id or link</li>
</ul>


# Examples:
```
python3.12 main.py --type album --path 'Infinite Hyperdeath' https://open.spotify.com/album/0eoB2aUIfAk7a6JBLwyZSj
```
\- will create folder 'Infinite Hyperdeath' and download album into it
```
python3.12 main.py --precise https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
```
\- will create folder 'Downloads' and download playlist filtered by duration into it
```
python3.12 main.py --sideload sideload.txt https://open.spotify.com/album/0eoB2aUIfAk7a6JBLwyZSj
```
\- will use sideload.txt instead of yt search

# More about sideload option:
It is rather experimental, so it is not that usable (for now?), but it does work as I intended it to. Basically, it is a csv with any extension with ; separator, where each line has 3 parameters: track_name;type;path
<ul>
<li>track_name is name of the song you want to sideload. For instance, if you want to sideload "A.U.M.", then you have to put there either "AUM" or "A.U.M.". Do note that both track_name here and inside of spotify processing are sanitized, so . and , are removed, \ and / are replaced with `-`</li>
<li>type is a type of sideload - either link (aliases; link, l, url, u), or path (alias: p)</li>
<li>path is either path or link, based on what you chose. Note that everything unaffected by sideload will be simply downloaded by other means, so either default or precise downloads</li>
</ul>
This sideload feature does not have any error handling, so be careful. 


# Future
I abandoned this project, mainly for one reason: it is hard to support this code. Maybe this is because of python, maybe because I lack experience, but problems like lack of error handling(basically nonexistent, just continue/return on error), lack of proper multithreading/paralleling, lack of solid code base that can be easily extended are kind of hard to get rid of until I rewrite everything from scratch. This is why I am currently planning to rewrite everything to Go, where all of these problems can be sort of easily solved. Please do look forward it. Now, what will happen to this repo? I will not nuke it nor overwrite in future, might sometimes do minor fixes and/or add features (geez, imagine saying something like this in a repo with barely anyone here, but will do anyway)
