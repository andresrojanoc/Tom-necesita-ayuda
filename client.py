#! python3
import json
import time
from websocket import create_connection
from tqdm import tqdm
from abc import ABCMeta, abstractstaticmethod

url = "ws://209.126.82.146:8080/"

def isprime(num):
    try:
        for n in range(2,int(num**0.5)+1):
            if num%n==0:
                return False
        return True
    except TypeError:
        return "Error in isprime(num): TypeError"


class ICommannds(metaclass=ABCMeta):

    @abstractstaticmethod
    def download_files(self):
        raise AttributeError("Please implement this method")

    @abstractstaticmethod
    def compile_contents(self):
        raise AttributeError("Please implement this method")

    @abstractstaticmethod
    def look_structure(self):
        raise AttributeError("Please implement this method")



class ClientDownloadFiles:

    def download_files(self,jsons_files):
        file_numbers = 0
        dictionary_downloaded = dict()
        while file_numbers < jsons_files:
            entry =  self.ws.recv()
            temp_dict = json.loads(entry)
            a = list(temp_dict.values())[0]
            b = list(temp_dict.values())[-1]
            dictionary_downloaded[a] = b
            file_numbers += 1
        return dictionary_downloaded


class ClientCompileContents:

    def compile_contents(self,content):
        if self.first == True:
            self.compiled_jsons = content
            global last_key
            last_key = int(list(content.items())[-1][0])
        else:
            for key, value in content.items():
                new_key = last_key + 1
                self.compiled_jsons[new_key] = value
                last_key += 1

class ClientLookStructure:

    def look_structure(self,dictionary):
        self.even_numbers = 0
        self.odd_numbers = 0
        self.prime_numbers = 0
        self.model = dictionary
        self.first_number = list(self.model.items())[0][1]
        self.last_number = list(self.model.items())[-1][1]

        max_key = max(self.model, key=self.model.get)
        min_key = min(self.model, key=self.model.get)

        self.max_number = self.model[max_key]
        self.min_number = self.model[min_key]

        for key, value in self.model.items():
            if (isprime(value)) == True:
                if value != 1 and value != 0:
                    self.prime_numbers += 1
            if (value % 2) == 0:
                self.even_numbers += 1
            else:
                self.odd_numbers += 1

        structure = [self.max_number,self.min_number,self.first_number,self.last_number,self.prime_numbers,self.even_numbers,self.odd_numbers]
        return structure

class Client(ClientDownloadFiles,ClientCompileContents,ClientLookStructure):

    def __init__(self,url):
        self.ws = create_connection(url)

        self.first = True
        self.outputs = 0
        self.jsons_files = 100
        self.blocks = 100


class Main(ICommannds):

    url = "ws://209.126.82.146:8080/"

    @staticmethod
    def main(iterations):

        client = Client(url)
        interrupted = 'No'
        final_result = []
        block_ouput = []
        iteration = 0

        with open("outputs.txt","w") as out_file:
            out_file.write("Data structures\n")
            out_file.write("max_number min_number first_number last_number number_of_prime_numbers number_of_even_numbers number_of_odd_numbers \n")
        out_file.close()

        try:
            for i in tqdm(range(iterations)):
                t_end = time.time() + 60
                while time.time() < t_end:
                    time.sleep(0.1)
                    batch_json_files = ClientDownloadFiles.download_files(client,client.jsons_files)
                    ClientCompileContents.compile_contents(client,batch_json_files)
                    dictionary_updated = client.compiled_jsons
                    client.first = False
                last = list(dictionary_updated.keys())[-1]
                partitions = int(list(dictionary_updated.keys())[-1])//client.blocks
                first_index = 0
                last_index = int(partitions)
                increment = last_index
                for i in range(client.blocks):
                    d1 = dict(list(dictionary_updated.items())[first_index:last_index])
                    first_index = last_index
                    last_index += increment
                    output = ClientLookStructure.look_structure(client,d1)
                    write_line = ""
                    for out in output:
                        write_line = write_line+str(out)+" "
                    with open("outputs.txt","a") as out_file:
                        out_file.write(str(i+1)+" "+write_line+"\n")
                    out_file.close()
                    final_result.append(write_line)
                    block_ouput.append(write_line)
                block_local = 0
                print(f"\nIteration: {iteration}")
                for block in block_ouput:
                    block_local += 1
                    print(f"block{block_local}: {block}")

        except KeyboardInterrupt:
            client.ws.close()
            print("The Program was interrupted via KeyboardInterrupt")
            print("The data structures information can be found in the file: outputs.txt")
            print("\nResult:\n")
            interrupted = 'Yes'

        if interrupted == 'No':
            client.ws.close()
            print("The data structures information can be found in the file: outputs.txt")
            print("\n\n")

        return final_result



if __name__ == "__main__":
    iterations = 3
    result = Main.main(iterations)
