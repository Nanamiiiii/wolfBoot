#!/usr/bin/python3
'''
 * keygen.py
 *
 * Copyright (C) 2021 wolfSSL Inc.
 *
 * This file is part of wolfBoot.
 *
 * wolfBoot is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * wolfBoot is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1335, USA
'''

import sys,os
from wolfcrypt import ciphers

def usage():
    print("Usage: %s [--ed25519 | --ed448 | --ecc256 | --ecc384 | --ecc521 | --rsa2048| --rsa3072 | --rsa4096] [ --force ] pub_key_file.c\n" % sys.argv[0])
    parser.print_help()
    sys.exit(1)

def dupsign():
    print("")
    print("Error: only one algorithm must be specified.")
    print("")
    usage()

Cfile_Banner="/* Public-key file for wolfBoot, automatically generated. Do not edit.  */\n"+ \
             "/*\n" + \
             " * This file has been generated and contains the public key which is\n"+ \
             " * used by wolfBoot to verify the updates.\n"+ \
             " */" \
             "\n#include <stdint.h>\n\n"

Ed25519_pub_key_define = "const uint8_t ed25519_pub_key[32] = {\n\t"
Ed448_pub_key_define= "const uint8_t ed448_pub_key[57] = {\n\t"
Ecc256_pub_key_define = "const uint8_t ecc256_pub_key[64] = {\n\t"
Ecc384_pub_key_define = "const uint8_t ecc384_pub_key[96] = {\n\t"
Ecc521_pub_key_define = "const uint8_t ecc521_pub_key[132] = {\n\t"
Rsa_2048_pub_key_define = "const uint8_t rsa2048_pub_key[%d] = {\n\t"
Rsa_3072_pub_key_define = "const uint8_t rsa3072_pub_key[%d] = {\n\t"
Rsa_4096_pub_key_define = "const uint8_t rsa4096_pub_key[%d] = {\n\t"

sign="ed25519"

import argparse as ap

parser = ap.ArgumentParser(prog='keygen.py', description='wolfBoot key generation tool')
parser.add_argument('--ed25519', dest='ed25519', action='store_true')
parser.add_argument('--ed448', dest='ed448', action='store_true')
parser.add_argument('--ecc256',  dest='ecc256', action='store_true')
parser.add_argument('--ecc384',  dest='ecc384', action='store_true')
parser.add_argument('--ecc521',  dest='ecc521', action='store_true')
parser.add_argument('--rsa2048', dest='rsa2048', action='store_true')
parser.add_argument('--rsa3072', dest='rsa3072', action='store_true')
parser.add_argument('--rsa4096', dest='rsa4096', action='store_true')
parser.add_argument('--force', dest='force', action='store_true')
parser.add_argument('cfile')

args=parser.parse_args()

#print(args.ecc256)
#sys.exit(0) #test

pubkey_cfile = args.cfile
sign=None
force=False
if (args.ed25519):
    sign='ed25519'
if (args.ed448):
    if sign is not None:
        dupsign()
    sign='ed448'
if (args.ecc256):
    if sign is not None:
        dupsign()
    sign='ecc256'
if (args.ecc384):
    if sign is not None:
        dupsign()
    sign='ecc384'
if (args.ecc521):
    if sign is not None:
        dupsign()
    sign='ecc521'
if (args.rsa2048):
    if sign is not None:
        dupsign()
    sign='rsa2048'
if (args.rsa3072):
    if sign is not None:
        dupsign()
    sign='rsa3072'
if (args.rsa4096):
    if sign is not None:
        dupsign()
    sign='rsa4096'

if sign is None:
    usage()

force = args.force


if pubkey_cfile[-2:] != '.c':
    print("** Warning: generated public key cfile does not have a '.c' extension")

key_file=sign+".der"

print ("Selected cipher:      " + sign)
print ("Output Private key:   " + key_file)
print ("Output C file:        " + pubkey_cfile)
print()

