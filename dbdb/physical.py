# defines the physical layer. The Storage class provides the persistent , (mostly) append only record storage . 

import os 
import struct 
import portalocker

class Storage(object):

    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = "!Q"
    INTEGER_LENGTH = 8

    def __init__(self,f):
        # file object opened to read and write 
        self._f = f
        self.locked = True
        self._ensure_superblock()

    # Ensures that there is enough space at the beginning of the file for the superblock.
    def _ensure_superblock(self):
        self.lock()
        self._seek_end()
        end_address = self._f.tell()
        if end_address < self.SUPERBLOCK_SIZE:
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    # locking to prevent race conditions
    def lock(self):
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False
        
    # unlocking 
    def unlock(self):
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False
    
    # seeking the end of the file to append new content 
    def _seek_end(self):
        self._f.seek(0, os.SEEK_END)

    # seeking the beginning of the file , where superblock is located which contains the root address
    def _seek_superblock(self):
        self._f.seek(0)

    # Convert Bytes to Int
    def _bytes_to_integer(self, integer_bytes):
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    # Reverse of the above
    def _integer_to_bytes(self, integer):
        return struct.pack(self.INTEGER_FORMAT, integer)

    # reads a fixed length byte string and converts to int
    def _read_integer(self):
        return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    # writes a integer to the file 
    def _write_integer(self, integer):
        self.lock()
        self._f.write(self._integer_to_bytes(integer))

    # writes data onto the file 
    def write(self, data):
        self.lock()
        self._seek_end()
        object_address = self._f.tell()
        self._write_integer(len(data))
        self._f.write(data)
        return object_address

    # Reads data from the file from a specific address 
    def read(self, address):
        self._f.seek(address)
        length = self._read_integer()
        data = self._f.read(length)
        return data

    # Commits the root address to the superblock. where root_address is the address of the root node of the Binary Tree. 
    def commit_root_address(self, root_address):
        self.lock()
        self._f.flush()
        self._seek_superblock()
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()
        
    # Retrieves the root address from the superblock , by seeking the superblock and retrieving the root addr 
    def get_root_address(self):
        self._seek_superblock()
        root_address = self._read_integer()
        return root_address
    
    # Close the File storage and release any locks 
    def close(self):
        self.unlock()
        self._f.close()

    # Checks if the file is closed . 
    @property
    def closed(self):
        return self._f.closed
    