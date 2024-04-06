#include "mpi.h"
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <string.h>

#pragma GCC target("avx")
#pragma GCC optimize(2)
#pragma GCC optimize(3)
#pragma GCC optimize("Ofast")
#pragma GCC optimize("inline")
#pragma GCC optimize("-fgcse")
#pragma GCC optimize("-fgcse-lm")
#pragma GCC optimize("-fipa-sra")
#pragma GCC optimize("-ftree-pre")
#pragma GCC optimize("-ftree-vrp")
#pragma GCC optimize("-fpeephole2")
#pragma GCC optimize("-ffast-math")
#pragma GCC optimize("-fsched-spec")
#pragma GCC optimize("unroll-loops")
#pragma GCC optimize("-falign-jumps")
#pragma GCC optimize("-falign-loops")
#pragma GCC optimize("-falign-labels")
#pragma GCC optimize("-fdevirtualize")
#pragma GCC optimize("-fcaller-saves")
#pragma GCC optimize("-fcrossjumping")
#pragma GCC optimize("-fthread-jumps")
#pragma GCC optimize("-funroll-loops")
#pragma GCC optimize("-fwhole-program")
#pragma GCC optimize("-freorder-blocks")
#pragma GCC optimize("-fschedule-insns")
#pragma GCC optimize("inline-functions")
#pragma GCC optimize("-ftree-tail-merge")
#pragma GCC optimize("-fschedule-insns2")
#pragma GCC optimize("-fstrict-aliasing")
#pragma GCC optimize("-fstrict-overflow")
#pragma GCC optimize("-falign-functions")
#pragma GCC optimize("-fcse-skip-blocks")
#pragma GCC optimize("-fcse-follow-jumps")
#pragma GCC optimize("-fsched-interblock")
#pragma GCC optimize("-fpartial-inlining")
#pragma GCC optimize("no-stack-protector")
#pragma GCC optimize("-freorder-functions")
#pragma GCC optimize("-findirect-inlining")
#pragma GCC optimize("-fhoist-adjacent-loads")
#pragma GCC optimize("-frerun-cse-after-loop")
#pragma GCC optimize("inline-small-functions")
#pragma GCC optimize("-finline-small-functions")
#pragma GCC optimize("-ftree-switch-conversion")
#pragma GCC optimize("-foptimize-sibling-calls")
#pragma GCC optimize("-fexpensive-optimizations")
#pragma GCC optimize("-funsafe-loop-optimizations")
#pragma GCC optimize("inline-functions-called-once")
#pragma GCC optimize("-fdelete-null-pointer-checks")

using namespace std;

#define MIN(a, b)  ((a)<(b)?(a):(b))

