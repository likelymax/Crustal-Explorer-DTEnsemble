#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

float antiform(char velocity[128], char output[128], float lon, float lat, float down, float r){
    float pi = 3.14159265352, R = 6371.;
    float deg = pi/180, vp, dp, vpvs, mhdp, orgdp = 0.1;
    int i = 0, sign;
    int max = 100;
    float depth[max], velp[max], ratio[max];
    FILE *fv, *fo;
    fv = fopen(velocity,"r");
    fo = fopen(output,"w");
    mhdp = -sqrt(r*r - lat*lat - lon*lon) + down;
    if (mhdp > down || mhdp < 0) mhdp = -1;
    while (fscanf(fv, "%f %f %f\n", &dp, &vp, &vpvs) == 3){
        depth[i] = dp;
        velp[i] = vp;
        ratio[i] = vpvs;
        i++;
    }
    sign = i;
    for (i = 0; i < sign; i ++){
        if (i <= sign - 3){
            if (orgdp < depth[i] && depth[i] >= mhdp){
                fprintf(fo, "%f %f %f\n", mhdp, velp[sign-2], ratio[sign-2]);
                fprintf(fo, "%f %f %f\n", mhdp + 1, velp[sign-1], ratio[sign-1]);
                break;
            }else{
                fprintf(fo, "%f %f %f\n", depth[i], velp[i], ratio[i]);
            }
        }else{
            fprintf(fo, "%f %f %f\n", mhdp, velp[sign-2], ratio[sign-2]);
            fprintf(fo, "%f %f %f\n", mhdp + 1, velp[sign-1], ratio[sign-1]);
            break;
        }
        orgdp = depth[i];
    }
    fclose(fo);
    fclose(fv);
    return mhdp;
}
