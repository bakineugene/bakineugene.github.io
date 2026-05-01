---
title: "Interrupts"
date: 2026-01-08
author: Eugene
tags: ['interrupts', 'stm32']
summary: "*20:55* **STM32: исключения/прерывания** Работа с прерываниями для STM32F10xxx подробно описана в В доках stm32 есть более \"общее\" понятие чем прерывания - это исключения."
---

*20:55*  
**STM32: исключения/прерывания**

Работа с прерываниями для STM32F10xxx подробно описана в `PM0056 (Programming Manual)`

В доках stm32 есть более "общее" понятие чем прерывания - это исключения. Для разработчика я пока не вижу между ними большой разницы. Почти у любого исключения есть IRQn - идентификатор запроса на прерывание,  почти все обрабатываются через `NVIC (Nested vectored interrupt controller)`. Для каждого есть место в таблице векторов исключений.

К системным исключениям относятся:
`Reset`, `NMI` - исключения из исключений. Не управляются NVIC
`Hard fault`, `Memory management fault`, `Bus fault`, `Usage fault` - ошибки
`SVCall`, `PendSV` - исключения для имплементации `RTOS`
`SysTick` - исключение при срабатывании `SysTick` таймера. Базовый таймер в STM32.

Все остальное это прерывания (`Interrupt` or `IRQ`). Это исключения, запрошенные периферией или пользовательским кодом. Предназначено для коммуникации периферии с процессором.
Системные исключения имеют отрицательный IRQn и настраиваются через `SCB_XXXX` регистры, а периферийные исключения имеют положительный IRQn и настраиваются через `NVIC_XXXX` регистры.

**Обработчики исключений**

Адреса обработчиков исключений определены в таблице векторов исключений, которая задается в startup скрипте. Он поставляется с CMSIS, но можно и свой написать.

[https://github.com/STMicroelectronics/cmsis-device-f1/blob/c8e9a4a4f16b6d2cb2a2083cbe5161025280fb22/Source/Templates/gcc/startup_stm32f103x6.s#L129](https://github.com/STMicroelectronics/cmsis-device-f1/blob/c8e9a4a4f16b6d2cb2a2083cbe5161025280fb22/Source/Templates/gcc/startup_stm32f103x6.s#L129)

Отрывок:

```
g_pfnVectors:
...
  .word PendSV_Handler
  .word SysTick_Handler
  .word WWDG_IRQHandler
  .word PVD_IRQHandler
  .word TAMPER_IRQHandler
  .word RTC_IRQHandler
  .word FLASH_IRQHandler
  .word RCC_IRQHandler
  .word EXTI0_IRQHandler
  .word EXTI1_IRQHandler
...
```

Для каждого обработчика определено имя имплементирующей его функции, которую необходимо написать разработчику.   

```
  .weak SysTick_Handler
  .thumb_set SysTick_Handler,Default_Handler
```

Если функции нет, а исключение прилетело - вместо нее подставляется бесконечный цикл.

```c
/**
 * @brief  This is the code that gets called when the processor receives an
 *         unexpected interrupt.  This simply enters an infinite loop, preserving
 *         the system state for examination by a debugger.
*/
Default_Handler:
Infinite_Loop:
  b Infinite_Loop
```

Интересно, что можно определить несколько "таблиц векторов" и менять сразу весь набор хендлеров, записав оффсет до альтернативной таблицы в регистр `SCB_VTOR`.

**Управление прерываниями**

Практически идентично AVR

Каждое исключение может быть в одном из состояний:
`Inactive` - не активно и не запланировано
`Pending` - запланировано для обработки. Определяется флагом в одном из регистров.
`Active` - обрабатывается процессором прямщас
`Active + Pending` - и обрабатывается и запланировано.

Прерывания можно **глобально включить/выключить** по аналогии с sei()/cli() используя CMSIS функции:

```c
void __disable_irq(void) // Disable Interrupts
void __enable_irq(void) // Enable Interrupts
```

Конкретное **прерывание можно включить/выключить** используя специальные наборы регистров. Бит соответствует IRQn.

`NVIC_ISER[0..2] (Interrupt Set-Enable Register)` - Для включения прерывания
`NVIC_ICER[0..2] (Interrupt Clear-Enable Register)` - Для выключения прерывания

Также доступны CMSIS функции:

```c
void NVIC_EnableIRQ(IRQn_t IRQn) // Enable IRQn
void NVIC_DisableIRQ(IRQn_t IRQn) // Disable IRQn
```

**Pending** состояние для прерываний управляется регистрами:
`NVIC_ISPR[0..2] (Interrupt set-pending registers)` для установки pending
`NVIC_ICPR[0..2] (Interrupt clear-pending registers)` для сброса pending
`NVIC_STIR (Software Trigger Interrupt Register)` - Это отдельный регистр для программного вызова одного прерывания.  

Также доступны CMSIS функции:
```c
void NVIC_SetPendingIRQ(IRQn_t IRQn) // Set IRQn pending
void NVIC_ClearPendingIRQ(IRQn_t IRQn) // Clear IRQn pending status
```

**Активный статус** можно посмотреть с помощью `NVIC_IABRx` - показывает какие прерывания обрабатываются (Active)

```c
uint32_t NVIC_GetActive (IRQn_t IRQn) //  Returns 1 for active, 0 for inactive
```

#interrupts #stm32

---

*20:55*  
Системные исключения управляются через отдельные регистры примерно так, как это сделано у AVR. Поэтому не вижу смысла пока в них закапываться.

В принципе на данном уровне уже доступен тот же набор функциональности, что и AVR разработчику. Но NVIC также позволяет управлять приоритетами, а также разрешать/запрещать "прервать прерывание". К этому я вернусь позже.

P.S. Уперся в лимиты телеги 😢
Подключить что-ли премиум 🤔

P.P.S. Премиум не дает писать больше 4096 символов 😕
Придется подружиться с сестрой таланта.

#interrupts #stm32