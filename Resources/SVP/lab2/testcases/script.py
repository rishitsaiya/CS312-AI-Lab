"""
For generation random matrices, go to https://onlinemathtools.com/generate-random-matrix

Download them into the directory as input1.txt, input2.txt etc

Add a line in the beginning of the file with size of matrix

And to get the solutions, run
$python3 script.py > output.txt

"""
import os
import requests
i = 1
files = os.listdir()
while f"input{i}" in files:
    with open(f"input{i}", "r") as file:
        text = []
        firstLine = True
        for line in file:
            if firstLine:
                firstLine = False
                continue            
            line = "-".join(line.split())
            text.append(line)
        text = "--".join(text)
        url = f"http://www.hungarianalgorithm.com/solve.php?c={text}&random=1"
        # url = text[:46]+text[47:]
        text = requests.get(url).text
        index = text.index("optimal value equals ")+21
        text = text[index:]
        index = text.index(".")
        text = text[:index]
        print(text, url)
    i += 1
        
