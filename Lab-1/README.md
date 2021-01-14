## To run : 

```
    $ ./run.sh input1.txt input2.txt input3.txt 
```

## TO Get Stats :
```
    $ ./stats.sh 2x2.txt 4x4.txt 6x6.txt 8x8.txt 10x10.txt 
```

### TO DO :
```
  1. comments in code
  2. Report
```

### Stats :

0 for bfs, 1 for dfs, 2 for dfid : Number of states explored "\s" Length of path

#### right,left,down,up


``` 
2x2
0 : 	13 10
1 : 	14 10
2 : 	62 10

4x4
0 : 	43 28
1 : 	35 32
2 : 	790 28

6x6
0 : 	99 38
1 : 	71 44
2 : 	5183 38

8x8
0 : 	187 64
1 : 	102 72
2 : 	31886 64

10x10
0 : 	312 86
1 : 	262 100
2 : 	20618 86
```

#### down,left,up,right


```
2x2
0 : 	13 10
1 : 	13 10
2 : 	63 10

4x4
0 : 	41 28
1 : 	48 28
2 : 	1149 28

6x6
0 : 	99 38
1 : 	83 38
2 : 	5478 38

8x8
0 : 	187 64
1 : 	168 64
2 : 	21885 64

10x10
0 : 	308 86
1 : 	252 86
2 : 	44146 86
```