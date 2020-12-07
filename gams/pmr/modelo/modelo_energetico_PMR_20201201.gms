$title MODELO PMR (Version 2.0, DICIEMBRE 2020, Centro Energia Universidad de Chile)


$onText
Modelo desarrollado por Centro de Energia, Facultad de Ciencias Fisicas y Matematicas, Universidad de Chile
http://www.centroenergia.cl/
http://pmr.centroenergia.cl/
Version 2.0 DICIEMBRE 2020

Prohibido su uso comercial.
La primera versión de este modelo fue financiada por el proyecto PMR Chile, Ministerio de Energia, AGCI, 2018-2019.
http://www.precioalcarbonochile.cl/

Cita:
Centro de Energia de la Universidad de Chile. Modelo Energético PMR. 2020.
Desarrolladores: Carlos Benavides, Manuel Diaz, Sebastian Gwinner, Erick Sierra, Rigoberto Torres, Rodrigo Palma.
contacto: cabenavi@centroenergia.cl

$offText
$offDigit


*Definicion de SET
*procesos/tecnologias
set i;
*productos
set k;
*sectores
set s;
*agnos
set t;
*etapas
set m;
*bloques
set b;
*flujos
set r;
*demanda
set d(k);
*energeticos
set j(k);
*set GEI
set u;
*set barras (caso generacion electrica)
set bar;
*set lineas
set l;
*set zonas con perfiles ERNC
set z;
*set offset
set of;
*set segmentos transporte
set seg;
*set de almacenamientos
set  alm(i);
*set curva de carga
set mod;
*set asociados a precios de energeticos
set jp;
*set de cap
set cap;
*set asociados a costos de inversion de procesos
set ci;
*set asociados a hidrologias
set h;
set h1(h);
set h2(h);
*set escenario
set esc;
*set escenario seleccionado
set esc_selec(esc);

*cargo set asociados a procesos
$call csv2gdx ../data_input/data_set_procesos.csv ID=test output=../data_input/data_set_procesos.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_procesos.gdx
$LOAD i=test
$gdxin
*display i;

*cargo set asociados a sectores
$call csv2gdx ../data_input/data_set_sectores.csv ID=test output=../data_input/data_set_sectores.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_sectores.gdx
$LOAD s=test
$gdxin
*display s;

*cargo set asociados a productos
$call csv2gdx ../data_input/data_set_productos.csv ID=test output=../data_input/data_set_productos.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_productos.gdx
$LOAD k=test
$gdxin
*display k;

*cargo set asociados a flujos
$call csv2gdx ../data_input/data_set_flujos.csv ID=test output=../data_input/data_set_flujos.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_flujos.gdx
$LOAD r=test
$gdxin
*display r;

*cargo set asociados a agnos
$call csv2gdx ../data_input/data_set_agnos.csv ID=test output=../data_input/data_set_agnos.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_agnos.gdx
$LOAD t=test
$gdxin
*display t;

*cargo set asociados a demandas
$call csv2gdx ../data_input/data_set_demandas.csv ID=test output=../data_input/data_set_demandas.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_demandas.gdx
$LOAD d=test
$gdxin
*display d;

*cargo set asociados a energeticos
$call csv2gdx ../data_input/data_set_energeticos.csv ID=test output=../data_input/data_set_energeticos.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_energeticos.gdx
$LOAD j=test
$gdxin
*display j;

*cargo set asociados a GEI
$call csv2gdx ../data_input/data_set_gei.csv ID=test output=../data_input/data_set_gei.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_gei.gdx
$LOAD u=test
$gdxin
*display u;

*cargo set asociados a offset
$call csv2gdx ../data_input/data_set_offset.csv ID=test output=../data_input/data_set_offset.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_offset.gdx
$LOAD of=test
$gdxin
display of;

*cargo set asociados a segmentos transporte
$call csv2gdx ../data_input/data_set_segmentos.csv ID=test output=../data_input/data_set_segmentos.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_segmentos.gdx
$LOAD seg=test
$gdxin
display seg;

*cargo set asociados a precios de energeticos
$call csv2gdx ../data_input/data_set_precios.csv ID=test output=../data_input/data_set_precios.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_precios.gdx
$LOAD jp=test
$gdxin
display jp;

*cargo set asociados a cap de emisiones
$call csv2gdx ../data_input/data_set_sec_cap.csv ID=test output=../data_input/data_set_sec_cap.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_sec_cap.gdx
$LOAD cap=test
$gdxin
display cap;

*cargo set asociados a costos de inversion de procesos
$call csv2gdx ../data_input/data_set_costo_inv_procesos.csv ID=test output=../data_input/data_set_costo_inv_procesos.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_costo_inv_procesos.gdx
$LOAD ci=test
$gdxin
*display ci;

*cargo set asociados a escenarios
$call csv2gdx ../data_input/data_set_escenarios.csv ID=test output=../data_input/data_set_escenarios.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_escenarios.gdx
$LOAD esc=test
$gdxin
display esc;

*set escenario seleccionado
$call csv2gdx ../data_input/data_set_escenario_sel.csv ID=test output=../data_input/data_set_escenario_sel.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_escenario_sel.gdx
$LOAD esc_selec=test
$gdxin
display esc_selec;

***********************************************************************************************************************************
*set especificios del sector generacion electrica

*cargo set asociados a etapas
$call csv2gdx ../data_input/data_set_etapas.csv ID=test output=../data_input/data_set_etapas.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_etapas.gdx
$LOAD m=test
$gdxin
*display m;

*cargo set asociados a bloques
$call csv2gdx ../data_input/data_set_bloques.csv ID=test output=../data_input/data_set_bloques.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_bloques.gdx
$LOAD b=test
$gdxin
*display b;

*cargo set asociados a barras
$call csv2gdx ../data_input/data_set_barras.csv ID=test output=../data_input/data_set_barras.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_barras.gdx
$LOAD bar=test
$gdxin
*display bar;

*cargo set asociados a lineas
$call csv2gdx ../data_input/data_set_lineas.csv ID=test output=../data_input/data_set_lineas.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_lineas.gdx
$LOAD l=test
$gdxin
*display l;

*cargo set asociados a zonas
$call csv2gdx ../data_input/data_set_zonas_ernc.csv ID=test output=../data_input/data_set_zonas_ernc.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_zonas_ernc.gdx
$LOAD z=test
$gdxin
*display z;

*cargo set asociados a curva de carga
$call csv2gdx ../data_input/data_set_curvas_carga.csv ID=test output=../data_input/data_set_curvas_carga.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_curvas_carga.gdx
$LOAD mod=test
$gdxin
display mod;


**********************************************************************************************************************************
*set auxiliares necesarios para la formulacion
Alias (r,rr);
Alias (i,ii);
Alias (t,tt);
Alias (b,bb)

*relacion flujos
set r1(r);
set r2(r);
set i1(i);
set r3(r);
alias (r3,r3_1);

*set auxiliares para cargar datos de precios de energeticos y costos de inversion por escenarios
set jp2(jp);
set jp3(ci);
set jp4(bar);


*set para datos
set label_sectores /ID/;
set label_productos /ID, Tipo/;
set label_procesos /ID, ID_Sector, ID_Producto, Tipo, Capacidad_Instalada, Fplanta, Estado, Agno_ini, Agno_fin, Vutil, Zona, ID_Curva, ID_Tecnologia, ID_Ener, ID_Precio_energ, ID_Costo_inversion, ConEsp, Cvar_no, Fcal, Fprecio, ID_Barra, Es_ERNC, ID_Zona_ERNC, Pmin, Regula, ConPropio, Inercia, Reserva_Primaria, Reserva_Secundaria,Impuesto, SPT, ID_Seg_Tran, Creditos /;
set label_flujos /ID_Proceso, ID_Producto, Tipo, Intensidad, Factor_Unidad/;
set label_demanda /Producto, Agno, Demanda/;
set label_energeticos /ID, ID_Producto, FConPr, FConE, FCO2, FCH4, FN20/;
set label_barras /ID/;
set label_lineas /Barra_ini, Barra_fin, Fmax, Fmin, Agno_ini, Resistencia, Reactancia, Tramos, Estado, Vutil, Inversion, COMA/;
set label_zonas_ernc /ID /;
set label_gei /ID, PCG/;
set label_offset /Offset, ID_Sector, ID_Gas, Agno_ini, Agno_fin, Abatimiento_max, Costo /;
set label_segmentos /ID/;
set label_inercia_reservas /Agno, Etapa, Bloque, Inercia_Minima, Reserva_Primaria, Factor_Reserva_Secundaria_M, Factor_Reserva_Secundaria_B, ID_Tecnologia/;
set label_mod /ID/;
set label_precios /ID/;
set label_cap /ID/;
set label_demanda_sec /Demanda,ID,ID_Curva/;
set label_costo_inversion /ID/;


*cargo datos sectores
Table datos_sectores(s,label_sectores) 'datos sectores'
$ondelim
$include ../data_input/data_sectores.csv
$offdelim
;
*display datos_sectores;

*cargo datos productos
Table datos_productos(k,label_productos) 'datos productos'
$ondelim
$include ../data_input/data_productos.csv
$offdelim
;
*display datos_productos;


*cargo datos procesos
Table datos_procesos(i,label_procesos) 'datos procesos'
$ondelim
$include ../data_input/data_procesos.csv
$offdelim
;
display datos_procesos;

*cargo datos energeticos
Table datos_energeticos(j,label_energeticos) 'datos energeticos'
$ondelim
$include ../data_input/data_energeticos.csv
$offdelim
;
*display datos_energeticos;

*cargo datos flujos
$onEmpty
Table datos_flujos(r,label_flujos) 'datos flujos'
$ondelim
$include ../data_input/data_flujos.csv
$offdelim
;
$offEmpty
*display datos_flujos;

*cargo datos demanda
$call csv2gdx ../data_input/data_demanda_sectorial.csv ID=test output=../data_input/data_demanda_sectorial.gdx  Index=1,2 values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_demanda_sectorial.gdx
parameter demanda(d,t);
$LOAD demanda=test
$gdxin
*display demanda;

*cargo datos precio de combustibles
$call csv2gdx ../data_input/data_precio_energeticos.csv ID=test output=../data_input/data_precio_energeticos.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_precio_energeticos.gdx
parameter precio_energetico_aux(jp,t)
$LOAD precio_energetico_aux=test
$gdxin
display precio_energetico_aux;

*cargo datos precio de combustibles por escenarios
$call csv2gdx ../data_input/data_precio_energeticos_escenarios.csv ID=test output=../data_input/data_precio_energeticos_esc.gdx  Index=1,2,3 Values=4 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_precio_energeticos_esc.gdx
$LOAD jp2=Dim3
parameter precio_energetico_esc(esc,t,jp2)
$LOAD precio_energetico_esc=test
$gdxin
display precio_energetico_esc;

*cargo datos relacion entre flujos
$call csv2gdx ../data_input/data_relacion_flujos.csv ID=test output=../data_input/data_relacion_flujos.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_relacion_flujos.gdx
parameter data_relacion(r1,r2)
$LOAD r1=Dim1
$LOAD r2=Dim2
$LOAD data_relacion=test
$gdxin
*display data_relacion;

*cargo datos participacion flujos
$call csv2gdx ../data_input/data_participacion_flujos.csv ID=test output=../data_input/data_participacion_flujos.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_participacion_flujos.gdx
parameter data_participacion(i1,r3)
$LOAD i1=Dim1
$LOAD r3=Dim2
$LOAD  data_participacion=test
$gdxin
*display data_participacion;

*cargo datos de factores de emision
$call csv2gdx ../data_input/data_fe.csv ID=test output=../data_input/data_fe.gdx  Index=1,2,3 Values=4 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_fe.gdx
parameter data_fe(s,j,u)
$LOAD  data_fe=test
$gdxin
*display data_fe;

*cargo datos de cap de emisiones
set u1(u);
$call csv2gdx ../data_input/data_cap.csv ID=test output=../data_input/data_cap.gdx  Index=1,2,3 Values=4 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_cap.gdx
parameter data_cap(cap,u1,t)
$LOAD u1=Dim2
$LOAD  data_cap=test
$gdxin
*display data_cap;

*cargo datos de impuesto de emisiones
$call csv2gdx ../data_input/data_impuesto.csv ID=test output=../data_input/data_impuesto.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_impuesto.gdx
parameter data_impuesto(u,t)
$LOAD  data_impuesto=test
$gdxin
*display data_impuesto;

*cargo datos de costos de inversion de tecnologias
$call csv2gdx ../data_input/data_costo_inversion.csv ID=test output=../data_input/data_costo_inversion.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_costo_inversion.gdx
parameter data_cinversion_old(i,t)
$LOAD  data_cinversion_old=test
$gdxin
*display data_cinversion_old;

*cargo datos costo de inversion procesos por escenarios
$call csv2gdx ../data_input/data_costo_inversion_procesos_escenarios.csv ID=test output=../data_input/data_costo_inversion_procesos_escenarios.gdx  Index=1,2,3 Values=4 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_costo_inversion_procesos_escenarios.gdx
$LOAD jp3=Dim3
parameter costo_inversion_esc(esc,t,jp3)
$LOAD costo_inversion_esc=test
$gdxin
display costo_inversion_esc;

*cargo datos de costos de operacion y mantenimiento anual
$call csv2gdx ../data_input/data_coma.csv ID=test output=../data_input/data_coma.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_coma.gdx
parameter data_coma(i,t)
$LOAD  data_coma=test
$gdxin
*display data_coma;


*cargo datos de potencia maxima instalada
set ipmax(i);
parameter data_pmax(i,t);
parameter data_pmax_aux(i,t);
$call csv2gdx ../data_input/data_pmax.csv ID=test output=../data_input/data_pmax.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_pmax.gdx
$LOAD ipmax=Dim1
$LOAD  data_pmax_aux=test
$gdxin
*valor por defecto en caso que no se ingresen datos
data_pmax(i,t)=1000000000;
*valor actualiazado por dato de entrada
data_pmax(ipmax,t)=data_pmax_aux(ipmax,t);


