library ieee;
use ieee.std_logic_1164.all;

entity reg_rtl is
    generic (N : integer := 8);
    port(
        i_r   : in  std_logic_vector(N-1 downto 0);
        reset : in  std_logic;
        clk   : in  std_logic;
        out_r : out std_logic_vector(N-1 downto 0)
    );
end reg_rtl;

architecture rtl of reg_rtl is
    signal reg : std_logic_vector(N-1 downto 0);
begin
    process(clk, reset)
    begin
        if reset = '1' then
            reg <= (others => '0');
        elsif rising_edge(clk) then
            reg <= i_r;
        end if;
    end process;
    
    out_r <= reg;
end rtl;