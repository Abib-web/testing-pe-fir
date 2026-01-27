import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mult_basic(dut):
    """Basic multiplier test (combinatorial)"""
    cocotb.log.info("=== Basic multiplier test ===")
    
    # Test 1: Simple multiplication
    dut.reset.value = 0
    dut.i_a.value = 3
    dut.i_b.value = 4
    await Timer(10, unit="ns")  # Wait for propagation
    
    result = int(dut.out_c.value)
    expected = 3 * 4  # 12
    assert result == expected, f"Expected {expected}, got {result}"
    cocotb.log.info(f"Test 1 PASSED: 3 * 4 = {result}")
    
    # Test 2: Reset
    dut.reset.value = 1
    await Timer(10, unit="ns")
    
    result = int(dut.out_c.value)
    assert result == 0, f"Expected 0 after reset, got {result}"
    cocotb.log.info(f"Test 2 PASSED: Reset works, output = {result}")
    
    # Test 3: Negative values
    dut.reset.value = 0
    dut.i_a.value = -5  # 8-bit signed
    dut.i_b.value = 3
    await Timer(10, unit="ns")
    
    result = int(dut.out_c.value)
    expected = (-5 * 3) & 0xFFFF  # Mask to 16 bits
    
    # Show signed value for clarity
    result_signed = result if result < 32768 else result - 65536
    
    assert result == expected, f"Expected {expected}, got {result}"
    cocotb.log.info(f"Test 3 PASSED: -5 * 3 = {result_signed}")

@cocotb.test()
async def test_mult_random(dut):
    """Random multiplier test"""
    cocotb.log.info("=== Random multiplier test ===")
    
    # Test 10 random multiplications
    for i in range(10):
        a = random.randint(-128, 127)  # 8-bit signed
        b = random.randint(-128, 127)  # 8-bit signed
        
        dut.reset.value = 0
        dut.i_a.value = a & 0xFF  # Mask to 8 bits
        dut.i_b.value = b & 0xFF
        await Timer(10, unit="ns")  # Wait for propagation
        
        result = int(dut.out_c.value)
        expected = (a * b) & 0xFFFF  # Mask to 16 bits
        
        # Convert for display
        result_signed = result if result < 32768 else result - 65536
        
        cocotb.log.info(f"Test {i+1}: {a} * {b} = {result_signed}")
        
        assert result == expected, f"Test {i+1} failed: {result} != {expected}"
    
    cocotb.log.info("All random multiplication tests passed!")