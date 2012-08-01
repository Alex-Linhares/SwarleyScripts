# TrueCryptPasswordHunter.py
# Copyright (C) 2012  Ian Thomas
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import string
import itertools
import subprocess

# SETTINGS ====================================================================

max_combination_size = 3
password_components_file = "password_components.txt"
truecrypt_device = "\\Device\\Harddisk1\\Partition1"
truecrypt_exe = "C:\\Program Files\\TrueCrypt\\truecrypt.exe"

# FUNCTIONS ===================================================================

def read_password_components():

    if not os.path.exists(password_components_file):
        raise RuntimeError("Password components file not found: '%s'" % password_components_file )
    file = open( password_components_file, "r" )
    
    password_components = file.readlines()
    if not password_components:
        raise RuntimeError("Password components file is empty!")
    
    password_components = map( lambda s: s.strip(), password_components ) # strip trailing newlines from each line
    print "Read %d password components: %s" % ( len(password_components), password_components )
    
    return password_components

def find_password_combination( password_components, combination_size ):
    
    print "%sTrying passwords of combination size %d...%s" % ( os.linesep, combination_size, os.linesep )
    product = itertools.product( password_components, repeat=combination_size )
    
    for prod in product:
        
        password = string.join( prod, '' )
        print "\tTrying password: '%s'" % password
        
        truecrypt_command = "\"%s\" /q /s /v %s /lT /m ro /a /p \"%s\" /b" % ( truecrypt_exe, truecrypt_device, password )
        process = subprocess.Popen( truecrypt_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        return_code = process.wait() # wait until TrueCrypt has finished trying current password
        ( stdout, stderr ) = process.communicate()
        
        if stderr:
            print "Error: '%s'" % stderr
            return False
        
        if return_code == 0:
            print "%sPassword found: %s" % ( os.linesep, password )
            return True
    
    return False

def find_password():
    
    password_components = read_password_components()
    
    for i in range( 1, max_combination_size + 1 ):
        if find_password_combination( password_components, i ):
            return True
    
    return False

# MAIN ========================================================================

print "Hunting TrueCrypt password for device '%s'..." % truecrypt_device

try:
    success = find_password()
    if success:
        print "Success!"
    else:
        print "Failed!"
except Exception as ex:
    print "Fatal Error: %s" % ex
