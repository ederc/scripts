system("--allow-net", 1);
system("--min-time", "0.001");
system("--ticks-per-sec", 1000);
LIB"LIB/f5ex2.lib";
sprintf("Example: F-744-h");
f744();
//schrans_troost();
bigint mem2 = memory(2);
int tr = timer;
ideal g = f5e(i);
timer-tr;
memory(2)-mem2;
nvars(basering);
size(i);
size(g);
$
