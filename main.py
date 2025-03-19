from resources.DownloadFiles import DownloadFiles

if __name__ == '__main__':
    downloadfiles = DownloadFiles()
    # input()

    downloadfiles.download_files(tipo='GIA')
    downloadfiles.download_files(tipo='DESTDA')
    downloadfiles.browsersefaz.navegador.close()
