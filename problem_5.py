import hashlib
from datetime import datetime, timezone


class Block:
    def __init__(self, timestamp: datetime, data: str, previous_hash: str) -> None:
        self.timestamp: datetime.datetime = timestamp
        self.data: str = data
        self.previous_hash: str = previous_hash
        self.hash: str = self.calc_hash()
        self.next = None
        self.prev = None

    def calc_hash(self) -> str:
        sha = hashlib.sha256()
        hash_str = (str(self.timestamp) + str(self.data) +
                    str(self.previous_hash)).encode('utf-8')
        sha.update(hash_str)
        return sha.hexdigest()

    def __repr__(self) -> str:
        return (f"Block(\n"
                f"  Timestamp: {self.timestamp},\n"
                f"  Data: {self.data},\n"
                f"  Previous Hash: {self.previous_hash},\n"
                f"  Hash: {self.hash}\n"
                f")\n")


class Blockchain:
    def __init__(self) -> None:
        genesis_block = self.__create_genesis_block()
        self.head = genesis_block
        self.tail = genesis_block
        self.size = 1

    def __create_genesis_block(self) -> None:
        """
        Create the genesis block (the first block in the blockchain).
        """
        new_block = Block(datetime.now(timezone.utc), None, None)
        return new_block

    def add_block(self, data: str) -> None:
        new_block = Block(datetime.now(timezone.utc), data, self.tail.hash)

        self.tail.next = new_block
        new_block.prev = self.tail

        self.tail = new_block

        self.size += 1

    def __repr__(self) -> str:
        cur_node = self.head
        chain_str = ""
        while cur_node is not None:
            chain_str += str(cur_node) + "\n"
            cur_node = cur_node.next
        return chain_str

    def is_valid(self) -> bool:
        cur_block: Block = self.tail

        while cur_block is not None:
            if cur_block.hash != cur_block.calc_hash():
                return False

            prev_block: Block = cur_block.prev
            if prev_block:
                if cur_block.previous_hash != prev_block.calc_hash():
                    return False

            cur_block = prev_block

        return True


if __name__ == "__main__":
    # Test cases
    multi_block_chain = Blockchain()
    multi_block_chain.add_block("Block 1 Data")
    multi_block_chain.add_block("Block 2 Data")
    multi_block_chain.add_block("Block 3 Data")

    assert multi_block_chain.is_valid()
    print("✅ Test Case 1: Blockchain with multiple blocks valid when not tampered")

    empty_chain = Blockchain()
    assert empty_chain.is_valid()
    print("✅ Test Case 2: Empty block chain valid when not tampered")

    one_block_chain = Blockchain()
    one_block_chain.add_block("Block 1 data")
    assert one_block_chain.is_valid()
    print("✅ Test Case 3: Chain with one block valid when not tampered")

    random_block = multi_block_chain.head.next.next
    random_block.data = "Tampered Data"
    assert multi_block_chain.is_valid() == False
    print("✅ Test Case 4: Chain with multiple blocks invalid when one block is tampered")

    empty_chain.head.data = "Genesis block tampered"
    assert empty_chain.is_valid() == False
    print("✅ Test Case 5: Chain with no blocks invalid when genesis block is tampered")
