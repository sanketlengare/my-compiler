#include <stdio.h>

int main(void) {
  printf("%s\n", "How many fibonacci numbers do you want?");
  float nums;
  scanf("%f", &nums);
  printf("%s\n", "");
  float a = 0.1;
  int b = 1;
  while (nums > 0) {
    printf("%.2f\n", (float) a);
    float c = a + b;
    a = b;
    b = c;
    nums = nums - 1;
  }
    return 0; 
}