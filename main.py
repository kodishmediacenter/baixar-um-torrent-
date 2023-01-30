from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return '''
        <form action="/" method="post">
            <label for="link">URL do torrent:</label>
            <input type="text" id="link" name="link">
            <br><br>
            <label for="cont">Nome do arquivo final:</label>
            <input type="text" id="cont" name="cont">
            <br><br>
            <input type="submit" value="Baixar">
        </form>
    '''

@app.route("/", methods=["POST"])
def download():
    link = request.form["link"]
    cont = request.form["cont"]

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

    return f"Torrent baixado com sucesso! Arquivo final: {cont}.mp4"

if __name__ == "__main__":
    app.run()
