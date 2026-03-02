## PWM режимы

См. раздел 11.7 *PWM Modes* [[ATtiny13A Datasheet](#ref-attiny13a)].

PWM используется для генерации сигнала с регулируемой скважностью (например, для управления яркостью светодиода или скоростью мотора).

ATtiny13A поддерживает два типа PWM:

* **Fast PWM**
* **Phase Correct PWM**

---

## Fast PWM (быстрый ШИМ)

Счетчик считает **только вверх** от `0` до `TOP`, затем сбрасывается в `0`.

* Быстрее (выше частота)
* Менее симметричный сигнал

### Режимы

#### Fast PWM, TOP = 0xFF

`WGM02 = 0, WGM01 = 1, WGM00 = 1`

```
TCCR0A |= (1 << WGM00) | (1 << WGM01)
TCCR0B &= ~(1 << WGM02)
```

Счетчик:

```
0 → 255 → 0 → ...
```

Частота:

```
f_PWM = F_CPU / (N * 256)
```

---

#### Fast PWM, TOP = OCR0A

`WGM02 = 1, WGM01 = 1, WGM00 = 1`

```
TCCR0A |= (1 << WGM00) | (1 << WGM01)
TCCR0B |= (1 << WGM02)
```

Счетчик:

```
0 → OCR0A → 0 → ...
```

Частота:

```
f_PWM = F_CPU / (N * (OCR0A + 1))
```

⚠️ В этом режиме:

* `OCR0A` задаёт TOP
* Канал A (OC0A) **ограничен** (используется как TOP)

---

## Phase Correct PWM (фазово-симметричный ШИМ)

Счетчик считает:

```
0 → TOP → 0 → ...
```

* Симметричный сигнал
* Меньше гармоник
* В 2 раза ниже частота

---

#### Phase Correct PWM, TOP = 0xFF

`WGM02 = 0, WGM01 = 0, WGM00 = 1`

```
TCCR0A |= (1 << WGM00)
TCCR0A &= ~(1 << WGM01)
TCCR0B &= ~(1 << WGM02)
```

Счетчик:

```
0 → 255 → 0 → ...
```

Частота:

```
f_PWM = F_CPU / (N * 510)
```

---

#### Phase Correct PWM, TOP = OCR0A

`WGM02 = 1, WGM01 = 0, WGM00 = 1`

```
TCCR0A |= (1 << WGM00)
TCCR0A &= ~(1 << WGM01)
TCCR0B |= (1 << WGM02)
```

Счетчик:

```
0 → OCR0A → 0 → ...
```

Частота:

```
f_PWM = F_CPU / (N * 2 * OCR0A)
```

⚠️ Особенность:

* `OCR0A` задаёт TOP
* Канал A ограничен

---

## Управление выводами в PWM

См. 11.7.3 *Compare Output Mode, Fast PWM*
См. 11.7.4 *Compare Output Mode, Phase Correct PWM*

### Для OC0A (PB0) и OC0B (PB1)

`TCCR0A`

| COM0x1 | COM0x0 | Описание                                |
| ------ | ------ | --------------------------------------- |
| 0      | 0      | Пин отключен                            |
| 1      | 0      | **Non-inverting PWM** (обычный ШИМ)     |
| 1      | 1      | **Inverting PWM** (инвертированный ШИМ) |

---

### Non-inverting PWM (обычный)

Поведение:

* При старте периода → HIGH
* При совпадении с `OCR0x` → LOW

Скважность:

```
Duty = OCR0x / TOP
```

---

### Inverting PWM

Поведение:

* При старте периода → LOW
* При совпадении → HIGH

Скважность:

```
Duty = 1 - (OCR0x / TOP)
```

---

## Пример настройки PWM (Fast PWM, OC0B)

```c
DDRB |= (1 << PB1);                 // PB1 (OC0B) как выход

OCR0B = 128;                       // ~50% duty

TCCR0A |= (1 << WGM00) | (1 << WGM01); // Fast PWM
TCCR0A |= (1 << COM0B1);               // Non-inverting на OC0B

TCCR0B |= (1 << CS01);                 // prescaler = 8
```

---

