from os import path, walk
from traceback import format_exc
from zipfile import ZipFile, ZIP_DEFLATED

from python.assistentes.log import Log


class ZIP:

    @staticmethod
    def descompactar(arquivo_zip, destino_arquivos):
        Log.imprime("DESCOMPACTANDO ARQUIVO " + arquivo_zip + " PARA " + destino_arquivos,
                    "DESCOMPACTANDO ARQUIVO " + arquivo_zip)
        try:
            with ZipFile(arquivo_zip, "r") as zp:
                zp.extractall(destino_arquivos)
        except:
            Log.imprime("ERRO NA DESCOMPACTACAO DO ARQUIVO " + arquivo_zip + format_exc(),
                        "ERRO NA DESCOMPACTACAO DO ARQUIVO", classe=ZIP)

    @staticmethod
    def compactar_arquivos(arquivo, destino, arcname=None):
        Log.imprime("COMPACTANDO ARQUIVO " + arquivo + " PARA " + destino, "COMPACTANDO ARQUIVO " + arquivo)
        zp = ZipFile(destino, 'w', ZIP_DEFLATED)
        if type(arquivo) is list:
            for i in range(len(arquivo)):
                if arcname is None:
                    zp.write(arquivo[i], path.basename(arquivo[i]))
                else:
                    zp.write(arquivo[i], arcname[i])
        else:
            ZIP.compactar_diretorio(zp, arquivo)
        zp.close()

    @staticmethod
    def compactar_diretorio(zp, pasta):
        relroot = path.abspath(pasta)
        Log.imprime("COMPACTANDO DIRETORIO " + relroot, "COMPACTANDO DIRETORIO " + relroot)
        for root, dirs, files in walk(pasta):
            # add directory (needed for empty dirs)
            zp.write(root, path.relpath(root, relroot))
            for file in files:
                filename = path.join(root, file)
                if path.isfile(filename):  # regular files only
                    arcname = path.join(path.relpath(root, relroot), file)
                    zp.write(filename, arcname)
