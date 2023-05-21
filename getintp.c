#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include "Intp.h"
#define MAX 400000

void getintp(float m_lon[MAX], float m_lat[MAX], float M_rho[MAX], float slon, float slat, int sign, float *output){
    int i;
    float mdensity, dp_intp;
    float loo_tmp[4], laa_tmp[4], rho_tmp[4];
    i = 0;
    int low, high;
    clpt(slon, slat, m_lon, m_lat, sign, &low, &high);
    loo_tmp[0] = m_lon[low + 1];
    loo_tmp[1] = m_lon[low];
    loo_tmp[2] = m_lon[high];
    loo_tmp[3] = m_lon[high - 1];
    laa_tmp[0] = m_lat[low + 1];
    laa_tmp[1] = m_lat[low];
    laa_tmp[2] = m_lat[high];
    laa_tmp[3] = m_lat[high - 1];
    rho_tmp[0] = M_rho[low + 1];
    rho_tmp[1] = M_rho[low];
    rho_tmp[2] = M_rho[high];
    rho_tmp[3] = M_rho[high - 1];
    intp3D(slon, slat, loo_tmp, laa_tmp, rho_tmp, 4, &dp_intp);
    *output = dp_intp;
}