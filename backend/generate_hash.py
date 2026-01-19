#!/usr/bin/env python3
"""
Script para generar hash bcrypt válido
"""
import bcrypt

password = "admin123"
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

print(f"Password: {password}")
print(f"Hash: {hashed.decode('utf-8')}")