*cargo datos de potencia minima instalada
set ipmin(i);
parameter data_pmin(i,t);
parameter data_pmin_aux(ipmin,t);
$call csv2gdx ../data_input/data_pmin.csv ID=test output=../data_input/data_pmin.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_pmin.gdx
$LOAD ipmin=Dim1
$LOAD  data_pmin_aux=test
$gdxin
*valor por defecto en caso que no se ingresen datos
display data_pmin_aux;
data_pmin(i,t)=0;
data_pmin(ipmin,t)=data_pmin_aux(ipmin,t);
display data_pmin;

*cargo datos de gases de efecto invernadero
Table datos_gei(u,label_gei) 'datos GEI'
$ondelim
$include ../data_input/data_gei.csv
$offdelim
;
*display datos_gei;

*cargo datos offset
$onEmpty
Table data_offset(of,label_offset) 'datos OFFSET'
$ondelim
$include ../data_input/data_offset.csv
$offdelim
;
$offEmpty
*display datos_offset;


*cargo datos para limitar la cantitidad de offset
$call csv2gdx ../data_input/data_limite_offset.csv ID=test output=../data_input/data_limite_offset.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_limite_offset.gdx
parameter data_limite_offset(u1,t)
$LOAD  data_limite_offset=test
$gdxin

*cargo datos de metas de eficiencia energetica para transporte
$call csv2gdx ../data_input/data_meta_ee.csv ID=test output=../data_input/data_meta_ee.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_meta_ee.gdx
parameter data_meta_ee(seg,t)
$LOAD  data_meta_ee=test
$gdxin
display data_meta_ee;


*cargo datos segmentos metas de EE para transporte
$onEmpty
Table datos_segmentos(seg,label_segmentos) 'datos segmento'
$ondelim
$include ../data_input/data_segmentos.csv
$offdelim
;
display datos_segmentos;
$offEmpty

*cargo datos precios de energeticos
Table datos_precios(jp,label_precios) 'datos precio energeticos'
$ondelim
$include ../data_input/data_precios.csv
$offdelim
;
display datos_precios;

*cargo datos sectores cap
Table datos_sec_cap(cap,label_cap) 'datos cap por sector'
$ondelim
$include ../data_input/data_sec_cap.csv
$offdelim
;
display datos_sec_cap;

*cargo datos de demanda sectorial
$onEmpty
Table datos_demanda(d,label_demanda_sec) 'datos demanda sectorial'
$ondelim
$include ../data_input/data_demanda.csv
$offdelim
;
display datos_demanda;
$offEmpty

*cargo factor de distribucion de demanda sectorial por etapas
$call csv2gdx ../data_input/data_dem_sec_etapa.csv ID=test output=../data_input/data_dem_sec_etapa.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_dem_sec_etapa.gdx
parameter datos_dem_sec_etapa(d,m);
$LOAD datos_dem_sec_etapa=test
$gdxin
display datos_dem_sec_etapa;

*cargo factor de distribucion de demanda sectorial por etapas
$call csv2gdx ../data_input/data_retiro_veh.csv ID=test output=../data_input/data_retiro_veh.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_retiro_veh.gdx
parameter datos_retiro(i,t);
$LOAD datos_retiro=test
$gdxin
display datos_retiro;

*cargo datos costos de inversion
Table datos_costo_inversion(ci,label_costo_inversion) 'datos costos inversion procesos'
$ondelim
$include ../data_input/data_costo_inv_procesos_id.csv
$offdelim
;
display datos_costo_inversion;

*cargo datos de costos de inversion de procesos
$call csv2gdx ../data_input/data_costo_inversion_procesos.csv ID=test output=../data_input/data_costo_inversion_procesos.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_costo_inversion_procesos.gdx
parameter costo_inv_proc_aux(ci,t)
$LOAD costo_inv_proc_aux=test
$gdxin
display costo_inv_proc_aux;


************************************************************************************************************************************
*datos especificos del sector generacion electrica

*cargo datos de duracion de bloques
$call csv2gdx ../data_input/data_duracion.csv ID=test output=../data_input/data_duracion.gdx  Index=1,2,3 Values=4 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_duracion.gdx
parameter data_duracion(t,m,b)
$LOAD  data_duracion=test
$gdxin
*display data_duracion;

*cargo datos de demanda
$call csv2gdx ../data_input/data_demanda_electrica.csv ID=test output=../data_input/data_demanda_electrica.gdx  Index=1,2,3,4 Values=5 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_demanda_electrica.gdx
parameter data_demanda_el(bar,t,m,b)
$LOAD  data_demanda_el=test
$gdxin
*display data_demanda_el;


*cargo datos de demanda electrica por escenarios
$call csv2gdx ../data_input/data_demanda_electrica_escenarios.csv ID=test output=../data_input/data_demanda_electrica_escenarios.gdx  Index=1,2,3,4,5 Values=6 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_demanda_electrica_escenarios.gdx
$LOAD jp4=Dim2
parameter data_demanda_el_esc(esc,jp4,t,m,b)
$LOAD  data_demanda_el_esc=test
$gdxin
display  data_demanda_el_esc;


*cargo perfiles ERNC
$call csv2gdx ../data_input/data_perfil_ernc.csv ID=test output=../data_input/data_perfil_ernc.gdx  Index=1,2,3,4 Values=5 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_perfil_ernc.gdx
parameter data_fp_aux(z,t,m,b)
$LOAD  data_fp_aux=test
$gdxin
*display data_fp;

*cargo datos barras
Table datos_barras(bar,label_barras) 'datos barras' 
$ondelim
$include ../data_input/data_barras.csv
$offdelim
;
*display datos_barras;

*cargo datos lineas
$onEmpty
Table datos_lineas(l,label_lineas) 'datos lineas' 
$ondelim
$include ../data_input/data_lineas.csv
$offdelim
;
*display datos_lineas;
$offEmpty

*cargo datos zonas con perfiles ERNC
Table datos_zonas(z,label_zonas_ernc) 'datos zonas ernc'
$ondelim
$include ../data_input/data_zonas_ernc.csv
$offdelim
;
*display datos_zonas;

*cargo factores de planta de centrales
parameter fplanta(i,t,m);
*valor por defecto
fplanta(i,t,m)=1;

*lectura cambiada con version 20201201
*set ifp(i);
*$call csv2gdx ../data_input/data_factor_planta.csv ID=test output=../data_input/data_factor_planta.gdx  Index=1,2,3 Values=4 UseHeader=Y StoreZero=Y
*$gdxin ../data_input/data_factor_planta.gdx
*parameter fplanta_aux(ifp,t,m);
*$LOAD ifp=Dim1
*$LOAD  fplanta_aux=test
*$gdxin
*display fplanta_aux;
*actualizo valores de factor de planta
*fplanta(ifp,t,m) = fplanta_aux(ifp,t,m);
*display fplanta;


*cargo factor de distribucion de demanda por barra
set aux3;
$call csv2gdx ../data_input/data_dem_distr_barra.csv ID=test output=../data_input/data_dem_distr_barra.gdx  Index=1,2 Values=3,4 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_dem_distr_barra.gdx
$LOAD aux3=Dim3
parameter datos_dem_bar(i,bar,aux3);
$LOAD datos_dem_bar=test
$gdxin
display datos_dem_bar;


*cargo factor de distribucion de demanda por etapas
$call csv2gdx ../data_input/data_dem_distr_etapa.csv ID=test output=../data_input/data_dem_distr_etapa.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_dem_distr_etapa.gdx
parameter datos_dem_etapa(i,m);
$LOAD datos_dem_etapa=test
$gdxin
display datos_dem_etapa;

*cargo factor de modulacion de demanda por bloques
$call csv2gdx ../data_input/data_dem_distr_bloque.csv ID=test output=../data_input/data_dem_distr_bloque.gdx  Index=1,2,3 Values=4 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_dem_distr_bloque.gdx
parameter datos_dem_bloque(mod,m,b);
$LOAD datos_dem_bloque=test
$gdxin
display datos_dem_bloque;

*cargo datos de curva de carga
Table datos_mod(mod,label_mod) 'datos curva de carga'
$ondelim
$include ../data_input/data_curvas_carga.csv
$offdelim
;

*cargo set asociados a almacenamiento
$call csv2gdx ../data_input/data_set_almacenamientos.csv ID=test output=../data_input/data_set_almacenamientos.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_set_almacenamientos.gdx
$LOAD alm=test
$gdxin
*display alm;

*leer datos_almacenamiento y perfil_almacenamiento
$call csv2gdx ../data_input/data_almacenamientos.csv ID=test output=../data_input/data_almacenamientos.gdx  Index=1 Values=2 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_almacenamientos.gdx
parameter datos_almacenamientos(alm);
$LOAD  datos_almacenamientos=test
$gdxin
*display datos_almacenamientos;

$call csv2gdx ../data_input/data_perfil_almacenamiento.csv ID=test output=../data_input/data_perfil_almacenamiento.gdx  Index=1,2,3,4 Values=5 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_perfil_almacenamiento.gdx
parameter perfil_almacenamiento(alm,t,m,b);
$LOAD perfil_almacenamiento=test
$gdxin
*display perfil_almacenamiento;

*cargo datos hidrologias
$call csv2gdx ../data_input/data_hidrologias.csv ID=test output=../data_input/data_hidrologias.gdx  Index=1 Values=2 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_hidrologias.gdx
$LOAD h=Dim1
parameter data_hidrologias(h)
$LOAD data_hidrologias=test
$gdxin
display data_hidrologias;


*cargo datos hidrologia planificacion
$call csv2gdx ../data_input/data_hidrologias_planificacion.csv ID=test output=../data_input/data_hidrologias_planificacion.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_hidrologias_planificacion.gdx
$LOAD h1=Dim1
display h1;

*cargo datos hidrologia simulacion
$call csv2gdx ../data_input/data_hidrologias_simulacion.csv ID=test output=../data_input/data_hidrologias_simulacion.gdx  Index=1 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_hidrologias_simulacion.gdx
$LOAD h2=Dim1
display h2;

*cargo dato hidrologias
set ifp(i);
$call csv2gdx ../data_input/data_factor_planta.csv ID=test output=../data_input/data_factor_planta.gdx  Index=1,2,3 Values=4 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_factor_planta.gdx
parameter fplanta_aux(ifp,h,m);
$LOAD ifp=Dim1
$LOAD  fplanta_aux=test
$gdxin
*display fplanta_aux;
*actualizo valores de factor de planta
loop (h1, fplanta(ifp,t,m) = fplanta_aux(ifp,h1,m));
display fplanta;

************************************************************************************************************************************

parameter factor(t);
parameter agno(t);
parameter cinv_a(i,t);
parameter precio_energetico(r,t);
parameter precio_energetico_ge(i,t);
parameter datos_dem_etapa_aux(i,m,b);
parameter datos_dem_etapa_aux2(r,bar,m,b);
parameter datos_dem_sec(d,m,b);

Scalar
*factor para transformar Tcal a MWh
factor_unidad /1163/
*tasa de descuento
tasa_descuento /0.06/
*agno inicio simulacion
tbase /2017/
*costo falla procesos
factor_falla /1000/;

*opcion para calcular los costos marginales sin el efecto del impuesto.
*flag = 1 si no afecta costos marginales
*flag = 0 si afecta los costos marginales
*flag = 2 si el impuesto se calcula como se hace actualmente
scalar flag /0/;

*opcion para resolver modelo integrado de generacion y demanda, 0 caso no integrado, 1 caso integrado generacion=demanda
scalar flag_integ /0/;

*SELECCION DE ESCENARIOS*****************

*asigno costo de inversion a procesos
parameter data_cinversion(i,t);
loop ((i,ci)$(datos_procesos(i,"ID_Costo_inversion")=datos_costo_inversion(ci,"ID")),data_cinversion(i,t)=costo_inv_proc_aux(ci,t));
display data_cinversion;

*selecciono escenario de costo de inversion
loop ((esc_selec,i,jp3)$(datos_procesos(i,"ID_Costo_inversion")=datos_costo_inversion(jp3,"ID")),data_cinversion(i,t)=costo_inversion_esc(esc_selec,t,jp3));

*costo de inversion anualizado
cinv_a(i,t)=data_cinversion(i,t)*tasa_descuento*(1+tasa_descuento)**(datos_procesos(i,"Vutil"))/((1+tasa_descuento)**datos_procesos(i,"Vutil")-1);
display cinv_a;


