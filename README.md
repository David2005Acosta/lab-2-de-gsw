# gsw-practico-unidad2-equipo04

**Gestion de Servidores Web - Laboratorio 2**
Caso: **"Dulce Hogar"** - Reposteria artesanal (El Salvador)

Montaje de un servidor web completo (Apache sobre Ubuntu Server LTS / WSL2)
que publica el catalogo de "Dulce Hogar", integra una API por **Reverse Proxy**
y sirve el sitio por **HTTPS local con mkcert**.

---

## Integrantes y roles

| Rol | Responsabilidad principal | Integrante |
|-----|---------------------------|------------|
| Coordinador / Git | Organiza tiempos, consolida el informe, gestiona el repositorio y prepara la defensa | José Santos Aguilar De La Cruz |
| Adm. de Servidor Base | Instala Apache, verifica estado, habilita modulos y crea la estructura de directorios | Carlos Josue Majano Granados |
| Adm. de Redes / Proxy | Configura Virtual Hosts, ProxyPass/Reverse y puertos (80 y 8900) | Luis Roman Lino Merino |
| Adm. de Certificados (SSL) | Instala mkcert, genera certificados y configura el Virtual Host HTTPS | Andersson Wilfredo Vargas Reyes |
| Adm. de Permisos (OS) | Aplica menor privilegio (chown/chmod), valida www-data y confia la CA en Windows | Edwin David Diaz Acosta |
| Documentador / QA | Capturas, redaccion del informe, pruebas de integracion y validacion de HTTPS | Dereck Enrique Ventura Benitez |

> Ajusten los nombres/roles segun el acuerdo final del equipo.

**Equipo N.º:** 4  |  **Seccion:** A

---

## Estructura del repositorio

```
.
|-- README.md
|-- informe-final.pdf
|-- informe-final.html          (fuente del PDF)
|-- fase1-dimensionamiento.txt
|-- fase2-apache.txt
|-- fase3-virtualhost.txt
|-- fase4-https.txt
|-- config/
|   |-- dulcehogar.local.conf
|   |-- dulcehogar.local-ssl.conf
|   |-- ports.conf
|   |-- rootCA.pem              (CA publica de mkcert - opcional)
|   |-- rootCA.crt
|-- capturas/
|   |-- fase2-apache-activo.png
|   |-- fase3-curl-exitoso.png
|   |-- fase4-https-sin-advertencia.png
|-- backend/                    (extra: API de la Unidad 1 en el puerto 9000)
|   |-- api.py
|   |-- dulcehogar-api.service
|-- sitio/                      (extra: contenido del catalogo)
|   |-- index.html
|-- scripts/                    (extra: ayuda para configurar Windows)
    |-- agregar-host-windows.bat
    |-- confiar-ca-windows.ps1
```

---

## Arquitectura de la solucion

```
 Navegador (Windows)
        |
        |  http://dulcehogar.local            (puerto 80)
        |  https://dulcehogar.local:8900      (puerto 8900, mkcert)
        v
 +-------------------------------+        /api/*        +------------------------+
 |  Apache 2.4 (Ubuntu/WSL2)     |  -------------->    |  API "Dulce Hogar"      |
 |  Virtual Host dulcehogar.local|  ProxyPass /        |  Python en :9000        |
 |  DocumentRoot: /var/www/...   |  ProxyPassReverse   |  (Unidad 1)             |
 +-------------------------------+                     +------------------------+
```

---

## Requisitos

- Windows 11 con **WSL2** y una distro **Ubuntu 24.04 LTS**.
- En la distro se instala: `apache2`, `libnss3-tools`, `wget`, `mkcert`.

---

## Como reproducirlo

### Fase 2 - Apache

```bash
sudo apt update
sudo apt install -y apache2
sudo systemctl enable --now apache2
sudo systemctl status apache2
curl http://localhost
sudo apache2ctl configtest
```

### Fase 3 - Virtual Host + Reverse Proxy

```bash
sudo mkdir -p /var/www/dulcehogar.local
sudo chown -R www-data:www-data /var/www/dulcehogar.local
sudo a2enmod proxy proxy_http headers
sudo cp config/dulcehogar.local.conf /etc/apache2/sites-available/
sudo a2ensite dulcehogar.local.conf
sudo apache2ctl configtest && sudo systemctl reload apache2
echo "127.0.0.1 dulcehogar.local" | sudo tee -a /etc/hosts
curl http://dulcehogar.local/api/saludo?nombre=Equipo
```

El backend de la Unidad 1 (puerto 9000) se instala una vez:

```bash
sudo mkdir -p /opt/dulcehogar
sudo cp backend/api.py /opt/dulcehogar/api.py
sudo cp backend/dulcehogar-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now dulcehogar-api
```

### Fase 4 - HTTPS con mkcert

```bash
sudo apt install -y libnss3-tools wget
wget -O mkcert https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64
chmod +x mkcert && sudo mv mkcert /usr/local/bin/mkcert
mkcert -install                 # OJO: con guion
mkcert dulcehogar.local
sudo mkdir -p /etc/apache2/ssl/dulcehogar.local
sudo mv dulcehogar.local*.pem /etc/apache2/ssl/dulcehogar.local/
sudo cp config/ports.conf /etc/apache2/ports.conf     # incluye Listen 8900
sudo a2enmod ssl
sudo cp config/dulcehogar.local-ssl.conf /etc/apache2/sites-available/
sudo a2ensite dulcehogar.local-ssl.conf
sudo apache2ctl configtest && sudo systemctl restart apache2
sudo ss -tlnp | grep apache2
curl https://dulcehogar.local:8900/api/saludo?nombre=Equipo
```

### Configuracion en Windows (una sola vez)

1. **Hosts:** ejecutar `scripts\agregar-host-windows.bat` como Administrador
   (agrega `127.0.0.1 dulcehogar.local`).
2. **Confiar la CA:** ejecutar `scripts\confiar-ca-windows.ps1` (agrega la CA
   de mkcert al almacen de confianza del usuario).

Luego abrir: **https://dulcehogar.local:8900/api/saludo?nombre=Equipo**

---

## Evidencia (capturas)

| Archivo | Que demuestra |
|---------|---------------|
| `capturas/fase2-apache-activo.png` | Apache corriendo y pagina por defecto |
| `capturas/fase3-curl-exitoso.png` | Reverse Proxy devolviendo el JSON de la API |
| `capturas/fase4-https-sin-advertencia.png` | HTTPS en :8900 con candado valido |

> Las capturas deben ser del entorno propio del equipo (no de Internet).

---

## Errores encontrados y solucion

- **`mkcert install` sin guion** crea un certificado para el dominio "install"
  y no instala la CA. Correcto: **`mkcert -install`**.
- **WSL2 se apaga al cerrar la sesion** y el puerto 8900 dejaba de responder.
  Solucion: mantener la distro en ejecucion; con `systemd` habilitado los
  servicios (apache2, dulcehogar-api) arrancan solos.
- **Windows no alcanzaba `localhost`** hasta que la distro quedo activa
  (reenvio de puertos de WSL2). Verificar con `ss -tlnp | grep apache2`.
- **Puerto 80 ocupado** (p. ej. IIS): revisar con `sudo ss -tlnp | grep :80`.

---

## Comandos de verificacion rapida

```bash
apache2ctl -M | grep -E 'proxy|proxy_http|headers|ssl'   # modulos activos
apache2ctl -t -D DUMP_VHOSTS                             # virtual hosts
systemctl status apache2 dulcehogar-api --no-pager       # servicios
sudo ss -tlnp | grep -E ':80|:8900|:9000'                # puertos
```
