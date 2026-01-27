import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock

@cocotb.test()
async def test_only_register_corrected(dut):
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut.reset.value = 1
    dut.i_x.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    # Après reset
    assert int(dut.out_x.value) == 0
    print("Etape 1: Apres reset, out_x = 0 OK")

    # Relâcher reset
    dut.reset.value = 0

    # Appliquer i_x avant front
    dut.i_x.value = 10
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    # Le registre capture immédiatement
    assert int(dut.out_x.value) == 10
    print("Etape 2: Apres 1er front, out_x = 10 OK")

    # Cycle suivant
    dut.i_x.value = 20
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert int(dut.out_x.value) == 20
    print("Etape 3: Apres 2eme front, out_x = 20 OK")

    print("Test registre OK")


@cocotb.test()
async def test_pe_debug_calculation(dut):
    """Debug du calcul dans le PE"""
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.reset.value = 1
    await RisingEdge(dut.clk)
    dut.reset.value = 0
    
    print("=== Debug calcul PE ===")
    
    # Appliquer des valeurs simples
    # Cycle 1: x=2 entre
    dut.i_x.value = 2
    dut.w.value = 3
    dut.i_s.value = 4
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    
    print(f"Cycle 1: i_x=2, w=3, s=4")
    print(f"  out_x = {int(dut.out_x.value)}")
    print(f"  out_s = {int(dut.out_s.value)}")
    print(f"  Attendu: out_x=2, out_s=4 (car x precedent = 0)")
    print(f"  Calcul: 4 + 3*0 = 4")
    
    # Cycle 2: x=5 entre
    dut.i_x.value = 5
    dut.w.value = 0  # Mettre w=0 pour isoler
    dut.i_s.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    
    print(f"\nCycle 2: i_x=5, w=0, s=0")
    print(f"  out_x = {int(dut.out_x.value)}")
    print(f"  out_s = {int(dut.out_s.value)}")
    print(f"  Attendu: out_x=5, out_s=0")
    
    # Cycle 3: Tester multiplication seule
    dut.i_x.value = 0
    dut.w.value = 3  # Multiplier avec x precedent=5
    dut.i_s.value = 0  # Pas d'addition
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    
    print(f"\nCycle 3: i_x=0, w=3, s=0")
    print(f"  out_x = {int(dut.out_x.value)}")
    print(f"  out_s = {int(dut.out_s.value)}")
    print(f"  Attendu: out_x=0, out_s=15 (3*5)")
    
    # Cycle 4: Tester addition seule
    dut.i_x.value = 0
    dut.w.value = 0  # Pas de multiplication
    dut.i_s.value = 10  # Juste addition
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    
    print(f"\nCycle 4: i_x=0, w=0, s=10")
    print(f"  out_x = {int(dut.out_x.value)}")
    print(f"  out_s = {int(dut.out_s.value)}")
    print(f"  Attendu: out_x=0, out_s=10")

@cocotb.test()
async def test_pe_complete(dut):
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.reset.value = 1
    dut.i_x.value = 0
    dut.w.value = 0
    dut.i_s.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    
    print("Cycle 0: Reset")
    print(f"  out_x = {int(dut.out_x.value)}, out_s = {int(dut.out_s.value)}")
    
    # Cycle 1: Appliquer valeurs
    dut.reset.value = 0
    dut.i_x.value = 2
    dut.w.value = 0
    dut.i_s.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    
    print("Cycle 1: i_x=2, w=0, s=0")
    print(f"  out_x = {int(dut.out_x.value)} (devrait etre 0 - valeur reset)")
    print(f"  out_s = {int(dut.out_s.value)} (devrait etre 0)")
    
    # Cycle 2: Utiliser x retarde
    dut.i_x.value = 5
    dut.w.value = 3
    dut.i_s.value = 4
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    
    print("Cycle 2: i_x=5, w=3, s=4")
    print(f"  out_x = {int(dut.out_x.value)} (devrait etre 2 - valeur cycle 1)")
    print(f"  out_s = {int(dut.out_s.value)} (devrait etre 4 + 3*2 = 10)")
    
    # Cycle 3: Suite
    dut.i_x.value = 0
    dut.w.value = 2
    dut.i_s.value = 6
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    
    print("Cycle 3: i_x=0, w=2, s=6")
    print(f"  out_x = {int(dut.out_x.value)} (devrait etre 5 - valeur cycle 2)")
    print(f"  out_s = {int(dut.out_s.value)} (devrait etre 6 + 2*5 = 16)")

@cocotb.test()
async def test_direct_inspection(dut):
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())
    
    print("Test inspection directe")
    
    # Reset
    dut.reset.value = 1
    dut.i_x.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    
    print(f"Apres reset: out_x = {int(dut.out_x.value)}")
    
    # Essayer d'appliquer i_x et voir IMMEDIATEMENT
    dut.reset.value = 0
    dut.i_x.value = 10
    
    # Attendre un peu SANS horloge
    await Timer(5, unit="ns")
    
    print(f"Apres i_x=10 (sans horloge): out_x = {int(dut.out_x.value)}")
    
    # Maintenant front d'horloge
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    
    print(f"Apres horloge: out_x = {int(dut.out_x.value)}")