# import tokens
# from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
import json


with open("escrow.teal.tok", "rb") as f:
    bytes_read = f.read()

    a = bytearray(bytes_read)


# program = b"\x01\x20\x01\x00\x22"  # int 0
program = a
lsig = transaction.LogicSigAccount(program)
sender = lsig.address()  # el sender el address del escrow 
# receiver = account.generate_account()
receiver = "ZZAF5ARA4MEC5PVDOP64JM5O5MQST63Q2KOY2FLYFLXXD3PFSNJJBYAFZM"
# receiver = "36JI63UMBEKRVLCYUWL76JIJS5YIUKSQNGXQSK6QZLIJJOWKWH3GPTEFYU"

algod_address = "http://localhost:4001"
# algod_address = "https://api.testnet.algoexplorer.io"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
# algod_token = ""

# create an algod client
acl = algod.AlgodClient(algod_token, algod_address, headers={ 'User-Agent': 'DoYouLoveMe?' })

account_info = acl.account_info("E3LXVFBQHN3YM6CUSRWPCEDEZXCAL3AO7XPAADEHIUCSRWOCAOKETPBSQM")
print("Accoount balance del escrow: {} microAlgos".format(account_info.get('amount')) + "/n")

# get suggested parameters
sp = acl.suggested_params()
print(sp.__dict__)
print(getattr(sp, 'fee'))
setattr(sp, 'fee', 1000)
setattr(sp, 'flat_fee', True)
print(getattr(sp, 'fee'))
print(getattr(sp, 'flat_fee'))

# create a transaction
amount = 1000000
note = "Hello World2".encode()
txn = transaction.PaymentTxn(sender, sp, receiver, amount, None, note)

# note: transaction is signed by logic only (no delegation)
# that means sender address must match to program hash
lstx = transaction.LogicSigTransaction(txn, lsig)
assert lstx.verify()

# send them over network
output = acl.send_transaction(lstx)
print(output)


  