if (sign == "ed25519"):
    ed = ciphers.Ed25519Private.make_key(32)
    priv,pub = ed.encode_key()
    if os.path.exists(key_file) and not force:
        choice = input("** Warning: key file already exist! Are you sure you want to "+
                "generate a new key and overwrite the existing key? [Type 'Yes, I am sure!']: ")
        if (choice != "Yes, I am sure!"):
            print("Operation canceled.")
            sys.exit(2)

    print()
    print("Creating file " + key_file)
    with open(key_file, "wb") as f:
        f.write(priv)
        f.write(pub)
        f.close()
    print("Creating file " + pubkey_cfile)
    with open(pubkey_cfile, "w") as f:
        f.write(Cfile_Banner)
        f.write(Ed25519_pub_key_define)
        i = 0
        for c in bytes(pub[0:-1]):
            f.write("0x%02X, " % c)
            i += 1
            if (i % 8 == 0):
                f.write('\n\t')
        f.write("0x%02X" % pub[-1])
        f.write("\n};\n")
        f.write("const uint32_t ed25519_pub_key_len = 32;\n")
        f.close()

if (sign == "ed448"):
    ed = ciphers.Ed448Private.make_key(57)
    priv,pub = ed.encode_key()
    if os.path.exists(key_file) and not force:
        choice = input("** Warning: key file already exist! Are you sure you want to "+
                "generate a new key and overwrite the existing key? [Type 'Yes, I am sure!']: ")
        if (choice != "Yes, I am sure!"):
            print("Operation canceled.")
            sys.exit(2)

    print()
    print("Creating file " + key_file)
    with open(key_file, "wb") as f:
        f.write(priv)
        f.write(pub)
        f.close()
    print("Creating file " + pubkey_cfile)
    with open(pubkey_cfile, "w") as f:
        f.write(Cfile_Banner)
        f.write(Ed448_pub_key_define)
        i = 0
        for c in bytes(pub[0:-1]):
            f.write("0x%02X, " % c)
            i += 1
            if (i % 8 == 0):
                f.write('\n\t')
        f.write("0x%02X" % pub[-1])
        f.write("\n};\n")
        f.write("const uint32_t ed448_pub_key_len = 57;\n")
        f.close()
if (sign[0:3] == 'ecc'):
    if (sign == "ecc256"):
        ec = ciphers.EccPrivate.make_key(32)
        banner = Ecc256_pub_key_define
        ecc_pub_key_len = 64
        qx,qy,d = ec.encode_key_raw()
        if os.path.exists(key_file) and not force:
            choice = input("** Warning: key file already exist! Are you sure you want to "+
                    "generate a new key and overwrite the existing key? [Type 'Yes, I am sure!']: ")
            if (choice != "Yes, I am sure!"):
                print("Operation canceled.")
                sys.exit(2)

    if (sign == "ecc384"):
        ec = ciphers.EccPrivate.make_key(48)
        banner = Ecc384_pub_key_define
        ecc_pub_key_len = 96
        qx,qy,d = ec.encode_key_raw()
        if os.path.exists(key_file) and not force:
            choice = input("** Warning: key file already exist! Are you sure you want to "+
                    "generate a new key and overwrite the existing key? [Type 'Yes, I am sure!']: ")
            if (choice != "Yes, I am sure!"):
                print("Operation canceled.")
                sys.exit(2)

    if (sign == "ecc521"):
        ec = ciphers.EccPrivate.make_key(66)
        banner = Ecc521_pub_key_define
        ecc_pub_key_len = 132
        qx,qy,d = ec.encode_key_raw()
        if os.path.exists(key_file) and not force:
            choice = input("** Warning: key file already exist! Are you sure you want to "+
                    "generate a new key and overwrite the existing key? [Type 'Yes, I am sure!']: ")
            if (choice != "Yes, I am sure!"):
                print("Operation canceled.")
                sys.exit(2)

    print()
    print("Creating file " + key_file)
    with open(key_file, "wb") as f:
        f.write(qx)
        f.write(qy)
        f.write(d)
        f.close()
    print("Creating file " + pubkey_cfile)
    with open(pubkey_cfile, "w") as f:
        f.write(Cfile_Banner)
        f.write(banner)
        i = 0
        for c in bytes(qx):
            f.write("0x%02X, " % c)
            i += 1
            if (i % 8 == 0):
                f.write('\n')
        for c in bytes(qy[0:-1]):
            f.write("0x%02X, " % c)
            i += 1
            if (i % 8 == 0):
                f.write('\n')
        f.write("0x%02X" % qy[-1])
        f.write("\n};\n")
        f.write("const uint32_t %s_pub_key_len = %d;\n" % (sign, ecc_pub_key_len))
        f.close()

