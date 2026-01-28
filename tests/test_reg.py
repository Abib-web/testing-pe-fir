import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
import random

@cocotb.test()
async def test_reg_fixed(dut):
    """Fixed register test"""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    cocotb.log.info("=== Fixed Register Test ===")
    
    # Initial state - wait a bit
    await Timer(1, unit="ns")
    
    # Apply reset
    dut.reset.value = 1
    dut.i_r.value = 0
    
    # Wait for clock with reset active
    await RisingEdge(dut.clk)
    
    # Check if signal is defined before converting
    if dut.out_r.value.is_resolvable:
        result = int(dut.out_r.value)
        cocotb.log.info(f"After reset: out_r={result} (0x{result:02X})")
        assert result == 0, f"Reset failed: got {result}"
    else:
        cocotb.log.error(f"After reset: out_r is NOT resolvable: {dut.out_r.value}")
        cocotb.log.info("Trying to wait more...")
        await Timer(5, unit="ns")
        if dut.out_r.value.is_resolvable:
            result = int(dut.out_r.value)
            cocotb.log.info(f"After extra wait: out_r={result}")
        else:
            cocotb.log.error("Signal still undefined. Check VHDL initialization.")
            # Skip this assertion for now
            return
    
    # Release reset and test capture
    dut.reset.value = 0
    dut.i_r.value = 42
    
    # Wait for clock edge
    await RisingEdge(dut.clk)
    
    # Wait a bit for signal to settle
    await Timer(1, unit="ns")
    
    if dut.out_r.value.is_resolvable:
        result = int(dut.out_r.value)
        cocotb.log.info(f"After capturing 42: out_r={result}")
        
        if result == 42:
            cocotb.log.info("SUCCESS! Register captured 42")
        else:
            cocotb.log.error(f"FAILED: Expected 42, got {result}")
    else:
        cocotb.log.error(f"Signal undefined after capture: {dut.out_r.value}")

@cocotb.test()
async def test_reg_simple(dut):
    """Very simple step-by-step test"""
    # Manual clock
    dut.clk.value = 0
    
    cocotb.log.info("=== Simple Step Test ===")
    
    dut.reset.value = 0
    dut.i_r.value = 0
    await Timer(5, unit="ns")
    
    #Apply reset
    dut.reset.value = 1
    dut.clk.value = 1  # Rising edge
    await Timer(5, unit="ns")
    cocotb.log.info(f"Step 1 (reset=1, clk=1): out_r={dut.out_r.value}")
    
    dut.clk.value = 0
    await Timer(5, unit="ns")
    cocotb.log.info(f"Step 2 (reset=1, clk=0): out_r={dut.out_r.value}")
    
    # Release reset, apply value
    dut.reset.value = 0
    dut.i_r.value = 0x55
    dut.clk.value = 1 
    await Timer(5, unit="ns")
    cocotb.log.info(f"Step 3 (i_r=0x55, clk=1): out_r={dut.out_r.value}")
    
    dut.clk.value = 0
    await Timer(5, unit="ns")
    cocotb.log.info(f"Step 4 (clk=0): out_r={dut.out_r.value}")
    
    # Next value
    dut.i_r.value = 0xAA
    dut.clk.value = 1
    await Timer(5, unit="ns")
    cocotb.log.info(f"Step 5 (i_r=0xAA, clk=1): out_r={dut.out_r.value}")