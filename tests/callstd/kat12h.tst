system("--allow-net", 1);
system("--min-time", "0.001");
system("--ticks-per-sec", 1000);
LIB"../LIB/f5ex2.lib";
sprintf("Example: Katsura-12-h");
katsuranh(12);
bigint mem2 = memory(2);
int tr = timer;
ideal g = std(i);
timer-tr;
memory(2)-mem2;
nvars(basering);
size(i);
size(g);
$
