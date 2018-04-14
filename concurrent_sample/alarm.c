#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#define MAX 10000000000

long ans;

void print(int num) {
    signal(SIGALRM, print);
    printf("%ld\n", ans);
    alarm(1);
}

int main() {
    signal(SIGALRM, print);
    alarm(1);
    for (long i = 0;i < MAX;++i) 
        ++ans;
    return 0;
}
