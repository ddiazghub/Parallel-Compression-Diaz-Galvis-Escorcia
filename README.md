# Compresor-Python
Compresión y descompresión de un archivo. Para utilizar los programas siga las siguientes indicaciones:

## Compresión
Para comprimir un archivo llamado "LaBiblia.txt", utilize el comando de consola:
```console
python ./compresor.py LaBiblia.txt
```
Opcionalmente se puede suministrar el nombre del archivo comprimido de salida. Si no se suministra, este será "comprimido.elmejorprofesor" por defecto.
```console
python ./compresor.py LaBiblia.txt --outfile LaBiblia.zip
```

## Descompresión
El descompresor por defecto buscará el archivo "comprimido.elmejorprofesor" en la carpeta actual y lo descomprimirá a un archivo llamado "descomprimido-elmejorprofesor.txt". Este programa puede ser ejecutado sin argumentos de consola:
```console
python ./descompresor.py
```
Opcionalmente se puede suministrar el nombre del archivo a descomprimir y el nombre del archivo descomprimido de salida.
```console
python ./descompresor.py --zipfile LaBiblia.zip --outfile LaBibliaOut.txt
```

## Verificación
Para verificar la integridad del archivo comprimido se debe utilizar el verificador. Por defecto, este recibe un archivo de texto como argumento y lo compara con el archivo "descomprimido-elmejorprofesor.txt".
```console
python ./verificador.py LaBiblia.txt
```
Opcionalmente se puede suministrar el nombre del archivo descomprimido a comparar.
```console
python ./verificador.py LaBiblia.txt --decompressed LaBibliaOut.txt
```