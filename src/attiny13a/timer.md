# ATtiny13A Timer/Counter

Единственный 8-битный счётчик.

См. раздел 11. *8-bit Timer/Counter0 with PWM* [[ATtiny13A Datasheet](#ref-attiny13a)].

Может тактироваться от того же источника, что и `CPU` (через prescaler) либо от внешнего источника с пина `T0 (PB2)`



## Прерывания

См. раздел 9.1 *Interrupt Vectors* [[ATtiny13A Datasheet](#ref-attiny13a)].

| Vector No. | Program Address | Source        | Interrupt Definition           |
|------------|-----------------|---------------|--------------------------------|
| 4          | 0x0003          | `TIM0_OVF`    | Timer/Counter Overflow         |
| 7          | 0x0006          | `TIM0_COMPA`  | Timer/Counter Compare Match A  |
| 8          | 0x0007          | `TIM0_COMPB`  | Timer/Counter Compare Match B  |

## Пины с функциями таймера

См. раздел 10.3.1 *Alternate Functions of Port B* [[ATtiny13A Datasheet](#ref-attiny13a)].

| Port Pin | Alternate Function                          |
|----------|----------------------------------------------|
| PB2      | T0: Timer/Counter0 Clock Source              |
| PB1      | OC0B: Timer/Counter0 Compare Match B Output  |
| PB0      | OC0A: Timer/Counter0 Compare Match A Output  |

## Регистры

### TCCR0A

См. раздел 11.9.1 [[ATtiny13A Datasheet](#ref-attiny13a)].  

`TCCR0A` - Timer/Counter Control Register A  
  
`COM0A1`, `COM0A0` - Compare Match A Settings  
`COM0B1`, `COM0B0` - Compare Match B Settings  
`WGM01`, `WGM00` - Waveform Generation Mode (Настройка режима работы счетчика)  

### TCCR0B

См. раздел 11.9.2 [[ATtiny13A Datasheet](#ref-attiny13a)].  

`TCCR0B` - Timer/Counter Control Register B  
  
`FOC0A` - Force Output Compare A (Принудительный вызов реакции на равенство OCR0A в не PWM режимах)  
`FOC0B` - Force Output Compare B (Принудительный вызов реакции на равенство OCR0B в не PWM режимах)  
`WGM02` - Waveform Generation Mode (Настройка режима работы счетчика)  
`CS00`, `CS01`, `CS02` - Настройки тактирования (выбор источника и настройки делителя)  

### TCNT0

См. раздел 11.9.3 [[ATtiny13A Datasheet](#ref-attiny13a)].  

`TCNT0`  - Текущее значение счетчика  

### OCR0A

См. раздел 11.9.4 [[ATtiny13A Datasheet](#ref-attiny13a)].  

`OCR0A`  - Output Compare A (Значение для сравнения A)  

### OCR0B

См. раздел 11.9.5 [[ATtiny13A Datasheet](#ref-attiny13a)].  

`OCR0B`  - Output Compare B (Значение для сравнения B)  

### TIMSK0

См. раздел 11.9.6 [[ATtiny13A Datasheet](#ref-attiny13a)].  

`TIMSK0` - Timer Interrupt Mask Register  

`OCIE0B` - Output Compare Interrupt B Enable  
`OCIE0A` - Output Compare Interrupt A Enable  
`TOIE0`  - Overflow Interrupt Enable  

### TIFR0

См. раздел 11.9.7 [[ATtiny13A Datasheet](#ref-attiny13a)].  

`TIFR0`  - Timer Interrupt Flag Register  

Флаги событий. При установленном бите в TIMSK0 соответствующий флаг приводит к вызову прерывания.  
Чтобы сбросить флаг программно - нужно установить его в 1. (Да, установить, чтобы сбросить)  

`OCF0A` - Output Compare Flag A  
`OCF0B` - Output Compare Flag B  
`TOV0`  - Overflow Flag  

## Использование / режимы работы

### Источник тактирования

| `TCCR0B[CS02]` | `TCCR0B[CS01]` | `TCCR0B[CS00]` | Источник                             |
|----------------|----------------|----------------|--------------------------------------|
| 0              | 0              | 0              | Нет / остановлен                     |
| 0              | 0              | 1              | Внутренний источник                  |
| 0              | 1              | 0              | Внутренний / 8                       |
| 0              | 1              | 1              | Внутренний / 64                      |
| 1              | 0              | 0              | Внутренний / 256                     |
| 1              | 0              | 1              | Внутренний / 1024                    |
| 1              | 1              | 0              | Внешний `T0 (PB2)` По фронту сигнала |
| 1              | 1              | 1              | Внешний `T0 (PB2)` По спаду сигнала  |

### Компаратор / задать значения для сравнения

см. 11.6 *Compare Match Output Unit* [[ATtiny13A Datasheet](#ref-attiny13a)].

Можно задать два значения для сравнения через регистры `OCR0A` и `OCR0B`.  
Компаратор постоянно сравнивает значение регистра `TCNT0` с `OCR0A` и `OCR0B`  
При совпадении выставляются флаги `TIFR0[OCF0A]`, `TIFR0[OCF0B]`.  

### Реакция на сигнал компаратора

* Прерывания `TIM0_COMPA`, `TIM0_COMPB`.  
* Переключение пинов `OC0A (PB0)`, `OC0B (PB1)`.  

Чтобы была возможность переключать пин - необходимо сконфигурировать пин как `output`, прописав 1 в соответствующий бит DDR регистра.  

### Нормальный/Стандартный режим

Дефолтный режим
Задается через `WGM00 = WGM01 = WGM02 = 0`

```
TCCR0A &= ~(1 << WGM00)
TCCR0A &= ~(1 << WGM01)
TCCR0B &= ~(1 << WGM02)
```

Счетчик считает только вверх, доходит до MAX (255) и сбрасывается в 0.  
При этом выставляется `TIFR0[TOV0]`, что при включенном `TIMSK0[TOIE0]` приводит к вызову прерывания.  
Компаратор в этом режиме также работает.  

#### Пример настройки

```c
TCCR0B = (1 << CS02) | (1 << CS00); // prescale = 1024
TIMSK0 |= (1 << TOIE0);             // Enables overflow interrupt 
```

### CTC режим (обнуление таймера по сигналу компаратора)  

Похож на дефолтный, но счетчик считает не до `MAX`, а до `OCR0A`.
Задается через `WGM00 = WGM02 = 0; WGM01 = 1`
Overflow Event в этом режиме происходит только если `OCR0A == MAX == 255`.  

```
TCCR0A &= ~(1 << WGM00)
TCCR0A |= (1 << WGM01)
TCCR0B &= ~(1 << WGM02)
```

В "не PWM" режимах можно управлять пинами `OC0A (PB0)`, `OC0B (PB1)` следующим образом:

`TCCR0A`

| COM0A1 | COM0A0 | Описание                                |
|--------|--------|-----------------------------------------|
| 0      | 0      | Управление пином `OC0A (PB0)` отключено |
| 0      | 1      | Изменить значение `OC0A (PB0)`          |
| 1      | 0      | Очистить `OC0A (PB0)`                   |
| 1      | 1      | Выставить `OC0A (PB0)`                  |

| COM0B1 | COM0B0 | Описание                                |
|--------|--------|-----------------------------------------|
| 0      | 0      | Управление пином `OC0B (PB1)` отключено |
| 0      | 1      | Изменить значение `OC0B (PB1)`          |
| 1      | 0      | Очистить `OC0B (PB1)`                   |
| 1      | 1      | Выставить `OC0B (PB1)`                  |

#### Пример настройки

```c
OCR0A = 253;                        // частота = F_CPU / prescale / (OCR0A + 1)
TCCR0B = (1 << CS01) | (1 << CS00); // Prescale = 64
TCCR0A |= (1 << WGM01);             // CTC mode

TIMSK0 |= (1 << OCIE0A);            // Enables Compare A interrupt

TCCR0A |= (1 << COM0A0);            // Enables toggling of PB0 pin
```

## Литература

##### ATtiny13A Datasheet {#ref-attiny13a}
Microchip Technology, Rev. 8126F–AVR–05/12

