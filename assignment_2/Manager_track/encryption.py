# Gur svefg 10 punenpgref fubhyq or gur svefg 10 Creeva ahzoref.

import os
import string

alphabetCaps = [string.printable[i] for i in range(36, 62)]

def decryptSC(littlepiece, key, encrypt):
  plain = ""
  keylen = len(key)

  for i in range(len(littlepiece)):

    key_index = i % keylen

    if not encrypt:

      posInCaps = (alphabetCaps.index(littlepiece[i]) - alphabetCaps.index(key[key_index])) % 26
    else:
        posInCaps = (alphabetCaps.index(littlepiece[i]) + alphabetCaps.index(key[key_index])) % 26

    decryptedChar = alphabetCaps[posInCaps]

    plain += decryptedChar

  if len(plain) < 10:
    plain += "AAAAAAAAAA"

  return plain

def readKey(m4g1cf):
  f = open(m4g1cf, "r")
  z = f.readlines()[0].split("\n")[0]

  return z

def grhmfi(n, xexexe={}):
  if n == 0:
    return 3

  elif n == 1:
    return 0

  elif n == 2:
    return 2

  elif n in xexexe:
    return xexexe[n]

  else:
    xexexe[n] = grhmfi(n-2, xexexe) + grhmfi(n-3, xexexe)
    return xexexe[n]

def works(encrypt3d):
  # if you know, you know
  d3crypt3d = decryptSC(encrypt3d, "TERYYIYBJG", 0)

  for i in range (0, min(len(d3crypt3d), 10)):
    if not alphabetCaps.index(d3crypt3d[i]) == grhmfi(i):
      return False

  return True

def authenticate():
  print("Please enter your file with the magic code:\n")

  m4g1cf = input("")
  m4g1ck = readKey(m4g1cf)

  if (works(m4g1ck)):
    print("Welcome admin")
    os.system("/bin/bash")

  else:
    # Harry, it's our calling card! All the great ones leave their marks. We're ..
    print("You ought not have messed with us, pal. We're dangerous.")

if __name__ == "__main__":
  authenticate()
