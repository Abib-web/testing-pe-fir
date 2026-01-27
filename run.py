import os
from cocotb_test.simulator import run

GHDL_ROOT = r"C:\Users\o.kone\OneDrive - Aldes Aeraulique\Desktop\ghdl"

os.environ["PATH"] = GHDL_ROOT + r"\bin;" + os.environ["PATH"]
os.environ["GHDL_PREFIX"] = GHDL_ROOT + r"\lib\ghdl"

""" # Test de l'additionneur
run(
    simulator="ghdl",
    vhdl_sources=["rtl/add_rtl.vhd"],
    toplevel="add_rtl",
    module="tests.test_add",  # Test spécifique à l'additionneur
    vhdl_compile_args=["--std=08"],
)

# Test du multiplieur
run(
    simulator="ghdl",
    vhdl_sources=["rtl/mult_rtl.vhd"],
    toplevel="mult_rtl",
    module="tests.test_mult", 
    vhdl_compile_args=["--std=08"],
)

# Test du registre
run(
    simulator="ghdl",
    vhdl_sources=["rtl/reg_rtl.vhd"],
    toplevel="reg_rtl",
    module="tests.test_reg",  
    vhdl_compile_args=["--std=08"],
) """
run(
    simulator="ghdl",
    vhdl_sources=[
        "rtl/add_rtl.vhd",    # Nécessaire pour pe_fir_rtl
        "rtl/mult_rtl.vhd",   # Nécessaire pour pe_fir_rtl  
        "rtl/reg_rtl.vhd",    # Nécessaire pour pe_fir_rtl
        "rtl/pe_fir_rtl.vhd", # Top-level
    ],
    toplevel="pe_fir_rtl",
    module="tests.test_pe",  
    vhdl_compile_args=["--std=08"],
)