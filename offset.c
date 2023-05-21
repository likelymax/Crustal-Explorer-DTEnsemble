#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

float offset(char velocity[128], char output[128], float lon, float lat, float alpha, float up, float down){
    float pi = 3.14159265352, R = 6371.;
    float deg = pi/180;
    float a = alpha * deg;
    float dp, vp, vpvs, angle, a_max, mhdp = 0, orgdp = 0.0;
    int max = 100;
    float depth[max], velp[max], ratio[max];
    printf("a is %f\n", a);
    // printf("%f %f\n", lon, lat);
    int i = 0, sign;
    FILE *fv, *fo;
    fv = fopen(velocity,"r");
    fo = fopen(output,"w");
    a_max = a + pi;
    if (lon > 0 && lat < 0){
        angle = -fabs(atan(lon/lat)) + pi;
    }else if (lon < 0 && lat < 0){
        angle = fabs(atan(lon/lat)) + pi;
    }else if (lon < 0 && lat > 0){
        angle = -fabs(atan(lon/lat));
    }else if (lon > 0 && lat == 0){
        angle = pi/2;
    }else if (lon < 0 && lat == 0){
        angle = -pi/2;
    }else if (lon == 0 && lat > 0){
        angle = 0;
    }else if (lon == 0 && lat < 0){
        angle = pi;
    }else{
        angle = fabs(atan(lon/lat));
    }
    if ((angle >= a && angle <= a_max)||(angle + 2*pi >= a && angle + 2*pi <= a_max)||(angle - 2*pi >= a && angle - 2*pi <= a_max)){
        mhdp = up;
    }else{
        mhdp = down;
    }
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