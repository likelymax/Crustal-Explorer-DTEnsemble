#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "moho.h"

int main (int argc, char **argv) {
    int i, error = 0, type_f= 0;
    float mhdp, lon, lat, alpha, up, down, alpha1, alpha2, cdp, newdp, r, az, moho_bot, moho_top, clon, clat;
    char type[50], velocity[128], output[128], dpth[128];
    FILE *fd;
    for (i=1; !error && i < argc; i++) {
        // printf("i is %d\n", i);
        if (argv[i][0] == '-') {
            switch(argv[i][1]) {
                case 'P':
                    sscanf(&argv[i][2],"%s",type);
                    break;
                case 'V':
                    strcpy(velocity,&argv[i][2]);
                    type_f = 1;
                    break;
                case 'O':
                    strcpy(output,&argv[i][2]);
                    break;
                case 'D':
                    strcpy(dpth, &argv[i][2]);
                    fd = fopen(dpth, "w");
                    break;
            }
        }
    }
    if (strcmp(type, "flat") == 0){
        printf("type is %s\n", type);
        if (type_f == 1){
            for (i=1; !error && i < argc; i++) {
                if (argv[i][0] == '-') {
                    if (argv[i][1] == 'T'){
                        sscanf(&argv[i][2],"%f\n", &mhdp);
                    }
                }
            }
        }
        newdp = flat(velocity, output, mhdp);
    }else if (strcmp(type, "offset") == 0){
        printf("type is %s\n", type);
        for (i=1; !error && i < argc; i++) {
            if (argv[i][0] == '-') {
                if (argv[i][1] == 'T'){
                    sscanf(&argv[i][2],"%f/%f/%f/%f/%f\n", &alpha, &up, &down, &lon, &lat);
                }
            }
        }
        newdp = offset(velocity, output, lon, lat, alpha, up, down);
    }else if (strcmp(type, "slope") == 0){
        printf("type is %s\n", type);
        for (i=1; !error && i < argc; i++) {
            if (argv[i][0] == '-') {
                if (argv[i][1] == 'T'){
                    sscanf(&argv[i][2],"%f/%f/%f/%f/%f\n", &alpha1, &alpha2, &cdp, &lon, &lat);
                }
            }
        }  
        newdp = slope(velocity, output, lon, lat, alpha1, alpha2, cdp);      
    }else if (strcmp(type, "antiform") == 0){
        printf("type is %s\n", type);
        for (i=1; !error && i < argc; i++) {
            if (argv[i][0] == '-') {
                if (argv[i][1] == 'T'){
                    sscanf(&argv[i][2],"%f/%f/%f/%f\n", &lon, &lat, &down, &r);
                }
            }
        }  
        newdp = antiform(velocity, output, lon, lat, down, r);
    }else if (strcmp(type, "synform") == 0){
        printf("type is %s\n", type);
        for (i=1; !error && i < argc; i++) {
            if (argv[i][0] == '-') {
                if (argv[i][1] == 'T'){
                    sscanf(&argv[i][2],"%f/%f/%f/%f\n", &lon, &lat, &up, &r);
                }
            }
        } 
        newdp = synform(velocity, output, lon, lat, up, r);
    }else if (strcmp(type, "fault") == 0){
        printf("type is %s\n", type);
        for (i=1; !error && i < argc; i++) {
            if (argv[i][0] == '-') {
                if (argv[i][1] == 'T'){
                    sscanf(&argv[i][2],"%f/%f/%f/%f/%f/%f/%f/%f\n", &az, &clon, &clat, &moho_top, &moho_bot, &lon, &lat, &r);
                }
            }
        }
        newdp = fault(velocity, output, az, clon, clat, lon, lat, moho_top, moho_bot, r);
    }
    fprintf(fd, "%f\n", newdp);
    fclose(fd);
}