*asigno precio de combustibles a procesos
loop ((i,jp,r)$(datos_procesos(i,"ID_Precio_energ")=datos_precios(jp,"ID") and datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso")),precio_energetico(r,t)=precio_energetico_aux(jp,t));
loop ((i,jp)$(datos_procesos(i,"ID_Precio_energ")=datos_precios(jp,"ID")),precio_energetico_ge(i,t)=precio_energetico_aux(jp,t));
display precio_energetico_ge;

*selecciono escenario de precio
loop ((esc_selec,i,jp2)$(datos_procesos(i,"ID_Precio_energ")=datos_precios(jp2,"ID")),precio_energetico_ge(i,t)=precio_energetico_esc(esc_selec,t,jp2));
display precio_energetico_ge;

*selecciono escenario demanda electrica
loop ((esc_selec,jp4),data_demanda_el(jp4,t,m,b)=data_demanda_el_esc(esc_selec,jp4,t,m,b));
display data_demanda_el;

*FIN SELECCION DE ESCENARIOS********************


*factor para traer a valor presente los costos
factor(t)=(1+tasa_descuento)**(-(ord(t)-1));
agno(t)=ord(t)-1+tbase;
*display factor;
*display tasa_descuento;
*display tbase;
*display agno;
*display cinv_a;

Scalar
id_generacion;
id_generacion= datos_sectores('generacion_electrica',"ID");
*display id_generacion;

Scalar
id_electricidad;
id_electricidad= datos_productos('electricidad',"ID");
display id_electricidad;

*calculo demanda auxiliar por etapa y bloque
datos_dem_etapa_aux2(r,bar,m,b)=0;
loop ((i,mod) $(datos_procesos(i,"ID_Curva")=datos_mod(mod,"ID")),datos_dem_etapa_aux(i,m,b)=datos_dem_etapa(i,m)*datos_dem_bloque(mod,m,b));
loop ((i,r) $(datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and  datos_flujos(r,"ID_Producto")=id_electricidad),datos_dem_etapa_aux2(r,bar,m,b)=datos_dem_bar(i,bar,'Participacion')*datos_dem_etapa_aux(i,m,b)*(1+datos_dem_bar(i,bar,'Perdidas')));

loop ((d,mod) $(datos_demanda(d,"ID_Curva")=datos_mod(mod,"ID")),datos_dem_sec(d,m,b)=datos_dem_sec_etapa(d,m)*datos_dem_bloque(mod,m,b));

*calculo factor de planta por bloque
parameter data_fp(i,t,m,b);
parameter flag_fp(i);
loop((i,z)$(datos_procesos(i,"ID_zona_ERNC")=datos_zonas(z,"ID")),
flag_fp(i)=1;
data_fp(i,t,m,b)=data_fp_aux(z,t,m,b));

*factor de emision auxiliar
*parameter factor_emision_aux(r,u);
*loop ((s,i,r,k,j,u) $(datos_procesos(i,"ID_Sector")=datos_sectores(s,"ID") and datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and datos_flujos(r,"ID_Producto")=datos_productos(k,"ID") and datos_productos(k,"ID")=datos_energeticos(j,"ID_Producto")),factor_emision_aux(r,u)=datos_energeticos(j,"FConE")*data_fe(s,j,u));
*display factor_emision_aux;

$call csv2gdx ../data_input/factor_emision_aux.csv ID=test output=../data_input/factor_emision_aux.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/factor_emision_aux.gdx
parameter factor_emision_aux(r,u)
$LOAD  factor_emision_aux=test
$gdxin
display factor_emision_aux;

*factor de emision auxiliar para centrales de generacion
*parameter factor_emision_ge_aux(i,u);
*loop ((s,i,j,u) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"ID_Sector")=datos_sectores(s,"ID") and datos_procesos(i,"ID_Ener")=datos_energeticos(j,"ID")),factor_emision_ge_aux(i,u)=datos_procesos(i,"ConEsp")*datos_procesos(i,"Fcal")*datos_energeticos(j,"FConE")*data_fe(s,j,u));
*display factor_emision_ge_aux;

$call csv2gdx ../data_input/factor_emision_ge_aux.csv ID=test output=../data_input/factor_emision_ge_aux.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/factor_emision_ge_aux.gdx
parameter factor_emision_ge_aux(i,u)
$LOAD  factor_emision_ge_aux=test
$gdxin
display factor_emision_ge_aux;

*Calculo de Flujo de energia minimo en funcion de P_min
*parameter F_min(r,t)         'flujo_minimo';
*loop((i,r) $(datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and datos_flujos(r,"Tipo")=2),F_min(r,t)=0+(data_pmin(i,t)*datos_procesos(i,"Fplanta")/datos_flujos(r,"Factor_Unidad"))$(data_pmin(i,t)>0));
*display F_min;

*restriccion de angulo de fase
Alias (bar,bari,barj);

*activar/desactivar perdidas
parameter ActivateLosses;
ActivateLosses = 1;
*factor de penalizacion de las perdidas de transmision
parameter PFL;
PFL = 10**(-6);
*porcentaje perdidas
parameter f_perdidas(l);
f_perdidas(l) = (ActivateLosses = 1) * datos_lineas(l,"Resistencia"); 
*costo de inversion anualizado
parameter cinv_a_tx(l);
*calculo de costo de inversion anualizado
cinv_a_tx(l)=datos_lineas(l,"Inversion")*tasa_descuento*(1+tasa_descuento)**(datos_lineas(l,"Vutil"))/((1+tasa_descuento)**datos_lineas(l,"Vutil")-1);
*parametro auxiliar para representar restricciones de sistema de Tx
parameter bigM;
bigM = 10**9;

*duracion etapas
parameter DurEta(t,m);
DurEta(t,m) = sum(b,data_duracion(t,m,b));

*costo inversion almacenamientos ($ / kWh)
parameter cinv_alm_a(alm,t);

*cargo datos de costos de inversion de almacenamientos
$call csv2gdx ../data_input/data_costo_inv_almacenamientos.csv ID=test output=../data_input/data_costo_inv_almacenamientos.gdx  Index=1,2 Values=3 UseHeader=Y StoreZero=Y
$gdxin ../data_input/data_costo_inv_almacenamientos.gdx
parameter data_cinversion_alm(alm,t);
$LOAD  data_cinversion_alm=test
$gdxin
*display data_cinversion;

*calculo de costo de inversion anualizado
cinv_alm_a(alm,t) = data_cinversion_alm(alm,t)*tasa_descuento*(1+tasa_descuento)**(datos_procesos(alm,"Vutil"))/((1+tasa_descuento)**datos_procesos(alm,"Vutil")-1);

*cargo datos inercia y reservas
Table datos_inercia_reservas(t, m, b, label_inercia_reservas) 'datos inercia y reservas'
$ondelim
$include ../data_input/data_inercia_reservas.csv
$offdelim
;
display datos_inercia_reservas;

*flag para flujos anuales que son desagregados por bloques
parameter flag_restr_b(r);
loop ((d,mod,r) $(datos_demanda(d,"ID_Curva")=datos_mod(mod,"ID") and datos_flujos(r,"ID_Producto")=datos_productos(d,"ID")), flag_restr_b(r)=1);

*presupuesto de emisiones
parameter presupuesto;
parameter ini_presupuesto;
parameter fin_presupuesto;
*numero grande significa que no tiene restriccion
presupuesto = 100000; 
ini_presupuesto =2020;
fin_presupuesto =2050;

**********************************************************************************************************************
*Modelo de optimizacion

Variable
    F(r,t)             'flujo asociado a cada proceso'
    Fb(r,t,m,b)        'flujo asociado a cada proceso para cada agno, etapa y bloque'
    P(i,t)             'potencia nueva instalada asociada a cada proceso'
    GEI_IND(cap,u,t)   'emisiones sector industria y mineria y otros sectores- variable auxliar'
    OFFSET(of,t)       'offset de emisiones'
    demanda_falla(d,t) 'variable de holgura'
    demanda_falla_b(d,t,m,b) 'variable de holgura por bloque'
    c_falla            'costo de no satisfacer demanda'
    c_falla_b          'costo de no satisfacer demanda por bloque'
    c_operacion        'costo operacion'
    c_inversion        'costo inversion'
    c_coma             'costo de operacion y mantenimiento anual'
    c_impuesto         'costo impuesto'
    c_offset           'costo offset'
    costo              'funcion objetivo'
    costo_sin_impuesto 'funcion objetivo sin impuesto';
  
*variables especificas del sector generacion electrica
Variables
    Ge(i,t,m,b)        'potencia media (MW)'
    Fp(l,t,m,b)        'flujo positivo por linea'
    Fn(l,t,m,b)        'flujo positivo por linea'
    Ph(bar,t,m,b)      'angulo de fase barra'
    Reserva(i,t,m,b)   'Reserva Primaria aportada por la central i'
    Res_P(i,t,m,b)     'Reserva Primaria aportada por la central i'
    Res_S(i,t,m,b)     'Reserva Secundaria aportada por la central i'
    Requisito_Res_S(t,m,b)   'requisito de reserva secundaria'
    dem_bar(bar,t,m,b) 'demanda electrica por barra'
    c_impuesto_ge      'costo impuesto'
    c_operacion_ge     'costo operacion'
    c_inversion_ge     'costo inversion'
    c_coma_ge          'costo de operacion y mantenimiento anual'
    c_perdidas         'costo de perdidas de energia'
    c_inversion_tx     'costo de inversion en transmision'
    c_coma_tx          'costo operacion y mantenimiento anual transmision'
    c_inversion_alm    'costo de inversion en sistema de almacenamiento'; 
    
Binary Variable
    Instalar_LT(l,t)   'decision de instalar LT';

Binary Variable
    OnOff(i,t,m,b)     'decision de encendido/apagado de central';
    
*cota de variables
F.lo(r,t) = 0;
Fb.lo(r,t,m,b) = 0;
*restriccion de potencia minina
P.lo(i,t) = data_pmin(i,t);
*cota generacion minima por defecto
Ge.lo(i,t,m,b) = 0;
*cotas flujos por lineas de Tx
Fp.lo(l,t,m,b)=0;
Fp.up(l,t,m,b)=datos_lineas(l,"Fmax");
Fn.lo(l,t,m,b)=datos_lineas(l,"Fmin");
Fn.up(l,t,m,b)=0;
*cotas desfases angulares
Ph.up(bar,t,m,b)=2*Pi;
Ph.lo(bar,t,m,b)=-2*Pi;
*cotas offset
OFFSET.up(of,t)=0+data_offset(of,"Abatimiento_max")$(agno(t)>=data_offset(of,"Agno_ini")and agno(t)<=data_offset(of,"Agno_fin"));
OFFSET.lo(of,t)=0;
*costas variables de fallas
demanda_falla.lo(d,t)=0;
demanda_falla_b.lo(d,t,m,b)=0;

*redefinir los bounds para la generacion de los almacenamientos
Ge.lo(alm,t,m,b) = - Inf;

* establecer bounds para las reservas
Res_P.up(i,t,m,b)=datos_procesos(i,"Reserva_Primaria");
Res_P.lo(i,t,m,b)=0;
Res_S.up(i,t,m,b)=datos_procesos(i,"Reserva_Secundaria");
Res_S.lo(i,t,m,b)=0;  

*restricciones de problema de optimizacion
Equation
   balance_proceso(i,t)                 'balance salida/entrada para cada proceso'
   balance_demanda(d,t)                 'balance demanda'
   balance_demanda_bloque(d,mod,t,m,b)  'balance demanda por bloque'
   relacion_flujo_bloque(r,t)           'relacion entre flujos por bloques y flujo anual'
   relacion_flujos(r1,t)                'relacion flujos'
   participacion_flujos(i1,r3,t)        'participacion flujos'
   produccion_maxima(i,t)               'produccion maxima proceso'
   max_inversion(i,r,t)                 'maxima inversion por agno'
   condicion_ini_inversion(i,r,t)       'agno entrada nueva inversion'
   condicion_log_potencia(i,r,t)        'condicion logica potencia'
   limite_emisiones_industria(cap,u1,t) 'cap de emisiones por gas para sector industria y otros sectores'
   limite_emisiones(cap,u1,t)           'cap de emisiones por gas'
   limite_offset(u1,t)                  'limite maximo offset'
   presupuesto_emisiones                'presupuesto de emisiones'    
   costo_operacion                      'costo_operacion'
   costo_inversion                      'costo_inversion'
   costo_coma                           'coma'
   costo_impuesto                       'costo_impuesto'
   costo_offset                         'costo_offset'
   costo_total                          'funcion objetivo'
   costo_total_sin_impuesto             'funcion objetivo sin considerar impuesto a las emisiones de GEI'
   costo_falla                          'costo falla'
   costo_falla_b                        'costo falla por bloque'
   balance_flujo_min(i,t)               'relacion de flujos minimo y potencia minima del proceso';

Equation
   flujo_maximo_bloque(i,t,m,b)         'flujo maximo por bloque' 
;

*sector generacion electrica
Equation
    balance_generacion_demanda(bar,t,m,b)   'balance generacion demanda'
    generacion_maxima_ERNC(i,z,t,m,b)       'cota maxima de generacion ERNC'
    generacion_maxima(i,t,m,b)              'cota maxima de generacion'
    generacion_maxima_etapa(ifp,t,m)        'generacion maxima por etapa'
    max_inversion_ge(i,t)                   'maxima inversion por agno'
    condicion_log_potencia_ge(i,t)          'condicion logica potencia instalada'
    modula(i,t,m,b,bb)                      'capacidad de modulacion de generacion para bloques de una misma etapa'
    angulo_fase_up(bar,bar,l,t,m,b)         'restriccion de angulo de fase'
    angulo_fase_lo(bar,bar,l,t,m,b)         'restriccion de angulo de fase'
    flujo_maximo_tx(l,t,m,b)                'flujo maximo por LT'
    flujo_minimo_tx(l,t,m,b)                'flujo minimo por LT'
    condicion_log_fmax(l,t)                 'condicion logica de flujo maximo'
    condicion_ini_inversion_tx(l,t)         'agno de inicio inversiones tx'
    limitar_almacenamiento(alm,t,m,b)       'limitar generacion almacenamiento por bloque'
    Minimo_Tecnico_up(i,t,m,b)              'restriccion de central operando a minimo tecnico'
    Minimo_Tecnico_dn(i,t,m,b)              'restriccion de central operando a minimo tecnico'
    Inercia_Minima_Sistema(t,m,b)           'requisito de inercia minima rotante del sistema'
    Reserva_Secundaria(t,m,b)               'calculo del requisito de reserva secundaria'
    Control_Frecuencia(t,m,b)               'incorporar al despacho el requisito de reservas primaria y secundaria'
    demanda_barra(bar,t,m,b)                'demanda electrica por bloque'
    costo_perdidas                          'costo perdidas de energia'
    costo_inversion_tx                      'costo inversion tx'
    costo_coma_tx                           'costo operacion y manteminiento tx'
    costo_inversion_alm                     'costo inversion sistema almacenamiento'
    costo_impuesto_ge                       'costo_impuesto asociado a emisiones del sector generacion electrica'
    costo_operacion_ge                      'costo_operacion sector generacion electrica'
    ;

