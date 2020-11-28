from behave import *
import json
import requests
from ctypes import cdll,c_int,c_char_p,c_size_t,create_string_buffer,sizeof,POINTER

(P1_UP ,
P1_LEFT,
P1_DOWN,
P1_RIGHT,
P1_BUTTON1,
P1_BUTTON2,
P2_UP,
P2_LEFT,
P2_DOWN,
P2_RIGHT,
P2_BUTTON1,
P2_BUTTON2,
START_1,
START_2,
COIN_1,
COIN_2,
SERVICE_1,
SERVICE_2,
KEYBOARD_A,
KEYBOARD_B,
KEYBOARD_C,
KEYBOARD_D,
KEYBOARD_E,
KEYBOARD_F,
KEYBOARD_G,
KEYBOARD_H,
KEYBOARD_I,
KEYBOARD_J,
KEYBOARD_K,
KEYBOARD_L,
KEYBOARD_M,
KEYBOARD_N,
KEYBOARD_O,
KEYBOARD_P,
KEYBOARD_Q,
KEYBOARD_R,
KEYBOARD_S,
KEYBOARD_T,
KEYBOARD_U,
KEYBOARD_V,
KEYBOARD_W,
KEYBOARD_X,
KEYBOARD_Y,
KEYBOARD_Z,
KEYBOARD_0,
KEYBOARD_1,
KEYBOARD_2,
KEYBOARD_3,
KEYBOARD_4,
KEYBOARD_5,
KEYBOARD_6,
KEYBOARD_7,
KEYBOARD_8,
KEYBOARD_9,
KEYBOARD_SPACE,
KEYBOARD_INTRO,
KEYBOARD_SUPR,
FUNCTION_1,
FUNCTION_2,
FUNCTION_3,
FUNCTION_4,
FUNCTION_5,
FUNCTION_6,
FUNCTION_7,
FUNCTION_8,
FUNCTION_9,
FUNCTION_10,
FUNCTION_11,
FUNCTION_12) = range(69)

Controles = c_int * 70

class AbadIA(object):
	def __init__(self):
		print("AbadIA CONSTRUCTOR")
		self.lib = cdll.LoadLibrary('./LibAbadIA.so')
		self.lib.LibAbadIA_init()
		self.lib.LibAbadIA_step.restype = c_char_p
#falta revisar tipo de controles
		self.lib.LibAbadIA_step.argtypes = [POINTER(c_int),c_char_p,c_size_t]
		self.lib.LibAbadIA_save.restype = c_char_p
		self.lib.LibAbadIA_save.argtypes = [c_char_p,c_size_t]
		self.lib.LibAbadIA_load.argtypes = [c_char_p]
		self.controles = Controles()

	def step(self):
		result = create_string_buffer(10000)
		tmp = self.lib.LibAbadIA_step(self.controles,result,sizeof(result)).decode()
		self.controles = Controles()
		return tmp

	def load(self,input):
		return self.lib.LibAbadIA_load(input)
