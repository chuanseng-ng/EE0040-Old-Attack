module s27(G0,G1,G3);
input G0,G1;
output G3;

  HS65_LH_NAND2X4 AND2_0 (.Z(G3), .A(G0), .B(G1) );
