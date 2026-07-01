# Kafka Data Streaming — Simple Guide

## 1. What is Kafka? (In Plain English)

Imagine a **post office** that never stops running. People (producers) drop letters into mailboxes (topics). Other people (consumers) come and pick up letters from those mailboxes whenever they want. The post office (Kafka) keeps track of every letter, in order, even after it's been picked up — so multiple people can read the same letter without it disappearing.

That's Kafka: a system for **moving streams of data (messages/events) from one place to another, reliably and in order.**

### Simple Example

A food delivery app:
- When a user places an order → the app **produces** a message: `"Order #123 placed"`
- Kafka stores this message in a **topic** called `orders`
- The kitchen service **consumes** that message to start cooking
- The delivery service **consumes** the same message to assign a driver
- The billing service **consumes** it too, to charge the customer

One event → many independent systems react to it, without talking to each other directly.

---

## 2. The Core Building Blocks

```
                         KAFKA CLUSTER
   ┌────────────────────────────────────────────────┐
   │                                                  │
   │   Topic: "orders"                                │
   │   ┌───────────────┐ ┌───────────────┐            │
   │   │ Partition 0   │ │ Partition 1   │            │
   │   │ [msg0][msg1]..│ │ [msg0][msg1]..│            │
   │   └───────────────┘ └───────────────┘            │
   │                                                  │
   └────────────────────────────────────────────────┘
        ▲                              │
        │ writes                       │ reads
        │                              ▼
 ┌─────────────┐               ┌───────────────┐
 │  PRODUCER   │               │   CONSUMER    │
 │ (App/Order  │               │ (Kitchen App, │
 │  Service)   │               │  Billing App) │
 └─────────────┘               └───────────────┘
```

| Term | Simple Meaning |
|---|---|
| **Topic** | A named category/mailbox for messages (e.g. `orders`) |
| **Partition** | A topic is split into partitions for scale — like splitting one mailbox into several lanes |
| **Producer** | The app that sends (writes) messages |
| **Consumer** | The app that reads messages |
| **Consumer Group** | A team of consumers sharing the work of reading a topic |
| **Broker** | A Kafka server that stores and serves the data |
| **Offset** | A bookmark — "I've read up to message #45" |

---

## 3. How Data Flows (Step by Step)

```
Producer                Kafka Broker                 Consumer
   │                          │                            │
   │  1. Send("order-123")    │                            │
   ├─────────────────────────>│                            │
   │                          │  2. Store in Partition       
   │                          │     [order-123] appended    
   │                          │                            │
   │                          │  3. Consumer polls topic     
   │                          │<───────────────────────────┤
   │                          │  4. Return message          
   │                          ├─────────────────────────────>
   │                          │  5. Consumer processes it   │
   │                          │  6. Commit offset (bookmark)│
   │                          │<─────────────────────────────
```

Kafka doesn't delete the message right after it's read — it stays for a configured time, so other consumers (or the same one, replaying) can read it again.

---

## 4. Producer Configuration — What to Watch

| Config | What it Does | Simple Advice |
|---|---|---|
| `bootstrap.servers` | Which Kafka brokers to connect to | Always list 2–3 for redundancy, not just one |
| `acks` | How many brokers must confirm receipt before producer considers the send "successful" | `acks=all` → safest (no data loss), `acks=1` → faster but riskier |
| `key.serializer` / `value.serializer` | How to convert your data (object → bytes) | Match the format your consumers expect (e.g. String, JSON, Avro) |
| `retries` | How many times to retry a failed send | Set > 0, combine with `acks=all` to avoid silent data loss |
| `enable.idempotence` | Prevents duplicate messages when retrying | Set `true` for exactly-once-ish delivery |
| `linger.ms` | Wait a little before sending, to batch messages together | Small value (5–20ms) improves throughput |
| `batch.size` | Max size of a batch of messages sent together | Bigger = more throughput, but more delay |
| `compression.type` | Compress messages before sending | `snappy` or `lz4` — saves bandwidth and disk |
| `max.in.flight.requests.per.connection` | How many unacknowledged requests can be sent at once | Set to `1` if you need strict ordering with retries |

**Golden rule:** if you care about **not losing data**, use `acks=all` + `retries>0` + `enable.idempotence=true`.

---

## 5. Consumer Configuration — What to Watch

| Config | What it Does | Simple Advice |
|---|---|---|
| `bootstrap.servers` | Brokers to connect to | Same as producer — list multiple |
| `group.id` | Identifies which consumer group this consumer belongs to | Consumers in the same group split the work; different group = each gets a full copy |
| `auto.offset.reset` | Where to start reading if no offset is saved yet | `earliest` = read from the beginning, `latest` = read only new messages |
| `enable.auto.commit` | Whether Kafka automatically saves your "bookmark" (offset) | Turn `false` if you want to control exactly when to commit (safer, avoids losing/reprocessing messages) |
| `key.deserializer` / `value.deserializer` | How to convert bytes back into your data | Must match what the producer used |
| `max.poll.records` | Max messages fetched in a single poll | Lower it if message processing is slow, to avoid timeouts |
| `session.timeout.ms` / `heartbeat.interval.ms` | Detects if a consumer has "died" | Increase if your processing takes a long time, to avoid being kicked out of the group |
| `fetch.min.bytes` | Minimum data size before broker responds | Higher value = better throughput, slightly more latency |

**Golden rule:** if you care about **not processing a message twice or skipping one**, turn off `enable.auto.commit` and manually commit *after* successfully processing the message.

---

## 6. Quick Mental Model

```
 PRODUCER SIDE                     CONSUMER SIDE
 ─────────────                     ─────────────
 "Did my message                   "Where do I start reading,
  get saved safely?"                and when do I mark it as done?"

  → acks                            → auto.offset.reset
  → retries                         → enable.auto.commit
  → idempotence                     → group.id
```

Producer configs are mostly about **reliability of sending**.
Consumer configs are mostly about **reliability of reading and tracking progress**.

---

## 7. TL;DR

- Kafka = a durable, ordered, replayable message pipeline.
- **Topics** hold data, split into **partitions** for scale.
- **Producers** write, **consumers** read (often in **consumer groups**).
- For safety: producer → `acks=all`, `idempotence=true`; consumer → manual offset commits.
- For speed: tune `batch.size`, `linger.ms`, `compression.type`, `fetch.min.bytes`.
