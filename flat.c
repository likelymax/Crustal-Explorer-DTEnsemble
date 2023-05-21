#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

float flat(char velocity[128], char output[128], float mhdp){
    FILE *fv, *fo;
    float dp, vp, vpvs, orgdp;
    int max = 100, i = 0, sign;
    fv = fopen(velocity, "r");
    fo = fopen(output,"w");
    orgdp = 0.00;
    float depth[max], velp[max], ratio[max];
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