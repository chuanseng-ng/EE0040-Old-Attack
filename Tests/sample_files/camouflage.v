
`timescale 1 ns/1 ps
module camouflage (
a,b,c,d,CLK,NRST,
Q1,Q2,Q3);

input a,b,c,d,CLK,NRST;
output Q1,Q2,Q3;

wire n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13;

HS65_LH_OR2X4 U1 (.Z(n1), .A(n6), .B(a) );

HS65_LH_NOR2X2 U2 (.Z(n2), .A(c), .B(d) );

HS65_LH_NAND2X2 U3 (.Z(n3), .A(n1), .B(b) );
HS65_LH_NAND2X2 U4 (.Z(n5), .A(n2), .B(b) );
HS65_LH_NAND2X2 U5 (.Z(n4), .A(n3), .B(n2) );

HS65_LH_DFPRQX4 U6 (.D(n4), .CP(n10), .RN(n13), .Q(Q3) );
HS65_LH_DFPRQX4 U7 (.D(n5), .CP(n12), .RN(n13), .Q(n7) );

HS65_LH_NAND2X2 U8 (.Z(n6), .A(Q3), .B(n5) );

HS65_LHS_XOR2X3 U9 (.Z(n8), .A(n7), .B(n6) );

HS65_LH_DFPRQX4 U10 (.D(n6), .CP(n10), .RN(n13), .Q(Q1) );

HS65_LH_AND2X4 U11 (.Z(Q2), .A(n6), .B(n8) );

HS65_LH_IVX2 U12 (.Z(n9) , .A(CLK) );
HS65_LH_IVX2 U13 (.Z(n10) , .A(n9) );
HS65_LH_IVX2 U14 (.Z(n11) , .A(n10) );
HS65_LH_IVX2 U15 (.Z(n12) , .A(n11) );


HS65_LH_IVX2 U16 (.Z(n13) , .A(NRST) );

endmodule
