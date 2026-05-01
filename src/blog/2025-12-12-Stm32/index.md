---
title: "Stm32"
date: 2025-12-12
author: Eugene
tags: ['cmsis', 'cubemx', 'hal', 'spl', 'stm32']
summary: "*11:53* Немного покопал сгенерированный проект 1. Нашлась причина по которой не работала загрузка прошивки без зажатия reset'а cubemx по дефолту вставляет вот такую подлянку: Если включить отладку ..."
---

*11:53*  
Немного покопал сгенерированный проект

1. Нашлась причина по которой не работала загрузка прошивки без зажатия reset'а 
[https://stackoverflow.com/questions/30829838/stm32-flashing-disabled-after-flashing-a-code-without-r-w-protection](https://stackoverflow.com/questions/30829838/stm32-flashing-disabled-after-flashing-a-code-without-r-w-protection)

cubemx по дефолту вставляет вот такую подлянку:

```c
/**
  * @brief Disable the Serial wire JTAG configuration
  * @note  DISABLE: JTAG-DP Disabled and SW-DP Disabled
  * @retval None
  */
#define __HAL_AFIO_REMAP_SWJ_DISABLE()  AFIO_DBGAFR_CONFIG(AFIO_MAPR_SWJ_CFG_DISABLE)
```

Если включить отладку через JTAG - она меняется на вот такой вызов и все работает

```c
/**
  * @brief Enable the Serial wire JTAG configuration
  * @note  NONJTRST: Full SWJ (JTAG-DP + SW-DP) but without NJTRST
  * @retval None
  */
#define __HAL_AFIO_REMAP_SWJ_NONJTRST()  AFIO_DBGAFR_CONFIG(AFIO_MAPR_SWJ_CFG_NOJNTRST)
```

2. [https://github.com/bakineugene/stm32-f1-cubemx-hal-blink](https://github.com/bakineugene/stm32-f1-cubemx-hal-blink)

Пытался повторить ручками то, что сделал cubemx на основе голых репозиториев и что-то все время не работало. Пошел от обратного и перевел все что можно на использование файлов из репозиториев. Что конкретно у меня не работало пока не разобрался, но в принципе в таком виде проект мне нравится.

3. Вместо использования --nostdlib cubemx генерирует заглушки ([https://github.com/bakineugene/stm32-f1-cubemx-hal-blink/blob/main/src/syscalls.c](https://github.com/bakineugene/stm32-f1-cubemx-hal-blink/blob/main/src/syscalls.c)). 

Пока не могу судить о преимуществах того или иного подхода

4. Ну и когда я сравнивал размеры прошивок - естественно не учел оптимизации компилятора.
cubemx по дефолту ставит OPT = -Og, в то время как cmsis я собирал с -O0

Если все собирать с -Og, то:
hal = 3.6Kb
spl = 2.6Kb
cmsis = 848b

#stm32 #hal #spl #cmsis #cubemx