> Datos de casos de covid-19 por departamento en Bolivia, publicados por UDAPE y transcritos diariamente

**Nota del 24 de Enero de 2022**

**LOS DATOS SERÁN ACTUALIZADOS EN ESTA NUEVA DIRECCIÓN: [sociedatos/covid19-bo-casos_por_departamento](https://github.com/sociedatos/covid19-bo-casos_por_departamento)**

---

**Fuente**: Reportes diarios de la situación del covid-19 en Bolivia publicados por UDAPE ([enlace](https://www.udape.gob.bo/index.php?option=com_wrapper&view=wrapper&Itemid=104))

En este repositorio encuentras:

- [Confirmados diarios](https://github.com/mauforonda/covid19-bolivia-udape/blob/master/confirmados_diarios.csv)
- [Decesos diarios](https://github.com/mauforonda/covid19-bolivia-udape/blob/master/decesos_diarios.csv)
- [Recuperados diarios](https://github.com/mauforonda/covid19-bolivia-udape/blob/master/recuperados_diarios.csv)
- [Confirmados acumulados](https://github.com/mauforonda/covid19-bolivia-udape/blob/master/confirmados_acumulados.csv)
- [Activos acumulados](https://github.com/mauforonda/covid19-bolivia-udape/blob/master/activos_acumulados.csv)
- [Decesos acumulados](https://github.com/mauforonda/covid19-bolivia-udape/blob/master/decesos_acumulados.csv)
- [Recuperados acumulados](https://github.com/mauforonda/covid19-bolivia-udape/blob/master/recuperados_acumulados.csv)

desde el 10 de marzo. 

Espero actualizar estos datos diariamente si es que la fuente lo permite. 

---

Decisiones cuestionables en la fuente:

- El 6 de septiembre de 2020 el SEDES Santa Cruz reporta una actualización que incrementa 1570 casos al conteo acumulado de decesos. Según [un comunicado del Ministerio de Salud](https://web.archive.org/web/20201019031006/https://www.boliviasegura.gob.bo/comunicados_proc2.php?Seleccion=476), el incremento es resultado de *una revisión retrospectiva de datos* y *no corresponden al día mencionado*. Como ninguna fuente oficial sugiere qué fecha de fallecimiento asignar a estos casos, UDAPE decidió no incluirlos en el conteo de casos diarios, pero sí en el conteo acumulado. Es decir que el 6 de septiembre de 2020 UDAPE reporta 23 decesos en `decesos_diarios` y un incremento de 1593 en `decesos_acumulados`. Por esta razón la suma de decesos diarios en Santa Cruz no produce el valor correspondiente en decesos acumulados. Dado que ésta es una decisión cuestionable y mi repositorio pretende ser simultáneamente fiel a la fuente y útil a usos prácticos de los datos, decido publicar tanto los valores diarios como acumulados que ofrece el reporte diario de UDAPE.
