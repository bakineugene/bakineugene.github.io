---
title: "Cpp"
date: 2025-09-15
author: Eugene
tags: ['cpp', 'vim']
summary: "*11:44* TIL: В плюсах происходит неявное преобразование к необходимому классу, если есть подходящий конструктор. P.S."
---

*11:44*  
TIL:

В плюсах происходит неявное преобразование к необходимому классу, если есть подходящий конструктор.

```c++
#include <iostream>

class A {
public:
    A() : a(0) {};
    A(int input) : a{input} {};

    int a{};
};

int main() {

    A a_1{};
    A a_2{1};
    A a_3 = 2;

    std::cout << a_1.a << " " << a_2.a << " " << a_3.a;

    return 0;
}
```

```bash
/tmp/cpp_1$ g++ ./main.cpp && ./a.out 
0 1 2
```

P.S. А чтобы запретить ипользовать конструктор для таких неявных преобразований нужно объявить его как `explicit`

```
explicit A(int input) : a{input} {};
```

```bash
$ g++ ./main.cpp && ./a.out 
./main.cpp: In function ‘int main()’:
./main.cpp:17:13: error: conversion from ‘int’ to non-scalar type ‘A’ requested
   17 |     A a_1 = 2;
      |             ^

```

#cpp

---

*11:51*  
И в обратную сторону тоже работает. Для этого нужно определить специальный оператор:

```c
operator Type() const;
```

например
```c++
#include <iostream>

class A {
public:
    A() : a(0) {};
    A(int input) : a{input} {};

    operator int() {
        return a;
    }

    int a{};
};

int main() {

    A a_1 = 2;
    int a_int = a_1;

    std::cout << a_int;

    return 0;
}

```

```bash
/tmp/cpp_1$ g++ ./main.cpp && ./a.out 
2
```

P.S.

На операторе также работает ключевое слово explicit, запрещающее неявное преобразование. Но явное через `(int) a`, например, все еще будет работать


#cpp

---

*17:29*  
TIL: Копирование в системный буфер обмена в Vim

В базовой версии Vim (который `sudo apt install vim` aka `vim.basic`) отсутствует поддержка системного буфера обмена
Для работы с ним необходимо установить сборку vim-gtk3

Пример команды на копирование текущего файла в системный буфер

```
"+yggG
```

При этом vim.gtk3 точно так же работает в терминале и сохраняет все остальные функции vim.basic

#vim