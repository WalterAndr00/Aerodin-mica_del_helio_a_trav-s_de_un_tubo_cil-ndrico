#%%
from __future__ import absolute_import
from sfepy import data_dir
from sfepy.mechanics.matcoefs import stiffness_from_lame
from sfepy.discrete.fem import Mesh, FEDomain, Field
import numpy as np
#%%
#Dirección de la malla
filename_mesh = data_dir + '/meshes/2d/malla_entrega.mesh'
#%%
filename_mesh
#%%
#Malla
mesh=Mesh.from_file(filename_mesh)

#%%
domain=FEDomain("domain",mesh)

#%%
#Rango de el eje x de la malla
min_x,max_x= domain.get_mesh_bounding_box()[:,0]

# %%
centro=(10,10)
radio=3
#%%
#Creación de los dominios y regiones
omega=domain.create_region("Omega","all")
bottom = domain.create_region('Bottom','vertices in (y < 0.001)', 'facet')
left=domain.create_region('Left', 'vertices in (x < 0.001)', 'facet')
top=domain.create_region("Top",'vertices in (y > 19.99)','facet')
#%%
field=Field.from_args("fu",np.float64,"vector",omega,approx_order=3)

#%%
presion=Field.from_args("fu2",np.float64,"scalar",omega,approx_order=1)
#%%
from sfepy.discrete import (FieldVariable, Material,Integral,Function,Equation,Equations,Problem)
u=FieldVariable("u","unknown",field)
v=FieldVariable("v","test",field,primary_var_name="u")
p=FieldVariable('p','unknown',presion)
q=FieldVariable('q' ,'test',presion,primary_var_name="p")

# %%
#Propiedades del material
from sfepy.mechanics.matcoefs import stiffness_from_lame

#%%
viscosidad={
    "name": "mu",
    "Viscosidad":0.0018
}
mu = Material("m", mu=viscosidad["Viscosidad"])


#%%
ter_viscosidad={
    "name": "ter_mu",
}

#%%
h=2
densidad= 0.164
velocidad_gas=343
viscosidad=0.001
c2=viscosidad/3
c3=h*densidad
c4=1/(velocidad_gas**2)
#%%
integral=Integral("i",order=3)
integral1=Integral("i",order=1)
integral2=Integral("i",order=2)
integral4=Integral("i",order=4)
integral5=Integral("i",order=5)
integral6=Integral("i",order=6)
#%%
from sfepy.terms import Term
from sfepy import terms
#%%
#Definir términos y construccion de ecuaciones
t1=Term.new("dw_dot(v,u)",integral,omega,v=v, u=u)
t2=Term.new("dw_convect(v,u)",integral,omega,v=v, u=u)
t3=Term.new("dw_div_grad(v,u)",integral,omega,v=v, u=u)
t4=Term.new("dw_st_grad_div(v,u)",integral,omega,v=v, u=u)
t5=Term.new("de_stokes(v,p)",integral,omega,v=v, p=p)
t6=Term.new("dw_dot(q,p)",integral,omega, q=q,p=p)
t7=Term.new("dw_convect_v_grad_s(q,u,p)",integral,omega,q=q,u=u, p=p)
t8=Term.new("dw_stokes(u,q)",integral5,omega,q=q, u=u)
#%%
eq1=Equation("balance",t1*c3+t2*densidad+t3*viscosidad-t5+t6+t7*c4)

eqs=Equations([eq1])

#%%
eqs

#%%
#Condiciones de frontera
from sfepy.discrete.conditions import Conditions, EssentialBC
#%%
import math
fix1_u=EssentialBC("fix1_u",bottom,{"u.all":0.7})
fix2_u=EssentialBC("fix2_u",left,{"u.all":3})
fix3_u=EssentialBC("fix3_u",top,{"u.0":3,"u.1":-3.4})
#%% 
#Definir las soluciones lineales y no lineales
from sfepy.base.base import IndexedStruct
from sfepy.solvers.ls import ScipyDirect
from sfepy.solvers.nls import Newton


#%%
ls=ScipyDirect({})
nls_status=IndexedStruct()
nls=Newton({},lin_solver=ls,status=nls_status)
#%%
pb=Problem("entrega",equations=eqs)


#%%
pb.save_regions_as_groups("regions")
#%%
pb.set_bcs(ebcs=Conditions([fix1_u,fix2_u,fix3_u]))

#%%
pb.set_solver(nls)
#%%
status=IndexedStruct()

#%%
vec=pb.solve(status=status)

# %%
pb.save_state("EntregaWalterC.vtk",vec)
#%%
