from yt_dlp import YoutubeDL
from pathlib import Path

def progress(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        if not percent:
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total:
                percent = f'{(downloaded / total) * 100:5.1f}%'

        if percent != getattr(progress, 'last', ''):
            progress.last = percent
            print(f'\r{percent}', end='', flush=True)
    elif d['status'] == 'finished':
        progress.last = ''
        print()

try:
    while True:
        url = input('\nType URL (or "f" to exit): ').strip()
        
        if url.lower() == 'f':  
            break
        
        if not url:
            print("URL cannot be empty")
            continue

        if not url.startswith(('http://', 'https://')):
            print('Please enter a valid URL (http/https).')
            continue

        download_dir = Path.home() / 'Downloads'
        download_dir.mkdir(parents=True, exist_ok=True)
        
        options = {
            'outtmpl': str(download_dir / '%(title)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
            'noprogress': True,
            'overwrites': False,
            'progress_hooks': [progress]
        }
        
        try:
            with YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)
                if info.get('_type') != 'playlist':
                    file_path = Path(ydl.prepare_filename(info))
                    if file_path.exists():
                        print(f'File already exists: {file_path.name}')
                        continue

                ydl.download([url])
        except Exception as e:
            print(f'Error: {e}')

except Exception as e:
    print(f"Error: {e}")