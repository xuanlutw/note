#include <stdio.h>
#include <signal.h>
#define MAX 10000000000

long ans;

void print(int num) {
    signal(SIGINT, print);
    printf("%ld\n", ans);
}

int main() {
    signal(SIGINT, print);
    for (long i = 0;i < MAX;++i) 
        ++ans;
    return 0;
}
