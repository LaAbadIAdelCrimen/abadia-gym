import json

file = """1// dia
4// momentoDia
0// duracionMomentoDia
4// oldMomentoDia
0// avanzarMomentoDia
31// obsequium
0// haFracasado
0// investigacionCompleta
0// bonus
239// mascaraPuertas
1// espejoCerrado
0// numeroRomano
103444// despDatosAlturaEspejo
123468// despBloqueEspejo
0// seAcabaLaNoche
0// haAmanecido
0// usandoLampara
1// lamparaDesaparecida
0// tiempoUsoLampara
0// cambioEstadoLampara
0// cntTiempoAOscuras
0// cntLeeLibroSinGuantes
0// pergaminoGuardado
136// numeroAleatorio
1// hayMovimiento
2// cntMovimiento
0// numPersonajeCamara
0// opcionPersonajeCamara
// SPRITE 0
1// esVisible
// SPRITE 1
1// esVisible
// SPRITE 2
0// esVisible
// SPRITE 3
1// esVisible
// SPRITE 4
0// esVisible
// SPRITE 5
0// esVisible
// SPRITE 6
0// esVisible
// SPRITE 7
0// esVisible
// SPRITE 8
0// esVisible
// SPRITE 9
0// esVisible
// SPRITE 10
0// esVisible
// SPRITE 11
1// esVisible
// SPRITE 12
0// esVisible
// SPRITE 13
0// esVisible
// SPRITE 14
0// esVisible
// SPRITE 15
0// esVisible
// SPRITE 16
0// esVisible
// SPRITE 17
0// esVisible
// SPRITE 18
0// esVisible
// SPRITE 19
0// esVisible
// SPRITE 20
0// esVisible
// SPRITE 21
0// esVisible
// SPRITE 22
0// esVisible
// SPRITE 23
0// esVisible
// SPRITE 24
0// esVisible
// SPRITE 25
0// esVisible
// GUILLERMO
0// orientacion
160// posX
42// posY
2// altura
0// estado
2// contadorAnimacion
0// bajando
0// orientacion
0// enDesnivel
0// giradoEnDesnivel
0// flipX
49152// despFlipX
-2// despX
-34// despY
16// valorPosicion
0// puedeQuitarObjetos
32// objetos
252// mascaraObjetos
0// contadorObjetos
8// permisosPuertas
8// numFotogramas
2// incrPosY
// ADSO
0// orientacion
158// posX
42// posY
2// altura
0// estado
0// contadorAnimacion
0// bajando
0// orientacion
0// enDesnivel
0// giradoEnDesnivel
0// flipX
49152// despFlipX
-2// despX
-32// despY
32// valorPosicion
0// puedeQuitarObjetos
0// objetos
3// mascaraObjetos
0// contadorObjetos
8// permisosPuertas
8// numFotogramas
60// mascarasPuertasBusqueda
-1// aDondeVa
-1// aDondeHaLlegado
0// oldEstado
0// movimientosFrustados
0// cntParaDormir
// MALAQUIAS
1// orientacion
55// posX
56// posY
15// altura
0// estado
0// contadorAnimacion
0// bajando
1// orientacion
0// enDesnivel
0// giradoEnDesnivel
0// flipX
49152// despFlipX
-2// despX
-34// despY
16// valorPosicion
0// puedeQuitarObjetos
0// objetos
0// mascaraObjetos
0// contadorObjetos
31// permisosPuertas
8// numFotogramas
63// mascarasPuertasBusqueda
2// aDondeVa
2// aDondeHaLlegado
0// estaMuerto
0// estado2
0// contadorEnScriptorium
// ABAD
1// orientacion
157// posX
45// posY
2// altura
2// estado
0// contadorAnimacion
0// bajando
1// orientacion
0// enDesnivel
0// giradoEnDesnivel
0// flipX
49152// despFlipX
-2// despX
-34// despY
16// valorPosicion
1// puedeQuitarObjetos
0// objetos
16// mascaraObjetos
0// contadorObjetos
25// permisosPuertas
8// numFotogramas
63// mascarasPuertasBusqueda
4// aDondeVa
-1// aDondeHaLlegado
0// contador
0// numFrase
0// guillermoBienColocado
0// lleganLosMonjes
0// guillermoHaCogidoElPergamino
// BERENGARIO
2// orientacion
61// posX
92// posY
15// altura
0// estado
0// contadorAnimacion
0// bajando
2// orientacion
0// enDesnivel
0// giradoEnDesnivel
0// flipX
49152// despFlipX
-2// despX
-34// despY
16// valorPosicion
0// puedeQuitarObjetos
0// objetos
0// mascaraObjetos
0// contadorObjetos
31// permisosPuertas
8// numFotogramas
63// mascarasPuertasBusqueda
2// aDondeVa
2// aDondeHaLlegado
0// encapuchado
0// estado2
1// estaVivo
0// contadorPergamino
// SEVERINO
1// orientacion
151// posX
47// posY
2// altura
0// estado
0// contadorAnimacion
0// bajando
1// orientacion
0// enDesnivel
0// giradoEnDesnivel
1// flipX
49152// despFlipX
-2// despX
-34// despY
16// valorPosicion
0// puedeQuitarObjetos
0// objetos
0// mascaraObjetos
0// contadorObjetos
12// permisosPuertas
8// numFotogramas
47// mascarasPuertasBusqueda
3// aDondeVa
2// aDondeHaLlegado
1// estaVivo
// JORGE
0// orientacion
0// posX
0// posY
0// altura
0// estado
0// contadorAnimacion
0// bajando
0// orientacion
0// enDesnivel
0// giradoEnDesnivel
0// flipX
49152// despFlipX
-2// despX
-34// despY
16// valorPosicion
0// puedeQuitarObjetos
0// objetos
0// mascaraObjetos
0// contadorObjetos
31// permisosPuertas
8// numFotogramas
63// mascarasPuertasBusqueda
0// aDondeVa
-6// aDondeHaLlegado
0// estaActivo
0// contadorHuida
// BERNARDO
0// orientacion
0// posX
0// posY
0// altura
0// estado
0// contadorAnimacion
0// bajando
0// orientacion
0// enDesnivel
0// giradoEnDesnivel
0// flipX
49152// despFlipX
-2// despX
-34// despY
16// valorPosicion
1// puedeQuitarObjetos
0// objetos
0// mascaraObjetos
0// contadorObjetos
31// permisosPuertas
8// numFotogramas
63// mascarasPuertasBusqueda
0// aDondeVa
-6// aDondeHaLlegado
0// estaEnLaAbadia
// PUERTA 0
1// orientacion
97// posX
55// posY
2// altura
1// identificador
0// estaAbierta
1// haciaDentro
0// estaFija
0// hayQueRedibujar
// PUERTA 1
2// orientacion
183// posX
30// posY
2// altura
2// identificador
0// estaAbierta
1// haciaDentro
0// estaFija
0// hayQueRedibujar
// PUERTA 2
0// orientacion
102// posX
95// posY
2// altura
4// identificador
0// estaAbierta
0// haciaDentro
0// estaFija
0// hayQueRedibujar
// PUERTA 3
2// orientacion
158// posX
40// posY
2// altura
8// identificador
1// estaAbierta
1// haciaDentro
0// estaFija
0// hayQueRedibujar
// PUERTA 4
3// orientacion
126// posX
38// posY
2// altura
16// identificador
0// estaAbierta
0// haciaDentro
0// estaFija
0// hayQueRedibujar
// PUERTA 5
2// orientacion
96// posX
118// posY
0// altura
0// identificador
1// estaAbierta
1// haciaDentro
1// estaFija
0// hayQueRedibujar
// PUERTA 6
2// orientacion
96// posX
123// posY
0// altura
0// identificador
1// estaAbierta
0// haciaDentro
1// estaFija
0// hayQueRedibujar
// OBJETO 0
1// orientacion
52// posX
94// posY
19// altura
0// seEstaCogiendo
0// seHaCogido
0// numPersonaje
// OBJETO 1
0// orientacion
107// posX
85// posY
6// altura
0// seEstaCogiendo
0// seHaCogido
0// numPersonaje
// OBJETO 2
0// orientacion
0// posX
0// posY
0// altura
0// seEstaCogiendo
1// seHaCogido
0// numPersonaje
// OBJETO 3
1// orientacion
54// posX
94// posY
19// altura
0// seEstaCogiendo
0// seHaCogido
0// numPersonaje
// OBJETO 4
0// orientacion
0// posX
0// posY
0// altura
0// seEstaCogiendo
0// seHaCogido
0// numPersonaje
// OBJETO 5
0// orientacion
0// posX
0// posY
0// altura
0// seEstaCogiendo
0// seHaCogido
0// numPersonaje
// OBJETO 6
0// orientacion
53// posX
53// posY
19// altura
0// seEstaCogiendo
0// seHaCogido
0// numPersonaje
// OBJETO 7
0// orientacion
8// posX
8// posY
2// altura
0// seEstaCogiendo
0// seHaCogido
0// numPersonaje
"""

