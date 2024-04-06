#include "mpi.h"
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <string.h>

using namespace std;

#define MIN(a, b)  ((a)<(b)?(a):(b))

int main2(int argc, char *argv[]) {
    int count;        /* Local prime count */
    double elapsed_time; /* Parallel execution time */
    int first;        /* Index of first multiple */
    int global_count; /* Global prime count */
    int high_value;   /* Highest value on this proc */
    int i;
    int id;           /* Process ID number */ //从0开始
    int index;        /* Index of current prime */
    int low_value;    /* Lowest value on this proc */
    char *marked;       /* Portion of 2,...,'n' */
    int n;            /* Sieving from 2, ..., 'n' */
    int p;            /* Number of processes */ //从1开始
    int proc0_size;   /* Size of proc 0's subarray */
    int prime;        /* Current prime */
    int size;         /* Elements in 'marked' */

    int low_id;          /* Lowest index on this proc */
    int high_id;         /* Highest index on this proc */

    char *before_marked;       /* before_mark array */


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

    /* Figure out this process's share of the array, as
       well as the integers represented by the first and
       last array elements */

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
        //标记该素数的倍数为非素数
        for (int i = first; i < before_n; i += prime) {
            before_marked[i] = 1;
        }
        while (before_marked[++index]);
        prime = index * 2 + 3;
    } while (prime * prime <= before_n);


    //选所有素数
    int N = (n - 1) / 2;//按照块分配数据，先去除1，从2开始计算
    int least = N % p;//剩下几个数不满足都分配到
    low_id = (long long) id * (N / p) + MIN(id, least);
    high_id = (long long) (id + 1) * (N / p) + MIN(id + 1, least) - 1;
    low_value = 3 + low_id * 2; //第一个数值
    high_value = 3 + high_id * 2;
    size = high_id - low_id + 1;

    /* Bail out if all the primes used for sieving are
       not all held by process 0 */

    proc0_size = N / p;

    if ((2 + proc0_size) < (int) sqrt((double) n)) {
        if (!id) printf("Too many processes\n");
        MPI_Finalize();
        exit(1);
    }
    /* Allocate this process's share of the array. */

    marked = (char *) malloc(size);

    if (marked == NULL) {
        printf("Cannot allocate enough memory\n");
        MPI_Finalize();
        exit(1);
    }

    memset(marked, 0, size);

    index = 0;
    prime = 3;
    do {
        if (prime * prime > low_value)
            first = (prime * prime - low_value) / 2;
        else {
            // 若low_value为该素数的倍数，则第一个倍数为low_value
            if (!(low_value % prime)) first = 0;
            else if (low_value % prime % 2 == 0) first = prime - ((low_value % prime) / 2);
                //以27 29 31 33 35为例，5为当前质数，找规律
                /*
                * 数	余数	first	5-x		5-余数
                * 27	2		4		1		3
                * 29	4		3		2		1
                * 31	1		2		3		4
                * 33	3		1		4		2
                */
                //得到余数为2的倍数，则直接除2.不然用5-余数再除2.
            else first = (prime - (low_value % prime)) / 2;
        }
        // 标记该素数的倍数为非素数
        for (i = first; i < size; i += prime) marked[i] = 1;
        //找到下一素数的位置
        while (before_marked[++index]);
        prime = index * 2 + 3;
    } while (prime * prime <= n);

    count = 0;
    for (i = 0; i < size; i++)
        if (!marked[i]) count++;
    if (p > 1)
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
