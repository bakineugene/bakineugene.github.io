---
title: "Cpp"
date: 2026-01-06
author: Eugene
tags: ['cpp', 'memory', 'move_semantics']
summary: "*07:55* Часть №3 Семантика перемещения В предыдущей серии сформировалась проблема - необходимо избежать дорогой операции копирования при работе с временными объектами."
---

*07:55*  
Часть №3 Семантика перемещения

В предыдущей серии сформировалась проблема - необходимо избежать дорогой операции копирования при работе с временными объектами. Для таких объектов есть специальный термин - `rvalue` (right value). 

[https://en.cppreference.com/w/cpp/language/value_category.html](https://en.cppreference.com/w/cpp/language/value_category.html)

Если сильно не углубляться, то: 
`lvalue` это именованные объекты, кроме случаев когда их явным образом превратили в `rvalue`.
`rvalue` это все безымянные объекты, а также именованные объекты, превращенные в `rvalue`

`lvalue` превращенное в `rvalue` называется `xvalue` (eXpiring) т.е. те, которым жить осталось недолго.

В коде `rvalue` обозначается через `&&`
Для преобразования из `lvalue` в `rvalue` используется функция `std::move` - которая, по сути, просто приведение. 
Т.е. `move` сам ничего и никуда не перемещает, а просто помечает значение как временное (можно грабить корованы).
После чего компилятор тоже ничего и никуда не перемещает, а просто вызывает оператор или конструктор, которые принимают объект соответствующей категории. 

Т.е. 

```c++
Type a; // переменная на стеке
Type* b = &a; // указатель
Type& c{a}; // ссылка
Type&& d = std::move(a); // rvalue ссылка, разрешающая "отобрать" ресурсы 
```

Теперь дело за малым. C++ позволяет определить конструктор и оператор присваивания, принимающие на вход rvalue ссылки. Когда мы принимаем объект по такой ссылке - мы знаем, что его данные можно просто отобрать. Объект нужно оставить в валидном состоянии.

[https://en.cppreference.com/w/cpp/language/move_constructor.html](https://en.cppreference.com/w/cpp/language/move_constructor.html)
[https://en.cppreference.com/w/cpp/language/move_operator.html](https://en.cppreference.com/w/cpp/language/move_operator.html)

Вместе с операциями из правила трех эти ребята образуют правило пяти. Если класс владеет ресурсами и определена хоть одна из операций (деструктор, операторы/конструкторы копирования/перемещения) - скорее всего нужно определить все пять.

```c++
    SimpleArray(SimpleArray<T>&& other) noexcept :
        memory_{other.memory_}, // данные забираем себе
        size_{other.size_} {

        cout << "constructor move" << endl;

        other.memory_ = nullptr; // объекту оставляем nullptr
        other.size_ = 0;
    }
    
    SimpleArray& operator=(SimpleArray<T>&& other) noexcept {
        if (this == &other) {
            return *this;
        }

        cout << "operator move" << endl;

        delete[] memory_;
        memory_ = other.memory_; // данные забираем себе
        size_ = other.size_;

        other.memory_ = nullptr; // объекту оставляем nullptr
        other.size_ = 0;

        return *this;
    }

```

Теперь, во-первых, пример из части 2.5 не приводит к копированию:

```
create array_4
create array_5
create array_6
create array_7
constructor move
```

Во-вторых, мы сами можем перемещать данные из одного объекта в другой, скастовав значение из `lvalue` в `rvalue`:

```c++
    SimpleArray<int> array_1(100);
    SimpleArray<int> array_2(1);

    cout << "array_1 size : " << array_1.size() << endl;
    cout << "array_2 size : " << array_2.size() << endl;

    array_2 = std::move(array_1);
    cout << "array_1 size : " << array_1.size() << endl;
    cout << "array_2 size : " << array_2.size() << endl;
```

Вывод:

```
array_1 size : 100
array_2 size : 1
operator move
array_1 size : 0
array_2 size : 100
```

В-третьих, удалив оператор и конструктор копирования можно вообще сделать "movable only" объект. На этом основан `std::unique_ptr`.

Ну и в-четвертых - move семантика это довольно простая и элегантная штука для работы с ресурсами в c++.

Полный код примера:
[https://gist.github.com/bakineugene/4d493b8ad4f3f189bcfb5247a43544b1/eba414f9c5fecfec10d08eab95962841a6030ddc](https://gist.github.com/bakineugene/4d493b8ad4f3f189bcfb5247a43544b1/eba414f9c5fecfec10d08eab95962841a6030ddc)

#cpp #memory #move_semantics