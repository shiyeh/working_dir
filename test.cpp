#include <iostream>
#define SQUARE(x) (x * x)

int main() {
    // int a = SQUARE(2);
    // int b = SQUARE(a++);
    // int c = SQUARE(a + b);
    // std::cout << a << " " << b << " " << c << std::endl;

    // int n = 5;
    // void *p = &n;
    // int *pi = static_cast<int*>(p);
    // ++*pi;
    // std::cout << *pi << std::endl;

    // int i = 4;
    // int j = i++;
    // int k = ++j;
    // std::cout << i << j << k << std::endl;

    int arr[] = {1, 2, 3, 4};
    int* p = arr;
    int* k = p;
    std::cout << (*(k + 2) + 1[p] + *(0 + arr)) << std::endl;

    return 0;
}