*restriccion propia del sector transporte
Equation
    meta_ee_transp(t,seg)                   'restriccion de eficiencia energetica';


*restricciones generales

*balance produccion=demanda'*
balance_demanda(d,t)..  sum(r $(datos_flujos(r,"ID_Producto")=datos_productos(d,"ID")), F(r,t)) =e= demanda(d,t)-demanda_falla(d,t);

*balance produccion=demanda por bloque'
balance_demanda_bloque(d,mod,t,m,b)$(datos_demanda(d,"ID_Curva")=datos_mod(mod,"ID")).. sum(r $(datos_flujos(r,"ID_Producto")=datos_productos(d,"ID")), Fb(r,t,m,b)) =e= demanda(d,t)*datos_dem_sec(d,m,b)-demanda_falla_b(d,t,m,b);

*modulacion flujos por bloques
flujo_maximo_bloque(i,t,m,b) $(datos_procesos(i,"ID_sector")<>id_generacion and flag_fp(i)=1).. sum(r $(datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and datos_flujos(r,"Tipo")=2),Fb(r,t,m,b)*datos_flujos(r,"Factor_Unidad")) =l=  (datos_procesos(i,"Capacidad_Instalada")*data_fp(i,t,m,b)*data_duracion(t,m,b))$(datos_procesos(i,"Estado")=1 and agno(t)<=datos_procesos(i,"Agno_fin"))+(P(i,t)*data_fp(i,t,m,b)*data_duracion(t,m,b))$(datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"));

*relacion flujo por bloques con flujo anual
relacion_flujo_bloque(r,t) $(flag_restr_b(r)=1).. sum((m,b),Fb(r,t,m,b)) =e= F(r,t);

*balance output-input para cada proceso
balance_proceso(i,t) $(datos_procesos(i,"ID_sector")<>id_generacion)..   sum(r $(datos_flujos(r,"Tipo")=2 and datos_flujos(r,"ID_Proceso")=datos_procesos(i,"ID")),F(r,t)) -  (sum(r $(datos_flujos(r,"Tipo")=2 and datos_flujos(r,"ID_Proceso")=datos_procesos(i,"ID")),datos_flujos(r,"Intensidad"))/sum(r $(datos_flujos(r,"Tipo")=2 and datos_flujos(r,"ID_Proceso")=datos_procesos(i,"ID")),1))*(sum(rr $(datos_flujos(rr,"ID_Proceso")=datos_procesos(i,"ID") and datos_flujos(rr,"Tipo")=1),F(rr,t))) =e=0;

*relacion entre flujos
relacion_flujos(r1,t).. F(r1,t)-sum(r2,data_relacion(r1,r2)*F(r2,t)) =e=0;


*flujo minimo del proceso
balance_flujo_min(i,t) $(datos_procesos(i,"ID_sector")<>id_generacion and data_pmin(i,t)>0)..  sum(r $(datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and datos_flujos(r,"Tipo")=2),F(r,t)*datos_flujos(r,"Factor_Unidad"))=g=(data_pmin(i,t)*datos_procesos(i,"Fplanta"));

*participacion flujos de entrada

*participacion flujos de entrada
participacion_flujos(i1,r3,t) $(data_participacion(i1,r3)>0).. F(r3,t)-data_participacion(i1,r3)*sum(r3_1 $(data_participacion(i1,r3_1)>0),F(r3_1,t)) =e=0;

*capacidad maxima
produccion_maxima(i,t) $(datos_procesos(i,"ID_sector")<>id_generacion).. sum(r $(datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and datos_flujos(r,"Tipo")=2),F(r,t)*datos_flujos(r,"Factor_Unidad")) =l=  (datos_procesos(i,"Capacidad_Instalada")*datos_procesos(i,"Fplanta"))$(datos_procesos(i,"Estado")=1 and agno(t)<=datos_procesos(i,"Agno_fin"))+(P(i,t)*datos_procesos(i,"Fplanta"))$(datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"));

*condicion logica de potencia instalada
condicion_log_potencia(i,r,t) $(datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and datos_flujos(r,"Tipo")=2 and ord(t)>1 and agno(t)<=datos_procesos(i,"Agno_fin")) .. P(i,t-1)-P(i,t) =l=0;

*agno entrada nueva inversiones
condicion_ini_inversion(i,r,t) $(datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and datos_flujos(r,"Tipo")=2 and ord(t)>0 and datos_procesos(i,"Agno_ini")>agno(t)) .. P(i,t) =e=0;

*maxima inversion por agno
max_inversion(i,r,t) $(datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and datos_flujos(r,"Tipo")=2 and ord(t)>1) .. P(i,t) =l=data_pmax(i,t);

*emisiones sector industrial y otros sectores
limite_emisiones_industria(cap,u1,t).. GEI_IND(cap,u1,t) =e= sum((i,r) $(datos_procesos(i,"SPT")=datos_sec_cap(cap,"ID") and datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso")),F(r,t)*factor_emision_aux(r,u1)*10**(-9));

*restriccion de meta de eficiencia energetica vehiculos nuevos
*meta_ee_transp(t,seg).. sum((i,r) $(datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and datos_procesos(i,"ID_Segmento_Tran")=datos_segmentos(seg,"ID")),(P(i,t)-P(i,t-1)+datos_retiro_vehiculos(i,t))*datos_flujos(r,"Intensidad") = ge = sum(i,(P(i,t)-P(i,t-1)+datos_retiro_vehiculos(i,t))*data_meta_ee(seg,t));
*meta_ee_transp(t,seg).. data_meta_ee(seg,t)*sum(i $(datos_procesos(i,"ID_Seg_Tran")=datos_segmentos(seg,"ID")),(P(i,t)-P(i,t-1))) =l=sum((i,r) $(datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and datos_flujos(r,"Tipo")=2 and datos_procesos(i,"ID_Seg_Tran")=datos_segmentos(seg,"ID")),(P(i,t)-P(i,t-1))*datos_flujos(r,"Intensidad")) ;
meta_ee_transp(t,seg).. data_meta_ee(seg,t)*sum(i $(datos_procesos(i,"ID_Seg_Tran")=datos_segmentos(seg,"ID")),(P(i,t)-P(i,t-1)+datos_retiro(i,t))) =l=sum((i,r) $(datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and datos_flujos(r,"Tipo")=2 and datos_procesos(i,"ID_Seg_Tran")=datos_segmentos(seg,"ID")),(P(i,t)-P(i,t-1)+datos_retiro(i,t))*datos_flujos(r,"Intensidad")*datos_procesos(i,"Creditos")) ;

*********************************************************************************************************************************************
*restricciones generacion electrica

*demanda por barra, agno y etapa
demanda_barra(bar,t,m,b).. dem_bar(bar,t,m,b) -sum(r $(datos_flujos(r,"ID_Producto")=id_electricidad),factor_unidad*F(r,t)*datos_dem_etapa_aux2(r,bar,m,b)/data_duracion(t,m,b)) =e=0;      

*balance generacion=demanda
balance_generacion_demanda(bar,t,m,b).. sum(i $(datos_procesos(i,"ID_Barra")=datos_barras(bar,"ID") and datos_procesos(i,"Agno_ini")<=agno(t)), Ge(i,t,m,b)*(1-datos_procesos(i,"ConPropio"))*data_duracion(t,m,b))-sum(l $(datos_lineas(l,"Barra_ini")=datos_barras(bar,"ID")),Fp(l,t,m,b)+Fn(l,t,m,b))*data_duracion(t,m,b)+sum(l $(datos_lineas(l,"Barra_fin")=datos_barras(bar,"ID")),Fp(l,t,m,b)+Fn(l,t,m,b))*data_duracion(t,m,b) =e= (data_demanda_el(bar,t,m,b)$(flag_integ=0)+dem_bar(bar,t,m,b)$(flag_integ=1))*data_duracion(t,m,b) +  0.5 * (sum(l $(datos_lineas(l,"Barra_ini")=datos_barras(bar,"ID")),f_perdidas(l) * (Fp(l,t,m,b)-Fn(l,t,m,b)))*data_duracion(t,m,b)+sum(l $(datos_lineas(l,"Barra_fin")=datos_barras(bar,"ID")),f_perdidas(l)*(Fp(l,t,m,b)-Fn(l,t,m,b)))*data_duracion(t,m,b));

*generacion maxima
generacion_maxima(i,t,m,b) $(not(alm(i)) and datos_procesos(i,"ID_sector")=id_generacion).. Res_P(i,t,m,b) + Res_S(i,t,m,b) + Ge(i,t,m,b) - datos_procesos(i,"Capacidad_Instalada")$(datos_procesos(i,"Estado")=1 and agno(t)<=datos_procesos(i,"Agno_fin")) - P(i,t)$(datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin")) =l=0;

*generacion maxima centrales renovables con perfiles (Ejemplo: centrales eolicas y solares)
generacion_maxima_ERNC(i,z,t,m,b) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"ID_zona_ERNC")=datos_zonas(z,"ID")).. Ge(i,t,m,b) - data_fp_aux(z,t,m,b) * datos_procesos(i,"Capacidad_Instalada")$(datos_procesos(i,"Estado")=1 and agno(t)<=datos_procesos(i,"Agno_fin")) - data_fp_aux(z,t,m,b)*P(i,t)$(datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin")) =l=0;

*generacion maxima por etapa para centrales con factor de planta anual (Ejemplo: centrales hidroelectricas)
generacion_maxima_etapa(ifp,t,m) $(datos_procesos(ifp,"ID_sector")=id_generacion).. sum(b,Ge(ifp,t,m,b)*data_duracion(t,m,b)) -(datos_procesos(ifp,"Capacidad_Instalada")*fplanta(ifp,t,m)*sum(b,data_duracion(t,m,b)))$(datos_procesos(ifp,"Estado")=1 and agno(t)<=datos_procesos(ifp,"Agno_fin")) - (P(ifp,t)*fplanta(ifp,t,m)*sum(b,data_duracion(t,m,b)))$(datos_procesos(ifp,"Estado")=0 or agno(t)>datos_procesos(ifp,"Agno_fin")) =l=0;

*maxima inversion por agno
max_inversion_ge(i,t) $(datos_procesos(i,"ID_sector")=id_generacion and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))) .. P(i,t) =l=data_pmax(i,t);

*variacion de potencia media durante cada etapa
modula(i,t,m,b,bb)$(datos_procesos(i,"ID_sector")=id_generacion and ord(bb)>ord(b) and datos_procesos(i,"Regula")=0).. Ge(i,t,m,b) - Ge(i,t,m,bb) =e= 0;

*condicion logica de potencia instalada
condicion_log_potencia_ge(i,t) $((datos_procesos(i,"ID_sector")=id_generacion) and ord(t)>1) .. P(i,t-1)-P(i,t) =l=0;

*flujos por lineas
angulo_fase_up(bari,barj,l,t,m,b)$(datos_lineas(l,"Estado") = 1 and datos_lineas(l,"Barra_ini")=datos_barras(bari,"ID") and datos_lineas(l,"Barra_fin")=datos_barras(barj,"ID")) .. Ph(bari,t,m,b)$(datos_lineas(l,"Barra_ini")=datos_barras(bari,"ID")) - Ph(barj,t,m,b)$(datos_lineas(l,"Barra_fin")=datos_barras(barj,"ID")) =g= - bigM * (1 - Instalar_LT(l,t)) + datos_lineas(l,"Reactancia") * (Fn(l,t,m,b) + Fp(l,t,m,b));
angulo_fase_lo(bari,barj,l,t,m,b)$(datos_lineas(l,"Estado") = 1 and datos_lineas(l,"Barra_ini")=datos_barras(bari,"ID") and datos_lineas(l,"Barra_fin")=datos_barras(barj,"ID")) .. Ph(bari,t,m,b)$(datos_lineas(l,"Barra_ini")=datos_barras(bari,"ID")) - Ph(barj,t,m,b)$(datos_lineas(l,"Barra_fin")=datos_barras(barj,"ID")) =l= + bigM * (1 - Instalar_LT(l,t)) + datos_lineas(l,"Reactancia") * (Fn(l,t,m,b) + Fp(l,t,m,b));


*condicion logica de instalacion
condicion_log_fmax(l,t) $(ord(t)>1 and datos_lineas(l,"Estado") = 0) .. Instalar_LT(l,t-1)-Instalar_LT(l,t) =l= 0;
 
*flujo maximo y minimo de las lineas candidatas
flujo_maximo_tx(l,t,m,b)$(datos_lineas(l,"Estado") = 0) .. Fp(l,t,m,b) - datos_lineas(l,"Fmax")*Instalar_LT(l,t) =l= 0;
flujo_minimo_tx(l,t,m,b)$(datos_lineas(l,"Estado") = 0) .. Fn(l,t,m,b) - datos_lineas(l,"Fmin")*Instalar_LT(l,t) =g= 0;

*agno entrada nueva inversiones en transmision
condicion_ini_inversion_tx(l,t) .. Instalar_LT(l,t)$(ord(t)>1 and datos_lineas(l,"Agno_ini")>agno(t) and datos_lineas(l,"Estado") = 0) =e=0;

*minimo tecnico
Minimo_Tecnico_up(i,t,m,b)$(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"Estado") = 1 and datos_procesos(i,"Pmin") > 0).. Ge(i,t,m,b) - OnOff(i,t,m,b) * datos_procesos(i,"Capacidad_Instalada") =l= 0;
Minimo_Tecnico_dn(i,t,m,b)$(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"Estado") = 1 and datos_procesos(i,"Pmin") > 0).. Ge(i,t,m,b) - OnOff(i,t,m,b) * datos_procesos(i,"Pmin") =g= 0;

* Calcular el requisito de reserva secundaria en funcion de la potencia instalada en la tecnologia señalada en el archivo de entrada
Reserva_Secundaria(t,m,b).. Requisito_Res_S(t,m,b) =e= datos_inercia_reservas(t,m,b,"Factor_Reserva_Secundaria_B") + datos_inercia_reservas(t,m,b,"Factor_Reserva_Secundaria_M") * sum(i$(datos_procesos(i,"ID_Tecnologia") = datos_inercia_reservas(t,m,b,"ID_Tecnologia")), (datos_procesos(i,"Capacidad_Instalada")$(datos_procesos(i,"Estado")=1 and agno(t)<=datos_procesos(i,"Agno_fin")) + P(i,t)$(datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))));