#igual el create_string_buffer puede ir aqui y no por todos lados			
#igual que en step
	def save(self,result,resultMaxLength):
		return self.lib.LibAbadIA_save(result,resultMaxLength)

	# @when('reinicio el juego')
	def reset_game(self):
		self.controles[KEYBOARD_E]=1
		self.status=self.step()

	# revisar si se usa @when('mando el comando "{comando}"')
	def snd_command(self, comando):
		assert comando=="UP" or comando =="QR" or comando=="RESET"
		if (comando=="UP"):
			self.controles[P1_UP]=1
			self.status=self.step()
		elif comando=="QR":
			self.controles[KEYBOARD_Q]=1
			self.controles[KEYBOARD_R]=1
			self.status=self.step()
		elif comando=="RESET":
			self.controles[KEYBOARD_E]=1
			self.status=self.step()
		else:
			print("la version lib solo soporta ahora mismo comando UP y QR (y RESET)")
			assert False

	# revisar si esto es el NOP @step('no hago nada')
	def do_nothing(context):
		context.status=context.abadIA.step()

	# revisar si tiene sentido no ir a tope @step('duplico la velocidad')
	def speedx2 (context):
		context.abadIA.controles[SERVICE_1]=1
		context.status=context.abadIA.step()

	# revisar @step('reduzco la velocidad')
	def speed_div_2(context):
		context.abadIA.controles[SERVICE_2]=1
		context.status=context.abadIA.step()

	# @when('digo que SI')
	def say_yes(context):
		context.abadIA.controles[KEYBOARD_S]=1
		context.status=context.abadIA.step()

	# @when('digo que NO')
	def say_no(context):
		context.abadIA.controles[KEYBOARD_N]=1
		context.status=context.abadIA.step()

	# @when('giro a la izquierda')
	def turn_left(context):
		context.abadIA.controles[P1_LEFT]=1
		context.status=context.abadIA.step()

	# @when('giro a la derecha')
	def turn_right(context):
		context.abadIA.controles[P1_RIGHT]=1
		context.status=context.abadIA.step()

	# revisar si se usa @when('doy media vuelta')
	def hard_turn(context):
		context.abadIA.controles[P1_RIGHT]=1
		context.status=context.abadIA.step()
		context.abadIA.controles[P1_RIGHT]=1
		context.status=context.abadIA.step()
		context.status=context.abadIA.step()

	# @when('avanzo')
	def forward(context):
		context.abadIA.controles[P1_UP]=1
		context.status=context.abadIA.step()

	# @when('avanzo "{numeroPasos}" pasos')
	def forward_n_steps(context,numeroPasos):
		i=0;
		while i < int(numeroPasos):
			context.abadIA.controles[P1_UP]=1
			context.status=context.abadIA.step()
			context.abadIA.controles[P1_UP]=1
			context.status=context.abadIA.step()
			i+=1

	# revisar si lo vamos a utilizar @when('Adso avanza "{numeroPasos}" pasos')
	def adso_n_stpes(context,numeroPasos):

		i=0;
		while i < int(numeroPasos):
			context.abadIA.controles[P1_DOWN]=1
			context.status=context.abadIA.step()
			i+=1


	# revisar @when('espero "{numeroIteraciones}" iteraciones')
	def waiting_for(context,numeroIteraciones):
		i=0;
		while i < int(numeroIteraciones):
			context.status=context.abadIA.step()
			i+=1

	# space @when('pulso espacio')
	def space(context):
		context.abadIA.controles[P1_BUTTON1]=1
		context.status=context.abadIA.step()

	# @when('cargo una partida')
	def load(context):
		assert context.abadIA.load(context.text.encode())


	# @step('grabo la partida')
	def save(context):
		result = create_string_buffer(10000)
		res=context.abadIA.save(result,sizeof(result)).decode()
		print("grabo la partida *"+res+"*")
		assert res.count('\n')==431

	# @step('grabo la partida y comparo el volcado')
	def save_and_check(context):
		print("lineas partida esperada: "+str(context.text.count('\n')+1));
		assert context.text.count('\n')+1==431;
		res=context.abadIA.save()
		print("***partida recibida***");
		print(res);
		print("***partida esperada***");
		print(context.text);
		assert res.count('\n')==431
		assert context.text==res


	# TODO: comparar contra tabla para poder ampliar lo que se comprueba
	# @then('el resultado es "{resultado}" con descripcion "{descripcion}"')
	def check1(context,resultado,descripcion):
		assert context.dump["resultado"]==resultado
		assert context.dump["descripcion"]==descripcion

	# @then('el resultado es "{resultado}"')
	def check2(context,resultado):
		print("mmmm *"+context.dump+"**"+resultado+"**");
		assert context.dump==resultado

	# @step('los valores iniciales son correctos')
	def check_ini(context):
		context.abadIA.controles[KEYBOARD_D]=1
		context.status=context.abadIA.step()
		print("resultDUMPtext**"+context.status);
		valid_json=False;
		try:
			#      json_object = json.loads(self.status.text)
			json_object = json.loads(context.status)
		except ValueError:
			print("El dump no devuelve un  JSON\n");
			valid_json = False;
		#      assert False
		else:
			valid_json = True;
			dump = json.loads(context.status)
			print("resultDUMP**"+str(dump));

		assert valid_json;

		context.dump=dump;
		for head in context.table[0].headings:
			print("***"+head+"***"+type(dump[head]).__name__+"***valor recibido***"+str(dump[head])+"***valor esperado***"+str(context.table[0][head])+"***");
			if (type(dump[head]).__name__=="bool"):
				assert str(dump[head])==(context.table[0][head])
			else:
				if (type(dump[head]).__name__=="int"):
					assert dump[head]==int(context.table[0][head])
				else:
					assert False