file2 = {"core_dia":1,"core_momentoDia":4,"core_duracionMomentoDia":0,"core_oldMomentoDia":0,"core_avanzarMomentoDia":0,"core_obsequium":31,"core_haFracasado":0,"core_investigacionCompleta":0,"core_bonus":0,"core_mascaraPuertas":239,"core_espejoCerrado":1,"core_numeroRomano":0,"core_despDatosAlturaEspejo":103444,"core_despBloqueEspejo":123468,"core_seAcabaLaNoche":0,"core_haAmanecido":0,"core_usandoLampara":0,"core_lamparaDesaparecida":1,"core_tiempoUsoLampara":0,"core_cambioEstadoLampara":0,"core_cntTiempoAOscuras":0,"core_cntLeeLibroSinGuantes":0,"core_pergaminoGuardado":0,"core_numeroAleatorio":113,"core_hayMovimiento":1,"core_cntMovimiento":0,"core_numPersonajeCamara":0,"core_opcionPersonajeCamara":0,"SPRITE_0_esVisible":1,"SPRITE_1_esVisible":1,"SPRITE_2_esVisible":0,"SPRITE_3_esVisible":0,"SPRITE_4_esVisible":0,"SPRITE_5_esVisible":0,"SPRITE_6_esVisible":0,"SPRITE_7_esVisible":0,"SPRITE_8_esVisible":0,"SPRITE_9_esVisible":0,"SPRITE_10_esVisible":0,"SPRITE_11_esVisible":0,"SPRITE_12_esVisible":0,"SPRITE_13_esVisible":0,"SPRITE_14_esVisible":0,"SPRITE_15_esVisible":0,"SPRITE_16_esVisible":0,"SPRITE_17_esVisible":0,"SPRITE_18_esVisible":0,"SPRITE_19_esVisible":0,"SPRITE_20_esVisible":0,"SPRITE_21_esVisible":0,"SPRITE_22_esVisible":0,"SPRITE_23_esVisible":0,"SPRITE_24_esVisible":0,"SPRITE_25_esVisible":0,"GUILLERMO_orientacion":0,"GUILLERMO_posX":136,"GUILLERMO_posY":168,"GUILLERMO_altura":0,"GUILLERMO_estado":0,"GUILLERMO_contadorAnimacion":0,"GUILLERMO_bajando":0,"GUILLERMO_enDesnivel":0,"GUILLERMO_giradoEnDesnivel":0,"GUILLERMO_flipX":0,"GUILLERMO_despFlipX":49152,"GUILLERMO_despX":-2,"GUILLERMO_despY":-34,"GUILLERMO_valorPosicion":16,"GUILLERMO_puedeQuitarObjetos":0,"GUILLERMO_objetos":32,"GUILLERMO_mascaraObjetos":252,"GUILLERMO_contadorObjetos":0,"GUILLERMO_permisosPuertas":8,"GUILLERMO_numFotogramas":8,"GUILLERMO_incrPosY":2,"ADSO_orientacion":0,"ADSO_posX":134,"ADSO_posY":170,"ADSO_altura":0,"ADSO_estado":0,"ADSO_contadorAnimacion":0,"ADSO_bajando":0,"ADSO_enDesnivel":0,"ADSO_giradoEnDesnivel":0,"ADSO_flipX":0,"ADSO_despFlipX":49152,"ADSO_despX":-2,"ADSO_despY":-32,"ADSO_valorPosicion":32,"ADSO_puedeQuitarObjetos":0,"ADSO_objetos":0,"ADSO_mascaraObjetos":3,"ADSO_contadorObjetos":0,"ADSO_permisosPuertas":8,"ADSO_numFotogramas":8,"ADSO_mascarasPuertasBusqueda":60,"ADSO_aDondeVa":0,"ADSO_aDondeHaLlegado":-1,"ADSO_oldEstado":0,"ADSO_movimientosFrustados":0,"ADSO_cntParaDormir":0,"MALAQUIAS_orientacion":0,"MALAQUIAS_posX":38,"MALAQUIAS_posY":38,"MALAQUIAS_altura":15,"MALAQUIAS_estado":0,"MALAQUIAS_contadorAnimacion":0,"MALAQUIAS_bajando":0,"MALAQUIAS_enDesnivel":0,"MALAQUIAS_giradoEnDesnivel":0,"MALAQUIAS_flipX":0,"MALAQUIAS_despFlipX":49152,"MALAQUIAS_despX":-2,"MALAQUIAS_despY":-34,"MALAQUIAS_valorPosicion":16,"MALAQUIAS_puedeQuitarObjetos":0,"MALAQUIAS_objetos":0,"MALAQUIAS_mascaraObjetos":3,"MALAQUIAS_contadorObjetos":0,"MALAQUIAS_permisosPuertas":31,"MALAQUIAS_numFotogramas":8,"MALAQUIAS_mascarasPuertasBusqueda":63,"MALAQUIAS_aDondeVa":0,"MALAQUIAS_aDondeHaLlegado":-6,"MALAQUIAS_estaMuerto":0,"MALAQUIAS_estado2":0,"MALAQUIAS_contadorEnScriptorium":224,"ABAD_orientacion":0,"ABAD_posX":136,"ABAD_posY":132,"ABAD_altura":2,"ABAD_estado":0,"ABAD_contadorAnimacion":0,"ABAD_bajando":0,"ABAD_enDesnivel":0,"ABAD_giradoEnDesnivel":0,"ABAD_flipX":0,"ABAD_despFlipX":49152,"ABAD_despX":-2,"ABAD_despY":-34,"ABAD_valorPosicion":16,"ABAD_puedeQuitarObjetos":1,"ABAD_objetos":0,"ABAD_mascaraObjetos":16,"ABAD_contadorObjetos":0,"ABAD_permisosPuertas":25,"ABAD_numFotogramas":8,"ABAD_mascarasPuertasBusqueda":63,"ABAD_aDondeVa":0,"ABAD_aDondeHaLlegado":-6,"ABAD_contador":0,"ABAD_numFrase":0,"ABAD_guillermoBienColocado":63,"ABAD_lleganLosMonjes":0,"ABAD_guillermoHaCogidoElPergamino":0,"BERENGARIO_orientacion":0,"BERENGARIO_posX":40,"BERENGARIO_posY":72,"BERENGARIO_altura":15,"BERENGARIO_estado":0,"BERENGARIO_contadorAnimacion":0,"BERENGARIO_bajando":0,"BERENGARIO_enDesnivel":0,"BERENGARIO_giradoEnDesnivel":0,"BERENGARIO_flipX":0,"BERENGARIO_despFlipX":49152,"BERENGARIO_despX":-2,"BERENGARIO_despY":-34,"BERENGARIO_valorPosicion":16,"BERENGARIO_puedeQuitarObjetos":0,"BERENGARIO_objetos":0,"BERENGARIO_mascaraObjetos":0,"BERENGARIO_contadorObjetos":0,"BERENGARIO_permisosPuertas":31,"BERENGARIO_numFotogramas":8,"BERENGARIO_mascarasPuertasBusqueda":63,"BERENGARIO_aDondeVa":0,"BERENGARIO_aDondeHaLlegado":-6,"BERENGARIO_encapuchado":0,"BERENGARIO_estado2":0,"BERENGARIO_estaVivo":1,"BERENGARIO_contadorPergamino":0,"SEVERINO_orientacion":0,"SEVERINO_posX":200,"SEVERINO_posY":40,"SEVERINO_altura":0,"SEVERINO_estado":0,"SEVERINO_contadorAnimacion":0,"SEVERINO_bajando":0,"SEVERINO_enDesnivel":0,"SEVERINO_giradoEnDesnivel":0,"SEVERINO_flipX":0,"SEVERINO_despFlipX":49152,"SEVERINO_despX":-2,"SEVERINO_despY":-34,"SEVERINO_valorPosicion":16,"SEVERINO_puedeQuitarObjetos":0,"SEVERINO_objetos":0,"SEVERINO_mascaraObjetos":0,"SEVERINO_contadorObjetos":0,"SEVERINO_permisosPuertas":12,"SEVERINO_numFotogramas":8,"SEVERINO_mascarasPuertasBusqueda":47,"SEVERINO_aDondeVa":0,"SEVERINO_aDondeHaLlegado":-6,"SEVERINO_estaVivo":1,"JORGE_orientacion":0,"JORGE_posX":0,"JORGE_posY":0,"JORGE_altura":0,"JORGE_estado":0,"JORGE_contadorAnimacion":0,"JORGE_bajando":0,"JORGE_enDesnivel":0,"JORGE_giradoEnDesnivel":0,"JORGE_flipX":0,"JORGE_despFlipX":49152,"JORGE_despX":-2,"JORGE_despY":-34,"JORGE_valorPosicion":16,"JORGE_puedeQuitarObjetos":0,"JORGE_objetos":0,"JORGE_mascaraObjetos":0,"JORGE_contadorObjetos":0,"JORGE_permisosPuertas":31,"JORGE_numFotogramas":8,"JORGE_mascarasPuertasBusqueda":63,"JORGE_aDondeVa":0,"JORGE_aDondeHaLlegado":-6,"JORGE_estaActivo":0,"JORGE_contadorHuida":0,"BERNARDO_orientacion":0,"BERNARDO_posX":0,"BERNARDO_posY":0,"BERNARDO_altura":0,"BERNARDO_estado":0,"BERNARDO_contadorAnimacion":0,"BERNARDO_bajando":0,"BERNARDO_enDesnivel":0,"BERNARDO_giradoEnDesnivel":0,"BERNARDO_flipX":0,"BERNARDO_despFlipX":49152,"BERNARDO_despX":-2,"BERNARDO_despY":-34,"BERNARDO_valorPosicion":16,"BERNARDO_puedeQuitarObjetos":1,"BERNARDO_objetos":0,"BERNARDO_mascaraObjetos":0,"BERNARDO_contadorObjetos":0,"BERNARDO_permisosPuertas":31,"BERNARDO_numFotogramas":8,"BERNARDO_mascarasPuertasBusqueda":63,"BERNARDO_aDondeVa":0,"BERNARDO_aDondeHaLlegado":-6,"BERNARDO_estaEnLaAbadia":0,"PUERTA_0_orientacion":1,"PUERTA_0_posX":97,"PUERTA_0_posY":55,"PUERTA_0_altura":2,"PUERTA_0_identificador":1,"PUERTA_0_estaAbierta":0,"PUERTA_0_haciaDentro":1,"PUERTA_0_estaFija":0,"PUERTA_0_hayQueRedibujar":0,"PUERTA_1_orientacion":2,"PUERTA_1_posX":183,"PUERTA_1_posY":30,"PUERTA_1_altura":2,"PUERTA_1_identificador":2,"PUERTA_1_estaAbierta":0,"PUERTA_1_haciaDentro":1,"PUERTA_1_estaFija":0,"PUERTA_1_hayQueRedibujar":0,"PUERTA_2_orientacion":0,"PUERTA_2_posX":102,"PUERTA_2_posY":95,"PUERTA_2_altura":2,"PUERTA_2_identificador":4,"PUERTA_2_estaAbierta":0,"PUERTA_2_haciaDentro":0,"PUERTA_2_estaFija":0,"PUERTA_2_hayQueRedibujar":0,"PUERTA_3_orientacion":3,"PUERTA_3_posX":158,"PUERTA_3_posY":40,"PUERTA_3_altura":2,"PUERTA_3_identificador":8,"PUERTA_3_estaAbierta":0,"PUERTA_3_haciaDentro":1,"PUERTA_3_estaFija":0,"PUERTA_3_hayQueRedibujar":0,"PUERTA_4_orientacion":3,"PUERTA_4_posX":126,"PUERTA_4_posY":38,"PUERTA_4_altura":2,"PUERTA_4_identificador":16,"PUERTA_4_estaAbierta":0,"PUERTA_4_haciaDentro":0,"PUERTA_4_estaFija":0,"PUERTA_4_hayQueRedibujar":0,"PUERTA_5_orientacion":2,"PUERTA_5_posX":96,"PUERTA_5_posY":118,"PUERTA_5_altura":0,"PUERTA_5_identificador":0,"PUERTA_5_estaAbierta":1,"PUERTA_5_haciaDentro":1,"PUERTA_5_estaFija":1,"PUERTA_5_hayQueRedibujar":0,"PUERTA_6_orientacion":2,"PUERTA_6_posX":96,"PUERTA_6_posY":123,"PUERTA_6_altura":0,"PUERTA_6_identificador":0,"PUERTA_6_estaAbierta":1,"PUERTA_6_haciaDentro":0,"PUERTA_6_estaFija":1,"PUERTA_6_hayQueRedibujar":0,"OBJETO_0_orientacion":1,"OBJETO_0_posX":52,"OBJETO_0_posY":94,"OBJETO_0_altura":19,"OBJETO_0_seEstaCogiendo":0,"OBJETO_0_seHaCogido":0,"OBJETO_0_numPersonaje":0,"OBJETO_1_orientacion":0,"OBJETO_1_posX":107,"OBJETO_1_posY":85,"OBJETO_1_altura":6,"OBJETO_1_seEstaCogiendo":0,"OBJETO_1_seHaCogido":0,"OBJETO_1_numPersonaje":0,"OBJETO_2_orientacion":0,"OBJETO_2_posX":0,"OBJETO_2_posY":0,"OBJETO_2_altura":0,"OBJETO_2_seEstaCogiendo":0,"OBJETO_2_seHaCogido":1,"OBJETO_2_numPersonaje":0,"OBJETO_3_orientacion":1,"OBJETO_3_posX":54,"OBJETO_3_posY":94,"OBJETO_3_altura":19,"OBJETO_3_seEstaCogiendo":0,"OBJETO_3_seHaCogido":0,"OBJETO_3_numPersonaje":0,"OBJETO_4_orientacion":0,"OBJETO_4_posX":0,"OBJETO_4_posY":0,"OBJETO_4_altura":0,"OBJETO_4_seEstaCogiendo":0,"OBJETO_4_seHaCogido":0,"OBJETO_4_numPersonaje":0,"OBJETO_5_orientacion":0,"OBJETO_5_posX":0,"OBJETO_5_posY":0,"OBJETO_5_altura":0,"OBJETO_5_seEstaCogiendo":0,"OBJETO_5_seHaCogido":0,"OBJETO_5_numPersonaje":0,"OBJETO_6_orientacion":0,"OBJETO_6_posX":53,"OBJETO_6_posY":53,"OBJETO_6_altura":19,"OBJETO_6_seEstaCogiendo":0,"OBJETO_6_seHaCogido":0,"OBJETO_6_numPersonaje":0,"OBJETO_7_orientacion":0,"OBJETO_7_posX":8,"OBJETO_7_posY":8,"OBJETO_7_altura":2,"OBJETO_7_seEstaCogiendo":0,"OBJETO_7_seHaCogido":0,"OBJETO_7_numPersonaje":0}

