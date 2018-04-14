#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#define MAX 10000000000

void* print(void* ans) {
    while(1) {
        printf("%ld\n", *(long*)ans);
        sleep(1);
    }
    return NULL;
}

int main() {
    long ans = 0;
    pthread_t tid;
    pthread_create(&tid, NULL, print, &ans);
    for (long i = 0;i < MAX;++i) 
        ++ans;
    return 0;
}
