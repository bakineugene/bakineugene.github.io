---
title: "Cmsis"
date: 2025-11-06
author: Eugene
tags: ['cmsis', 'stm32']
summary: "*12:30* На этот раз собрал пример моргалки используя cmsis репозитории В итоге понадобились И В cmsis каждый блок регистров задается через структуру."
---

*12:30*  
[https://github.com/bakineugene/stm32-f1-cmsis-blink](https://github.com/bakineugene/stm32-f1-cmsis-blink)

На этот раз собрал пример моргалки используя cmsis репозитории
В итоге понадобились

[https://github.com/STMicroelectronics/cmsis-device-f1](https://github.com/STMicroelectronics/cmsis-device-f1)
И
[https://github.com/ARM-software/CMSIS_5](https://github.com/ARM-software/CMSIS_5)

```c
#include "stm32f1xx.h"

// Need that for some reason
void _init(){}

void main(void)
{
    RCC->APB2ENR |= RCC_APB2ENR_IOPCEN;
    GPIOC->CRH &= ~(GPIO_CRH_CNF13 | GPIO_CRH_MODE13);
    GPIOC->CRH |= GPIO_CRH_MODE13_1;

    while (1)
    {
        GPIOC->ODR |= GPIO_ODR_ODR13;
        for (int i = 0; i < 500000; i++)
            ; // arbitrary delay
        GPIOC->ODR &= ~GPIO_ODR_ODR13;
        for (int i = 0; i < 100000; i++)
            ; // arbitrary delay
    }
}
```

В cmsis каждый блок регистров задается через структуру. Поля структуры задают смещения для конкретных регистров блока. 
Также есть define'ы для битовых масок определенных значений.

Например
```c
#define RCC_APB2ENR_IOPCEN                   RCC_APB2ENR_IOPCEN_Msk            /*!< I/O port C clock enable */
```

Кажется без чтения документации все равно не обойтись, но кое-что можно найти просто поиском по header файлу

Единственное с чем я не разобрался - это ошибка линкера
```
 undefined reference to `_init'
```

Этот референс определен в .s файле 
```
/* Call static constructors */
    bl __libc_init_array

```
и, вроде бы, отвечает за инициализацию c++ объектов. Т.е. скорее всего не важен для c кода. 
Заткнул заглушкой, как нужно делать идиоматично - пока без понятия.

#cmsis #stm32