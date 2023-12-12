tm=2; 
tmr=0.5;
r=3;

Point(1)={0,0,0,tm};
Point(2)={40,0,0,tm};
Point(3)={40,20,0,tm};
Point(4)={0,20,0,tm};

Point(5)={10,10,0};
Point(6)={10+r,10,0,tmr};
Point(7)={10-r,10,0,tmr};


Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Circle(5) = {6,5,7};
Circle(6) = {7,5,6};

Curve Loop(1)={1,2,3,4};
Curve Loop(2)={5,6};

Plane Surface(1)={1,2};

Physical Surface(1)={1};
Physical Line("Bottom")={1};
Physical Line("Top")={3};
Physical Line("Left")={4};


Mesh 2;
Mesh.SurfaceFace=1;
Mesh.Point=1;
Save "malla_entrega.mesh";

