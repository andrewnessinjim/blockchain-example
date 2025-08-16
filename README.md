# Simplified Blockchain Implementation

## Block Design:

Each block in the chain is a node, and these nodes are doubly linked to form a doubly linked list.

Each block object (from `Block` class) has the following parameters:

- `data`: This can hold any kind of data in a real world blockchain. But we are storing strings in this example.
- `timestamp`: This is the block creation time in GMT.
- `hash`: This is the hash of the block calculated by the `_calculate_hash()` method. The string `data`, `timestamp` and `previous_hash` are used in combination to generate the hash using sha256 algorithm.
- `previous_hash`: This holds the hash of the previous block in the chain. This is a key feature of blockchain. If any block is modified, its hash changes and thus invalidates the next block in the chain and trying to make it valid will invalidate the next block. This makes tampering data very difficult. It is further made difficult by adding a constraint on the hash code pattern. This increases the computation power needed for generating a valid hash and makes it almost impossible to make the chain valid again once tampered. This is called proof of work and not implemented in this simplified version.
- `prev` and `next`: These are pointers used to form the doubly-linked list, or in other words, doubly-linked blockchain.

## Blockchain Design and Time Complexity

The blockchain class supports two operations - adding data and testing if the chain is valid. Their working and time complexity are explained in this section.

### Adding Data (or block)

Adding a block (`add_block` function) requires the below actions:

1. Get the hash code of the latest block. This can be done in `O(1)` time because the blockchain holds a `tail` pointer that always points to the latest block.
2. Get current timestamp. This is `O(1)`.
3. Calculate the hash of the block. This depends on 3 values - `data`, `previous_hash` (from step 1) and `timestamp` (from step 2). The last 2 values are always constant length. The hash algorithm needs to iterate on each character of our string `data`. If the max length of our data is `s`, then this step's complexity is `O(s)` .
4. Create a block from the values in steps 1, 2 and 3. This is `O(1)` because we just create a python object with the calculated values.
5. Set the current `tail`'s `next` pointer to the new block. Set the new block's `prev` pointer to the current `tail`. Update the `tail` to point to the new block. All this is constant time operation because the reference to `tail` is already available and no iteration is involved.

Overall, by summing up each of the complexities in the above list, adding a block needs `O(1 + 1 + s + 1 + 1)`. By dropping constants, the time complexity to add a block is `O(s)`.

### Validation

Validating starts from the tail of the chain (current block will be tail in first iteration) and below steps are required:

1. Calculate the hash code of the current block and compare with the stored hash. If they are different, the block and the whole chain is invalid. Calculating the hash is `O(s)` as described in the previous section
2. If they are the same, we compare its `previous_hash` value the previous block's `hash`. This is `O(1)` operation because the chain is doubly linked and we can refer the previous node in constant time. If they are not same, the chain is invalid.
3. We repeat steps 1 and 2 for every block in the chain in the reverse order of insertion. In the worst case we have to iterate through the whole chain. If there are `n` blocks, then we iterate `n` times.

From step 3, we are iterating `n` times. From step 1 and 2, we need `O(s + 1)` time in each iteration. Hence, the overall time complexity is `O(n * (s + 1))`, or `O(ns + n)`. By dropping lower order terms, the time complexity for checking the validity of the blockchain is `O(ns)`.

## Space Complexity

The space complexity is also `O(ns)` because we need space to store `n` blocks and each block's `data` can be of length `s` at max. Other values in a block are of constant size - `hash`, `previous_hash`, `timestamp`, `prev` and `next`, so they do not contribute to the space complexity.

## References

[YouTube: Blockchain: Massively Simplified | Richie Etwaru | TEDxMorristown](https://www.youtube.com/watch?v=k53LUZxUF50)  
[YouTube: How does a blockchain work - Simply Explained](https://www.youtube.com/watch?v=SSo_EIwHSd4)  
[YouTube: Creating a blockchain with Javascript](https://www.youtube.com/watch?v=zVqczFZr124)  
[Udacity Knowledge: Detailed problem description](https://knowledge.udacity.com/questions/363520)  
[How to protect the latest block in block chain be tampered?](https://bitcoin.stackexchange.com/questions/79258/how-to-protect-the-latest-block-in-block-chain-be-tampered)