int main(int argc, char *argv[]) {
    int count = 0;        /* Local prime count */
    double elapsed_time; /* Parallel execution time */
    int first;        /* Index of first multiple */
    int global_count; /* Global prime count */
    int high_value;   /* Highest value on this proc */
    int id;           /* Process ID number */ //从0开始
    int index;        /* Index of current prime */
    int low_value;    /* Lowest value on this proc */
    char *marked;       /* Portion of 2,...,'n' */
    int n;            /* Sieving from 2, ..., 'n' */
    int p;            /* Number of processes */ //从1开始
    int proc0_size;   /* Size of proc 0's subarray */
    int prime;        /* Current prime */
    int size;         /* Elements in 'marked' */

    int low_id;
    int high_id;

    char *before_marked;

    int L1_cache_size = 32768;
    int L2_cache_size = 262144;//学校262144  本地524288
    int L3_cache_size = 36700160;// 36700160  67108864

    MPI_Init(&argc, &argv);

    /* Start the timer */

    MPI_Comm_rank(MPI_COMM_WORLD, &id);
    MPI_Comm_size(MPI_COMM_WORLD, &p);
    MPI_Barrier(MPI_COMM_WORLD);

    elapsed_time = -MPI_Wtime();

    if (argc != 2) {
        if (!id) printf("Command line: %s <m>\n", argv[0]);
        MPI_Finalize();
        exit(1);
    }
    n = atoi(argv[1]);

    //选前根号n的素数
    int before_n = (int) sqrt((double) n);
    before_marked = (char *) malloc(before_n);
    if (before_marked == NULL) {
        printf("Cannot allocate enough memory \n");
        MPI_Finalize();
        exit(1);
    }
    memset(before_marked, 0, before_n);
    index = 0;
    prime = 3;
    do {
        //最小值为3，一定满足prime * prime > low_value
        first = (prime * prime - 3) / 2;
        // 标记该素数的倍数为非素数
        for (register int i = first; i < before_n; i += prime) {
            before_marked[i] = 1;
        }
        while (before_marked[++index]);
        prime = index * 2 + 3;
    } while (prime * prime <= before_n);


    //选所有素数
    int N = (n - 1) / 2;
    //按照块分配数据，先去除1，从2开始计算
    int least = N % p;
    //剩下几个数不满足都分配到
    //long long 用于防止运算溢出，在1e9出现，若要测试更大数据会爆int
    low_id = (long long) id * N / p;
    high_id = (long long) (id + 1) * N / p - 1;
    low_value = 3 + low_id * 2; //第一个数值
    high_value = 3 + high_id * 2;
    size = high_id - low_id + 1;

    proc0_size = N / p;
    if ((2 + proc0_size) < (int) sqrt((double) n)) {
        if (!id) printf("Too many processes\n");
        MPI_Finalize();
        exit(1);
    }
    //cache优化
    int block_size = L1_cache_size;//实测结果
    int block_num = size / block_size;
    int Block_least = size % block_size;
    int block_id = 0;
    int block_low_id = low_id;
    int block_high_id = block_size + low_id;
    int block_low_value = block_low_id * 2 + 3;
    int block_high_value = block_high_id * 2 + 3;

    if (block_num == 0) block_size = size;
    marked = (char *) malloc(block_size);

    if (marked == NULL) {
        printf("Cannot allocate enough memory\n");
        MPI_Finalize();
        exit(1);
    }

    while (block_id <= block_num) {
        index = 0;
        prime = 3;

        memset(marked, 0, block_size);

        do {
            if (prime * prime > block_low_value)
                first = (prime * prime - block_low_value) / 2;
            else {
                if (!(block_low_value % prime)) first = 0;
                else if (block_low_value % prime % 2 == 0) first = prime - ((block_low_value % prime) / 2);
                    //以27 29 31 33 35为例，5为当前质数，找规律
                    /*
                    * 数		余数		first	5-x		5-余数
                    * 27	2		4		1		3
                    * 29	4		3		2		1
                    * 31	1		2		3		4
                    * 33	3		1		4		2
                    */
                    //得到余数为2的倍数，则直接除2.不然用5-余数再除2.
                else first = (prime - (block_low_value % prime)) / 2;
            }
            //标记
            for (register int i = first; i < block_size; i += prime) marked[i] = 1;
            while (before_marked[++index]);
            prime = index * 2 + 3;
        } while (prime * prime <= block_high_value);
        register int block_count = 0;
        for (register int i = 0; i < block_size; i++) {
            if (!marked[i]) {
                block_count++;
            }
        }
        count += block_count;
        // 处理下一块
        block_id++;
        block_low_id = block_id * block_size + low_id;
        block_high_id = (block_id + 1) * block_size - 1 + low_id;
        block_low_value = block_low_id * 2 + 3;
        block_high_value = block_high_id * 2 + 3;
        if (block_id == block_num) {
            block_high_value = high_value;
            block_high_id = high_id;
            block_size = (block_high_value - block_low_value) / 2 + 1;
        }
    }


    MPI_Reduce(&count, &global_count, 1, MPI_INT, MPI_SUM,
               0, MPI_COMM_WORLD);

    /* Stop the timer */

    elapsed_time += MPI_Wtime();


    /* Print the results */

    if (!id) {
        printf("There are %d primes less than or equal to %d\n",
               global_count + 1, n);
        printf("SIEVE (%d) %10.6f\n", p, elapsed_time);
    }
    MPI_Finalize();
    return 0;
}
