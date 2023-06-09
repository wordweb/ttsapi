from flask import Flask, request
import edge_tts
import os
import time


app = Flask(__name__)

@app.route('/generate-audio', methods=['POST'])
async def generate_audio():
    data = request.json
    text = data['text']
    lang = data.get('lang', 'zh-CN-XiaoyiNeural')
    speed = data.get('speed', '-4%')
    volume = data.get('volume', '+0%')
    timestamp = int(time.time())
    
    audio_data = edge_tts.Communicate(text, voice=lang, rate=speed, volume=volume)
    filename = f".\mp3\{timestamp}.mp3"
    await audio_data.save(filename)

    return {'filename': f"{timestamp}.mp3"}

@app.route('/download-audio/<filename>', methods=['GET'])
def download_audio(filename):
    file_path = f".\mp3\{filename}"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, attachment_filename=file_path)
    else:
        return {'error': 'File not found'}

@app.route('/delete-audio/<filename>', methods=['GET'])
def delete_audio(filename):
    timestamp=f".\mp3\{filename}"
    print(timestamp)
    if os.path.exists(timestamp):
        os.remove(timestamp)
        return {'message': f'{filename} has been deleted'}
    else:
        return {'message': 'File not found'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
