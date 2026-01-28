import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_add_basic(dut):
    """Basic adder test (combinatorial)"""
    cocotb.log.info("=== Basic adder test ===")
    
    # Test 1: Simple addition
    dut.reset.value = 0
    dut.i_a.value = 10
    dut.i_b.value = 20
    await Timer(10, unit="ns")  # Wait for propagation
    
    result = int(dut.out_c.value)
    assert result == 30, f"Expected 30, got {result}"
    cocotb.log.info(f"Test 1 PASSED: 10 + 20 = {result}")
    
    # Test 2: Reset
    dut.reset.value = 1
    await Timer(10, unit="ns")
    
    result = int(dut.out_c.value)
    assert result == 0, f"Expected 0 after reset, got {result}"
    cocotb.log.info(f"Test 2 PASSED: Reset works, output = {result}")
    
    # Test 3: Negative values
    dut.reset.value = 0
    dut.i_a.value = -50  # In two's complement
    dut.i_b.value = 30
    await Timer(10, unit="ns")
    
    result = int(dut.out_c.value)
    expected = (-50 + 30) & 0xFFFF  # Mask to 16 bits
    
    # Convert for display
    result_signed = result if result < 32768 else result - 65536
    
    assert result == expected, f"Expected {expected} (-20), got {result}"
    cocotb.log.info(f"Test 3 PASSED: -50 + 30 = {result_signed}")

@cocotb.test()
async def test_add_random(dut):
    """Random adder test"""
    cocotb.log.info("=== Random adder test ===")
    
    # Test 10 random additions
    for i in range(10):
        a = random.randint(-32768, 32767) 
        b = random.randint(-32768, 32767) 
        
        dut.reset.value = 0
        dut.i_a.value = a & 0xFFFF 
        dut.i_b.value = b & 0xFFFF
        await Timer(10, unit="ns")  
        
        result = int(dut.out_c.value)
        expected = (a + b) & 0xFFFF          
        # Convert for display
        result_signed = result if result < 32768 else result - 65536
        
        cocotb.log.info(f"Test {i+1}: {a} + {b} = {result_signed}")
        
        assert result == expected, f"Test {i+1} failed: {result} != {expected}"
    
    cocotb.log.info("All random addition tests passed!")