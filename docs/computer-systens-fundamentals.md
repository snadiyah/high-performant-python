# Computer System Fundamentals

There are 3 basic parts that affects speed

- Computing Units
- Memory Units
- Communication

## Computing Units
Speed depends on:

- Instruction per Cycle (IPC):
    - IPC = how much work the CPU can do in one tick 
    - IPC tells you how many instructions the CPU can complete per cycle
    
- Clock Speed
    - Number of cycles completed in one sec

GPU: High IPC, High Clock Speed but slow communication


----
## Memory Units


- Spinning Hard-drive
    - Spinning hard drive with persistent storage but slow read and write
- Solid-state Hard-drive
    - Similar with spinning hd, faster read/write but max 1TB
- RAM (Max capacity 64GB)
    - Store app code and data
    - Fast read/write
- L1/L2 Cache (Capacity @ megabytes)
    - Extremely fast but very small capacity
  
----

## Communication layer

- Front side bus
  Communication used for RAM <---> Cache
  
- External bus
  Communication used for HD <>network cards, HD<>CPU, HD<>System Memory
  
GPU communicate via PCI - which is much slower than frontside  bus

### Bus Speed

Bus speed describes how fast data can be transferred across a system bus. It is determined by two main properties:

**Bus Width** 

Bus width defines how much data can be transferred in a single cycle.
- Measured in bits (e.g. 8-bit, 32-bit, 64-bit)
- Wider buses can carry more data at the same time

**Analogy:**  
Bus width is like the number of lanes on a highway — more lanes allow more cars to travel simultaneously.

---

**Bus Frequency** 

Bus frequency defines how often data transfer cycles occur.
- Measured in Hz, MHz, or GHz
- Higher frequency means more transfer cycles per second

**Analogy:**  
Bus frequency is like the speed limit on the highway — higher speed allows cars to move more often per second.

*Bus speed (bandwidth) is the combination of bus width and bus frequency*


  