* la suma de las reservas de todas las centrales debe, al menos, satisfacer el requisito P + S
Control_Frecuencia(t,m,b).. Requisito_Res_S(t,m,b) + datos_inercia_reservas(t,m,b,"Reserva_Primaria") - sum(i $(datos_procesos(i,"ID_sector")=id_generacion), Res_P(i,t,m,b) + Res_S(i,t,m,b)) =l= 0;

*inercia minima
Inercia_Minima_Sistema(t,m,b).. sum(i $(datos_procesos(i,"ID_sector")=id_generacion), Ge(i,t,m,b) *  datos_procesos(i,"Inercia")) - datos_inercia_reservas(t,m,b,"Inercia_Minima") =g= 0;

*limitacion de energia almacenada e inyectada por bloques para sistemas de almacenamineto
limitar_almacenamiento(alm,t,m,b) $(datos_procesos(alm,"ID_sector")=id_generacion).. Ge(alm,t,m,b) * data_duracion(t,m,b) - DurEta(t,m)/24 * datos_almacenamientos(alm) * perfil_almacenamiento(alm,t,m,b) * datos_procesos(alm,"Capacidad_Instalada")$(datos_procesos(alm,"Estado")=1 and agno(t)<=datos_procesos(alm,"Agno_fin")) - DurEta(t,m)/24 * datos_almacenamientos(alm) * perfil_almacenamiento(alm,t,m,b) * P(alm,t)$(datos_procesos(alm,"Estado")=0 or agno(t)>datos_procesos(alm,"Agno_fin")) =e= 0;


******************************************************************************************************************************************************************************************************************************

*cap de emisiones del sector generacion, industrias y otros sectores
limite_emisiones(cap,u1,t).. GEI_IND(cap,u1,t)+sum((i,m,b) $(datos_procesos(i,"SPT")=datos_sec_cap(cap,"ID") and datos_procesos(i,"ID_sector")=id_generacion),Ge(i,t,m,b)*factor_emision_ge_aux(i,u1)*data_duracion(t,m,b)*10**(-9)) =l=data_cap(cap,u1,t)+sum(of $(data_offset(of,"ID_Gas")=datos_gei(u1,"ID")),OFFSET(of,t));

*limite para restringir la cantidad maxima de offset que se pueden adquirir. Se expresa como un porcentaje del cap maximo (Ejemplo:10% de los derechos de emisiones)
limite_offset(u1,t).. sum(of $(data_offset(of,"ID_Gas")=datos_gei(u1,"ID")),OFFSET(of,t)) =l=data_limite_offset(u1,t);

*********************************************************************************************************************************************
*presupuesto de emisiones 
presupuesto_emisiones.. sum((i,r,t,u1) $(datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and agno(t)>ini_presupuesto and agno(t)<fin_presupuesto),F(r,t)*factor_emision_aux(r,u1)*10**(-9))+sum((i,m,b,t,u1) $(datos_procesos(i,"ID_sector")=id_generacion),Ge(i,t,m,b)*factor_emision_ge_aux(i,u1)*data_duracion(t,m,b)*10**(-9)) =l=presupuesto;


*********************************************************************************************************************************************

*funcion objetivo: minimiza costo de energeticos + inversion en nuevas tecnologias + impuesto a emisiones. Valores expresados en millones US$

costo_impuesto..    c_impuesto =e= sum((i,r,u,t) $( datos_procesos(i,"Impuesto")=1 and datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso")),factor(t)*F(r,t)*factor_emision_aux(r,u)*data_impuesto(u,t)*10**(-9));

costo_operacion..   c_operacion =e=sum((r,k,j,t) $(datos_energeticos(j,"ID_Producto")=datos_productos(k,"ID") and datos_flujos(r,"ID_Producto")=datos_productos(k,"ID")),factor(t)*F(r,t)*datos_energeticos(j,"FConPr")*precio_energetico(r,t))*10**(-6);

costo_inversion..   c_inversion =e=sum((i,t,tt) $(ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))),factor(tt)*1000*10**(-6)*(P(i,t)*cinv_a(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P(i,t)-P(i,t-1))*cinv_a(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1)))));

costo_coma..        c_coma =e=sum((i,t,tt) $(ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))),factor(tt)*1000*10**(-6)*(P(i,t)*data_coma(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P(i,t)-P(i,t-1))*data_coma(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1)))));

costo_falla..       c_falla =e=sum((d,t),demanda_falla(d,t)*factor_falla);

costo_falla_b..     c_falla_b =e=sum((d,mod,t,m,b)$(datos_demanda(d,"ID_Curva")=datos_mod(mod,"ID")),demanda_falla_b(d,t,m,b)*factor_falla);

*costos asociados al sector generacion electrica

costo_operacion_ge..   c_operacion_ge =e=sum((i,j,t,m,b) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"ID_Ener")=datos_energeticos(j,"ID")),factor(t)*Ge(i,t,m,b)*datos_procesos(i,"ConEsp")*datos_procesos(i,"Fprecio")*precio_energetico_ge(i,t)*data_duracion(t,m,b))*10**(-6);

costo_impuesto_ge..    c_impuesto_ge =e= sum((i,u,t,m,b) $(datos_procesos(i,"Impuesto")=1 and datos_procesos(i,"ID_sector")=id_generacion),factor(t)*Ge(i,t,m,b)*factor_emision_ge_aux(i,u)*data_duracion(t,m,b)*data_impuesto(u,t)*10**(-9));

costo_perdidas.. c_perdidas =e= PFL * sum((l,t,m,b), f_perdidas(l) * (Fp(l,t,m,b) - Fn(l,t,m,b) ));

costo_inversion_tx.. c_inversion_tx =e= sum((l,t)$(datos_lineas(l,"Estado") = 0), factor(t) * cinv_a_tx(l) * Instalar_LT(l,t)) ;

costo_coma_tx..        c_coma_tx =e= sum((l,t)$(datos_lineas(l,"Estado") = 0), factor(t) * datos_lineas(l,"COMA") * Instalar_LT(l,t));

costo_inversion_alm..   c_inversion_alm =e=sum((alm,t,tt) $(ord(tt)>=ord(t) and (datos_procesos(alm,"Estado")=0 or agno(t)>datos_procesos(alm,"Agno_fin"))),factor(tt)*1000*10**(-6)*(datos_almacenamientos(alm)*P(alm,t)*cinv_alm_a(alm,t)$(ord(t)=1)+(P(alm,t)-P(alm,t-1))*datos_almacenamientos(alm)*cinv_alm_a(alm,t)$(ord(t)>1)));

*costos offset
costo_offset..         c_offset =e= sum((of,t),factor(t)*OFFSET(of,t)*data_offset(of,"Costo"));

*costo total
costo_total..       costo =e= c_inversion+c_coma+c_operacion+c_impuesto+c_operacion_ge+c_impuesto_ge+c_offset+c_perdidas+c_inversion_tx+c_coma_tx+c_inversion_alm+c_falla+c_falla_b;

*costo total sin impuesto
costo_total_sin_impuesto..  costo_sin_impuesto =e= c_inversion+c_coma+c_operacion+c_offset+c_operacion_ge+c_perdidas+c_inversion_tx+c_coma_tx+c_inversion_alm+c_falla+c_falla_b;


Model Modelo_Energetico_PMR /all/;
*Model Modelo_Energetico_PMR /balance_proceso, balance_demanda, relacion_flujos, participacion_flujos, produccion_maxima, max_inversion, condicion_ini_inversion, condicion_log_potencia, limite_emisiones_industria, limite_emisiones, limite_offset, costo_operacion, costo_inversion, costo_coma, costo_impuesto, costo_offset, costo_total, costo_total_sin_impuesto, costo_falla, balance_generacion_demanda, costo_operacion_ge, costo_impuesto_ge, costo_perdidas, costo_inversion_tx,costo_coma_tx, costo_inversion_alm/;

*fin modelo de optimizacion

*************************************************************************************************************
*Definicion de optimizador
option lp = cplex;
option threads = 10;
option profile=1;
option resLim=15000;
option optCR=0.005;

*===========================================================================================================
* calculo del impuesto de acuerdo a legislizacion chilena
parameter sol_cmg_real(i,t,m,b);
Parameter sol_cvariable_real(i,t,m,b);
Parameter impuesto(i,t,m,b);
Parameter margen_noCub(i,t,m,b);
Parameter monto_aPrr(i,t,m,b);
Parameter sum_monto_aPrr_pBlo(t,m,b);
Parameter prop_retiro_pBlo(i,t,m,b);
Parameter pago_propRetiroGen_pBlo(i,t,m,b);
Parameter sum_pago_propRetiroGen_pBlo(t,m,b);
Parameter pago_retiroGen_Anual(i,t);
Parameter pago_impuestoGen_pBlo(i,t,m,b);
Parameter pago_impuestoGen_Anual(i,t);
Parameter pago_totalGen_pBlo(i,t,m,b);
Parameter pago_totalGen_Anual(i,t);
Parameter pago_porNuevoMW(i,t);
parameter nuevo_cinv_a(i,t);
parameter sol_potencia_aux(i,t);

File results14 / "../data_output/pre_solucion_pagosGen_Blo.csv" /;
File results15 / "../data_output/pre_solucion_pagosGen_Anuales.csv" /;
File results17 / "../data_output/solucion_pagosGen_Blo.csv" /;
File results18 / "../data_output/solucion_pagosGen_Anuales.csv" /;

if(flag = 2,
* Exportar archivo LP
$echo writelp "../data_output/modelo_energetico_PMR_Chile_2.lp" > cplex.o97
Modelo_Energetico_PMR.optfile=97;

*Se resuelve problema de optimizacion sin incorporar pago de impuesto
solve Modelo_Energetico_PMR minimizing costo_sin_impuesto using mip;

*se calcula la prorrata del pago de impuesto
sol_potencia_aux(i,t)=0+datos_procesos(i,"Capacidad_Instalada")$(datos_procesos(i,"Estado")=1 and agno(t)<=datos_procesos(i,"Agno_fin"))+P.l(i,t)$(datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"));

*costo marginal real visto por cada generador en cada bloque/mes/año
loop((i,bar) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"ID_Barra")=datos_barras(bar,"ID")),  sol_cmg_real(i,t,m,b) = balance_generacion_demanda.m(bar,t,m,b)*1000000/factor(t) );

*costo variable real visto por cada generador en cada bloque/mes/año
*loop((i,j) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"ID_Ener")=datos_energeticos(j,"ID")),sol_cvariable_real(i,t,m,b)=datos_procesos(i,"ConEsp")*precio_energetico(j,t)*datos_procesos(i,"Fprecio"));
loop((i,j) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"ID_Ener")=datos_energeticos(j,"ID")),sol_cvariable_real(i,t,m,b)=datos_procesos(i,"ConEsp")*precio_energetico_ge(i,t)*datos_procesos(i,"Fprecio"));

*impuesto bloque
loop((i,t),  impuesto(i,t,m,b) = 0 $( Ge.l(i,t,m,b)=0) + ( sum(u , datos_gei(u,"PCG")*factor_emision_ge_aux(i,u)*data_impuesto(u,t)*0.001) ) $(Ge.l(i,t,m,b)>0)   );

*margen no cubierto por el generador sujeto a impuesto: margen_noCub(i,t,m,b)=imp+cv-cmg
margen_noCub(i,t,m,b) =  0 $(Ge.l(i,t,m,b)=0)  + (sol_cvariable_real(i,t,m,b)+impuesto(i,t,m,b)-sol_cmg_real(i,t,m,b)) $(sol_cvariable_real(i,t,m,b)+impuesto(i,t,m,b) > sol_cmg_real(i,t,m,b) and (Ge.l(i,t,m,b)>0)) ;

*dinero no cubierto por cada generador sujeto a impuesto en cada bloque
loop (i $(datos_procesos(i,"ID_sector")=id_generacion), monto_aPrr(i,t,m,b) = (0 $(sol_cvariable_real(i,t,m,b) + 0.001*sum(u, datos_gei(u,"PCG")*factor_emision_ge_aux(i,u)*data_impuesto(u,t)) <= sol_cmg_real(i,t,m,b))) + (data_duracion(t,m,b) * Ge.l(i,t,m,b)*(sol_cvariable_real(i,t,m,b) + 0.001*sum(u, datos_gei(u,"PCG")*factor_emision_ge_aux(i,u)*data_impuesto(u,t)) - sol_cmg_real(i,t,m,b))  $((sol_cvariable_real(i,t,m,b) + 0.001*sum(u, datos_gei(u,"PCG")*factor_emision_ge_aux(i,u)*data_impuesto(u,t)) > sol_cmg_real(i,t,m,b)))));

*suma de dinero de todos los generadores según lo no cubierto para todos los generadores sujetos a impuestos
sum_monto_aPrr_pBlo(t,m,b) = sum(i $(datos_procesos(i,"ID_sector")=id_generacion), monto_aPrr(i,t,m,b));

*proporcion retiros por bloque
loop( i $(datos_procesos(i,"ID_Sector")=id_generacion), prop_retiro_pBlo(i,t,m,b) =  (  0 $( Ge.l(i,t,m,b)=0)  + (Ge.l(i,t,m,b)/sum(ii, Ge.l(ii,t,m,b))) $(Ge.l(i,t,m,b)>0)  )  ) ;

