
# Primeros pasos

Antes de ejecutar el proyecto necesitamos considerar lo siguiente.

- Tener instaldo **nodejs**: Se puede usar cualquier tipo de instalación de su preferencia, [Documentación](https://nodejs.org/es).
- Instalar el **CLI** de AWS: Puede consultar la documentación [Aquí](https://docs.aws.amazon.com/es_es/cli/latest/userguide/getting-started-install.html)
- Generar su **Access key ID** y **Secret access key** en la consola de AWS, más espeficio en el servicio ***IAM*** para acceder a los servicios del **CLI** y **CDK** sin problemas
- Instalar **CDK** de AWS globalmente con: `npm install -g aws-cdk` y comprobar la instalación `cdk --version`

# AWS CDK

Este proyecto esta implementado con de **AWS CDK** la cual en palabras de aws es una herramienta que *"permite crear aplicaciones fiables, escalables y rentables en la nube con la considerable potencia expresiva de un lenguaje de programación"*. esto quiere decir que podermos crear un stack completo con todos de los productos que maneja aws pero con código aunque este tipo de aplicaciónes es también conocido como Infraestructura como código o IaC (Infrastructure as Code) por sus siglas en inglés.

El proyecto de CDK puede ser escrito en diversos lenguajes pero en nuestro caso usaremos Python ya que cuenta con bastante soporte por la comunidad.

# Descripcion del proyecto

Este proyecto en específico consiste en ejecutar una función lambda a partir de un disparador, este disparador corresponde a que cuando se guarde un archivo .csv en un determinado bucket de S3, este generara la orden a una función lambda para leer ese archivo, extraer información, hacer operaciones con esta información y generar un pequeño reporte que será enviado por correo electrónico.

# Ejecución del proyecto parte 1 CDK.

1. Debes ir a tu consola de aws y crear un bucket de S3 para almacenar los archivos .csv
2. Una vez descargado el repositorio ejecutar lo siguiente:

```sh
$ cd storiapp-with-CD/
$ python3 -m venv .venv
$ source .venv/bin/activate # linux o mac
% .venv\Scripts\activate.bat # windows
$ pip install -r requirements.txt
```

Si tiene algunos accesKeys que le hayan sido proporcionados por el autor de este repositorio, el siguiente paso bastaria con ejecutar `cdk synth` y si no hay errores ahora `cdk deploy` para tener lista la parte del stack en aws, pero si no es así **siga los siguientes pasos**.

## Ejecución personalizada

1. Abra el código del proyecto desde la raiz en un IDE como por ejemplo Visual Studio Code con `code .`

2. Y modifique las siguientes lineas de código en el archivo `stackstori/stackstori_stack.py`:

```python
 environment={
    'EMAIL_ADDRESS': "",
    'EMAIL_PASSWORD': "",
    'EMAIL_RECEIVER': "",
},
```
Estas variables son:

- EMAIL_ADDRESS: El correo del remitente.
- EMAIL_PASSWORD: No es la contraseña del email remitente, una contraseña de aplicación que se crea desde tu cuenta de [Google](https://myaccount.google.com/?hl=es) y es una cadena de 16 letras.
- EMAIL_RECEIVER: El correo del destinatario.

3. Modifique la ARN de su bucket de S3 en la siguiente parte de código:

```python
s3 = s3_.Bucket.from_bucket_arn(self, "storiapp", "arn:aws:s3:::nombre_de_tu_bucket")
```
1. De esta forma se podrá ejecutar `cdk synth` y si no hay errores `cdk deploy`

Ahora que ya se tiene deplegado su proyecto de CDK puede verificar su **cloudformation** en la consola de aws para verificar que se subio de manera correcta. Ya que ahora se tiene una lambda programada con un trigger de S3

# Ejecución del proyecto parte 2 trigger de S3.

Para esta parte con todo funcionando de manera correcta en aws gracias a CDK, solo falta hacer que funcione el trigger y para ello ejecutaremos una paqueña API que envia un documento al bucket que tengamos definido tanto en el código de CDK como de manera real.

Para ello ya en la raiz del proyecto ejecutaremos:

```sh
npm install
node uploadFile.js
```
El código en `uploadFile.js` tiene definido el nombre del bucket como `storiapp` si así no se llama su bucket, favor de colocar el nombre correcto.

Finalmente use un programa como insomnia o postman para crear un método `POST` hacia la url `http://localhost:3001/api/upload-csv`.

Elija el tipo de `body` como `form-data` para habilitar la parte de key-value donde `key` sera **file** de tipo **File** y `value` sera algún archivo .csv que hemos dejado en la carpeta ***csv_files***

De esa forma recibira un correo el destinatario con el resumen de su actividad financiera 👌

***NOTA:*** Lo que sigue es solo referencia de CDK no es usarlo pero pude servirle como referencia.

# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
