#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#define MAXS 90000

void clpt(float lon, float lat, float loo[MAXS], float laa[MAXS], int sign, int *low, int *high){
    int i, count = 0,low_tmp, high_tmp;
    float pi = 3.14159265352, deg, con;
    float dif_dist = 1000000, dist;
    deg = pi/180.;
    con = cos(lat*deg)*deg*6371;
    for (i = 0;i<sign; i++){    
        dist = sqrt((lon - loo[i])*(lon - loo[i])*con*con + (lat - laa[i])*(lat - laa[i])*6371 * deg * 6371 * deg);
        if (dist < dif_dist) {
            if (count == 0){
                high_tmp = i;
                count++;
            }else if(count == 1){
                count++;
            }else{
                high_tmp = low_tmp;
            }
            low_tmp = i; 
            dif_dist = dist;
        }  
    }
    *low = low_tmp;
    *high = high_tmp;
    return;
}
void intp3D(float lon, float lat, float loo[4], float laa[4], float dp[4], int p, float *depth){
    int i;
    float z_u = 0, z_b = 0;
    for (i = 0; i<=3; i++){
        if (loo[i] != lon || laa[i] != lat){
            z_u = z_u + dp[i]/pow(pow((loo[i] - lon),2) + pow((laa[i] - lat),2), p/2);
            z_b = z_b + 1/pow(pow((loo[i] - lon),2) + pow((laa[i] - lat),2), p/2);
        }else{
            *depth = dp[i];
            return;
        }
    }
    *depth = z_u/z_b;
}