*pago de los retiros por bloque
loop( i $(datos_procesos(i,"ID_Sector")=id_generacion), pago_propRetiroGen_pBlo(i,t,m,b) = prop_retiro_pBlo(i,t,m,b)*sum_monto_aPrr_pBlo(t,m,b)   );

sum_pago_propRetiroGen_pBlo(t,m,b) = sum(i $(datos_procesos(i,"ID_sector")=id_generacion),  pago_propRetiroGen_pBlo(i,t,m,b)   );

*pago que debe hacer el generador, proporcional a sus retiros, debido a lo no cubierto por los generadores sujetos a impuestos 
loop(i $(datos_procesos(i,"ID_Sector")=id_generacion) , pago_retiroGen_Anual(i,t) = sum((m,b), pago_propRetiroGen_pBlo(i,t,m,b) ));

*pago de centrales por impuestos que no es prorrateado
pago_impuestoGen_pBlo(i,t,m,b) = impuesto(i,t,m,b) * data_duracion(t,m,b) * Ge.l(i,t,m,b) $(margen_noCub(i,t,m,b)=0)  +   0 $((margen_noCub(i,t,m,b)>0) and (sol_cmg_real(i,t,m,b)=sol_cvariable_real(i,t,m,b)))  +  ((sol_cmg_real(i,t,m,b)-sol_cvariable_real(i,t,m,b))* data_duracion(t,m,b) * Ge.l(i,t,m,b)) $((margen_noCub(i,t,m,b)>0) and (sol_cvariable_real(i,t,m,b))<sol_cmg_real(i,t,m,b)) ;

loop(i $(datos_procesos(i,"ID_Sector")=id_generacion) ,  pago_impuestoGen_Anual(i,t) = sum((m,b),  pago_impuestoGen_pBlo(i,t,m,b)   ) );

pago_totalGen_pBlo(i,t,m,b) = pago_propRetiroGen_pBlo(i,t,m,b) + pago_impuestoGen_pBlo(i,t,m,b);

pago_totalGen_Anual(i,t) = pago_impuestoGen_Anual(i,t) + pago_retiroGen_Anual(i,t);

pago_porNuevoMW(i,t) = 999999999 $(sol_potencia_aux(i,t)=0) + (pago_totalGen_Anual(i,t)/sol_potencia_aux(i,t)) $(sol_potencia_aux(i,t)>0);

*una vez calculada la prorrata, se agrega al costo de inversion de cada proceso (en $/kW)
nuevo_cinv_a(i,t) = cinv_a(i,t) + pago_porNuevoMW(i,t)/1000;
cinv_a(i,t) = nuevo_cinv_a(i,t);

*imprimir los resultados
put results14;
put "agno,eta,blo,cen,pot, gen,cmg,cv,imp,imp+cv,margen_noCub,monto_aPrr,sum_monto_aPrr_pBlo,pago_propRetiroGen_pBlo,sum_pago_propRetiroGen_pBlo,pago_impuestoGen_pBlo,pago_totalGen_pBlo" /;
loop((i,t,m,b) $(datos_procesos(i,"ID_sector")=id_generacion),
  put t.tl, ",", m.tl, ",",b.tl, ",", i.tl:40, ",",sol_potencia_aux(i,t), ",", Ge.l(i,t,m,b), ",", sol_cmg_real(i,t,m,b), ",", sol_cvariable_real(i,t,m,b), ",",impuesto(i,t,m,b)    , ",",  (sol_cvariable_real(i,t,m,b)+impuesto(i,t,m,b)), ",",margen_noCub(i,t,m,b), ",",monto_aPrr(i,t,m,b), ",",sum_monto_aPrr_pBlo(t,m,b), ",",pago_propRetiroGen_pBlo(i,t,m,b), ",",sum_pago_propRetiroGen_pBlo(t,m,b), ",",pago_impuestoGen_pBlo(i,t,m,b), ",", pago_totalGen_pBlo(i,t,m,b) /
);
putclose;

put results15;
put "agno,cen,pot,pago_retiroGen_Anual,pago_impuestoGen_Anual,pago_totalGen_Anual, pago_porNuevoMW" /;
loop((i,t) $(datos_procesos(i,"ID_sector")=id_generacion),
  put t.tl, ",",i.tl:40, ",",sol_potencia_aux(i,t), ",",pago_retiroGen_Anual(i,t), ",",pago_impuestoGen_Anual(i,t), ",",pago_totalGen_Anual(i,t), ",", pago_porNuevoMW(i,t)  /
);
putclose;


*se resuelve nuevamente el problema de optimizacion
* Exportar archivo LP
$echo writelp "../data_output/modelo_energetico_PMR_Chile_2_2.lp" > cplex.o96
Modelo_Energetico_PMR.optfile=96;

solve Modelo_Energetico_PMR minimizing costo_sin_impuesto using mip;

*se calcula la prorrata del pago de impuesto nuevamente
sol_potencia_aux(i,t)=0;
sol_potencia_aux(i,t)=datos_procesos(i,"Capacidad_Instalada")$(datos_procesos(i,"Estado")=1 and agno(t)<=datos_procesos(i,"Agno_fin"))+P.l(i,t)$(datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"));
*costo marginal real visto por cada generador en cada bloque/mes/año
loop((i,bar) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"ID_Barra")=datos_barras(bar,"ID")),  sol_cmg_real(i,t,m,b) = balance_generacion_demanda.m(bar,t,m,b)*1000000/factor(t) );

*costo variable real visto por cada generador en cada bloque/mes/año
*loop((i,j) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"ID_Ener")=datos_energeticos(j,"ID")),sol_cvariable_real(i,t,m,b)=datos_procesos(i,"ConEsp")*precio_energetico(j,t)*datos_procesos(i,"Fprecio"));
loop((i,j) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"ID_Ener")=datos_energeticos(j,"ID")),sol_cvariable_real(i,t,m,b)=datos_procesos(i,"ConEsp")*precio_energetico_ge(i,t)*datos_procesos(i,"Fprecio"));

*impuesto bloque
loop((i,t),  impuesto(i,t,m,b) = 0 $( Ge.l(i,t,m,b)=0) + ( sum(u , datos_gei(u,"PCG")*factor_emision_ge_aux(i,u)*data_impuesto(u,t)*0.001) ) $(Ge.l(i,t,m,b)>0)   );

*margen no cubierto por el generador sujeto a impuesto: margen_noCub(i,t,m,b)=imp+cv-cmg
margen_noCub(i,t,m,b) =  0 $(Ge.l(i,t,m,b)=0)  + (sol_cvariable_real(i,t,m,b)+impuesto(i,t,m,b)-sol_cmg_real(i,t,m,b)) $(sol_cvariable_real(i,t,m,b)+impuesto(i,t,m,b) > sol_cmg_real(i,t,m,b) and (Ge.l(i,t,m,b)>0)) ;

*dinero no cubierto por cada generador sujeto a impuesto en cada bloque
loop (i $(datos_procesos(i,"ID_sector")=id_generacion), monto_aPrr(i,t,m,b) = (0 $(sol_cvariable_real(i,t,m,b) + 0.001*sum(u, datos_gei(u,"PCG")*factor_emision_ge_aux(i,u)*data_impuesto(u,t)) <= sol_cmg_real(i,t,m,b))) + (data_duracion(t,m,b) * Ge.l(i,t,m,b)*(sol_cvariable_real(i,t,m,b) + 0.001*sum(u, datos_gei(u,"PCG")*factor_emision_ge_aux(i,u)*data_impuesto(u,t)) - sol_cmg_real(i,t,m,b))  $((sol_cvariable_real(i,t,m,b) + 0.001*sum(u, datos_gei(u,"PCG")*factor_emision_ge_aux(i,u)*data_impuesto(u,t)) > sol_cmg_real(i,t,m,b)))));

*suma de dinero de todos los generadores según lo no cubierto para todos los generadores sujetos a impuestos
sum_monto_aPrr_pBlo(t,m,b) = sum(i $(datos_procesos(i,"ID_sector")=id_generacion), monto_aPrr(i,t,m,b));

*proporcion retiros por bloque
loop( i $(datos_procesos(i,"ID_Sector")=id_generacion), prop_retiro_pBlo(i,t,m,b) =  (  0 $( Ge.l(i,t,m,b)=0)  + (Ge.l(i,t,m,b)/sum(ii, Ge.l(ii,t,m,b))) $(Ge.l(i,t,m,b)>0)  )  ) ;

*pago de los retiros por bloque
loop( i $(datos_procesos(i,"ID_Sector")=id_generacion), pago_propRetiroGen_pBlo(i,t,m,b) = prop_retiro_pBlo(i,t,m,b)*sum_monto_aPrr_pBlo(t,m,b)   );

sum_pago_propRetiroGen_pBlo(t,m,b) = sum(i $(datos_procesos(i,"ID_sector")=id_generacion),  pago_propRetiroGen_pBlo(i,t,m,b)   );

*pago que debe hacer el generador, proporcional a sus retiros, debido a lo no cubierto por los generadores sujetos a impuestos 
loop(i $(datos_procesos(i,"ID_Sector")=id_generacion) , pago_retiroGen_Anual(i,t) = sum((m,b), pago_propRetiroGen_pBlo(i,t,m,b) ));

*pago de centrales por impuestos que no es prorrateado
pago_impuestoGen_pBlo(i,t,m,b) = impuesto(i,t,m,b) * data_duracion(t,m,b) * Ge.l(i,t,m,b) $(margen_noCub(i,t,m,b)=0)  +   0 $((margen_noCub(i,t,m,b)>0) and (sol_cmg_real(i,t,m,b)=sol_cvariable_real(i,t,m,b)))  +  ((sol_cmg_real(i,t,m,b)-sol_cvariable_real(i,t,m,b))* data_duracion(t,m,b) * Ge.l(i,t,m,b)) $((margen_noCub(i,t,m,b)>0) and (sol_cvariable_real(i,t,m,b))<sol_cmg_real(i,t,m,b)) ;

loop(i $(datos_procesos(i,"ID_Sector")=id_generacion) ,  pago_impuestoGen_Anual(i,t) = sum((m,b),  pago_impuestoGen_pBlo(i,t,m,b)   ) );

pago_totalGen_pBlo(i,t,m,b) = pago_propRetiroGen_pBlo(i,t,m,b) + pago_impuestoGen_pBlo(i,t,m,b);

pago_totalGen_Anual(i,t) = pago_impuestoGen_Anual(i,t) + pago_retiroGen_Anual(i,t);

pago_porNuevoMW(i,t) = 999999999 $(sol_potencia_aux(i,t)=0) + (pago_totalGen_Anual(i,t)/sol_potencia_aux(i,t)) $(sol_potencia_aux(i,t)>0);

*imprimir los resultados de nuevo
put results17;
put "agno,eta,blo,cen,pot, gen,cmg,cv,imp,imp+cv,margen_noCub,monto_aPrr,sum_monto_aPrr_pBlo,pago_propRetiroGen_pBlo,sum_pago_propRetiroGen_pBlo,pago_impuestoGen_pBlo,pago_totalGen_pBlo" /;
loop((i,t,m,b) $(datos_procesos(i,"ID_sector")=id_generacion),
  put t.tl, ",", m.tl, ",",b.tl, ",", i.tl:40, ",",sol_potencia_aux(i,t), ",", Ge.l(i,t,m,b), ",", sol_cmg_real(i,t,m,b), ",", sol_cvariable_real(i,t,m,b), ",",impuesto(i,t,m,b)    , ",",  (sol_cvariable_real(i,t,m,b)+impuesto(i,t,m,b)), ",",margen_noCub(i,t,m,b), ",",monto_aPrr(i,t,m,b), ",",sum_monto_aPrr_pBlo(t,m,b), ",",pago_propRetiroGen_pBlo(i,t,m,b), ",",sum_pago_propRetiroGen_pBlo(t,m,b), ",",pago_impuestoGen_pBlo(i,t,m,b), ",", pago_totalGen_pBlo(i,t,m,b) /
);
putclose;

put results18;
put "agno,cen,pot,pago_retiroGen_Anual,pago_impuestoGen_Anual,pago_totalGen_Anual, pago_porNuevoMW" /;
loop((i,t) $(datos_procesos(i,"ID_sector")=id_generacion),
  put t.tl, ",",i.tl:40, ",",sol_potencia_aux(i,t), ",",pago_retiroGen_Anual(i,t), ",",pago_impuestoGen_Anual(i,t), ",",pago_totalGen_Anual(i,t), ",", pago_porNuevoMW(i,t)  /
);
putclose;
);

*===========================================================================================================
if(flag=0,
* Exportar archivo LP 
*$echo writelp "../data_output/modelo_energetico_PMR_Chile_0.lp" > cplex.o98
Modelo_Energetico_PMR.optfile=98;

*Se resuelve problema de optimizacion con impuesto
solve Modelo_Energetico_PMR minimizing costo using mip;
);

if (flag=1,
* Exportar archivo LP 
$echo writelp "../data_output/modelo_energetico_PMR_Chile_1.lp" > cplex.o95
Modelo_Energetico_PMR.optfile=95;

*Se resuelve problema de optimizacion con impuesto
solve Modelo_Energetico_PMR minimizing costo using mip;

sol_potencia_aux(i,t)=0;
sol_potencia_aux(i,t)=datos_procesos(i,"Capacidad_Instalada")$(datos_procesos(i,"Estado")=1 and agno(t)<=datos_procesos(i,"Agno_fin"))+P.l(i,t)$(datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"));

*Se fija solucion de potencia de centrales electricas
P.lo(i,t) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))= sol_potencia_aux(i,t);
P.up(i,t) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))= sol_potencia_aux(i,t);

