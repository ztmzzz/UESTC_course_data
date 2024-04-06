#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "timer.h"
#include "check.h"
#include <cuda_runtime.h>
//32 64 96 128 160 192 224 256
#define SOFTENING 1e-9f
#define BLOCK_SIZE 64
#define BLOCK_STRIDE 32
/*
 * Each body contains x, y, and z coordinate positions,
 * as well as velocities in the x, y, and z directions.
 */

typedef struct {
    float4 *pos, *vel;
} Body;

/*
 * Do not modify this function. A constraint of this exercise is
 * that it remain a host function.
 */

void randomizeBodies(float *data, int n) {
    for (int i = 0; i < n; i++) {
        data[i] = 2.0f * (rand() / (float) RAND_MAX) - 1.0f;
    }
}

/*
 * This function calculates the gravitational impact of all bodies in the system
 * on all others, but does not update their positions.
 */

__global__
void bodyForce(float4 *p, float4 *v, float dt, int n) {
    int id = threadIdx.x + blockDim.x * (int) (blockIdx.x / BLOCK_STRIDE);
    if (id < n) {
        int block_start = blockIdx.x % BLOCK_STRIDE;
        int total_block = n / BLOCK_SIZE;
        float Fx = 0.0f;
        float Fy = 0.0f;
        float Fz = 0.0f;
        float dx, dy, dz, distSqr, invDist, invDist3;
        float4 temp;
        __shared__ float3 spos[BLOCK_SIZE];
        float4 p_temp = p[id];
        for (int block_id = block_start; block_id < total_block; block_id += BLOCK_STRIDE) {
            //写入共享内存
            temp = p[block_id * BLOCK_SIZE + threadIdx.x];
            spos[threadIdx.x] = make_float3(temp.x, temp.y, temp.z);
            __syncthreads();

#pragma unroll 32
            for (int j = 0; j < BLOCK_SIZE; ++j) {
                dx = spos[j].x - p_temp.x;
                dy = spos[j].y - p_temp.y;
                dz = spos[j].z - p_temp.z;
                distSqr = dx * dx + dy * dy + dz * dz + SOFTENING;
                invDist = rsqrtf(distSqr);
                invDist3 = invDist * invDist * invDist;

                Fx += dx * invDist3;
                Fy += dy * invDist3;
                Fz += dz * invDist3;
            }
            __syncthreads();
        }
        atomicAdd(&v[id].x, dt * Fx);
        atomicAdd(&v[id].y, dt * Fy);
        atomicAdd(&v[id].z, dt * Fz);
    }
}

__global__ void change_pos(float4 *p, float4 *v, float dt, int n) {
    int i = threadIdx.x + blockDim.x * blockIdx.x;
    if (i < n) {
        p[i].x += v[i].x * dt;
        p[i].y += v[i].y * dt;
        p[i].z += v[i].z * dt;
    }
}

int main(const int argc, const char **argv) {

    /*
 * Do not change the value for `nBodies` here. If you would like to modify it,
 * pass values into the command line.
 */

    int nBodies = 2 << 11;
    int salt = 0;
    if (argc > 1) nBodies = 2 << atoi(argv[1]);

    /*
     * This salt is for assessment reasons. Tampering with it will result in automatic failure.
     */

    if (argc > 2) salt = atoi(argv[2]);

    const float dt = 0.01f; // time step
    const int nIters = 10;  // simulation iterations

    int bytes = 2 * nBodies * sizeof(float4);
    float *buf;

    cudaMallocHost(&buf, bytes);

    size_t Block_num = (nBodies + BLOCK_SIZE - 1) / BLOCK_SIZE;

    /*
  * As a constraint of this exercise, `randomizeBodies` must remain a host function.
  */

    float *temp_buf = (float *) malloc(nBodies * sizeof(float) * 6);
    randomizeBodies(temp_buf, 6 * nBodies); // Init pos / vel data
    //buf转换成我定义的格式
    int idx = 0;
    for (int i = 0; i < 4 * nBodies; i++) {
        if ((i + 1) % 4 == 0) {
            buf[i] = 0;
            idx += 3;
            continue;
        }
        buf[i] = temp_buf[idx++];
    }
    idx = 3;
    for (int i = 4 * nBodies; i < 8 * nBodies; i++) {
        if ((i + 1) % 4 == 0) {
            buf[i] = 0;
            idx += 3;
            continue;
        }
        buf[i] = temp_buf[idx++];
    }

    double totalTime = 0.0;

    float *device_buf;
    cudaMalloc(&device_buf, bytes);
    Body d_p = {(float4 *) device_buf, ((float4 *) device_buf) + nBodies};
    cudaMemcpy(device_buf, buf, bytes, cudaMemcpyHostToDevice);

    /*
     * This simulation will run for 10 cycles of time, calculating gravitational
     * interaction amongst bodies, and adjusting their positions to reflect.
     */

    /*******************************************************************/
    // Do not modify these 2 lines of code.
    for (int iter = 0; iter < nIters; iter++) {
        StartTimer();
        /*******************************************************************/

        /*
         * You will likely wish to refactor the work being done in `bodyForce`,
         * as well as the work to integrate the positions.
         */

        bodyForce<<<Block_num * BLOCK_STRIDE, BLOCK_SIZE>>>(d_p.pos, d_p.vel, dt, nBodies); // compute interbody forces

        /*
         * This position integration cannot occur until this round of `bodyForce` has completed.
         * Also, the next round of `bodyForce` cannot begin until the integration is complete.
         */

        change_pos<<<Block_num, BLOCK_SIZE>>>(d_p.pos, d_p.vel, dt, nBodies);

        if (iter == nIters - 1)
//            cudaDeviceSynchronize();
            cudaMemcpy(buf, device_buf, bytes, cudaMemcpyDeviceToHost);

        /*******************************************************************/
        // Do not modify the code in this section.
        const double tElapsed = GetTimer() / 1000.0;
        totalTime += tElapsed;
    }

    //把我的格式转换成老师的
    Body temp = {(float4 *) buf, ((float4 *) buf) + nBodies};
    for (int i = 0; i < nBodies; i++) {
        temp_buf[i * 6] = temp.pos[i].x;
        temp_buf[i * 6 + 1] = temp.pos[i].y;
        temp_buf[i * 6 + 2] = temp.pos[i].z;
        temp_buf[i * 6 + 3] = temp.vel[i].x;
        temp_buf[i * 6 + 4] = temp.vel[i].y;
        temp_buf[i * 6 + 5] = temp.vel[i].z;
    }
    buf = temp_buf;

    double avgTime = totalTime / (double) (nIters);
    float billionsOfOpsPerSecond = 1e-9 * nBodies * nBodies / avgTime;

#ifdef ASSESS
    checkPerformance(buf, billionsOfOpsPerSecond, salt);
#else
    checkAccuracy(buf, nBodies);
    printf("%d Bodies: average %0.3f Billion Interactions / second\n", nBodies, billionsOfOpsPerSecond);
//    printf("%0.3f\n", billionsOfOpsPerSecond);
    salt += 1;
#endif
    /*******************************************************************/

    /*
     * Feel free to modify code below.
     */

    cudaFree(buf);
    cudaFree(device_buf);
}