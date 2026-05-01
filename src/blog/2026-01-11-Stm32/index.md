---
title: "Stm32"
date: 2026-01-11
author: Eugene
tags: ['exti', 'interrupts', 'stm32', 'systick']
summary: "*19:47* **SysTick исключение** Самый простой таймер для настройки. Нужно вызвать всего одну CMSIS функцию : вся магия обращения к правильным регистрам произойдет внутри."
---

*19:47*  
**SysTick исключение**

[https://arm-software.github.io/CMSIS_5/Core/html/group__SysTick__gr.html](https://arm-software.github.io/CMSIS_5/Core/html/group__SysTick__gr.html)

Самый простой таймер для настройки. Нужно вызвать всего одну CMSIS функцию `SysTick_Config(ticks_count)`: вся магия обращения к правильным регистрам произойдет внутри. Таймер вызовет исключение через `ticks_count` тиков.

Для `ticks_count` максимальное значение 24bit - 1 == `16 777 215`
Удобно оперировать долей от `SystemCoreClock`, например:

```c
if(SysTick_Config(SystemCoreClock / 1000)) {  // 1 мс
    /*
     * Может вернуть 1 (failure)
     * Тогда попадем в этот блок
     */  
}
```

Чтобы `SystemCoreClock` содержал актуальное значение - необходимо вызвать `SystemCoreClockUpdate` после правок RCC конфигурации  

[https://arm-software.github.io/CMSIS_6/main/Core/group__system__init__gr.html](https://arm-software.github.io/CMSIS_6/main/Core/group__system__init__gr.html)

Пример обработчика:
```c
void SysTick_Handler(void) {
    UpdateBlinkTime();
}
```

#stm32 #interrupts #systick

---

*19:57*  
**EXTI исключение**

Для использования EXTI необходимо подать питание на AFIO (Alternate Function Input Output), отвечающее за конфигурацию I/O портов, а не только за альтернативные функции.

```
To read/write the AFIO_EVCR, AFIO_MAPR and AFIO_EXTICRX registers, the AFIO clock
should first be enabled.
```

**RM0008 9.4.3 - 9.4.6 External interrupt configuration register [1..4] (AFIO_EXTICR[1..4])**

```
EXTICR1 - pins 0..3
EXTICR2 - pins 4..7
EXTICR3 - pins 8..11
EXTICR4 - pins 12..15
```

**RM0008 10.2.5 External interrupt/event line mapping**

Все пины с одинаковым номером обрабатываются одной "линией" EXTI.
Для настройки линии есть 4 бита в EXTICR регистрах, чтобы выбрать, с какого именно порта мы будем "ловить" исключение.
Т.е. нельзя одновременно отслеживать и PA1 и PB1:

```
0000: PA[x] pin
0001: PB[x] pin
0010: PC[x] pin
0011: PD[x] pin
0100: PE[x] pin
0101: PF[x] pin
0110: PG[x] pin
```

Сделал пару макросов для настройки EXTICR

```c
#define RESET_EXTICR(exti, pin) AFIO->EXTICR[exti - 1] &= ~AFIO_EXTICR##exti##_EXTI##pin
#define SET_EXTICR(exti, pin, port) AFIO->EXTICR[exti - 1] |= AFIO_EXTICR##exti##_EXTI##pin##_##port

RESET_EXTICR(3, 9);
SET_EXTICR(3, 9, PB);
```

**RM0008 10.2.4 Functional description**

В этом разделе описывается принципиальная схема работы с EXTI.

1. `Hardware interrupt selection` - Настроить обработку прерывания в ответ на событие
2. `Hardware event selection` - Настроить некоторую реакцию периферии в ответ на событие
3. `Software interrupt/event selection` - Настроить программный вызов события

Интересный пункт про возможность задавать реакцию периферии 
Но пока больше интересен пункт 1

```
To configure the 20 lines as interrupt sources, use the following procedure:
* Configure the mask bits of the 20 Interrupt lines (EXTI_IMR)
* Configure the Trigger Selection bits of the Interrupt lines (EXTI_RTSR and EXTI_FTSR)
* Configure the enable and mask bits that control the NVIC IRQ channel mapped to the 
  External Interrupt Controller (EXTI) so that an interrupt coming from one of
  the 20 lines can be correctly acknowledged
```

**RM0008 10.3 EXTI registers**

Регистры для управления EXTI

`EXTI_IMR` для включения прерывания
`EXTI_EMR` для включения реакции периферии
`EXTI_RTSR` (Rising Trigger Selection) для включения реакции по восходящему фронту
`EXTI_FTSR` (Falling Trigger Selection) для включения реакции по нисходящему фронту
`EXTI_SWIER` (Software Interrupt Event) для запроса прерывания
`EXTI_PR` (Pending) При обработке прерывания мы должны сбрасывать этот бит записывая туда 1

```
This bit is set when the selected edge event arrives on the external interrupt line. This bit is
cleared by writing a 1 into the bit or by changing the sensitivity of the edge detector.
```

Тоже временно добавил макросов. Возможно потом пойму, что это неудобно, но пока хочется и CMSIS и читаемого кода

```c
#define ENABLE_EXTI(pin) EXTI->IMR |= EXTI_IMR_MR##pin
#define ENABLE_EXTI_FALLING(pin) EXTI->FTSR |= EXTI_FTSR_TR##pin
#define DISABLE_EXTI_FALLING(pin) EXTI->FTSR &= ~EXTI_FTSR_TR##pin
#define ENABLE_EXTI_RISING(pin) EXTI->RTSR |= EXTI_RTSR_TR##pin
#define DISABLE_EXTI_RISING(pin) EXTI->RTSR &= ~EXTI_RTSR_TR##pin
#define RESET_EXTI_PENDING(pin) EXTI->PR = EXTI_PR_PR##pin
#define EXTI_PENDING(pin) EXTI->PR & EXTI_PR_PR##pin

ENABLE_EXTI(9);
ENABLE_EXTI_FALLING(9);
DISABLE_EXTI_RISING(9);
RESET_EXTI_PENDING(9);
```

После настройки необходимо активировать прерывание

```
NVIC_EnableIRQ(EXTI9_5_IRQn);
```

**Прерывания**

`EXTI0`, `EXTI1`, `EXTI2`, `EXTI3`, `EXTI4`, `EXTI9_5`, `EXTI15_10`

Я было думал, что у stm32 на каждую ногу можно повесить по обработчику, но и тут не обошлось без групповых. Разве что, в отличии от AVR, с помощью Pending флага можно в точности узнать на какой ножке произошло "событие". 

Pending флаг нужно сбрасывать вручную:

```c
#define RESET_EXTI_PENDING(pin) EXTI->PR = EXTI_PR_PR##pin
#define EXTI_PENDING(pin) EXTI->PR & EXTI_PR_PR##pin

void EXTI9_5_IRQHandler(void) {
    if (EXTI_PENDING(9)) {
        RESET_EXTI_PENDING(9);
        BlinkSecondLED();
    }
}
```

#stm32 #interrupts #exti