* Exportar archivo LP
$echo writelp "../data_output/modelo_energetico_PMR_Chile_1_2.lp" > cplex.o99
Modelo_Energetico_PMR.optfile=99;

*Se resuelve problema de optimizacion considerando la funcion objetivo que no incorpora pago de impuesto. De esta forma los costos marginales del sector generacion electrica no quedan afectados por la aplicación del impuesto.

solve Modelo_Energetico_PMR minimizing costo_sin_impuesto using mip;

);

*************************************************************************************************************
*Incertidumbre hidrologica
*actualizo valores de factor de planta
Equation
generacion_maxima_etapa_sim(ifp,t,m)    'generacion maxima por etapa para cada simulacion';

*modified by James 12-06-2020 (30 is 2050 - 2020)
loop ((t, h1, h2), fplanta(ifp,t,m) = min(1, max((34 - ord(t))/30, 0))*fplanta_aux(ifp,h1,m) + min(1, max((ord(t) - 4)/30, 0))*fplanta_aux(ifp,h2,m));

sol_potencia_aux(i,t)=0;
sol_potencia_aux(i,t)=datos_procesos(i,"Capacidad_Instalada")$(datos_procesos(i,"Estado")=1 and agno(t)<=datos_procesos(i,"Agno_fin"))+P.l(i,t)$(datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"));

*Se fija solucion de potencia de centrales electricas
P.lo(i,t) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))= sol_potencia_aux(i,t);
P.up(i,t) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))= sol_potencia_aux(i,t);

*Equation
*actualizacion de factor de planta
generacion_maxima_etapa_sim(ifp,t,m) $(datos_procesos(ifp,"ID_sector")=id_generacion).. sum(b,Ge(ifp,t,m,b)*data_duracion(t,m,b)) -(datos_procesos(ifp,"Capacidad_Instalada")*fplanta(ifp,t,m)*sum(b,data_duracion(t,m,b)))$(datos_procesos(ifp,"Estado")=1 and agno(t)<=datos_procesos(ifp,"Agno_fin")) - (P(ifp,t)*fplanta(ifp,t,m)*sum(b,data_duracion(t,m,b)))$(datos_procesos(ifp,"Estado")=0 or agno(t)>datos_procesos(ifp,"Agno_fin")) =l=0;

Model Modelo_Energetico_PMR_simulacion /balance_proceso,balance_demanda,balance_demanda_bloque,relacion_flujo_bloque,relacion_flujos,participacion_flujos,produccion_maxima,max_inversion,condicion_ini_inversion,condicion_log_potencia,limite_emisiones_industria,limite_emisiones,limite_offset,presupuesto_emisiones,costo_operacion,costo_inversion,costo_coma,costo_impuesto,costo_offset,costo_total,costo_total_sin_impuesto,costo_falla,costo_falla_b,balance_flujo_min,flujo_maximo_bloque,balance_generacion_demanda,generacion_maxima_ERNC,generacion_maxima,generacion_maxima_etapa_sim,max_inversion_ge,condicion_log_potencia_ge,modula,angulo_fase_up,angulo_fase_lo,flujo_maximo_tx,flujo_minimo_tx,condicion_log_fmax,condicion_ini_inversion_tx,limitar_almacenamiento,Minimo_Tecnico_up,Minimo_Tecnico_dn,Inercia_Minima_Sistema,Reserva_Secundaria,Control_Frecuencia,demanda_barra,costo_perdidas,costo_inversion_tx,costo_coma_tx,costo_inversion_alm,costo_impuesto_ge,costo_operacion_ge,meta_ee_transp/;

* Exportar archivo LP
*$echo writelp "../data_output/modelo_energetico_PMR_Chile_1_3.lp" > cplex.o99
Modelo_Energetico_PMR_simulacion.optfile=99;


solve Modelo_Energetico_PMR_simulacion minimizing costo using mip;


*************************************************************************************************************
*Resultados del problema de optimizacion
display costo.l,c_inversion.l, c_coma.l, c_operacion.l, c_operacion_ge.l, c_impuesto_ge.l;

parameters
*demanda de energia por flujo y agno. Expresada en Tcal
sol_energia(r,t)

*emisiones para cada flujo modelado. Expresada en millones de ton
sol_emisiones(r,u,t)

*emisiones de GEI por sector, proceso, combustible, gas y agno. Expresada en millones de ton de COeq
sol_emisiones_co2e(r,u,t)

*potencia instalada por sector, proceso, combustible y agno. Expresada en MWt
sol_potencia(s,i,t)

*emisiones sector generacion electrica. Expresada en millones de ton 
sol_emisiones_ge(i,u,t)

*emisiones sector generacion electrica. Expresada en millones de ton de COeq
sol_emisiones_ge_co2e(i,u,t);

*sol_energia(r,i,k,t)=0;
*sol_energia(s,i,k,t)=sum(r $(datos_procesos(i,"ID_Sector")=datos_sectores(s,"ID") and datos_flujos(r,"ID_Proceso")=datos_procesos(i,"ID") and datos_flujos(r,"ID_Producto")=datos_productos(k,"ID") and datos_flujos(r,"Tipo")=1),F.l(r,t));

sol_energia(r,t)=0;
sol_energia(r,t)=F.l(r,t);

sol_emisiones(r,u,t)=0;
sol_emisiones(r,u,t)=F.l(r,t)*factor_emision_aux(r,u)*10**(-9);

sol_emisiones_co2e(r,u,t)=0;
sol_emisiones_co2e(r,u,t)=F.l(r,t)*factor_emision_aux(r,u)*datos_gei(u,"PCG")*10**(-9);

sol_potencia(s,i,t)=0;
sol_potencia(s,i,t)=datos_procesos(i,"Capacidad_Instalada")$(datos_procesos(i,"Estado")=1 and agno(t)<=datos_procesos(i,"Agno_fin"))+P.l(i,t)$(datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin")); ;

sol_emisiones_ge(i,u,t)=0;
sol_emisiones_ge(i,u,t) = sum((m,b) $(datos_procesos(i,"ID_sector")=id_generacion),Ge.l(i,t,m,b)*factor_emision_ge_aux(i,u)*data_duracion(t,m,b)*0.001*10**(-6));

sol_emisiones_ge_co2e(i,u,t)=0;
sol_emisiones_ge_co2e(i,u,t) = sum((m,b) $(datos_procesos(i,"ID_sector")=id_generacion),Ge.l(i,t,m,b)*factor_emision_ge_aux(i,u)*data_duracion(t,m,b)*datos_gei(u,"PCG")*0.001*10**(-6));

*resumen de componentes de costos funcion objetivo*
File results22 / "../data_output/solucion_resumen_costos.csv" /;
put results22;
put "costo_funcion_objetivo",",",costo.l /
put "costo_inversion_generacion",",",(sum((i,t,tt) $(datos_procesos(i,"ID_sector")=id_generacion and ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))),factor(tt)*1000*10**(-6)*(P.l(i,t)*cinv_a(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P.l(i,t)-P.l(i,t-1))*cinv_a(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1)))))) /
put "costo_inversion_otros_sectores",",",(sum((i,t,tt) $(datos_procesos(i,"ID_sector")<>id_generacion and ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))and datos_procesos(i,"Tipo")=2),factor(tt)*1000*10**(-6)*(P.l(i,t)*cinv_a(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P.l(i,t)-P.l(i,t-1))*cinv_a(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1)))))) /
put "costo_inversion_otros_sectores_aux",",",(sum((i,t,tt) $(datos_procesos(i,"ID_sector")<>id_generacion and ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))and datos_procesos(i,"Tipo")=1),factor(tt)*1000*10**(-6)*(P.l(i,t)*cinv_a(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P.l(i,t)-P.l(i,t-1))*cinv_a(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1)))))) /
put "costo_inversion_tx",",",(sum((l,t)$(datos_lineas(l,"Estado") = 0), factor(t) * cinv_a_tx(l) * Instalar_LT.l(l,t))) /
put "costo_inversion_alm",",",(sum((alm,t,tt) $(ord(tt)>=ord(t) and (datos_procesos(alm,"Estado")=0 or agno(t)>datos_procesos(alm,"Agno_fin"))),factor(tt)*1000*10**(-6)*(datos_almacenamientos(alm)*P.l(alm,t)*cinv_alm_a(alm,t)$(ord(t)=1)+(P.l(alm,t)-P.l(alm,t-1))*datos_almacenamientos(alm)*cinv_alm_a(alm,t)$(ord(t)>1)))) /
put "coma_generacion",",",sum((i,t,tt) $(datos_procesos(i,"ID_sector")=id_generacion and ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))),factor(tt)*1000*10**(-6)*(P.l(i,t)*data_coma(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P.l(i,t)-P.l(i,t-1))*data_coma(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1))))) /
put "coma_otros_sectores",",",sum((i,t,tt) $(datos_procesos(i,"ID_sector")<>id_generacion and ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))),factor(tt)*1000*10**(-6)*(P.l(i,t)*data_coma(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P.l(i,t)-P.l(i,t-1))*data_coma(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1))))) /
put "coma_tx",",",c_coma_tx.l /
put "costo_operacion_otros_sectores",",",c_operacion.l /
put "costo_operacion_generacion",",",c_operacion_ge.l /
put "costo_impuesto_otros_sectores",",",c_impuesto.l /
put "costo_impuesto_generacion",",",c_impuesto_ge.l /
put "costo_offset",",",c_offset.l /
put "costo_penalizacion_perdidas",",",c_perdidas.l /
put "costo_penalizacion_falla",",",c_falla.l /
putclose;


