# ![icon](image_icon.gif) LCIIIMULATOR  
**LC-3 Simulator**

Un simulador del microprocesador LC-3 diseñado para emular su comportamiento, permitiendo la ejecución de instrucciones en lenguaje ensamblador y el análisis de registros y memoria en tiempo real.

---

## Descripción

**LCIIIMULATOR** es una herramienta educativa que facilita la comprensión y práctica del ensamblador LC-3.  
Ofrece funcionalidades para:  
- Ejecución paso a paso de instrucciones.  
- Visualización en tiempo real de los registros y la memoria.  
- Emulación de instrucciones binarias.  
- Soporte para flujo de ejecución condicionado.  

Ideal para estudiantes y entusiastas de la arquitectura de computadoras.

---

## Instalación

### Para Linux
1. Asegúrate de tener Python3.10.x instalado:  
   sudo apt update  
   sudo apt install python3 python3-pip -y  
2. Descarga los siguientes archivos del repositorio:

   - `back_end.py`
   - `back_end2.py`
   - `back_end3.py`
   - `front_end.pyw`
4. (Opcional) Instala las dependencias necesarias si no tienes:  
   Tkinter
5. Ejecuta la interfaz gráfica:  
   python3 frond_end.pyw  

### Para Windows
1. Descarga LCIIIMULATOR.exe del repositorio
2. Ejecuta LCIIIMULATOR.exe

Si quieres ejecutar por pyhton:
1. Descarga e instala Python desde python.org (asegúrate de marcar la opción "Add Python to PATH").  
2. Asegúrate de que el entorno de ventanas (Tkinter) esté instalado:  
   - En la mayoría de las instalaciones de Python para Windows, Tkinter ya viene incluido.  
   - Si encuentras problemas al ejecutar la interfaz gráfica, verifica que Tkinter esté disponible. 
3. Descarga los siguientes archivos del repositorio:

   - `back_end.py`
   - `back_end2.py`
   - `back_end3.py`
   - `front_end.pyw`
5. Ejecuta la interfaz gráfica:  
   python frond_end.pyw  

---

## Uso

1. Ejecuta la interfaz gráfica (como se explicó arriba).  
2. Carga un archivo de instrucciones LC-3 (en formato binario o ensamblador).  
3. Elige entre las opciones de ejecución:  
   - Automática: Corre hasta el final de la instrucción.  
   - Paso a paso: Controla la ejecución manualmente.  
4. Observa cómo se actualizan los registros y la memoria en tiempo real.  

---
## Estructura del Proyecto

LCIIIMULATOR/  
├── front_end/         -> Archivos para la interfaz gráfica  
├── back_end/          -> Lógica para las conversiones de instrucciones  
├── back_end2/         -> Lógica para el simulador  
├── back_end3/         -> Funciones para cargar o guardar  
└── README.md          -> Este archivo  

---

## Licencia

Este proyecto está licenciado bajo la **GPLv3**. Consulta el archivo LICENSE para más detalles.

---

## Contribuciones

¡Las contribuciones son bienvenidas!  
1. Haz un fork del repositorio.  
2. Crea una rama para tu funcionalidad (`git checkout -b mi-funcionalidad`).  
3. Realiza un pull request.  

---

## Autores

- [MrTayon](https://github.com/MrTayon)  
- [Nico-Ant](https://github.com/Nico-Ant)  
- [rmgleon](https://github.com/rmgleon)  

