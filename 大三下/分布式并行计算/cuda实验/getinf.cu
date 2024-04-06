#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
int main()
{
    int deviceCount;
    cudaGetDeviceCount(&deviceCount);
    int dev;
    for (dev = 0; dev < deviceCount; dev++)
    {
        cudaDeviceProp deviceProp;
        cudaGetDeviceProperties(&deviceProp, dev);
        if (dev == 0)
        {
            if (/*deviceProp.major==9999 && */deviceProp.minor = 9999 && deviceProp.major == 9999)
                printf("\n");

        }
        printf("\nDevice%d:\"%s\"\n", dev, deviceProp.name);
        printf("Total amount of global memory                   %zu bytes\n", deviceProp.totalGlobalMem);
        printf("Number of mltiprocessors                        %d\n", deviceProp.multiProcessorCount);
        printf("Total amount of constant memory:                %zu bytes\n", deviceProp.totalConstMem);
        printf("Total amount of shared memory per block         %zu bytes\n", deviceProp.sharedMemPerBlock);
        printf("Total number of registers available per block:  %d\n", deviceProp.regsPerBlock);
        printf("Warp size                                       %d\n", deviceProp.warpSize);
        printf("Maximum number of threada per block:            %d\n", deviceProp.maxThreadsPerBlock);
        printf("Maximum sizes of each dimension of a block:     %d x %d x %d\n", deviceProp.maxThreadsDim[0],
            deviceProp.maxThreadsDim[1],
            deviceProp.maxThreadsDim[2]);
        printf("Maximum size of each dimension of a grid:       %d x %d x %d\n", deviceProp.maxGridSize[0], deviceProp.maxGridSize[1], deviceProp.maxGridSize[2]);
        printf("Maximum memory pitch :                          %zu bytes\n", deviceProp.memPitch);
        printf("Texture alignmemt                               %zu bytes\n", deviceProp.texturePitchAlignment);
        printf("Clock rate                                      %.2f GHz\n", deviceProp.clockRate * 1e-6f);
    }
    printf("\nTest PASSED\n");
    getchar();
}