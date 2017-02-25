# pwcrack
A simple CPU based python password cracker.

## Help text
```
pwcrack.py
A simple CPU based python password cracker by Bit.
Syntax:
    --help             Displays this help
-m  --mode 0|1         Selects the cracking mode. 0: bruteforce, 1: dictionary
-a  --algorithm        Selects the hashing algorithm.
-h  --hashes file      Selects the hash file to read from. Required.
-c  --charset letters  Changes the character set. Only used in bruteforce mode.
-s  --seek attempt     Seeks to start searching at attempt. Incompatible with
                       random flag.
-r  --random max       Randomly attempts hashes up to max length. *
-d  --dictionary file  Selects the dictionary file to read from. Only used in
                       dictionary mode.
-o  --output file      Selects the ouput file to output solved hashes.
-p  --pre-computed     Indicates that the dictionary is pre-computed. Only used
                       in dictionary mode. *
-g  --generate         Generates pre-computed dictionary instead of solving
                       hashes. Only used in dictionary mode. Compatible with
                       seek option. Hashes options not required.
Examples:
Bruteforce the file ./test-md5-hashes.hash under md5:
  pwcrack.py -m 0 -a md5 -h "./test-md5-hashes.hash"
Dictionary attack the hashes under sha1:
  pwcrack.py -m 1 -a sha1 -h "./test-sha1-hashes.hash" -d "./test.dict"
Bruteforce the hashes starting at 5 characters:
  pwcrack.py -m 0 -a md5 -h "./test-sha1-hashes.hash" -s 00000
Only use numbers:
  pwcrack.py -m 0 -a md5 -h "./test-sha1-hashes.hash" -c 0123456789
Generate hashes to ./output-sha1.hash:
  pwcrack.py -m 0 -a sha1 -g -o "./output-sha1.hash"
```
