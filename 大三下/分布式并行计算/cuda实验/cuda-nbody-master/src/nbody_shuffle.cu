#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "timer.h"
#include "check.h"
#include <cuda_runtime.h>

#define SOFTENING 1e-9f
#define BLOCK_SIZE 32
#define BLOCK_STRIDE 32

typedef struct
{
    float x, y, z, vx, vy, vz;
} Body;

void randomizeBodies(float *data, int n)
{
    for (int i = 0; i < n; i++)
    {
        data[i] = 2.0f * (rand() / (float)RAND_MAX) - 1.0f;
    }
}

__global__ void bodyForce(Body *p, float dt, int n)
{

    // int i = threadIdx.x + blockIdx.x * blockDim.x;
    int cycle_times = n / BLOCK_SIZE;
    // 计算要处理的数据index
    int i = threadIdx.x + (int)(blockIdx.x / BLOCK_STRIDE) * blockDim.x;
    // 此块对应要处理的数据块的起始位置
    int start_block = blockIdx.x % BLOCK_STRIDE;
    if (i < n)
    {
        Body ptemp = p[i];
        Body temp;
        float share_x,share_y,share_z;
        float dx, dy, dz, distSqr, invDist, invDist3;
        float Fx = 0.0f;
        float Fy = 0.0f;
        float Fz = 0.0f;
        // 这里的cycle_times 在已知块大小时使用常数性能会高一些
        for (int block_num = start_block; block_num < cycle_times; block_num += BLOCK_STRIDE)
        {
            temp = p[block_num * BLOCK_SIZE + threadIdx.x];
            share_x = temp.x;
            share_y = temp.y;
            share_z = temp.z;
            // 编译优化，只有 BLOCK_SIZE 为常量时才有用
#pragma unroll
            for (int j = 0; j < BLOCK_SIZE; j++)
            {
                dx = __shfl_sync(0xFFFFFFFF,share_x,j) - ptemp.x;
                dy = __shfl_sync(0xFFFFFFFF,share_y,j) - ptemp.y;
                dz = __shfl_sync(0xFFFFFFFF,share_z,j) - ptemp.z;
                distSqr = dx * dx + dy * dy + dz * dz + SOFTENING;
                invDist = rsqrtf(distSqr);
                invDist3 = invDist * invDist * invDist;
                Fx += dx * invDist3;
                Fy += dy * invDist3;
                Fz += dz * invDist3;
            }
            // 块内同步，防止spos提前被写入
            __syncthreads();
        }
        // 块之间不同步，原子加保证正确性
        atomicAdd(&p[i].vx, dt * Fx);
        atomicAdd(&p[i].vy, dt * Fy);
        atomicAdd(&p[i].vz, dt * Fz);
        // p[i].vx += dt * Fx;
        // p[i].vy += dt * Fy;
        // p[i].vz += dt * Fz;
    }
}

__global__ void integrate_position(Body *p, float dt, int n)
{
    int i = threadIdx.x + blockIdx.x * blockDim.x;
    if (i < n)
    {
        p[i].x += p[i].vx * dt;
        p[i].y += p[i].vy * dt;
        p[i].z += p[i].vz * dt;
    }
}

int main(const int argc, const char **argv)
{

    int nBodies = 2 << 11;
    int salt = 0;
    if (argc > 1)
        nBodies = 2 << atoi(argv[1]);

    /*
   * This salt is for assessment reasons. Tampering with it will result in automatic failure.
   */

    if (argc > 2)
        salt = atoi(argv[2]);

    const float dt = 0.01f; // time step
    const int nIters = 10;  // simulation iterations

    int bytes = nBodies * sizeof(Body);
    float *buf;
    cudaMallocHost(&buf, bytes);

    randomizeBodies(buf, 6 * nBodies); // Init pos / vel data

    double totalTime = 0.0;

    int deviceId;
    cudaGetDevice(&deviceId);

    size_t threadsPerBlock = BLOCK_SIZE;
    size_t numberOfBlocks = (nBodies + threadsPerBlock - 1) / threadsPerBlock;

    float *d_buf;
    cudaMalloc(&d_buf, bytes);
    Body *d_p = (Body *)d_buf;
    /*
   * This simulation will run for 10 cycles of time, calculating gravitational
   * interaction amongst bodies, and adjusting their positions to reflect.
   */

    cudaMemcpy(d_buf, buf, bytes, cudaMemcpyHostToDevice);
    /*******************************************************************/
    // Do not modify these 2 lines of code.gg
    for (int iter = 0; iter < nIters; iter++)
    {
        StartTimer();
    /*******************************************************************/

        /*
        * You will likely wish to refactor the work being done in `bodyForce`,
        * as well as the work to integrate the positions.
        */
        bodyForce<<<numberOfBlocks * BLOCK_STRIDE, threadsPerBlock>>>(d_p, dt, nBodies); // compute interbody forces
        /*
        * This position integration cannot occur until this round of `bodyForce` has completed.
        * Also, the next round of `bodyForce` cannot begin until the integration is complete.
        */
        integrate_position<<<nBodies / threadsPerBlock, threadsPerBlock>>>(d_p, dt, nBodies);

        if (iter == nIters - 1)
        {
            cudaMemcpy(buf, d_buf, bytes, cudaMemcpyDeviceToHost);
        }

    /*******************************************************************/
    // Do not modify the code in this section.
        const double tElapsed = GetTimer() / 1000.0;
        totalTime += tElapsed;
    }

    double avgTime = totalTime / (double)(nIters);
    float billionsOfOpsPerSecond = 1e-9 * nBodies * nBodies / avgTime;

#ifdef ASSESS
    checkPerformance(buf, billionsOfOpsPerSecond, salt);
#else
    checkAccuracy(buf, nBodies);
    printf("%d Bodies: average %0.3f Billion Interactions / second\n", nBodies, billionsOfOpsPerSecond);
    salt += 1;
#endif
    /*******************************************************************/

    /*
   * Feel free to modify code below.
   */
    cudaFree(d_buf);
    cudaFreeHost(buf);
}
