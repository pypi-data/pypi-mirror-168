import os.path
import unittest
import uuid

from ..core.compression import FileCompressor, Zstd

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
folder_path = os.path.join(base_dir, "tests")


class TestZstd(unittest.TestCase):
    def setUp(self) -> None:
        self.comp = Zstd()

        self.original = f"{folder_path}/example_files/bee_movie.txt"

    def test_compress_decompress(self):
        decompressed_path = f"{folder_path}/example_files/bee_movie_decompressed.txt"
        compressed_path = f"{folder_path}/example_files/bee_movie_compressed.txt"
        orig_size = os.path.getsize(self.original)
        with open(self.original, "rb") as fs, open(compressed_path, "wb") as fo:
            self.comp.compress(fs, fo)
        self.assertLess(
            os.path.getsize(compressed_path), orig_size, "File post compression not smaller"
        )
        with open(compressed_path, "rb") as ch, open(decompressed_path, "wb") as co:
            self.comp.decompress(ch, co)
        self.assertEqual(
            os.path.getsize(decompressed_path),
            orig_size,
            "File post decompression not original size",
        )

        os.remove(compressed_path)
        os.remove(decompressed_path)


class TestFileCompressor(unittest.TestCase):
    def setUp(self) -> None:
        self.file_compressor = FileCompressor()
        self.original = f"{folder_path}/example_files/bee_movie.txt"

    def test_compression(self):
        compressed_path = f"{folder_path}/example_files/bee_movie_compressed{uuid.uuid4()}.txt"
        self.file_compressor.compression(file_path_in=self.original, file_path_out=compressed_path)
        self.assertLess(os.path.getsize(compressed_path), os.path.getsize(self.original))
        os.remove(compressed_path)

    def test_decompression(self):
        decompressed_path = f"{folder_path}/example_files/bee_movie_decompressed{uuid.uuid4()}.txt"
        compressed_path = f"{folder_path}/example_files/bee_movie_compressed{uuid.uuid4()}.txt"
        self.file_compressor.compression(file_path_in=self.original, file_path_out=compressed_path)
        self.file_compressor.decompression(
            file_path_in=compressed_path, file_path_out=decompressed_path
        )
        self.assertEqual(os.path.getsize(self.original), os.path.getsize(decompressed_path))
        self.assertLess(os.path.getsize(compressed_path), os.path.getsize(decompressed_path))
        os.remove(compressed_path)
        os.remove(decompressed_path)


if __name__ == "__main__":
    unittest.main()
