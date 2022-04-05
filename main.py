from flask import Flask, render_template
from isodate import parse_duration
import requests

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route("/<id>")
def main(id):
    
    playListItems = "https://www.googleapis.com/youtube/v3/playlistItems"
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    key = ""
    
    search_params = {
        'key': key,
        'playlistId' : id,
        'part' : "contentDetails ",
        'maxResults' : 50
    }

    r = requests.get(playListItems,search_params)

    results = r.json()['items']
    video_ids = []

    for result in results:
            video_ids.append(result['contentDetails']['videoId'])

    video_params = {
            'key' : key,
            'id' : ','.join(video_ids),
            'part' : 'snippet,contentDetails',
            'maxResults' : 9
        }

    r = requests.get(video_url, params=video_params)
    results = r.json()['items']
    videos = []

    for result in results:
        videos.append( {
            'id' : result['id'],
            'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
            'thumbnail' : result['snippet']['thumbnails']['high']['url'],
            'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
            'title' : result['snippet']['title'],
        })

    #return '<pre>{}</pre>'.format(json.dumps(results, indent=2))
    return render_template('index.html', videos=videos)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)