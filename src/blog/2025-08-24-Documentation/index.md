---
title: "Documentation"
date: 2025-08-24
author: Eugene
tags: ['cpp', 'documentation']
summary: "*14:36* Некоторое время назад осознал полезность всяческих диаграмм и для рисования использовал софт типа и Однако со временем понял, что мне важнее не графическая часть, а структурная."
---

*14:36*  
Некоторое время назад осознал полезность всяческих диаграмм и для рисования использовал софт типа [https://www.drawio.com/](https://www.drawio.com/) и [https://www.libreoffice.org/discover/draw/](https://www.libreoffice.org/discover/draw/)

Однако со временем понял, что мне важнее не графическая часть, а структурная. И наткнулся на решения, генерирующие диаграммы из кода:

* PlantUML (java)
Main - [https://plantuml.com/ru/](https://plantuml.com/ru/)
Web Editor - [https://editor.plantuml.com/uml/SoWkIImgAStDuNBAJrBGjLDmpCbCJbMmKiX8pSd9vt98pKi1IW80](https://editor.plantuml.com/uml/SoWkIImgAStDuNBAJrBGjLDmpCbCJbMmKiX8pSd9vt98pKi1IW80)

* D2 (Go)
[https://d2lang.com/](https://d2lang.com/)

* Mermaid (JS)
[https://github.com/mermaid-js/mermaid-cli](https://github.com/mermaid-js/mermaid-cli)
Web Editor - [https://mermaid.live](https://mermaid.live)

#documentation

---

*15:07*  
Рубрика TIL

В процессе изучения c++. Интересный синтаксис инициализации полей класса.

При подходе "в лоб" поле a будет проинициализировано дважды. Перед конструктором и в самом конструкторе

```c++
#include <iostream>

class Example2 {
public:
    Example2() {
        std::cout << "Example2" << std::endl;
    }
};

class Example {
    Example2 a;

public:
    Example(Example2 value) {
        a = value; // Regular assignment
    }
};

int main() {
    Example example{Example2()};
}
```

```shell
$ g++ init.cpp && ./a.out 
Example2
Example2
```

А если объявить поле константным - и вовсе не скомпилируется.

```
$ g++ init.cpp && ./a.out 
init.cpp: In constructor ‘Example::Example(Example2)’:
init.cpp:15:13: error: passing ‘const Example2’ as ‘this’ argument discards qualifiers [-fpermissive]
   15 |         a = value; // Regular assignment
      |             ^~~~~
init.cpp:3:7: note:   in call to ‘constexpr Example2& Example2::operator=(const Example2&)’
    3 | class Example2 {
      |       ^~~~~~~~
```

И на помощь приходят списки инициализации - инструкция как инициализировать поля до вызова конструктора.
Присвоение в конструкторе уже не нужно.
[https://cppscripts.com/cpp-initializer-list](https://cppscripts.com/cpp-initializer-list)

```c
class Example {
    const Example2 a;

public:
    Example(Example2 value): a(value) {
    }
};
```

#cpp