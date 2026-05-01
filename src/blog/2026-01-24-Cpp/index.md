---
title: "Cpp"
date: 2026-01-24
author: Eugene
tags: ['cpp', 'memory', 'move_semantics', 'shared_ptr', 'smart_pointers', 'unique_ptr']
summary: "*14:22* Пройдемся теперь по умным указателям. Умные указатели - это, конечно, очень крутая штука. После знакомства с ними появилось хоть какое-то понимание, как на C++ можно писать крупные проекты."
---

*14:22*  
Пройдемся теперь по умным указателям.

Умные указатели - это, конечно, очень крутая штука. После знакомства с ними появилось хоть какое-то понимание, как на C++ можно писать крупные проекты. Хотя я еще ни одного крупного проекта на плюсах не трогал, но с умными указателями это уже не кажется таким уж мазохизмом.

Чтобы получше понять концепцию - написал самую базовую имплементацию:
[https://gist.github.com/bakineugene/2ae0ad7d1f2f4d011f87a1582ef410ba](https://gist.github.com/bakineugene/2ae0ad7d1f2f4d011f87a1582ef410ba)

**std::unique_ptr : Unique Pointer**

Первый из них - `std::unique_ptr`
[https://en.cppreference.com/w/cpp/memory/unique_ptr.html](https://en.cppreference.com/w/cpp/memory/unique_ptr.html)
Моя упрощенная/учебная имплементация: [https://gist.github.com/bakineugene/2ae0ad7d1f2f4d011f87a1582ef410ba#file-unique-h-L4](https://gist.github.com/bakineugene/2ae0ad7d1f2f4d011f87a1582ef410ba#file-unique-h-L4)

Это как раз `movable only` тип, хранящий указатель на объект.
На самом деле тут даже объяснять особо нечего. Все уже было сказано в посте про `RAII` и про move семантику.
Но можно обсудить интерфейс `std::unique_ptr`

Для использования нужно подключить `#include <memory>`

`std::unique_ptr` содержит указатель на объект, массив объектов или nullptr.

Для создания указателя можно как вызвать напрямую конструктор, передав ему `new Object`
Либо воспользоваться специальной функцией `std::make_unique<Object>()`, которая создаст экземпляр `Object` конструктором по умолчанию.

std::unique_ptr старается вести себя как обычный указатель
Чтобы определить владеет ли указатель каким либо объектом - определен `operator bool`
Определены операторы `operator*`, `operator->`, `operator[]` для доступа к завернутому объекту.

```cpp
struct Foo {
    int bar{};
};
std::unique_ptr<Foo> ptr;
if (!ptr) {
    // not initialized
}

ptr = std::make_unique<Foo>();

ptr->bar = 42;
```

Кроме того можно:
`T* get()` - получить доступ непосредственно к хранимому указателю
`T* release()` - забрать хранимый указатель у `unique_ptr`. После этого вызова владение переходит вызывающему коду (ответственность за вызов delete)
`reset(T*)` - позволяет завернуть в `unique_ptr` новый указатель (уничтожив старый)
`swap(unique_ptr&)` - позволяет поменять местами содержимое двух `unique_ptr`

Также есть возможность задавать `deleter` - но это необходимо только на случай, если заворачиваемый объект не умеет прибрать за собой - например был инициализирован C кодом

#cpp #move_semantics #smart_pointers #memory #unique_ptr

---

*20:12*  
**std::shared_ptr : Shared Pointer**

Это указатель, который позволяет поделить владение объектом.
Когда последний `shared_ptr` будет уничтожен - он прихватит с собой и managed объект.

[https://en.cppreference.com/w/cpp/memory/shared_ptr.html](https://en.cppreference.com/w/cpp/memory/shared_ptr.html)

Сильно упрощенная версия:
[https://gist.github.com/bakineugene/2ae0ad7d1f2f4d011f87a1582ef410ba#file-shared-h-L1](https://gist.github.com/bakineugene/2ae0ad7d1f2f4d011f87a1582ef410ba#file-shared-h-L1)

Объяснение устройства с картинками: [https://ddanilov.me/shared-ptr-is-evil/](https://ddanilov.me/shared-ptr-is-evil/)

```
In a typical implementation, shared_ptr holds only two pointers:
    the stored pointer (one returned by get());
    a pointer to control block.
```

Кроме самого указателя на managed объект - создаем и храним указатель на специальную вспомогательную структуру с метаданными.

```
The control block is a dynamically-allocated object that holds:
    either a pointer to the managed object or the managed object itself;
    the deleter (type-erased);
    the allocator (type-erased);
    the number of shared_ptrs that own the managed object;
    the number of weak_ptrs that refer to the managed object.
```

Структура единая и для `shared` и для `weak`, поэтому содержит счетчики обоих типов указателей.

При создании `ptr` инкрементит соответствующее число. При уничтожении декрементит.
При создании копии инстансы `shared_ptr` и `weak_ptr` делят между собой указатель на эти метаданные, поэтому текущее кол-во "пользователей" видят все.
Когда количество shared == 0 - уничтожается managed объект (в общем случае просто вызывается деструктор).
Когда количество и shared и weak указателей == 0, уничтожается и структура с метаданными.

Образно говоря, вот так (но на самом деле нет):
```cpp
~Shared() {
    if (!counter_) return;
    --counter_->strong;
    if (counter_->strong == 0) {
        delete pointer_;
    }
    if (counter_->strong == 0 && counter_->weak == 0) {
        delete counter_;
    }
}
```

**Usage**

Использование `std::shared_ptr` в целом похоже на `std::unique_ptr`

Для создания можно применять конструктор, передав в него `new Object` или `unique_ptr<Object>&&`, либо воспользоваться ф-цией `std::make_shared<Object>()`.

Добавились функции `unique` и `use_count` для получении информации о кол-ве `shared_ptr` пользователей.

**different pointers**

Можно заметить, вот такую интересную фразу в implementation details:

```
The pointer held by the shared_ptr directly is the one returned by get(), while the pointer/object held by the control block is the one that will be deleted when the number of shared owners reaches zero. These pointers are not necessarily equal.
```

Указатель возвращаемый из get() может не указывать на managed object. Добиться такого можно используя `aliasing constructor`:

```
The aliasing constructor: constructs a shared_ptr which shares ownership information with the initial value of r, but holds an unrelated and unmanaged pointer ptr. However, calling get() on this shared_ptr will always return a copy of ptr. It is the responsibility of the programmer to make sure that this ptr remains valid as long as this shared_ptr exists
```

Т.е. мы можем получить указатель, который возвращает какое-то значение, являющееся составной частью managed объекта.
При этом, несмотря на то, что из get() будет возвращаться совсем другой указатель - подсчет использований будет идти для "базового" managed объекта.

```cpp
int main(void) {
    auto base_ptr = std::shared_ptr<int[]>(new int[2]);

    base_ptr[0] = 123;
    base_ptr[1] = 456;

    auto ptr_0 = std::shared_ptr<int>(base_ptr, &base_ptr.get()[0]);
    auto ptr_1 = std::shared_ptr<int>(base_ptr, &base_ptr.get()[1]);

    std::cout << "ptr_0 = " << *ptr_0 << std::endl;
    std::cout << "ptr_1 = " << *ptr_1 << std::endl;
    std::cout << "base_ptr count = " << base_ptr.use_count() << std::endl;
}
```

```
$ ./a.out
ptr_0 = 123
ptr_1 = 456
base_ptr count = 3
```

В целом - подсчет ссылок это уже почти GC. 

Но, если создать кольцевую зависимость между разными managed объектами - то память никогда не освободится.
Тут то и приходит на помощь weak_ptr

#cpp #smart_pointers #memory #shared_ptr