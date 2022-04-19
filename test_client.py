#! python3
import unittest
from client import isprime
from client import Client
from client import ClientDownloadFiles
from client import ClientCompileContents
from client import ClientLookStructure
from client import Main
from tqdm import tqdm

url = "ws://209.126.82.146:8080/"

class TestClient(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        print('setupClass')

    def setUp(self):
        print('setUp')
        self.client = Client(url)

    def test_isprime(self):
        print('isprime')
        self.assertEqual(isprime(2),True)
        self.assertEqual(isprime(5),True)
        self.assertEqual(isprime(7),True)
        self.assertEqual(isprime(6),False)
        self.assertEqual(isprime(9),False)
        self.assertEqual(isprime(-9),"Error in isprime(num): TypeError")
        self.assertEqual(isprime("9"),"Error in isprime(num): TypeError")

    def test_download_files(self):
        print('download_files')
        batch_json_files = ClientDownloadFiles.download_files(self.client,self.client.jsons_files)
        length = len(batch_json_files)
        keys = []
        values = []
        for key, value in batch_json_files.items():
            keys.append(key)
            values.append(value)
        b = list(range(1,101))
        value_type = type(values[0])
        self.assertEqual(len(batch_json_files),100)
        self.assertEqual(type(batch_json_files),type(dict()))
        self.assertEqual(keys,b)
        self.assertEqual(value_type,type(1))

    def test_compile_contents(self):
        print('compile_contents')
        for i in tqdm(list(range(100))):
            batch_json_files = ClientDownloadFiles.download_files(self.client,self.client.jsons_files)
            ClientCompileContents.compile_contents(self.client,batch_json_files)
            self.client.dictionary_updated = self.client.compiled_jsons
            self.client.first = False
        keys = []
        values = []
        for key, value in self.client.dictionary_updated.items():
            keys.append(key)
            values.append(value)
        b = list(range(1,10001))
        value_type = type(values[0])
        self.assertEqual(len(self.client.dictionary_updated),10000)
        self.assertEqual(type(self.client.dictionary_updated),type(dict()))
        self.assertEqual(keys,b)
        self.assertEqual(value_type,type(1))

    def test_look_structure(self):
        print('look_structure')
        for i in tqdm(list(range(100))):
            batch_json_files = ClientDownloadFiles.download_files(self.client,self.client.jsons_files)
            ClientCompileContents.compile_contents(self.client,batch_json_files)
            self.client.dictionary_updated = self.client.compiled_jsons
            self.client.first = False

        output = ClientLookStructure.look_structure(self.client,self.client.dictionary_updated)

        max_value = max(self.client.dictionary_updated, key=self.client.dictionary_updated.get)
        min_value = min(self.client.dictionary_updated, key=self.client.dictionary_updated.get)
        first = list(self.client.dictionary_updated.values())[0]
        last = list(self.client.dictionary_updated.values())[-1]

        prime_numbers=0
        even_numbers=0
        odd_numbers=0

        for key, value in self.client.dictionary_updated.items():
            if (isprime(int(value))) == True:
                if int(value) != 1 and int(value) != 0:
                    prime_numbers += 1
            if (int(value) % 2) == 0:
                even_numbers += 1
            else:
                odd_numbers += 1

        self.assertEqual(output[0],self.client.dictionary_updated[max_value])
        self.assertEqual(output[1],self.client.dictionary_updated[min_value])
        self.assertEqual(output[2],first)
        self.assertEqual(output[3],last)
        self.assertEqual(output[4],prime_numbers)
        self.assertEqual(output[5],even_numbers)
        self.assertEqual(output[6],odd_numbers)


class TestMain(unittest.TestCase):

    def test_main(self):
        print('main')
        result = Main.main(1)
        list1 = [1,2,3,4]
        first_result = result[0]
        structure_list = first_result.split()
        structure_list = [int(i) for i in structure_list]
        numbers_in_list = structure_list[-1]+structure_list[-2]
        self.assertEqual(len(result),100)
        self.assertEqual(len(structure_list),7)
        self.assertEqual(type(result),type(list1))
        self.assertEqual(max(structure_list),structure_list[0])
        self.assertEqual(min(structure_list[:4]),structure_list[1])


if __name__ == '__main__':
    unittest.main(verbosity=2,warnings='ignore')
    unittest.main()
