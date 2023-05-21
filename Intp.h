#define MAXS 15000000
#ifndef _INTP_
    #define _INTP_
    void clpt(float lon, float lat, float loo[MAXS], float laa[MAXS], int sign, int *low, int *high);
	void intp3D(float lon, float lat, float loo[4], float laa[4], float dp[4], int p, float *depth);
#endif 
	