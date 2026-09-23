# The Transformer Architecture, In Depth: Encoder and Decoder

## Overview: Why the Transformer Exists

Before Transformers, sequence models (RNNs, LSTMs) processed tokens one at a time, in order — which made them slow to train (no parallelism across the sequence) and prone to losing information over long distances. The Transformer's core bet: replace recurrence entirely with **attention**, so every token can look directly at every other token, in parallel, regardless of distance.

```mermaid
graph LR
    A[RNN/LSTM] --> B[Sequential processing<br/>token by token]
    C[Transformer] --> D[Parallel processing<br/>via attention]
    B --> E[Slow training,<br/>long-range info decays]
    D --> F[Fast training,<br/>direct long-range access]
```

## The Full Architecture at a Glance

```mermaid
graph TD
    A[Input Tokens] --> B[Input Embedding + Positional Encoding]
    B --> C[Encoder Stack<br/>N layers]
    C --> D[Encoder Output]

    E[Output Tokens<br/>shifted right] --> F[Output Embedding + Positional Encoding]
    F --> G[Decoder Stack<br/>N layers]
    D --> G
    G --> H[Linear Layer]
    H --> I[Softmax]
    I --> J[Output Probabilities]
```

The original Transformer ("Attention Is All You Need") is an **encoder-decoder** architecture, built for sequence-to-sequence tasks like translation. Modern LLMs typically use only one half — GPT-style models use decoder-only, BERT-style models use encoder-only — but both are built from the same underlying blocks, so understanding the full architecture explains both.

## Step 1: Input Embedding and Positional Encoding (Shared by Both Sides)

### Embeddings

Each input token (a word or subword) is converted into a dense vector — a learned representation that captures meaning, not just an arbitrary ID.

```mermaid
graph LR
    A["Token: 'cat'"] --> B[Embedding Lookup Table] --> C[Dense vector<br/>e.g. 512 dimensions]
```

### Positional Encoding

Because attention has no inherent sense of order — it looks at all tokens simultaneously — the model needs a separate signal telling it *where* each token sits in the sequence.

```mermaid
graph TD
    A[Token Embedding] --> C[+]
    B[Positional Encoding<br/>sin/cos functions of position] --> C
    C --> D[Final Input Representation]
```

The original paper uses fixed sine and cosine functions at different frequencies for each position:

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

This particular choice (sinusoidal, rather than a learned embedding) lets the model generalize to sequence lengths it didn't see during training, and gives it an easy way to learn *relative* positions, since `PE(pos+k)` can be expressed as a linear function of `PE(pos)`.

## Step 2: The Core Mechanism — Scaled Dot-Product Attention

Every attention block in the Transformer — encoder self-attention, decoder self-attention, and encoder-decoder cross-attention — uses the same underlying operation, just with different inputs.

```mermaid
graph TD
    A[Input] --> B[Query Q]
    A --> C[Key K]
    A --> D[Value V]
    B --> E["Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) · V"]
    C --> E
    D --> E
    E --> F[Output]
```

### The Intuition

- **Query (Q)** — "what am I looking for?" — a representation of the current token's information need
- **Key (K)** — "what do I contain?" — a representation each token exposes about itself
- **Value (V)** — "what do I actually contribute?" — the information passed along if attended to

The dot product `Q·K^T` measures how well each query matches each key (similarity), scaled down by `sqrt(d_k)` to keep gradients stable (large dot products push softmax into regions with tiny gradients), then passed through softmax to get attention weights that sum to 1, which are used to compute a weighted sum of the values.

```mermaid
sequenceDiagram
    participant Query
    participant Key
    participant Value

    Query->>Key: Dot product (similarity score)
    Note over Query,Key: Scaled by sqrt(d_k)
    Key->>Key: Softmax across all keys
    Key->>Value: Weighted sum using<br/>softmax weights
    Value-->>Query: Attention output
```

### Multi-Head Attention

Rather than computing attention once, the Transformer splits Q, K, V into multiple smaller "heads," runs attention in parallel across each, and concatenates the results.

```mermaid
graph TD
    A[Input] --> B[Linear projections<br/>into h heads]
    B --> C[Head 1 Attention]
    B --> D[Head 2 Attention]
    B --> E[Head ... Attention]
    B --> F[Head h Attention]
    C & D & E & F --> G[Concatenate]
    G --> H[Final Linear Projection]
```

