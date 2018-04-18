#include <stdio.h>
#include <unistd.h>
#include <termios.h>

#define FG_BLACK        "30"
#define FG_RED          "31"
#define FG_GREEN        "32"
#define FG_YELLOW       "33"
#define FG_BLUE         "34"
#define FG_PURPLE       "35"
#define FG_CYAN         "36"
#define FG_WHITE        "37"
#define FG_LIGHT_BLACK  "90"
#define FG_LIGHT_RED    "91"
#define FG_LIGHT_GREEN  "92"
#define FG_LIGHT_YELLOW "93"
#define FG_LIGHT_BLUE   "94"
#define FG_LIGHT_PURPLE "95"
#define FG_LIGHT_CYAN   "96"
#define FG_LIGHT_WHITE  "97"

#define BG_BLACK        "40"
#define BG_RED          "41"
#define BG_GREEN        "42"
#define BG_YELLOW       "43"
#define BG_BLUE         "44"
#define BG_PURPLE       "45"
#define BG_CYAN         "46"
#define BG_WHITE        "47"
#define BG_LIGHT_BLACK  "100"
#define BG_LIGHT_RED    "101"
#define BG_LIGHT_GREEN  "102"
#define BG_LIGHT_YELLOW "103"
#define BG_LIGHT_BLUE   "104"
#define BG_LIGHT_PURPLE "105"
#define BG_LIGHT_CYAN   "106"
#define BG_LIGHT_WHITE  "107"

#define BOLD            "1"
#define UNDERLINE       "4"
#define BLINK           "6"
#define RESET           "0"

#define set_feature(x) printf("\033[%sm", (x))


#define cusor_up(x)         printf("\033[%dA", (x));fflush(stdout)
#define cusor_down(x)       printf("\033[%dB", (x));fflush(stdout)
#define cusor_forward(x)    printf("\033[%dC", (x));fflush(stdout)
#define cusor_back(x)       printf("\033[%dD", (x));fflush(stdout)
#define cusor_next_l(x)     printf("\033[%dE", (x));fflush(stdout)
#define cusor_pre_l(x)      printf("\033[%dF", (x));fflush(stdout)
#define cusor_set_col(x)    printf("\033[%dG", (x));fflush(stdout)
#define cusor_set(x, y)     printf("\033[%d;%dH", (x), (y));fflush(stdout)
#define cusor_save()        printf("\033[s");fflush(stdout)
#define cusor_restore()     printf("\033[u");fflush(stdout)


#define erase_display_b()   printf("\033[0J");fflush(stdout)
#define erase_display_f()   printf("\033[1J");fflush(stdout)
#define erase_display_all() printf("\033[3J");fflush(stdout)
#define erase_display_al()  printf("\033[2J");fflush(stdout)   // no erase catch
#define erase_line_b()      printf("\033[0K");fflush(stdout)
#define erase_line_f()      printf("\033[1K");fflush(stdout)
#define erase_line_all()    printf("\033[2K");fflush(stdout)
#define scroll_up()         printf("\033[S");fflush(stdout)
#define scroll_down()       printf("\033[T");fflush(stdout)

int cusor_row() {
    static struct termios term, oterm;
    char c;
    int row = 0;
    tcgetattr(0, &oterm);
    term = oterm;
    term.c_lflag &= ~(ICANON | ECHO);
    term.c_cc[VMIN] = 1;
    term.c_cc[VTIME] = 0;
    tcsetattr(0, TCSANOW, &term);
    printf("\033[6n");                      
    fflush(stdout);                         
    c = getchar();  // esc
    c = getchar();  // [
    while ((c = getchar()) != ';')
        row = row * 10 + c - '0';
    while ((c = getchar()) != 'R');
    tcsetattr(0, TCSANOW, &oterm);
    return row;
}

int cusor_col() {
    static struct termios term, oterm;
    char c;
    int col = 0;
    tcgetattr(0, &oterm);
    term = oterm;
    term.c_lflag &= ~(ICANON | ECHO);
    term.c_cc[VMIN] = 1;
    term.c_cc[VTIME] = 0;
    tcsetattr(0, TCSANOW, &term);
    printf("\033[6n");                      
    fflush(stdout);                         
    c = getchar();  // esc
    c = getchar();  // [
    while ((c = getchar()) != ';');
    while ((c = getchar()) != 'R')
        col = col * 10 + c - '0';
    tcsetattr(0, TCSANOW, &oterm);
    return col;
}

int main() {
    // 4 bits test
    set_feature(FG_LIGHT_RED);
    set_feature(BG_BLUE);
    printf("Test\n");
    set_feature(FG_LIGHT_YELLOW);
    set_feature(BG_PURPLE);
    set_feature(BOLD);
    printf("Test\n");
    set_feature(FG_LIGHT_CYAN);
    set_feature(BG_WHITE);
    set_feature(BLINK);
    printf("Test\n");
    set_feature(FG_BLACK);
    set_feature(BG_LIGHT_GREEN);
    set_feature(UNDERLINE);
    printf("Test\n");
    set_feature(RESET);
    // 8 bits bg test
    for (int i = 0;i < 16;++i) {
        printf("\033[0;48;5;%dm", i);
        printf(" ");
    }
    printf("\n");
    for (int i = 232;i < 256;++i) {
        printf("\033[0;48;5;%dm", i);
        printf(" ");
    }
    for (int i = 16;i < 232;++i) {
        if ((i - 16) % 36 == 0) printf("\n");
        printf("\033[0;48;5;%dm", i);
        printf(" ");
    }
    printf("\n");
    // 8 bits fg test
    for (int i = 0;i < 16;++i) {
        printf("\033[0;38;5;%dm", i);
        printf("O");
    }
    printf("\n");
    for (int i = 232;i < 256;++i) {
        printf("\033[0;38;5;%dm", i);
        printf("O");
    }
    for (int i = 16;i < 232;++i) {
        if ((i - 16) % 36 == 0) printf("\n");
        printf("\033[0;38;5;%dm", i);
        printf("O");
    }
    printf("\n");
    // 24 bits has some problem
    // printf("\033[0;38;2;%d:%d:%dm", r, g, b);
    // Cursor test
    cusor_save();        
    sleep(1);
    cusor_up(7);        
    putchar('a');
    sleep(1);
    cusor_down(3);      
    putchar('b');
    sleep(1);
    cusor_forward(7);   
    putchar('c');
    sleep(1);
    cusor_back(4);   
    putchar('d');      
    sleep(1);
    cusor_next_l(2);
    putchar('e');      
    sleep(1);
    cusor_pre_l(12);
    putchar('f');      
    sleep(1);
    //cusor_set_col(11);
    putchar('g');      
    sleep(1);
    cusor_restore();   
    putchar('h');      
    sleep(1);
    cusor_set(18, 12);   
    putchar('i');      
    sleep(1);
    erase_line_b();
    sleep(1);
    erase_line_f();
    sleep(1);
    erase_line_all();
    sleep(1);
    scroll_up();
    sleep(1);
    scroll_down();
    sleep(1);
    erase_display_b();
    sleep(1);
    erase_display_f();
    sleep(1);
    erase_display_all();
    sleep(1);
    printf("row = %d, col = %d\n", cusor_row(), cusor_col());
 	return 0;
}
