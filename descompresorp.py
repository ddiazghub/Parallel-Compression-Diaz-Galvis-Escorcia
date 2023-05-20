import os
from argparse import ArgumentParser
from timeit import default_timer as timer
from typing import Callable
from constants import REF_BYTE_LENGTH, WINDOW_SIZE, CHUNK_SIZE
from mpi_globals import RANK
from process import Root, Worker
from descompresor import process_chunk
from mpi4py import MPI
from mpi_globals import CHANNEL

def chunk_processor(chunk_size: int, shared_memory: bytearray) -> Callable[[str, int], bytearray | bytes]:
    """Funciones que permiten descomprimir un archivo comprimido con el algoritmo LZ77.
    La primera descomprime parcialmente una parte del archivo. Retorna a la parte descomprimida como un buffer de bytes y la lista de referencias que no pudieron ser resueltas.
    La segunda se ejecuta justo antes de escribir al archivo de salida y lee la anterior parte descomprimida para resolver referencias.
        
    Args:
        chunk_size (int): Tamaño de cada parte del archivo.
    """
    def decompress_chunk(filename: str, chunk_number: int) -> bytearray | bytes:
        """Lee y descomprime parcialmente una parte de un archivo comprimido con el algoritmo LZ77.
            
        Args:
            filename (str): Nombre del archivo comprimido.
            chunk_number (int): El número de la parte a descomprimir.
        """
        chunk_start = chunk_number * chunk_size

        with open(filename, "rb") as file:
            file.seek(chunk_start)
            chunk = file.read(chunk_size)
            window = bytearray(shared_memory)

            if chunk_number > 0:
                Worker.wait(chunk_number)
                window[:] = shared_memory[:WINDOW_SIZE]

            window_length = len(window)
            output = process_chunk(chunk, window)
            shared_memory[:WINDOW_SIZE] = output[-WINDOW_SIZE:]
            Worker.notify_holder(chunk_number + 1)

            return output[window_length:]

    return decompress_chunk


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="Descompresor LZ77 en paralelo",
        description="Descomprime un archivo comprimido usando el algoritmo LZ77 en paralelo"
    )
    
    parser.add_argument("zipfile", help="Nombre del archivo a descomprimir")
    parser.add_argument("-o", "--outfile", help="Nombre del archivo descomprimido", default="descomprimidop-elmejorprofesor.txt")
    parser.add_argument("-c", "--chunk-size", help="Tamaño de las partes en las cuales se dividirá el archivo de entrada", type=int, default=CHUNK_SIZE) 

    args = parser.parse_args()
    zipfile, outfile, chunk_size = args.zipfile, args.outfile, args.chunk_size
    chunk_size = chunk_size + REF_BYTE_LENGTH - chunk_size % REF_BYTE_LENGTH

    window = bytearray(WINDOW_SIZE)
    comm = MPI.COMM_WORLD

    if RANK == 0:
        root_process = Root(zipfile, outfile, chunk_size)
        start_time = timer()
        root_process.run()
        end_time = timer()
        execution_time = end_time - start_time
        print(execution_time)
    else:
        dec_chunk = chunk_processor(chunk_size, window)
        worker = Worker(zipfile, outfile, dec_chunk)
        worker.run()