file="""1// dia
4// momentoDia
0// duracionMomentoDia
4// oldMomentoDia
0// avanzarMomentoDia
31// obsequium
0// haFracasado
0// investigacionCompleta
0// bonus
239// mascaraPuertas
1// espejoCerrado
0// numeroRomano
103444// despDatosAlturaEspejo
123468// despBloqueEspejo
0// seAcabaLaNoche
0// haAmanecido
0// usandoLampara
1// lamparaDesaparecida
0// tiempoUsoLampara
0// cambioEstadoLampara
0// cntTiempoAOscuras
0// cntLeeLibroSinGuantes
0// pergaminoGuardado
136// numeroAleatorio
1// hayMovimiento
0// cntMovimiento
0// numPersonajeCamara
0// opcionPersonajeCamara
// SPRITE 0
1// esVisible
// SPRITE 1
1// esVisible
// SPRITE 2
0// esVisible
// SPRITE 3
0// esVisible
// SPRITE 4
0// esVisible
// SPRITE 5
0// esVisible
// SPRITE 6
0// esVisible
// SPRITE 7
0// esVisible
// SPRITE 8
0// esVisible
// SPRITE 9
0// esVisible
// SPRITE 10
0// esVisible
// SPRITE 11
0// esVisible
// SPRITE 12
0// esVisible
// SPRITE 13
0// esVisible
// SPRITE 14
0// esVisible
// SPRITE 15
0// esVisible
// SPRITE 16
0// esVisible
// SPRITE 17
0// esVisible
// SPRITE 18
0// esVisible
// SPRITE 19
0// esVisible
// SPRITE 20
0// esVisible
// SPRITE 21
0// esVisible
// SPRITE 22
0// esVisible
// SPRITE 23
0// esVisible
// SPRITE 24
0// esVisible
// SPRITE 25
0// esVisible
// GUILLERMO
3// posOrientacion
136// posX
167// posY
0// altura
0// estado
0// contadorAnimacion
0// bajando
3// orientacion
0// enDesnivel
0// giradoEnDesnivel
1// flipX
49152// despFlipX
-2// despX
-34// despY
16// valorPosicion
0// puedeQuitarObjetos
32// objetos
252// mascaraObjetos
0// contadorObjetos
8// permisosPuertas
8// numFotogramas
2// incrPosY
// ADSO
1// posOrientacion
134// posX
168// posY
0// altura
0// estado
0// contadorAnimacion
0// bajando
1// orientacion
0// enDesnivel
0// giradoEnDesnivel
0// flipX
49152// despFlipX
-2// despX
-32// despY
32// valorPosicion
0// puedeQuitarObjetos
0// objetos
3// mascaraObjetos
0// contadorObjetos
8// permisosPuertas
8// numFotogramas
60// mascarasPuertasBusqueda
-1// aDondeVa
-1// aDondeHaLlegado
0// oldEstado
0// movimientosFrustados
0// cntParaDormir
// MALAQUIAS
3// posOrientacion
38// posX
40// posY
15// altura
0// estado
3// contadorAnimacion
0// bajando
3// orientacion
0// enDesnivel
0// giradoEnDesnivel
0// flipX
49152// despFlipX
-2// despX
-34// despY
16// valorPosicion
0// puedeQuitarObjetos
0// objetos
3// mascaraObjetos
0// contadorObjetos
31// permisosPuertas
8// numFotogramas
63// mascarasPuertasBusqueda
2// aDondeVa
-6// aDondeHaLlegado
0// estaMuerto
0// estado2
0// contadorEnScriptorium
// ABAD
3// posOrientacion
136// posX
132// posY
2// altura
0// estado
0// contadorAnimacion
0// bajando
3// orientacion
0// enDesnivel
0// giradoEnDesnivel
0// flipX
49152// despFlipX
-2// despX
-34// despY
16// valorPosicion
1// puedeQuitarObjetos
0// objetos
16// mascaraObjetos
0// contadorObjetos
25// permisosPuertas
8// numFotogramas
63// mascarasPuertasBusqueda
3// aDondeVa
3// aDondeHaLlegado
0// contador
0// numFrase
0// guillermoBienColocado
0// lleganLosMonjes
0// guillermoHaCogidoElPergamino
// BERENGARIO
3// posOrientacion
40// posX
72// posY
15// altura
0// estado
0// contadorAnimacion
0// bajando
3// orientacion
0// enDesnivel
0// giradoEnDesnivel
0// flipX
49152// despFlipX
-2// despX
-34// despY
16// valorPosicion
0// puedeQuitarObjetos
0// objetos
0// mascaraObjetos
0// contadorObjetos
31// permisosPuertas
8// numFotogramas
63// mascarasPuertasBusqueda
2// aDondeVa
-6// aDondeHaLlegado
0// encapuchado
0// estado2
1// estaVivo
0// contadorPergamino
// SEVERINO
0// posOrientacion
200// posX
40// posY
0// altura
0// estado
0// contadorAnimacion
0// bajando
0// orientacion
0// enDesnivel
0// giradoEnDesnivel
0// flipX
49152// despFlipX
-2// despX
-34// despY
16// valorPosicion
0// puedeQuitarObjetos
0// objetos
0// mascaraObjetos
0// contadorObjetos
12// permisosPuertas
8// numFotogramas
47// mascarasPuertasBusqueda
2// aDondeVa
-6// aDondeHaLlegado
1// estaVivo
// JORGE
0// posOrientacion
0// posX
0// posY
0// altura
0// estado
0// contadorAnimacion
0// bajando
0// orientacion
0// enDesnivel
0// giradoEnDesnivel
0// flipX
49152// despFlipX
-2// despX
-34// despY
16// valorPosicion
0// puedeQuitarObjetos
0// objetos
0// mascaraObjetos
0// contadorObjetos
31// permisosPuertas
8// numFotogramas
63// mascarasPuertasBusqueda
0// aDondeVa
-6// aDondeHaLlegado
0// estaActivo
0// contadorHuida
// BERNARDO
0// posOrientacion
0// posX
0// posY
0// altura
0// estado
0// contadorAnimacion
0// bajando
0// orientacion
0// enDesnivel
0// giradoEnDesnivel
0// flipX
49152// despFlipX
-2// despX
-34// despY
16// valorPosicion
1// puedeQuitarObjetos
0// objetos
0// mascaraObjetos
0// contadorObjetos
31// permisosPuertas
8// numFotogramas
63// mascarasPuertasBusqueda
0// aDondeVa
-6// aDondeHaLlegado
0// estaEnLaAbadia
// PUERTA 0
1// posOrientacion
97// posX
55// posY
2// altura
1// identificador
0// estaAbierta
1// haciaDentro
0// estaFija
0// hayQueRedibujar
// PUERTA 1
2// posOrientacion
183// posX
30// posY
2// altura
2// identificador
0// estaAbierta
1// haciaDentro
0// estaFija
0// hayQueRedibujar
// PUERTA 2
0// posOrientacion
102// posX
95// posY
2// altura
4// identificador
0// estaAbierta
0// haciaDentro
0// estaFija
0// hayQueRedibujar
// PUERTA 3
3// posOrientacion
158// posX
40// posY
2// altura
8// identificador
0// estaAbierta
1// haciaDentro
0// estaFija
0// hayQueRedibujar
// PUERTA 4
3// posOrientacion
126// posX
38// posY
2// altura
16// identificador
0// estaAbierta
0// haciaDentro
0// estaFija
0// hayQueRedibujar
// PUERTA 5
2// posOrientacion
96// posX
118// posY
0// altura
0// identificador
1// estaAbierta
1// haciaDentro
1// estaFija
0// hayQueRedibujar
// PUERTA 6
2// posOrientacion
96// posX
123// posY
0// altura
0// identificador
1// estaAbierta
0// haciaDentro
1// estaFija
0// hayQueRedibujar
// OBJETO 0
1// posOrientacion
52// posX
94// posY
19// altura
0// seEstaCogiendo
0// seHaCogido
0// numPersonaje
// OBJETO 1
0// posOrientacion
107// posX
85// posY
6// altura
0// seEstaCogiendo
0// seHaCogido
0// numPersonaje
// OBJETO 2
0// posOrientacion
0// posX
0// posY
0// altura
0// seEstaCogiendo
1// seHaCogido
0// numPersonaje
// OBJETO 3
1// posOrientacion
54// posX
94// posY
19// altura
0// seEstaCogiendo
0// seHaCogido
0// numPersonaje
// OBJETO 4
0// posOrientacion
0// posX
0// posY
0// altura
0// seEstaCogiendo
0// seHaCogido
0// numPersonaje
// OBJETO 5
0// posOrientacion
0// posX
0// posY
0// altura
0// seEstaCogiendo
0// seHaCogido
0// numPersonaje
// OBJETO 6
0// posOrientacion
53// posX
53// posY
19// altura
0// seEstaCogiendo
0// seHaCogido
0// numPersonaje
// OBJETO 7
0// posOrientacion
8// posX
8// posY
2// altura
0// seEstaCogiendo
0// seHaCogido
0// numPersonaje
"""
def dict2check(dict):
    ant = ""
    result = ""
    for key in dict.keys():
        print ("key: {} value: {}".format(key, dict[key]))
        elements = key.split("_")
        pre = "NaN"
        name = "NaN"

        if (elements[0] == "core"):
            pre = ""
            name = elements[1]
        else:
            if (len(elements) == 3):
                pre = "{} {}".format(elements[0], elements[1])
                name = elements[2]
            else:
                pre = elements[0]
                name = elements[1]

            if (ant != pre):
                ant = pre
                result += "// {}\n".format(pre)

        result += "{}// {}\n".format(dict[key], name)
    return result

