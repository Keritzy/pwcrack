# pwcrack.py
# Password cracker in python by Bit.
#     --help             Displays this help
# -m  --mode 0|1         Selects the cracking mode. 0: bruteforce, 1: dictionary
# -a  --algorithm        Selects the hashing algorithm.
# -h  --hashes file      Selects the hash file to read from.
# -c  --charset letters  Changes the character set. Only used in bruteforce mode.
# -s  --seek attempt     Seeks to start searching at attempt. Incompatible with
#                        random flag.
# -r  --random max       Randomly attempts hashes up to max length. *
# -d  --dictionary file  Selects the dictionary file to read from. Only used in
#                        dictionary mode.
# -o  --output file      Selects the ouput file to output solved hashes.
# -p  --pre-computed     Indicates that the dictionary is pre-computed. Only used
#                        in dictionary mode. *
# -g  --generate         Generates pre-computed dictionary instead of solving
#                        hashes. Only used in dictionary mode. Compatible with
#                        seek option.

import sys
import getopt
import hashlib

mode = 0
algorithm = "md5"
hashes = []
cracked = {}
dictionary = []
charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
generate = 0
seek = 0
output = 0

def syntax(code):
  print("pwcrack.py\nPassword cracker in python by Bit.\n    --help             Displays this help\n-m  --mode 0|1         Selects the cracking mode. 0: bruteforce, 1: dictionary\n-a  --algorithm        Selects the hashing algorithm.\n-h  --hashes file      Selects the hash file to read from.\n-c  --charset letters  Changes the character set. Only used in bruteforce mode.\n-s  --seek attempt     Seeks to start searching at attempt. Incompatible with\n                       random flag.\n-r  --random max       Randomly attempts hashes up to max length.\n-d  --dictionary file  Selects the dictionary file to read from. Only used in\n                       dictionary mode.\n-o  --output file      Selects the ouput file to output solved hashes.\n-p  --pre-computed     Indicates that the dictionary is pre-computed. Only used\n                       in dictionary mode.\n-g  --generate         Generates pre-computed dictionary instead of solving\n                       hashes. Only used in dictionary mode. Compatible with\n                       seek option.")
  sys.exit(code)
  
def errorQuit(message, code):
  print(message)
  sys.exit(code)

try:
  options, args = getopt.getopt(sys.argv[1:], "m:a:h:c:s:r:d:o:pg", ["mode=", "algorithm=", "hashes=", "charset=", "seek=", "random=", "dictionary=", "output=", "pre-computed", "generate"])
except getopt.GetoptError:
  syntax(2)
  
print(options) # debug

for option, arg in options:
  
  if option in ("-m", "--mode"):
    try:
      mode = int(arg)
    except ValueError:
      errorQuit("Error! Option <" + option + "> is not a mode.", 2)
      
  elif option in ("-a", "--algorithm"):
    algorithm = arg
    
  elif option in ("-h", "--hashes"):
    try:
      with open(arg, "r") as file:
        hashes = file.read().split("\n")
    except IOError:
      errorQuit("Error! Option <" + option + "> is not a file.", 2)
      
  elif option in ("-c", "--charset"):
    charset = arg
    
  elif option in ("-s", "--seek"):
    seek = arg
      
  elif option in ("-r", "--random"):
    print("wip")
    
  elif option in ("-d", "--dictionary"):
    try:
      with open(arg, "r") as file:
        dictionary = file.read().split("\n")
    except IOError:
      errorQuit("Error! Option <" + option + "> is not a file.", 2)
      
  elif option in ("-o", "--ouput"):
    output = arg
    
  elif option in ("-p", "--pre-computed"):
    print("wip")
    
  elif option in ("-g", "--generate"):
    generate = 1

if output != 0:
  outputFile = open(output, "w")

def write(text):
  if output == 0:
    print(text)
  else:
    outputFile.write(text + "\n")

if mode == 0: # Bruteforce
  # Increments the character by one
  def incrementChar(index, charset):
    index[0] += 1
    for pos in range(len(index)):
      if index[pos] + 0 >= len(charset):
        if len(index) <= pos + 1:
          index.append(0)
          index[pos] = 0
        else:
          index[pos + 1] += 1
          index[pos] = 0
    return index
  
  # Decodes index into attempt
  def decodeAttempt(index):
    attempt = ""
    for pos in index:
      attempt = charset[pos] + attempt;
    return attempt
  
  def encodeAttempt(attempt):
    index = []
    for pos in range(len(attempt)):
      for char in range(len(charset)):
        if charset[char] == attempt[len(attempt) - 1 - pos]:
          index.append(char)
    return index
  
  index = [0]
  if seek != 0:
    index = encodeAttempt(seek)
  
  while 1:
    attempt = decodeAttempt(index)
    attemptHash = getattr(hashlib, algorithm)(attempt.encode("utf-8")).hexdigest()
    if generate == 1:
      write(attemptHash + " " + attempt)
    else:
      for hash in range(len(hashes)):
        if hashes[hash] == attemptHash:
          cracked[hashes[hash]] = attempt
          write(hashes[hash] + " " + attempt)
    incrementChar(index, charset)
    
elif mode == 1: # Dictonary
  index = 0
  while 1:
    attempt = dictionary[index]
    try:
      attemptHash = getattr(hashlib, algorithm)(attempt.encode("utf-8")).hexdigest()
      for hash in range(len(hashes)):
        if hashes[hash] == attemptHash:
          cracked[hashes[hash]] = attempt
          write(hashes[hash] + " " + attempt)
    except UnicodeDecodeError: # It doesn't like Unicode characters... Unicode characters shouldn't even be in passwords anyways
      attemptHash = "";
    if index >= len(dictionary) - 1: # We're done
      sys.exit(0)
    index += 1
