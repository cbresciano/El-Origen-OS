from web3 import Account
acct = Account.create()
print("Dirección:", acct.address)
print("Clave privada:", acct.key.hex())
