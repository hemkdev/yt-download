from yt_dlp import YoutubeDL

def progresso(d):
    if d['status'] == 'downloading':
        print(f'\r{d["_percent_str"]}', end='')

try:
    while True:
        url = input('\nType URL (or "exit"): ')
        
        if url.lower() == 'exit':
            break
        
        if not url.strip():
            print("URL cannot be empty")
            continue
        
        opcao = {
            'outtmpl': r'C:\Code\Downloads\%(title)s.%(ext)s',
            'format': 'best[ext=mp4]',
            'quiet': True,
            'progress_hooks': [progresso]
        }
        
        with YoutubeDL(opcao) as ydl:
            ydl.download([url])

except Exception as e:
    print(f"Error: {e}")