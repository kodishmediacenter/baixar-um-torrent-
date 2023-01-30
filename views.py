from django.shortcuts import render
import subprocess

def index(request):
    if request.method == "POST":
        link = request.POST["link"]
        cont = request.POST["cont"]

        # Baixa o torrent
        subprocess.run(["transmission-cli", "-w", "./", link])

        # Converte arquivos para MP4
        subprocess.run(["ffmpeg", "-i", "*.webm", "-c:v", "copy", "-c:a", "copy", "webm.mp4"])
        subprocess.run(["ffmpeg", "-i", "*.mkv", "-c:v", "copy", "-c:a", "copy", "mkv.mp4"])
        subprocess.run(["ffmpeg", "-i", "*.avi", "-c:v", "copy", "-c:a", "copy", "avi.mp4"])
        subprocess.run(["ffmpeg", "-i", "*.ts", "-c:v", "copy", "-c:a", "copy", "ts.mp4"])

        # Renomeia o arquivo final
        subprocess.run(["mv", "*.mp4", f"{cont}.mp4"])

        # Move o arquivo final para o diretório do Apache2
        subprocess.run(["sudo", "mv", f"{cont}.mp4", "/var/www/html/"])

        # Adiciona a mensagem de sucesso ao template
        success_message = f"Torrent baixado com sucesso! Arquivo final: {cont}.mp4"

        return render(request, "index.html", {'success_message': success_message})

    return render(request, "index.html")

