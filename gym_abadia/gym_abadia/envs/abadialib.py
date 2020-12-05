import json
import logging
from ctypes import cdll,c_int,c_char_p,c_size_t,create_string_buffer,sizeof,POINTER


class AbadIA(object):

	def __init__(self):
		(self.P1_UP,
		 self.P1_LEFT,
		 self.P1_DOWN,
		 self.P1_RIGHT,
		 self.P1_BUTTON1,
		 self.P1_BUTTON2,
		 self.P2_UP,
		 self.P2_LEFT,
		 self.P2_DOWN,
		 self.P2_RIGHT,
		 self.P2_BUTTON1,
		 self.P2_BUTTON2,
		 self.START_1,
		 self.START_2,
		 self.COIN_1,
		 self.COIN_2,
		 self.SERVICE_1,
		 self.SERVICE_2,
		 self.KEYBOARD_A,
		 self.KEYBOARD_B,
		 self.KEYBOARD_C,
		 self.KEYBOARD_D,
		 self.KEYBOARD_E,
		 self.KEYBOARD_F,
		 self.KEYBOARD_G,
		 self.KEYBOARD_H,
		 self.KEYBOARD_I,
		 self.KEYBOARD_J,
		 self.KEYBOARD_K,
		 self.KEYBOARD_L,
		 self.KEYBOARD_M,
		 self.KEYBOARD_N,
		 self.KEYBOARD_O,
		 self.KEYBOARD_P,
		 self.KEYBOARD_Q,
		 self.KEYBOARD_R,
		 self.KEYBOARD_S,
		 self.KEYBOARD_T,
		 self.KEYBOARD_U,
		 self.KEYBOARD_V,
		 self.KEYBOARD_W,
		 self.KEYBOARD_X,
		 self.KEYBOARD_Y,
		 self.KEYBOARD_Z,
		 self.KEYBOARD_0,
		 self.KEYBOARD_1,
		 self.KEYBOARD_2,
		 self.KEYBOARD_3,
		 self.KEYBOARD_4,
		 self.KEYBOARD_5,
		 self.KEYBOARD_6,
		 self.KEYBOARD_7,
		 self.KEYBOARD_8,
		 self.KEYBOARD_9,
		 self.KEYBOARD_SPACE,
		 self.KEYBOARD_INTRO,
		 self.KEYBOARD_SUPR,
		 self.FUNCTION_1,
		 self.FUNCTION_2,
		 self.FUNCTION_3,
		 self.FUNCTION_4,
		 self.FUNCTION_5,
		 self.FUNCTION_6,
		 self.FUNCTION_7,
		 self.FUNCTION_8,
		 self.FUNCTION_9,
		 self.FUNCTION_10,
		 self.FUNCTION_11,
		 self.FUNCTION_12) = range(69)
		self.Controles = c_int * 70

		logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%d-%m-%y %H:%M:%S',
							level=logging.INFO)
		logging.info("AbadIA CONSTRUCTOR")

		self.lib = cdll.LoadLibrary('./LibAbadIA.so')

		logging.info("loaded")
		self.lib.LibAbadIA_init()
		logging.info("Initiated")
		self.lib.LibAbadIA_step.restype = c_char_p
		self.lib.LibAbadIA_step.argtypes = [POINTER(c_int), c_char_p, c_size_t]

		self.lib.LibAbadIA_save.restype = c_char_p
		self.lib.LibAbadIA_save.argtypes = [c_char_p,c_size_t]

		self.lib.LibAbadIA_load.argtypes = [c_char_p]
		# falta revisar tipo de controles
		self.controles = self.Controles()
		logging.info("loaded")
		return

	def step(self):
		result = create_string_buffer(10000)
		tmp = self.lib.LibAbadIA_step(self.controles, result, sizeof(result))
		logging.info("step result: {}".format(tmp))
		self.controles = self.Controles()
		return json.loads(tmp)

	def load(self,input):
		return self.lib.LibAbadIA_load(input)
