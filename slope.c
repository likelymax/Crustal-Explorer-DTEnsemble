#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

float slope(char velocity[128], char output[128], float lon, float lat, float alpha1, float alpha2, float cdp){
    float pi = 3.14159265352, R = 6371.;
    float deg = pi/180, vp, dp, vpvs;
    float a = tan(alpha1 * deg), dist, del_dp, mhdp = 0, orgdp = 0.0;
    int i = 0, sign;
    int max = 100;
    float depth[max], velp[max], ratio[max];
    FILE *fv, *fo;
    fv = fopen(velocity,"r");
    fo = fopen(output,"w");
    dist = (a *lon - lat)/sqrt(a*a + 1);
    del_dp = sin(alpha2 * deg) * dist;
    mhdp = cdp - del_dp;
    if (mhdp > 10){
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
    }else{
        printf("moho depth is too shallow\n");
    }
    fclose(fo);
    fclose(fv);
    return mhdp;
}