'''
# py3 run-all.py
# python3 -m nose_check binkeul cmp
# nosetests --pdb
'''
import nose ,os
os .system ("python3 -m nose_check binkeul cmp")
print ("="*77 )
nose .main (argv =["test*",'--pdb','-v'])
