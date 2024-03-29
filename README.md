# asm-emu
**Assembler emulator -- эмулятор языка ассемблера**

Компилятор языка ассемблера состоит из нескольких частей:

1. ***Лексер***

    Проверяет, чтобы в программе использовались только лексемы, которые были заранее определены и размечены.
    На выходе генерируется список токенов, для однозначной интерпритации написанного.
    
2. ***Парсер***

    Разбирает список токенов и проверяет их соответсвие с грамматикой из файла `asm_grammar.txt`.
    На выходе генерирует валидный список команд.
    
3. ***Компилятор***
    
    Генерирует двоичное представление программы из валидного списка команд. Также, все метки перехода в программе заменяются конкретными адресами.
    
4. ***Ассемблер***
    
    Выполняет полученный двоичный код.
    
## Эмулятор ассемблера

   * Эмулятор ассемблера реализован на архитектуре фон Неймана -- память команд и данных находятся в одном пространстве. 
   По умолчанию, отношения памяти команд к памяти данных 1 к 3.
   * Кроме общей памяти, эмулятор имеет 7 регистров общего назначения (R1-R7), и регистры PC (номер команды), SP (указатель на стек).
   * После выполения любых команд, обновляются флаги состояний. Поддерживаются флаги знака, чётности, нуля, переноса и переполнения.
   * Весь код выполняется на стеке, из-за чего формат команд одноадресный.
   * Используются RISC-формат команд -- с постоянной длинной.
   По умолчанию команда делится на 4 части:
   ```
        [0......27]
        X1_X2_X3_X4, всего 27 бит
        [0-7]   X1 -- код команды (смотреть constants.py)
        [8-15]  X2 -- литерал
        [16-23] X3 -- адрес
        [24-26] X4 -- номер регистра
   ```
   Во время формирования команды, неиспользуемые части заполняются нулями. Исключение -- косвенный переход по адресу(@R1), находящимся в регистре. 
   В этом случае, кроме номера регистра, поле литерал заполняется одними единицами.
   
## Список команд эмулятора
  ```
  PUSH #FF ;Загрузка литерала 0xFF в стек
  PUSH @BB ;Загрузка данных по адресу 0xBB в стек
  PUSH R1  ;Загрузка данных в стек из R1
  PUSH @R1 ;Загрузка данных по адресу, которых хранится в регистре R1, в стек
  
  POP @CC ;Выгрузка данных с вершины стека по адресу 0xCC
  POP R2  ;Выгрузка данных с вершины стека в регистр R2
  POP @R2 ;Выгрузка данных с вершины стека по адресу, который хранится в регистре R2
  
  INC ;Инкремент верхушки стека
  DEC ;Декремент верхушки стека
  ADD ;Сложение двух верхних чисел стека
  SUB ;Вычитание последнего из предсполеднего элементов стека
  MUL ;Умножение двух верхних чисел стека, при этом результат всегда возвращается в стек двумя числами
  ; старшими и младшими битами. Если малых результатах старшая часть разряда будет равно нулю.
  ADC ;Сложение двух верхних чисел стека + Carry
  
  AND ;Логическое и между последними элементами стека
  OR  ;Логическое или между последними элементами стека
  XOR ;Логическое исключающее или между последними элементами стека
  NOR ;Логическое не-или или между последними элементами стека
  NOT ;Логическое отрицание или между последними элементами стека
  
  CMP ;Сравнение последнего и предпоследнего элементов стека
  
  SHL ;Сдвиг на 1 бит влево
  SHR ;Сдвиг на 1 бит вправо
  
  LABEL:    ;Метка для перехода
  
  JC LABEL  ;Переход по метке LABEL, если флаг переноса
  NJC LABEL ;Переход по метке LABEL, если не флаг переноса
  JZ LABEL  ;Переход по метке LABEL, если флаг нуля
  NJZ LABEL ;Переход по метке LABEL, если не флаг нуля
  JP LABEL  ;Переход по метке LABEL, если флаг чётности
  NJP LABEL ;Переход по метке LABEL, если не флаг чётности
  JO LABEL  ;Переход по метке LABEL, если флаг переполнения
  NJO LABEL ;Переход по метке LABEL, если не флаг переполнения
  JS LABEL  ;Переход по метке LABEL, если флаг знака
  NJS LABEL ;Переход по метке LABEL, если не флаг знака
  JML LABEL ;Безусловный переход по метке LABEL
  
  NOPE ;Пропуск такта
  ```
  ## Запуск
  Находять в корневой папке, установите локальный пакет ассемблера pyasm: `pip3 install -e .`
  
  Запустите GUI эмулятора: `python3 gui/main.py`
  
  ## GUI
  Эмулятор имеет графический интерфейс, позволяющий быстро загрузить программу через соответствующее поле, 
  визуально отслеживать информацию в памяти, в стеке, в регистрах или флагах, выполнять программу сразу или по шагово с следованием по памяти.
  
  <img src="https://i.imgur.com/zhRWMlq.png" width="800">