File results32 / "../data_output/solucion_resumen_costos_sin_tasa.csv" /;
put results32;
put "costo_inversion_generacion",",",(sum((i,t,tt) $(datos_procesos(i,"ID_sector")=id_generacion and ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))),1000*10**(-6)*(P.l(i,t)*cinv_a(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P.l(i,t)-P.l(i,t-1))*cinv_a(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1)))))) /
put "costo_inversion_otros_sectores",",",(sum((i,t,tt) $(datos_procesos(i,"ID_sector")<>id_generacion and ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))and datos_procesos(i,"Tipo")=2),1000*10**(-6)*(P.l(i,t)*cinv_a(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P.l(i,t)-P.l(i,t-1))*cinv_a(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1)))))) /
put "costo_inversion_otros_sectores_aux",",",(sum((i,t,tt) $(datos_procesos(i,"ID_sector")<>id_generacion and ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))and datos_procesos(i,"Tipo")=1),1000*10**(-6)*(P.l(i,t)*cinv_a(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P.l(i,t)-P.l(i,t-1))*cinv_a(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1)))))) /
put "costo_inversion_tx",",",(sum((l,t)$(datos_lineas(l,"Estado") = 0), cinv_a_tx(l) * Instalar_LT.l(l,t))) /
put "costo_inversion_alm",",",(sum((alm,t,tt) $(ord(tt)>=ord(t) and (datos_procesos(alm,"Estado")=0 or agno(t)>datos_procesos(alm,"Agno_fin"))),1000*10**(-6)*(datos_almacenamientos(alm)*P.l(alm,t)*cinv_alm_a(alm,t)$(ord(t)=1)+(P.l(alm,t)-P.l(alm,t-1))*datos_almacenamientos(alm)*cinv_alm_a(alm,t)$(ord(t)>1)))) /
put "coma_generacion",",",sum((i,t,tt) $(datos_procesos(i,"ID_sector")=id_generacion and ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))),1000*10**(-6)*(P.l(i,t)*data_coma(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P.l(i,t)-P.l(i,t-1))*data_coma(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1))))) /
put "coma_otros_sectores",",",sum((i,t,tt) $(datos_procesos(i,"ID_sector")<>id_generacion and ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))),1000*10**(-6)*(P.l(i,t)*data_coma(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P.l(i,t)-P.l(i,t-1))*data_coma(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1))))) /
put "coma_tx",",", (sum((l,t)$(datos_lineas(l,"Estado") = 0), datos_lineas(l,"COMA") * Instalar_LT.l(l,t))) /
put "costo_operacion_otros_sectores",",",(sum((r,k,j,t) $(datos_energeticos(j,"ID_Producto")=datos_productos(k,"ID") and datos_flujos(r,"ID_Producto")=datos_productos(k,"ID")),F.l(r,t)*datos_energeticos(j,"FConPr")*precio_energetico(r,t))*10**(-6)) /
put "costo_operacion_generacion",",",(sum((i,j,t,m,b) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"ID_Ener")=datos_energeticos(j,"ID")),Ge.l(i,t,m,b)*datos_procesos(i,"ConEsp")*datos_procesos(i,"Fprecio")*precio_energetico_ge(i,t)*data_duracion(t,m,b))*10**(-6)) /
put "costo_impuesto_otros_sectores",",", (sum((i,r,u,t) $( datos_procesos(i,"Impuesto")=1 and datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso")),F.l(r,t)*factor_emision_aux(r,u)*data_impuesto(u,t)*10**(-9))) /
put "costo_impuesto_generacion",",",(sum((i,u,t,m,b) $(datos_procesos(i,"Impuesto")=1 and datos_procesos(i,"ID_sector")=id_generacion),Ge.l(i,t,m,b)*factor_emision_ge_aux(i,u)*data_duracion(t,m,b)*data_impuesto(u,t)*10**(-9))) /
put "costo_offset",",",sum((of,t),OFFSET.l(of,t)*data_offset(of,"Costo"))/
put "costo_penalizacion_perdidas",",",c_perdidas.l /
put "costo_penalizacion_falla",",",c_falla.l /
putclose;

*archivo auxiliar para analizar distribicion de demanda por barra, etapa y bloque
*File results43 / "../data_output/datos_dem_etapa_aux2.csv" /;
*results43.nd=5;
*put results43;
*put "flujo,barra,etapa,bloque,demanda,datos_dem_bar,datos_dem_etapa_aux" /;
*loop ((r,i,bar,m,b)$(datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and datos_flujos(r,"ID_Producto")=id_electricidad),
*put r.tl:40,",",bar.tl,",",m.tl,",",b.tl,",",dem_bar.l(bar,t,m,b)datos_dem_etapa_aux2(r,bar,m,b),",",datos_dem_bar(i,bar),",",datos_dem_etapa_aux(i,m,b) /
*);
*putclose;
    
*File results99 / "../data_output/demanda_barra_procesos.csv" /;
*put results99;
*results99.nd=5;
*parameter aux99;
*put "barra,proceso,sector,flujo,agno, etapa,bloque,aux,flujo" /;
*loop((bar,i,r,t,m,b) $((agno(t)=2017 or agno(t)=2025) and datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso") and datos_flujos(r,"ID_Producto")=id_electricidad and *datos_dem_etapa_aux2(r,bar,m,b)>0),
*    aux99=(factor_unidad*datos_dem_etapa_aux2(r,bar,m,b)/data_duracion(t,m,b));
*    put bar.tl,",",i.tl:40,",",datos_procesos(i,"ID_sector"),",",r.tl,",", t.tl,",", m.tl,",", b.tl,",",aux99,",",F.l(r,t) /
*);
*putclose;

*imprimo flujos*
File results / "../data_output/solucion_flujos.csv" /;
put results;
put "flujo,agnos,producto,flujo" /;
loop((r,k,t) $(datos_productos(k,"ID")=datos_flujos(r,"ID_Producto")),
  put r.tl,",", t.tl,",",k.tl,",", F.l(r,t) /
);
putclose;

*imprimo flujos por bloques*
File results88 / "../data_output/solucion_flujos_bloques.csv" /;
put results88;
put "flujo,producto,agno, etapa,bloque,flujo" /;
loop((r,k,t,m,b) $(flag_restr_b(r)=1 and datos_productos(k,"ID")=datos_flujos(r,"ID_Producto")),
  put r.tl,",",k.tl:40,",",t.tl,",",m.tl,",",b.tl,",",Fb.l(r,t,m,b) /
);
putclose;


*imprimo consumo de energia*
File results3 / "../data_output/solucion_energia.csv" /;
put results3;
put "flujo,agno,energia" /;
loop((r,t),
  put r.tl:20,",",t.tl,",",sol_energia(r,t) /
);
putclose;

*imprimo emisiones*
File results4 / "../data_output/solucion_emisiones.csv" /;
put results4;
put "flujo,GEI,agno,emisiones" /;
loop((r,u,t),
  put r.tl:20,",", u.tl:30,",",t.tl,",",sol_emisiones(r,u,t) /
);
putclose;

*imprimo potencia instalada por proceso*
File results5 / "../data_output/solucion_potencia.csv" /;
put results5;
put "sector,proceso,agno,potencia" /;
loop((s,i,t) $(datos_procesos(i,"ID_Sector")=datos_sectores(s,"ID")),
  put s.tl:20,",",i.tl:40,",",t.tl,",",sol_potencia(s,i,t) /
);
putclose;

*imprimo generacion electrica*
File results6 / "../data_output/solucion_generacion.csv" /;
put results6;
put "central,agno,etapa,bloque,generacion" /;
loop((i,t,m,b) $(datos_procesos(i,"ID_Sector")=id_generacion),
  put i.tl:40,",",t.tl,",",m.tl,",",b.tl,",",Ge.l(i,t,m,b) /
);
putclose;

*imprimo generacion electrica anual*
File results7 / "../data_output/solucion_generacion_anual.csv" /;
put results7;
put "central,agno,generacion" /;
loop((i,t) $(datos_procesos(i,"ID_Sector")=id_generacion),
  put i.tl:40,",",t.tl,",",sum((m,b),Ge.l(i,t,m,b)*data_duracion(t,m,b)) /
);
putclose;

*imprimo emisiones generacion electrica*
File results8 / "../data_output/solucion_emisiones_ge.csv" /;
results8.nd=5;
put results8;
put "proceso,GEI,agno,emisiones" /;
loop((i,u,t) $(datos_procesos(i,"ID_sector")=id_generacion),
  put i.tl:40,",",u.tl:30,",",t.tl,",",sol_emisiones_ge(i,u,t) /
);
putclose;

*imprimo offset*
File results9 / "../data_output/solucion_offset.csv" /;
put results9;
put "GEI,agno,offset" /;
loop((of,t) ,
  put of.tl:30,",",t.tl,",",OFFSET.l(of,t) /
);
putclose;

*imprimo flujos por lineas*
File results10 / "../data_output/solucion_lineas.csv" /;
put results10;
put "linea,agno,etapa,bloque,flujo" /;
loop((l,t,m,b) ,
  put l.tl:30,",",t.tl,",",m.tl,",",b.tl,",",(Fp.l(l,t,m,b)+Fn.l(l,t,m,b)) /
);
putclose;

*imprimo flujos maximos por lineas nuevas*
File results16 / "../data_output/solucion_expansion_lineas.csv" /;
put results16;
put "linea,agno,fmax" /;
loop((l,t) $ (datos_lineas(l,"Estado") = 0) ,
  put l.tl:30,",",t.tl,",",(datos_lineas(l,"Fmax") * Instalar_LT.l(l,t)) /
);
putclose;

*imprimo costos marginales,demanda y perdidas por barra*
File results11 / "../data_output/solucion_barras.csv" /;
put results11;
put "barra,agno,etapa,bloque,dem,cmg,perdidas" /;
loop((bar,t,m,b) ,
  put bar.tl:30,",",t.tl,",",m.tl,",",b.tl,",",data_demanda_el(bar,t,m,b),",",(1000000*balance_generacion_demanda.m(bar,t,m,b)/factor(t)),",",(0.5*(sum(l $(datos_lineas(l,"Barra_ini")=datos_barras(bar,"ID")),f_perdidas(l)*(Fp.l(l,t,m,b)-Fn.l(l,t,m,b)))+sum(l $(datos_lineas(l,"Barra_fin")=datos_barras(bar,"ID")),f_perdidas(l)*(Fp.l(l,t,m,b)-Fn.l(l,t,m,b))))) /
);
putclose;

*imprimo emisiones CO2e*
File results12 / "../data_output/solucion_emisiones_co2e.csv" /;
put results12;
put "flujo,GEI,agno,emisiones" /;
loop((r,u,t),
  put r.tl:20,",",u.tl:30,",",t.tl,",",sol_emisiones_co2e(r,u,t) /
);
putclose;

*imprimo emisiones generacion electrica en CO2e*
File results13 / "../data_output/solucion_emisiones_ge_co2e.csv" /;
put results13;
put "proceso,GEI,agno,emisiones" /;
loop((i,u,t) $(datos_procesos(i,"ID_sector")=id_generacion),
  put i.tl:40,",",u.tl:30,",",t.tl,",",sol_emisiones_ge_co2e(i,u,t) /
);
putclose;

*imprimo demanda de falla para balance procesos*
File results19 / "../data_output/solucion_demanda_no_suminstrada.csv" /;
put results19;
put "agno,producto,demanda" /;
loop((d,t),
  put t.tl,",",d.tl,",",demanda_falla.l(d,t)/
);
putclose;

*imprimo demanda electrica por bloque*
File results20 / "../data_output/solucion_demanda_barra.csv" /;
put results20;
put "barra,agno,etapa,bloque,potencia,energia" /;
loop((bar,t,m,b),
  put bar.tl,",",t.tl,",",m.tl,",",b.tl,",",dem_bar.l(bar,t,m,b),",",(dem_bar.l(bar,t,m,b)*data_duracion(t,m,b))/
);
putclose;

File results21 / "../data_output/solucion_recaudacion_impuesto.csv" /;
put results21;
put "agno,recaudacion_generacion,recaudacion_otros_sectores" /;
loop(t,
put t.tl,",",sum((i,u,m,b) $(datos_procesos(i,"Impuesto")=1 and datos_procesos(i,"ID_sector")=id_generacion),Ge.l(i,t,m,b)*factor_emision_ge_aux(i,u)*data_duracion(t,m,b)*data_impuesto(u,t)*10**(-9)),",",sum((i,r,u) $( datos_procesos(i,"Impuesto")=1 and datos_procesos(i,"ID")=datos_flujos(r,"ID_Proceso")),F.l(r,t)*factor_emision_aux(r,u)*data_impuesto(u,t)*10**(-9)) /
);
putclose;

File results23 / "../data_output/solucion_detalle_costos.csv" /;
put results23;
put "agno,emisiones_otros_sec,emisiones_gen,costo_inversion,costo_inversion_tx,coma,coma_tx,costo_operacion_otros_sec,costo_operacion_generacion" /;
loop(t,
put t.tl,",",sum((r,u),sol_emisiones_co2e(r,u,t)),",",sum((i,u),sol_emisiones_ge_co2e(i,u,t)),",",(sum((i,tt) $(ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))),1000*10**(-6)*(P.l(i,t)*cinv_a(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P.l(i,t)-P.l(i,t-1))*cinv_a(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1)))))+sum((alm,tt) $(ord(tt)>=ord(t) and (datos_procesos(alm,"Estado")=0 or agno(t)>datos_procesos(alm,"Agno_fin"))),1000*10**(-6)*(datos_almacenamientos(alm)*P.l(alm,t)*cinv_alm_a(alm,t)$(ord(t)=1)+(P.l(alm,t)-P.l(alm,t-1))*datos_almacenamientos(alm)*cinv_alm_a(alm,t)$(ord(t)>1)))),",",sum(l$(datos_lineas(l,"Estado") = 0),cinv_a_tx(l)*Instalar_LT.l(l,t)),",",sum((i,tt) $(ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))),1000*10**(-6)*(P.l(i,t)*data_coma(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P.l(i,t)-P.l(i,t-1))*data_coma(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1))))),",",sum(l$(datos_lineas(l,"Estado") = 0),datos_lineas(l,"COMA")*Instalar_LT.l(l,t)),",",(sum((r,k,j) $(datos_energeticos(j,"ID_Producto")=datos_productos(k,"ID") and datos_flujos(r,"ID_Producto")=datos_productos(k,"ID")),F.l(r,t)*datos_energeticos(j,"FConPr")*precio_energetico(r,t))*10**(-6)),",",(sum((i,j,m,b) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"ID_Ener")=datos_energeticos(j,"ID")),Ge.l(i,t,m,b)*datos_procesos(i,"ConEsp")*datos_procesos(i,"Fprecio")*precio_energetico_ge(i,t)*data_duracion(t,m,b))*10**(-6)) /;
);
putclose;

File resultsBID / "../data_output/solution_generation_sector.csv" /;
put resultsBID;
put "agno,emission,CAPEX,OPEX" /;
loop(t,
put t.tl,",",sum((i,u),sol_emisiones_ge_co2e(i,u,t)),",",(sum((i,tt) $(ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))),1000*10**(-6)*(P.l(i,t)*cinv_a(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P.l(i,t)-P.l(i,t-1))*cinv_a(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1)))))+sum((alm,tt) $(ord(tt)>=ord(t) and (datos_procesos(alm,"Estado")=0 or agno(t)>datos_procesos(alm,"Agno_fin"))),1000*10**(-6)*(datos_almacenamientos(alm)*P.l(alm,t)*cinv_alm_a(alm,t)$(ord(t)=1)+(P.l(alm,t)-P.l(alm,t-1))*datos_almacenamientos(alm)*cinv_alm_a(alm,t)$(ord(t)>1)))+sum(l$(datos_lineas(l,"Estado") = 0),cinv_a_tx(l)*Instalar_LT.l(l,t))),",",(sum((i,tt) $(ord(tt)>=ord(t) and (datos_procesos(i,"Estado")=0 or agno(t)>datos_procesos(i,"Agno_fin"))),1000*10**(-6)*(P.l(i,t)*data_coma(i,t)$(agno(t)=tbase or rel_eq(agno(t),(datos_procesos(i,"Agno_fin")+1)))+(P.l(i,t)-P.l(i,t-1))*data_coma(i,t)$(agno(t)>tbase and rel_ne(agno(t),(datos_procesos(i,"Agno_fin")+1)))))+sum(l$(datos_lineas(l,"Estado") = 0),datos_lineas(l,"COMA")*Instalar_LT.l(l,t))+(sum((r,k,j) $(datos_energeticos(j,"ID_Producto")=datos_productos(k,"ID") and datos_flujos(r,"ID_Producto")=datos_productos(k,"ID")),F.l(r,t)*datos_energeticos(j,"FConPr")*precio_energetico(r,t))*10**(-6))+(sum((i,j,m,b) $(datos_procesos(i,"ID_sector")=id_generacion and datos_procesos(i,"ID_Ener")=datos_energeticos(j,"ID")),Ge.l(i,t,m,b)*datos_procesos(i,"ConEsp")*datos_procesos(i,"Fprecio")*precio_energetico_ge(i,t)*data_duracion(t,m,b))*10**(-6))) /;
);
putclose;

*imprimo flujos por procesos*
*execute '=test flujos_procesos';
*File results2 / "../data_output/solucion_flujos_procesos.csv" /;
*put results2;
*put "proceso,flujo,agnos,producto,tipo,flujo" /;
*loop((i,r,k,t) $(datos_productos(k,"ID")=datos_flujos(r,"ID_Producto") and datos_flujos(r,"ID_Proceso")=datos_procesos(i,"ID")),
*  put i.tl:40,",",r.tl,",", t.tl,",",k.tl:30,",",datos_flujos(r,"Tipo"),",",F.l(r,t) /
*);
*putclose;


*temp—VERIFY fplanta
File resultsFPLANT / "../data_output/fplanta.csv" /;
put resultsFPLANT;
put "master_id,tech,year,month,fplanta" /;
loop((esc_selec,ifp,t,m),
  put esc_selec.tl,",",ifp.tl,",",t.tl,",",m.tl,",",(fplanta(ifp,t,m))/
);
putclose;











