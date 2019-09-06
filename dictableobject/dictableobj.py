#--start requirements--
#pip installs
from security import Encrypting, Hashing

#customs

#builtins
import copy
import json
#import datetime

#--end requirements--

class DictableObj:
	"""Interehit this object to give it the Dictify ability to transform into a dict."""

	keys = {
		'hash': ['hashattrname','S'],
		'range': ['rangeattrname','S'],
		}

	def Dictify(self):
		"""Turn this object into a dictionary by copying it and viewing its __dict__
		Returns:
			dict: new_self
		"""
		new_self = copy.deepcopy(self.__dict__)

		#TODO: add in support for non built in classes?
		#fields = list(self.__dict__.keys())
		#for fieldname in fields:
		#	if type(new_self[fieldname]).__module__ == 'numpy':
		#		selecting[fieldname] = getattr(self,fieldname).tolist()[0]

		return new_self

class SecurableObject(DictableObj):
	"""A securable object.
	Attributes:
		data (str): Encrypted object as a string.
	"""
	
	def __init__(self,kwargs):

		try:
			self.data = kwargs['data']
		except:
			self.data = None

		return super().__init__()

	def Secure(self,passphrase=None,public_attributes=[]):
		"""Secures the object by encrypting itself and storing in the data attribute.
		Args:
			passphrase (str): Secret passphrase for encryption.
			public_attributes (list): Attributes that will remain unsecured and public.
		Note:
			Does not clear other attribute fields.
		"""

		if passphrase == None:
			return self.Dictify()
		else:
			self.data = Encrypting.Symmetric.Encrypt(json.dumps(self.Dictify()).encode('utf-8'),passphrase).decode('utf-8')
			
		#secure data and dictify
		my_secure_dict = self.Dictify()

		#new obfuscated obj
		new_me = {'data':my_secure_dict['data']}

		for pub_att in public_attributes:
			new_me[pub_att] = my_secure_dict[pub_att]

		return new_me

	def Expose(obj_as_dict: dict,passphrase=None):
		"""Expose a previously secured object.
		Args:
			obj_as_dict (dict): Secured object.
			passphrase (str): Secret passphrase.
		Return:
			dict: So can instantiate.
		"""
		if passphrase == None:
			return obj_as_dict
		else:
			interpreted = json.loads(Encrypting.Symmetric.Decrypt(obj_as_dict['data'].encode('utf-8'),passphrase).decode('utf-8'))

		interpreted['data'] = None #so its clear need to obfuscate again

		return interpreted

class DiscreteStatusObject(SecurableObject):
	"""An object that has a state, is discrete in time, and securable.
	Attributes:
		status (int): Integer to reepresent a status of the living object.
		nowDN (int): Datenum
		data (str): Reserved data for secure storage.
	"""

	def __init__(self,kwargs):
		
		try:
			self.status = kwargs['status']
		except:
			self.status = 1

		try:
			self.nowDN = kwargs['nowDN']
		except:
			#dt = datetime.datetime.utcnow()
			#self.nowDN = (dt - dt.min).total_seconds() #TODO: choose how to generate time? Timimng.DN ?
			self.nowDN =None
		return super().__init__(kwargs)

	def Obfuscate(self,passphrase=None,public_attributes=[]):
		"""Obfuscate a living object by securing its data and showing public attributes with nowDN and status.
		Args:
			passphrase (str): Secret passphrase used to encrypt.
		Returns:
			dict: Dict of the obfuscated object.
		Notes:
			If passphrase=='' then does not encrypt/secure.
		"""
		
		new_me = self.Secure(passphrase,['nowDN','status']+public_attributes)

		return new_me

class UniqueStatusObject(SecurableObject):
	"""An object that has a state, is unique, and securable.
	Attributes:
		status (int): Integer to reepresent a state of the living object.
		ID (str): Unique identifier string.
		data (str): Reserved data for secure storage.
	"""
	def __init__(self,kwargs):
		
		try:
			self.status = kwargs['status']
		except:
			self.status = 1

		try:
			self.ID = kwargs['ID']
		except:
			self.ID = Hashing.HashStr(Encrypting.GeneratePassphrase()) #hash because formatting

		return super().__init__(kwargs)

	def Obfuscate(self,passphrase=None,public_attributes=[]):
		"""Obfuscate a living object by securing its data and showing public attributeswith ID and status.
		Args:
			passphrase (str): Secret passphrase used to encrypt.
		Returns:
			dict: Dict of the obfuscated object.
		Notes:
			If passphrase=='' then does not encrypt/secure.
		"""
		
		new_me = self.Secure(passphrase,['ID','status'])

		return new_me

class Tests:

	def main():

		Tests.test_dictableobj()
		Tests.test_securableobject()

		pass

	def test_dictableobj():

		input_dict = {'workit':'buyitbringitdoitbettermakeusstronger'}

		class myobj(DictableObj):
			def __init__(self,kwargs):
				self.workit = kwargs['workit']
				return super().__init__()
		
		d_obj = myobj(input_dict)
		d_obj_dict = d_obj.Dictify()

		if not isinstance(d_obj_dict,dict): raise ValueError('DictableObj.Dictify returned incorrect type')
		if d_obj_dict != input_dict: raise ValueError('DictableObj.Dictify returned incorrect DN')

		pass

	def test_securableobject():

		input_dict = {
			'workit':'buyitbringitdoitbettermakeusstronger',
			'publicatt': 'data to not be public',
			}

		#make new obj and inherit
		class myobj(SecurableObject):
			def __init__(self,kwargs):
				self.workit = kwargs['workit']
				self.publicatt = kwargs['publicatt']
				return super().__init__(kwargs)

		#instantiate new obj
		s_obj = myobj(input_dict)

		#list of public attributes that dont need to be stored in encrypted data
		public_attributes = ['publicatt']

		#obfuscate it for storage
		secured_s_obj_dict = s_obj.Secure('secretpassphrase',public_attributes=public_attributes)
		
		#interpret it after loading from storage
		exposed_s_obj = myobj(myobj.Expose(secured_s_obj_dict,'secretpassphrase'))


		#test if public is still viewable and the others are gone

		pass

	def test_discreteobject():

		input_dict = {'workit':'buyitbringitdoitbettermakeusstronger'}

		#make new obj and inherit
		class myobj(DiscreteStatusObject):
			def __init__(self,kwargs):
				self.workit = kwargs['workit']
				return super().__init__(kwargs)

		#instantiate new obj
		s_obj = myobj(input_dict)

		#obfuscate it for storage
		secured_s_obj = s_obj.Obfuscate('secretpassphrase')
			
		#interpret it after loading from storage
		exposed_s_obj = myobj(myobj.Expose(secured_s_obj,'secretpassphrase'))

		pass

readme = """

# DictableObject
#### What this does and why make it

# Installation
Installing to use in your own scripts in a virtual environment?

`pip install git+https://github.com/pmp47/DictableObject`

Installing to edit this code and contribute? Clone/download this repo and...

`pip install -r requirements.txt`

#Motivation




# Further Information
Looking for more explanation? The code itself is documented in a way meant to be read and understood easily. A good place to start with this package would be:
```python
dictableobj.Tests.main
```

# TODO
 Currently there are yet to be implimented features:
 * Complete recurrent layer capability so sequential networks may be evolved, such has LSTM
 * Higher dimensionality of layers must be added in order to support typical computer vision applications such as 2-D Convolutions


 ##### fin

"""