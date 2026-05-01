---
title: "Cpp"
date: 2025-12-29
author: Eugene
tags: ['cpp', 'memory', 'raii']
summary: "*09:57* Про управление памятью в c++ Часть №0 Вместо ф-ций malloc/calloc в C++ для выделения памяти используется оператор new/new)."
---

*09:57*  
Про управление памятью в c++

Часть №0

Вместо ф-ций malloc/calloc в C++ для выделения памяти используется оператор new/new[] ([https://en.cppreference.com/w/cpp/memory/new/operator_new.html](https://en.cppreference.com/w/cpp/memory/new/operator_new.html)). 
Если не вдаваться в подробности (которых я толком пока не знаю), то можно думать о new как о malloc + вызов конструктора (инициализация). new можно переопределять как глобально, так и на уровне класса.

Вместо ф-ции free используется выражение delete/delete[] ([https://en.cppreference.com/w/cpp/language/delete.html](https://en.cppreference.com/w/cpp/language/delete.html)). Опять же (очень упрощенно) можно его представить в виде пары вызовов - деструктор + free. 

В C++ появляются конструкторы и деструкторы ([https://en.cppreference.com/w/cpp/language/destructor.html](https://en.cppreference.com/w/cpp/language/destructor.html)), с помощью которых можно инициализировать struct/class, а также "прибрать за собой".

Очень важная особенность: стандарт гарантирует, что деструктор будет вызван при выходе из области видимости объекта!

Это важно, поскольку, в отличии от C - в плюсах появляются исключения, и просто освободить память при выходе из функции уже не получится.

```
A destructor is a special member function that is called when the lifetime of an object ends.
The purpose of the destructor is to free the resources that the object may have acquired during its lifetime.
```

Часть №1 RAII

На основе этих гарантий основан паттерн RAII ([https://en.cppreference.com/w/cpp/language/raii.html](https://en.cppreference.com/w/cpp/language/raii.html)).

Расшифровывается как Resource Acquisition Is Initialization - получение ресурса это инициализация (видимо инициализация объекта). Альтернативное название: SBRM (Scope‑Bound Resource Management) - управление ресурсами с помощью области видимости.

Если нам важно не забыть про ресурс (память в данном случае) - мы привязываем его к некоторому объекту. 
* Храним указатель на ресурс внутри объекта
* Память выделяем в конструкторе
* Освобождаем в деструкторе
При этом сам объект мы создаем на стеке. И при выходе из области видимости объекта память (или другой ресурс) освободится даже если выход произошел из-за исключения.

[https://gist.github.com/bakineugene/4d493b8ad4f3f189bcfb5247a43544b1/6a5558956875524b2b16eb3df94b41d62e2d26eb](https://gist.github.com/bakineugene/4d493b8ad4f3f189bcfb5247a43544b1/6a5558956875524b2b16eb3df94b41d62e2d26eb)

```c++
class RAII {

public:
    RAII(string name_input): name{name_input} {
        memory = new int[100];
        cout << "    constructor call for " << name  << endl;
    }

    ~RAII() {
        delete[] memory;
        cout << "    destructor call for " << name << endl;
    }

    int* memory;
    string name;
};

int main(void) {
    {
        cout << "entering block 1" << endl;
        RAII raii("object 1");
        cout << "leaving block 1" << endl;
    }
    try {
        cout << "entering block 2" << endl;
        RAII raii("object 2");
        throw std::logic_error("error");
        cout << "leaving block 2" << endl;
    } catch (std::logic_error a) {
        cout << "catch block 2" << endl;
    }
}

```

```shell
entering block 1
    constructor call for object 1
leaving block 1
    destructor call for object 1
entering block 2
    constructor call for object 2
    destructor call for object 2
catch block 2
```

#cpp #memory #raii