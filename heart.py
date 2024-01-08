import matplotlib.pyplot as plt
import numpy as np
from numpy import sin
from numpy import cos

x = np.linspace(-2, 2, 10000)
f = lambda x: np.sqrt(cos(x)) * cos(80 * x) + 0.5 * np.sqrt(abs(x))

plt.plot(x, f(x))
plt.show()

print('            =========                           =========')
print('      =====          ============     =========          ========')
print('   =                             =  = 		                    =')
print(' =                                 =                              =')
print('=                                                                  =')
print('=					                                                =')
print(' =				      	                                            =')
print('    =				  	                                           =')
print('      =                                                          =')
print('        =                                                      =')
print('          =                                                 =')
print('            =                                            =')
print('                =                                    = ')
print('                   =                              =')
print('                     =                         = ')
print('                        =                  =')
print('                            =           = ')
print('                               =     =')
print(' 		                          =	')