if (sign == "rsa2048"):
    rsa = ciphers.RsaPrivate.make_key(2048)
    if os.path.exists(key_file) and not force:
        choice = input("** Warning: key file already exist! Are you sure you want to "+
                "generate a new key and overwrite the existing key? [Type 'Yes, I am sure!']: ")
        if (choice != "Yes, I am sure!"):
            print("Operation canceled.")
            sys.exit(2)
    priv,pub = rsa.encode_key()
    print()
    print("Creating file " + key_file)
    with open(key_file, "wb") as f:
        f.write(priv)
        f.close()
    print("Creating file " + pubkey_cfile)
    with open(pubkey_cfile, "w") as f:
        f.write(Cfile_Banner)
        f.write(Rsa_2048_pub_key_define % len(pub))
        i = 0
        for c in bytes(pub):
            f.write("0x%02X, " % c)
            i += 1
            if (i % 8 == 0):
                f.write('\n')
        f.write("\n};\n")
        f.write("const uint32_t rsa2048_pub_key_len = %d;\n" % len(pub))
        f.close()

if (sign == "rsa3072"):
    rsa = ciphers.RsaPrivate.make_key(3072)
    if os.path.exists(key_file) and not force:
        choice = input("** Warning: key file already exist! Are you sure you want to "+
                "generate a new key and overwrite the existing key? [Type 'Yes, I am sure!']: ")
        if (choice != "Yes, I am sure!"):
            print("Operation canceled.")
            sys.exit(2)
    priv,pub = rsa.encode_key()
    print()
    print("Creating file " + key_file)
    with open(key_file, "wb") as f:
        f.write(priv)
        f.close()
    print("Creating file " + pubkey_cfile)
    with open(pubkey_cfile, "w") as f:
        f.write(Cfile_Banner)
        f.write(Rsa_3072_pub_key_define % len(pub))
        i = 0
        for c in bytes(pub):
            f.write("0x%02X, " % c)
            i += 1
            if (i % 8 == 0):
                f.write('\n')
        f.write("\n};\n")
        f.write("const uint32_t rsa3072_pub_key_len = %d;\n" % len(pub))
        f.close()

if (sign == "rsa4096"):
    rsa = ciphers.RsaPrivate.make_key(4096)
    if os.path.exists(key_file) and not force:
        choice = input("** Warning: key file already exist! Are you sure you want to "+
                "generate a new key and overwrite the existing key? [Type 'Yes, I am sure!']: ")
        if (choice != "Yes, I am sure!"):
            print("Operation canceled.")
            sys.exit(2)
    priv,pub = rsa.encode_key()
    print()
    print("Creating file " + key_file)
    with open(key_file, "wb") as f:
        f.write(priv)
        f.close()
    print("Creating file " + pubkey_cfile)
    with open(pubkey_cfile, "w") as f:
        f.write(Cfile_Banner)
        f.write(Rsa_4096_pub_key_define % len(pub))
        i = 0
        for c in bytes(pub):
            f.write("0x%02X, " % c)
            i += 1
            if (i % 8 == 0):
                f.write('\n')
        f.write("\n};\n")
        f.write("const uint32_t rsa4096_pub_key_len = %d;\n" % len(pub))
        f.close()