Each head can learn to focus on a different kind of relationship — one head might track syntactic dependencies, another might track coreference, another might track local word order — and multi-head attention lets the model capture all of these simultaneously rather than being forced into a single attention pattern.

## The Encoder Block

### Structure

```mermaid
graph TD
    A[Input from<br/>previous layer] --> B[Multi-Head Self-Attention]
    B --> C[Add & Norm]
    A -.residual.-> C
    C --> D[Feed-Forward Network]
    D --> E[Add & Norm]
    C -.residual.-> E
    E --> F[Output to<br/>next layer]
```

Each encoder layer has exactly two sub-layers: multi-head self-attention, then a position-wise feed-forward network — each wrapped with a residual connection and layer normalization.

### Self-Attention in the Encoder

"Self" means Q, K, and V all come from the *same* sequence — every token in the input attends to every other token in the input, including itself, with **no restrictions** on what it can see (unlike the decoder, covered below).

```mermaid
graph LR
    A["Token: 'The'"] -.attends to.-> B["Token: 'cat'"]
    A -.attends to.-> C["Token: 'sat'"]
    A -.attends to.-> D["Token: 'on'"]
    A -.attends to.-> E["Token: 'the'"]
    A -.attends to.-> F["Token: 'mat'"]
```

This is why encoders are well-suited to *understanding* tasks — classification, embedding generation — where the whole input is available at once and every part of it can inform every other part.

### Add & Norm (Residual Connection + Layer Normalization)

```mermaid
graph LR
    A[Sub-layer input x] --> B[Sub-layer function<br/>e.g. Attention]
    A --> C["+"]
    B --> C
    C --> D[Layer Normalization]
    D --> E[Output]
```

`LayerNorm(x + Sublayer(x))` — the residual connection (`x +`) lets gradients flow directly through the network during backpropagation, which is what makes it practical to stack many layers deep without vanishing gradients; layer normalization stabilizes the scale of activations at each layer.

### The Feed-Forward Network

A simple two-layer fully-connected network, applied identically and independently to each position:

```
FFN(x) = max(0, xW1 + b1)W2 + b2
```

```mermaid
graph LR
    A[Attention output<br/>per position] --> B[Linear<br/>expand dimension]
    B --> C[ReLU]
    C --> D[Linear<br/>project back down]
```

While attention lets tokens exchange information with each other, the feed-forward network processes each token's representation independently afterward — it's where a lot of the model's per-token "reasoning" capacity actually lives.

### Stacking Encoder Layers

```mermaid
graph TD
    A[Input Embeddings + PE] --> B[Encoder Layer 1]
    B --> C[Encoder Layer 2]
    C --> D[...]
    D --> E[Encoder Layer N]
    E --> F[Final Encoder Output]
```

The original paper stacks 6 identical encoder layers (N=6); larger modern models stack far more. Each layer refines the representation further, building progressively richer contextual understanding of every token.

## The Decoder Block

### Structure

```mermaid
graph TD
    A[Output tokens so far<br/>shifted right] --> B[Masked Multi-Head<br/>Self-Attention]
    B --> C[Add & Norm]
    A -.residual.-> C
    C --> D[Multi-Head<br/>Cross-Attention]
    E[Encoder Output] --> D
    D --> F[Add & Norm]
    C -.residual.-> F
    F --> G[Feed-Forward Network]
    G --> H[Add & Norm]
    F -.residual.-> H
    H --> I[Output to<br/>next layer]
```

Each decoder layer has **three** sub-layers — one more than the encoder — because it needs to both attend to what it's generated so far *and* attend to the encoder's output.

### Masked Self-Attention

The decoder generates output tokens one at a time, left to right. At training time, it sees the full target sequence at once (for parallel training), but it must be prevented from "cheating" by looking at future tokens it hasn't generated yet.

```mermaid
graph TD
    A["Position 3<br/>('sat')"] -.can attend to.-> B["Position 1<br/>('The')"]
    A -.can attend to.-> C["Position 2<br/>('cat')"]
    A -.can attend to.-> A
    A -.X cannot attend to.-> D["Position 4<br/>('on') — future"]
```

This is enforced with a **causal mask**: before the softmax step in attention, all positions corresponding to future tokens are set to `-infinity`, so after softmax their attention weight becomes exactly 0.

```mermaid
graph LR
    A[Raw attention scores] --> B[Apply causal mask:<br/>future positions = -infinity]
    B --> C[Softmax]
    C --> D["Future positions get<br/>weight = 0"]
```

