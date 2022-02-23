import yfinance as yf
import csv
import sys

def try_index(array, text):

    try:
        ret = array[array.index(text) + 1]
    except:
        ret = None
    return ret

inp = sys.argv

try:
    inp.index("--help")

    print("Para usar el script se necesita la libreria de python \"yfinance\"")
    print("Para instalarla ejecute: \"pip install yfinance\"")
    
    print("-p path: directorio donde se quiere guardar el csv descargado. Sino se guardara en el directorio actual")
    print("")
    print("-a asset: nombre del activo. Por defecto: btc-usd")
    print("")
    print("-s start: fecha de inicio. Por defecto \"2021-01-01\"")
    print("")
    print("-e end: fecha final del rango. Por defecto \"2021-12-31\"")
except:
    pass
else:
    sys.exit()


path_csv = try_index(inp,"-p")
asset = try_index(inp,"-a")
_start = try_index(inp,"-s")
_end = try_index(inp,"-e")

path_csv = path_csv if not (path_csv is None) else ""
asset = asset if not (asset is None) else "btc-usd"
_start = _start if not (_start is None) else "2021-01-01"
_end = _end if not (_end is None) else "2021-12-31"


print(path_csv+asset+'_'+_start+'_'+_end+".csv")

try:
    data = yf.download(asset,start = _start, end = _end)
    data.to_csv(path_csv+asset+'_'+_start+'_'+_end+".csv")
except:
    print("\nError\n")
else:
    print("\nComplete\n")

print("ejecute \"python script.py --help\" para mayor información")