#igual el create_string_buffer puede ir aqui y no por todos lados
#igual que en step
	def save(self,result,resultMaxLength):
		result = create_string_buffer(10000)
		return self.lib.LibAbadIA_save(result,resultMaxLength)

	# @when('reinicio el juego')
	def reset_game(self):
		self.controles[self.KEYBOARD_E]=1
		self.status=self.step()
		return self.status

	# revisar si se usa @when('mando el comando "{comando}"')
	def snd_command(self, comando):
		assert comando=="UP" or comando =="QR" or comando=="RESET"
		if (comando=="UP"):
			self.controles[self.P1_UP]=1
			self.status=self.step()
		elif comando=="QR":
			self.controles[self.KEYBOARD_Q]=1
			self.controles[self.KEYBOARD_R]=1
			self.status=self.step()
		elif comando=="RESET":
			self.controles[self.KEYBOARD_E]=1
			self.status=self.step()
		else:
			print("la version lib solo soporta ahora mismo comando UP y QR (y RESET)")
			assert False

	# revisar si esto es el NOP @step('no hago nada')
	def do_nothing(context):
		context.status=context.abadIA.step()

	# revisar si tiene sentido no ir a tope @step('duplico la velocidad')
	def speedx2 (context):
		context.abadIA.controles[self.SERVICE_1]=1
		context.status=context.abadIA.step()

	# revisar @step('reduzco la velocidad')
	def speed_div_2(context):
		context.abadIA.controles[self.SERVICE_2]=1
		context.status=context.abadIA.step()

	# @when('digo que SI')
	def say_yes(context):
		context.abadIA.controles[self.KEYBOARD_S]=1
		context.status=context.abadIA.step()

	# @when('digo que NO')
	def say_no(context):
		context.abadIA.controles[self.KEYBOARD_N]=1
		context.status=context.abadIA.step()

	# @when('giro a la izquierda')
	def turn_left(context):
		context.abadIA.controles[self.P1_LEFT]=1
		context.status=context.abadIA.step()

	# @when('giro a la derecha')
	def turn_right(context):
		context.abadIA.controles[self.P1_RIGHT]=1
		context.status=context.abadIA.step()

	# revisar si se usa @when('doy media vuelta')
	def hard_turn(context):
		context.abadIA.controles[self.P1_RIGHT]=1
		context.status=context.abadIA.step()
		context.abadIA.controles[self.P1_RIGHT]=1
		context.status=context.abadIA.step()
		context.status=context.abadIA.step()

	# @when('avanzo')
	def forward(context):
		context.abadIA.controles[self.P1_UP]=1
		context.status=context.abadIA.step()

	# @when('avanzo "{numeroPasos}" pasos')
	def forward_n_steps(context,numeroPasos):
		i=0;
		while i < int(numeroPasos):
			context.abadIA.controles[self.P1_UP]=1
			context.status=context.abadIA.step()
			context.abadIA.controles[self.P1_UP]=1
			context.status=context.abadIA.step()
			i+=1

	# revisar si lo vamos a utilizar @when('Adso avanza "{numeroPasos}" pasos')
	def adso_n_stpes(context,numeroPasos):

		i=0;
		while i < int(numeroPasos):
			context.abadIA.controles[self.P1_DOWN]=1
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
		context.abadIA.controles[self.P1_BUTTON1]=1
		context.status=context.abadIA.step()

	# @when('cargo una partida')
	def setGameInfo(context):
		assert context.abadIA.load(context.text)

	# @step('grabo la partida')
	def getGameInfo(self):
		# print("create the buffer")
		result = create_string_buffer(10000)
		# print("get the context of the game")
		res = self.lib.LibAbadIA_save(result,sizeof(result))
		# print("grabo la partida *"+res+"*")
		return res

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
		context.abadIA.controles[self.KEYBOARD_D]=1
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