This single mechanism is what makes the decoder autoregressive — each position's output can only depend on positions at or before it, matching how generation actually works at inference time (you can't attend to a word you haven't generated yet).

### Cross-Attention (Encoder-Decoder Attention)

The second sub-layer is where the decoder actually consults the input sequence. Here, the **Query** comes from the decoder's own (masked self-attention) output, but the **Key and Value** come from the encoder's final output.

```mermaid
graph TD
    A[Decoder's Query<br/>from masked self-attention] --> C[Cross-Attention]
    B[Encoder Output<br/>as Key and Value] --> C
    C --> D["Decoder token asks:<br/>'which input tokens<br/>are relevant to me right now?'"]
```

This is the mechanism that actually connects the two halves — without cross-attention, the decoder would be generating output with no knowledge of the input at all. In translation, this is where "the French word I'm generating now" learns to attend to "the relevant English words" from the source sentence.

### Feed-Forward Network and Add & Norm

Identical in structure and purpose to the encoder's version — a two-layer network applied per-position, wrapped in a residual connection and layer normalization.

### Stacking Decoder Layers

```mermaid
graph TD
    A[Output Embeddings + PE] --> B[Decoder Layer 1]
    B --> C[Decoder Layer 2]
    C --> D[...]
    D --> E[Decoder Layer N]
    E --> F[Final Decoder Output]
```

Every decoder layer performs cross-attention against the *same* final encoder output — the encoder runs once, and its output is reused by every decoder layer.

## Step 3: Final Output — Linear + Softmax

```mermaid
graph LR
    A[Decoder Output] --> B[Linear Layer<br/>projects to vocabulary size]
    B --> C[Softmax]
    C --> D[Probability distribution<br/>over the vocabulary]
```

The decoder's final representation for each position is projected (via a linear layer) into a vector the size of the entire vocabulary, then softmax turns that into a probability distribution — the model's predicted next token. During generation, this happens one token at a time, with the newly generated token fed back in as part of the input for predicting the next one.

## Encoder vs. Decoder — Side-by-Side

```mermaid
graph TD
    A[Encoder] --> B[Self-Attention<br/>unmasked, bidirectional]
    A --> C[Feed-Forward]
    D[Decoder] --> E[Self-Attention<br/>masked, causal]
    D --> F[Cross-Attention<br/>to encoder output]
    D --> G[Feed-Forward]
```

| | Encoder | Decoder |
|---|---|---|
| Sub-layers per block | 2 (self-attention, FFN) | 3 (masked self-attn, cross-attn, FFN) |
| Self-attention type | Unmasked — sees the whole input | Masked/causal — sees only past + present |
| Extra attention type | None | Cross-attention to encoder output |
| Typical use | Understanding tasks (classification, embeddings) — e.g. BERT | Generation tasks (autoregressive text generation) — e.g. GPT |
| Runs once or repeatedly at inference? | Once per input | Repeatedly, one token at a time |

## Why Modern LLMs Are Often Decoder-Only

```mermaid
graph TD
    A[Full Encoder-Decoder<br/>e.g. original Transformer, T5] --> B[Best for: translation,<br/>distinct input/output sequences]
    C[Encoder-Only<br/>e.g. BERT] --> D[Best for: classification,<br/>embeddings, understanding]
    E[Decoder-Only<br/>e.g. GPT family] --> F[Best for: open-ended generation,<br/>a single unified text stream]
```

Most modern general-purpose LLMs (GPT-family models, and similar) use **decoder-only** architectures: there's no separate encoder, and the "input" (prompt) and "output" (completion) are just treated as one continuous sequence with causal masking throughout. This works well because a decoder-only model, with sufficiently causal self-attention, is already capable of "understanding" the prompt (through the tokens it can attend to) before generating a response — you don't strictly need a separate encoder pass to get that.

## Summary

- **Shared foundation:** token embeddings + positional encoding, and the same scaled dot-product attention mechanism used throughout
- **Encoder block:** unmasked self-attention (every token sees every other token) + feed-forward network, each wrapped in residual connections and layer norm; stacked N times; well-suited to understanding the full input at once
- **Decoder block:** masked/causal self-attention (only past + present) + cross-attention to the encoder's output + feed-forward network; stacked N times; built for autoregressive generation
- **Cross-attention** is the specific mechanism connecting the two halves — decoder queries, encoder keys/values
- **Final step:** linear projection to vocabulary size, then softmax, to produce the next-token probability distribution