pre = "core_"
output = {}
for line in file.split("\n"):
    print(line)
    res = line.split("// ")

    if (len(res) == 2):
        value = res[0]
        key = res[1]
        if (value == ""):
            pre = key.replace(" ", "_")+"_"
        else:
            output[pre+key] = value

    print("value ({}) key ({})".format(value, pre+key))
print(json.dumps(output))

print ("dict2check")
# print(dict2check(file2))
# print(dict2check(output))
out2 = dict2check(output)

import difflib

print("-----------")
print(file[:250])
print("-----------")
print(output["core_oldMomentoDia"])
print("-----------")
print(out2[:250])
print("-----------")
for line in difflib.context_diff(file, out2):
    print(line)
print("file -----------")
print(file)
print("out -----------")
print(out2)

fout = open("/tmp/o1", "w")
fout.write(file)
fout.close()

fout = open("/tmp/c2", "w")
fout.write(out2)
fout.close()

dic2 = {'core_dia': 1, 'core_momentoDia': 4, 'core_duracionMomentoDia': 0, 'core_oldMomentoDia': 4, 'core_avanzarMomentoDia': 0, 'core_obsequium': 31, 'core_haFracasado': 0, 'core_investigacionCompleta': 0, 'core_bonus': 0, 'core_mascaraPuertas': 239, 'core_espejoCerrado': 1, 'core_numeroRomano': 0, 'core_despDatosAlturaEspejo': 103444, 'core_despBloqueEspejo': 123468, 'core_seAcabaLaNoche': 0, 'core_haAmanecido': 0, 'core_usandoLampara': 0, 'core_lamparaDesaparecida': 1, 'core_tiempoUsoLampara': 0, 'core_cambioEstadoLampara': 0, 'core_cntTiempoAOscuras': 0, 'core_cntLeeLibroSinGuantes': 0, 'core_pergaminoGuardado': 0, 'core_numeroAleatorio': 81, 'core_hayMovimiento': 1, 'core_cntMovimiento': 2, 'core_numPersonajeCamara': 0, 'core_opcionPersonajeCamara': 0, 'SPRITE_0_esVisible': 1, 'SPRITE_1_esVisible': 1, 'SPRITE_2_esVisible': 0, 'SPRITE_3_esVisible': 0, 'SPRITE_4_esVisible': 0, 'SPRITE_5_esVisible': 0, 'SPRITE_6_esVisible': 0, 'SPRITE_7_esVisible': 0, 'SPRITE_8_esVisible': 0, 'SPRITE_9_esVisible': 0, 'SPRITE_10_esVisible': 0, 'SPRITE_11_esVisible': 0, 'SPRITE_12_esVisible': 0, 'SPRITE_13_esVisible': 0, 'SPRITE_14_esVisible': 0, 'SPRITE_15_esVisible': 0, 'SPRITE_16_esVisible': 0, 'SPRITE_17_esVisible': 0, 'SPRITE_18_esVisible': 0, 'SPRITE_19_esVisible': 0, 'SPRITE_20_esVisible': 0, 'SPRITE_21_esVisible': 0, 'SPRITE_22_esVisible': 0, 'SPRITE_23_esVisible': 0, 'SPRITE_24_esVisible': 0, 'SPRITE_25_esVisible': 0, 'GUILLERMO_orientacion': 2, 'GUILLERMO_posX': 135, 'GUILLERMO_posY': 168, 'GUILLERMO_altura': 0, 'GUILLERMO_estado': 0, 'GUILLERMO_contadorAnimacion': 2, 'GUILLERMO_bajando': 0, 'GUILLERMO_enDesnivel': 0, 'GUILLERMO_giradoEnDesnivel': 0, 'GUILLERMO_flipX': 1, 'GUILLERMO_despFlipX': 49152, 'GUILLERMO_despX': -2, 'GUILLERMO_despY': -34, 'GUILLERMO_valorPosicion': 16, 'GUILLERMO_puedeQuitarObjetos': 0, 'GUILLERMO_objetos': 32, 'GUILLERMO_mascaraObjetos': 252, 'GUILLERMO_contadorObjetos': 0, 'GUILLERMO_permisosPuertas': 8, 'GUILLERMO_numFotogramas': 8, 'GUILLERMO_incrPosY': 2, 'ADSO_orientacion': 1, 'ADSO_posX': 132, 'ADSO_posY': 169, 'ADSO_altura': 0, 'ADSO_estado': 0, 'ADSO_contadorAnimacion': 0, 'ADSO_bajando': 0, 'ADSO_enDesnivel': 0, 'ADSO_giradoEnDesnivel': 0, 'ADSO_flipX': 0, 'ADSO_despFlipX': 49152, 'ADSO_despX': -2, 'ADSO_despY': -32, 'ADSO_valorPosicion': 32, 'ADSO_puedeQuitarObjetos': 0, 'ADSO_objetos': 0, 'ADSO_mascaraObjetos': 3, 'ADSO_contadorObjetos': 0, 'ADSO_permisosPuertas': 8, 'ADSO_numFotogramas': 8, 'ADSO_mascarasPuertasBusqueda': 60, 'ADSO_aDondeVa': -1, 'ADSO_aDondeHaLlegado': -1, 'ADSO_oldEstado': 0, 'ADSO_movimientosFrustados': 0, 'ADSO_cntParaDormir': 0, 'MALAQUIAS_orientacion': 3, 'MALAQUIAS_posX': 38, 'MALAQUIAS_posY': 44, 'MALAQUIAS_altura': 15, 'MALAQUIAS_estado': 0, 'MALAQUIAS_contadorAnimacion': 0, 'MALAQUIAS_bajando': 0, 'MALAQUIAS_enDesnivel': 0, 'MALAQUIAS_giradoEnDesnivel': 0, 'MALAQUIAS_flipX': 0, 'MALAQUIAS_despFlipX': 49152, 'MALAQUIAS_despX': -2, 'MALAQUIAS_despY': -34, 'MALAQUIAS_valorPosicion': 16, 'MALAQUIAS_puedeQuitarObjetos': 0, 'MALAQUIAS_objetos': 0, 'MALAQUIAS_mascaraObjetos': 3, 'MALAQUIAS_contadorObjetos': 0, 'MALAQUIAS_permisosPuertas': 31, 'MALAQUIAS_numFotogramas': 8, 'MALAQUIAS_mascarasPuertasBusqueda': 63, 'MALAQUIAS_aDondeVa': 2, 'MALAQUIAS_aDondeHaLlegado': -6, 'MALAQUIAS_estaMuerto': 0, 'MALAQUIAS_estado2': 0, 'MALAQUIAS_contadorEnScriptorium': 224, 'ABAD_orientacion': 3, 'ABAD_posX': 136, 'ABAD_posY': 132, 'ABAD_altura': 2, 'ABAD_estado': 0, 'ABAD_contadorAnimacion': 0, 'ABAD_bajando': 0, 'ABAD_enDesnivel': 0, 'ABAD_giradoEnDesnivel': 0, 'ABAD_flipX': 0, 'ABAD_despFlipX': 49152, 'ABAD_despX': -2, 'ABAD_despY': -34, 'ABAD_valorPosicion': 16, 'ABAD_puedeQuitarObjetos': 1, 'ABAD_objetos': 0, 'ABAD_mascaraObjetos': 16, 'ABAD_contadorObjetos': 0, 'ABAD_permisosPuertas': 25, 'ABAD_numFotogramas': 8, 'ABAD_mascarasPuertasBusqueda': 63, 'ABAD_aDondeVa': 3, 'ABAD_aDondeHaLlegado': 3, 'ABAD_contador': 0, 'ABAD_numFrase': 0, 'ABAD_guillermoBienColocado': 63, 'ABAD_lleganLosMonjes': 3, 'ABAD_guillermoHaCogidoElPergamino': 0, 'BERENGARIO_orientacion': 2, 'BERENGARIO_posX': 40, 'BERENGARIO_posY': 77, 'BERENGARIO_altura': 15, 'BERENGARIO_estado': 0, 'BERENGARIO_contadorAnimacion': 0, 'BERENGARIO_bajando': 0, 'BERENGARIO_enDesnivel': 0, 'BERENGARIO_giradoEnDesnivel': 0, 'BERENGARIO_flipX': 0, 'BERENGARIO_despFlipX': 49152, 'BERENGARIO_despX': -2, 'BERENGARIO_despY': -34, 'BERENGARIO_valorPosicion': 16, 'BERENGARIO_puedeQuitarObjetos': 0, 'BERENGARIO_objetos': 0, 'BERENGARIO_mascaraObjetos': 0, 'BERENGARIO_contadorObjetos': 0, 'BERENGARIO_permisosPuertas': 31, 'BERENGARIO_numFotogramas': 8, 'BERENGARIO_mascarasPuertasBusqueda': 63, 'BERENGARIO_aDondeVa': 2, 'BERENGARIO_aDondeHaLlegado': -6, 'BERENGARIO_encapuchado': 0, 'BERENGARIO_estado2': 0, 'BERENGARIO_estaVivo': 1, 'BERENGARIO_contadorPergamino': 0, 'SEVERINO_orientacion': 3, 'SEVERINO_posX': 200, 'SEVERINO_posY': 45, 'SEVERINO_altura': 0, 'SEVERINO_estado': 0, 'SEVERINO_contadorAnimacion': 2, 'SEVERINO_bajando': 0, 'SEVERINO_enDesnivel': 0, 'SEVERINO_giradoEnDesnivel': 0, 'SEVERINO_flipX': 0, 'SEVERINO_despFlipX': 49152, 'SEVERINO_despX': -2, 'SEVERINO_despY': -34, 'SEVERINO_valorPosicion': 16, 'SEVERINO_puedeQuitarObjetos': 0, 'SEVERINO_objetos': 0, 'SEVERINO_mascaraObjetos': 0, 'SEVERINO_contadorObjetos': 0, 'SEVERINO_permisosPuertas': 12, 'SEVERINO_numFotogramas': 8, 'SEVERINO_mascarasPuertasBusqueda': 47, 'SEVERINO_aDondeVa': 2, 'SEVERINO_aDondeHaLlegado': -6, 'SEVERINO_estaVivo': 1, 'JORGE_orientacion': 0, 'JORGE_posX': 0, 'JORGE_posY': 0, 'JORGE_altura': 0, 'JORGE_estado': 0, 'JORGE_contadorAnimacion': 0, 'JORGE_bajando': 0, 'JORGE_enDesnivel': 0, 'JORGE_giradoEnDesnivel': 0, 'JORGE_flipX': 0, 'JORGE_despFlipX': 49152, 'JORGE_despX': -2, 'JORGE_despY': -34, 'JORGE_valorPosicion': 16, 'JORGE_puedeQuitarObjetos': 0, 'JORGE_objetos': 0, 'JORGE_mascaraObjetos': 0, 'JORGE_contadorObjetos': 0, 'JORGE_permisosPuertas': 31, 'JORGE_numFotogramas': 8, 'JORGE_mascarasPuertasBusqueda': 63, 'JORGE_aDondeVa': 0, 'JORGE_aDondeHaLlegado': -6, 'JORGE_estaActivo': 0, 'JORGE_contadorHuida': 0, 'BERNARDO_orientacion': 0, 'BERNARDO_posX': 0, 'BERNARDO_posY': 0, 'BERNARDO_altura': 0, 'BERNARDO_estado': 0, 'BERNARDO_contadorAnimacion': 0, 'BERNARDO_bajando': 0, 'BERNARDO_enDesnivel': 0, 'BERNARDO_giradoEnDesnivel': 0, 'BERNARDO_flipX': 0, 'BERNARDO_despFlipX': 49152, 'BERNARDO_despX': -2, 'BERNARDO_despY': -34, 'BERNARDO_valorPosicion': 16, 'BERNARDO_puedeQuitarObjetos': 1, 'BERNARDO_objetos': 0, 'BERNARDO_mascaraObjetos': 0, 'BERNARDO_contadorObjetos': 0, 'BERNARDO_permisosPuertas': 31, 'BERNARDO_numFotogramas': 8, 'BERNARDO_mascarasPuertasBusqueda': 63, 'BERNARDO_aDondeVa': 0, 'BERNARDO_aDondeHaLlegado': -6, 'BERNARDO_estaEnLaAbadia': 0, 'PUERTA_0_orientacion': 1, 'PUERTA_0_posX': 97, 'PUERTA_0_posY': 55, 'PUERTA_0_altura': 2, 'PUERTA_0_identificador': 1, 'PUERTA_0_estaAbierta': 0, 'PUERTA_0_haciaDentro': 1, 'PUERTA_0_estaFija': 0, 'PUERTA_0_hayQueRedibujar': 0, 'PUERTA_1_orientacion': 2, 'PUERTA_1_posX': 183, 'PUERTA_1_posY': 30, 'PUERTA_1_altura': 2, 'PUERTA_1_identificador': 2, 'PUERTA_1_estaAbierta': 0, 'PUERTA_1_haciaDentro': 1, 'PUERTA_1_estaFija': 0, 'PUERTA_1_hayQueRedibujar': 0, 'PUERTA_2_orientacion': 0, 'PUERTA_2_posX': 102, 'PUERTA_2_posY': 95, 'PUERTA_2_altura': 2, 'PUERTA_2_identificador': 4, 'PUERTA_2_estaAbierta': 0, 'PUERTA_2_haciaDentro': 0, 'PUERTA_2_estaFija': 0, 'PUERTA_2_hayQueRedibujar': 0, 'PUERTA_3_orientacion': 3, 'PUERTA_3_posX': 158, 'PUERTA_3_posY': 40, 'PUERTA_3_altura': 2, 'PUERTA_3_identificador': 8, 'PUERTA_3_estaAbierta': 0, 'PUERTA_3_haciaDentro': 1, 'PUERTA_3_estaFija': 0, 'PUERTA_3_hayQueRedibujar': 0, 'PUERTA_4_orientacion': 3, 'PUERTA_4_posX': 126, 'PUERTA_4_posY': 38, 'PUERTA_4_altura': 2, 'PUERTA_4_identificador': 16, 'PUERTA_4_estaAbierta': 0, 'PUERTA_4_haciaDentro': 0, 'PUERTA_4_estaFija': 0, 'PUERTA_4_hayQueRedibujar': 0, 'PUERTA_5_orientacion': 2, 'PUERTA_5_posX': 96, 'PUERTA_5_posY': 118, 'PUERTA_5_altura': 0, 'PUERTA_5_identificador': 0, 'PUERTA_5_estaAbierta': 1, 'PUERTA_5_haciaDentro': 1, 'PUERTA_5_estaFija': 1, 'PUERTA_5_hayQueRedibujar': 0, 'PUERTA_6_orientacion': 2, 'PUERTA_6_posX': 96, 'PUERTA_6_posY': 123, 'PUERTA_6_altura': 0, 'PUERTA_6_identificador': 0, 'PUERTA_6_estaAbierta': 1, 'PUERTA_6_haciaDentro': 0, 'PUERTA_6_estaFija': 1, 'PUERTA_6_hayQueRedibujar': 0, 'OBJETO_0_orientacion': 1, 'OBJETO_0_posX': 52, 'OBJETO_0_posY': 94, 'OBJETO_0_altura': 19, 'OBJETO_0_seEstaCogiendo': 0, 'OBJETO_0_seHaCogido': 0, 'OBJETO_0_numPersonaje': 0, 'OBJETO_1_orientacion': 0, 'OBJETO_1_posX': 107, 'OBJETO_1_posY': 85, 'OBJETO_1_altura': 6, 'OBJETO_1_seEstaCogiendo': 0, 'OBJETO_1_seHaCogido': 0, 'OBJETO_1_numPersonaje': 0, 'OBJETO_2_orientacion': 0, 'OBJETO_2_posX': 0, 'OBJETO_2_posY': 0, 'OBJETO_2_altura': 0, 'OBJETO_2_seEstaCogiendo': 0, 'OBJETO_2_seHaCogido': 1, 'OBJETO_2_numPersonaje': 0, 'OBJETO_3_orientacion': 1, 'OBJETO_3_posX': 54, 'OBJETO_3_posY': 94, 'OBJETO_3_altura': 19, 'OBJETO_3_seEstaCogiendo': 0, 'OBJETO_3_seHaCogido': 0, 'OBJETO_3_numPersonaje': 0, 'OBJETO_4_orientacion': 0, 'OBJETO_4_posX': 0, 'OBJETO_4_posY': 0, 'OBJETO_4_altura': 0, 'OBJETO_4_seEstaCogiendo': 0, 'OBJETO_4_seHaCogido': 0, 'OBJETO_4_numPersonaje': 0, 'OBJETO_5_orientacion': 0, 'OBJETO_5_posX': 0, 'OBJETO_5_posY': 0, 'OBJETO_5_altura': 0, 'OBJETO_5_seEstaCogiendo': 0, 'OBJETO_5_seHaCogido': 0, 'OBJETO_5_numPersonaje': 0, 'OBJETO_6_orientacion': 0, 'OBJETO_6_posX': 53, 'OBJETO_6_posY': 53, 'OBJETO_6_altura': 19, 'OBJETO_6_seEstaCogiendo': 0, 'OBJETO_6_seHaCogido': 0, 'OBJETO_6_numPersonaje': 0, 'OBJETO_7_orientacion': 0, 'OBJETO_7_posX': 8, 'OBJETO_7_posY': 8, 'OBJETO_7_altura': 2, 'OBJETO_7_seEstaCogiendo': 0, 'OBJETO_7_seHaCogido': 0, 'OBJETO_7_numPersonaje': 0}
out2 = dict2check(dic2)
fout = open("/tmp/o3", "w")
fout.write(out2)
fout.close()


