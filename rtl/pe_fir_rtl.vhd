library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity pe_fir_rtl is
    generic (N : integer := 8);
    port(
        i_x, w    : in  std_logic_vector(N-1 downto 0);
        i_s       : in  std_logic_vector(2*N-1 downto 0);
        reset, clk: in  std_logic;
        out_s     : out std_logic_vector(2*N-1 downto 0);
        out_x     : out std_logic_vector(N-1 downto 0)
    );
end pe_fir_rtl;

architecture rtl of pe_fir_rtl is
    -- Signaux internes
    signal reg_out_x : std_logic_vector(N-1 downto 0);
    signal mult_result : std_logic_vector(2*N-1 downto 0);
    signal add_result : std_logic_vector(2*N-1 downto 0);
    
begin
    -- 1. Registre sur x (latence 1 cycle)
    reg_inst : entity work.reg_rtl
        generic map (N => N)
        port map (
            i_r => i_x,
            reset => reset,
            clk => clk,
            out_r => reg_out_x
        );
    
    -- out_x est la sortie du registre
    out_x <= reg_out_x;
    
    -- 2. Multiplicateur combinatoire
    mult_inst : entity work.mult_rtl
        generic map (N => N)
        port map (
            i_a => w,
            i_b => reg_out_x,  -- x retardé d'un cycle
            reset => reset,
            out_c => mult_result
        );
    
    -- 3. Additionneur combinatoire
    add_inst : entity work.add_rtl
        generic map (N => 2*N)
        port map (
            i_a => i_s,
            i_b => mult_result,
            reset => reset,
            out_c => out_s  -- Sortie directe
        );
    
end rtl;