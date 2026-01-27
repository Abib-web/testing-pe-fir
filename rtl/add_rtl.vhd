library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity add_rtl is
    generic (N : integer := 16);
    port(
        i_a, i_b : in  std_logic_vector(N-1 downto 0);
        reset    : in  std_logic;
        out_c    : out std_logic_vector(N-1 downto 0)
    );
end add_rtl;

architecture addition of add_rtl is
begin
    process(i_a, i_b, reset)
    begin
        if reset = '1' then
            out_c <= (others => '0');
        else
            out_c <= std_logic_vector(signed(i_a) + signed(i_b));
        end if;
    end process;
end addition;