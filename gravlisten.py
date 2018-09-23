# gravlisten
# barrystyle 23092018
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json, time, os, sys, binascii

# user-config section
rpchost = ''
rpcuser = ''
rpcpass = ''

#main loop, catch exceptions
print ''
oldhash = ''
txiter=[]
txmemory=[]
primenumber = '030331ef01000000001976a914'
rpcpipe = AuthServiceProxy('http://' + rpcuser + ':' + rpcpass + '@' + rpchost + ':11000')
while True:
   try:
      #heartbeat     
      comms = rpcpipe.getbestblockhash()
      if comms not in oldhash:
         oldhash = comms
         print oldhash + ' ' + str(rpcpipe.getblockcount())
      time.sleep(5)
      #check for tx
      incmd = rpcpipe.listtransactions()
      for tx in incmd:
        if tx not in txmemory:
          if 'receive' in str(tx):
             fields = str(tx).split(',')
             for field in fields:
                 if 'txid' in field:
                    temptxid = field.split('u')[2].replace('{','').replace('}','').replace('\'','').strip()
                    bypass=False
                    if temptxid not in txiter:
                       txiter.append(temptxid)
                       #in the case this doesnt exist yet
                       try:
                         seentx=open('seentx.log','r')
                         seendata=seentx.read()                               # check if we've actioned already
                         seentx.closed
                       except:
                         seentx=open('seentx.log','w')
                         seentx.write(' ')
                         seentx.closed
                         seendata=' '
                       if temptxid in seendata:
                         bypass=True
                       if bypass==False:
                         txrawdata=rpcpipe.getrawtransaction(temptxid)
                         if primenumber in txrawdata:
                            payload = txrawdata.split(primenumber)[1][:40]
                            print ' * ' + str(payload),
                            payloadcombine=''
                            for x in range(0,20):
                               paybyte=chr(int(payload[x*2:(x*2)+2],16))
                               if paybyte.isalpha():                          # replace any nasties with a space
                                  payloadcombine += paybyte
                               else:
                                  payloadcombine += ' '
                            print '\''+payloadcombine+'\''                    # action goes here
                         seentx=open('seentx.log','a')
                         seentx.write(str(temptxid))                          # write that we've actioned this
                         seentx.closed
             txmemory.append(tx)
          else:
             txmemory.append(tx)
        else:
          time.sleep(1)      
   except:
      time.sleep(1)
