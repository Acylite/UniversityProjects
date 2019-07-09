import sys
import converter
converter = converter.Converter()
final = converter.final
idx0 = 1
idxn = len(final)-1
midval = (idx0 + idxn)// 2

for i in range(1, len(final)+1):
    converter.writer(i)


        
    
