from flask import Flask, json, flash, Blueprint, url_for, jsonify, make_response, request, render_template, redirect, abort
import requests

router = Blueprint('router', __name__)


@router.route('/')
def admin():
    return render_template('template.html')

@router.route('/proyectoCenso/list')
def list_all_Censos():  
    r = requests.get("http://localhost:8080/proyectoCenso/list")
    # print(type(r.json()))
    # print(r.json())
    data = r.json()
    return render_template('fragmento/proyecto Censo/lista.html', list=data["data"])

@router.route('/proyectoCenso/list/generadores')
def list_generadores():  
    r = requests.get("http://localhost:8080//proyectoCenso/list/generadores")
    # print(type(r.json()))
    # print(r.json())
    data = r.json()
    return render_template('fragmento/generador/lista.html', list=data["data"])

@router.route('/proyectoCenso/registro')
def view_registro_censo():  
    return render_template('fragmento/proyecto Censo/registro.html')


@router.route('/proyectoCenso/nuevo', methods=["POST"])
def registrar_censo():
    headers = {'Content-type': 'application/json'}
    form = request.form
    data = {
        "nroIntegrantesFamilia": int(form["nroIntegrantesFamilia"]),
        "descripcion": form["descripcion"],
        "direccion": form["direccion"],
        "haveGenerador": form.get("haveGenerador") == '1',

    }

    if data["haveGenerador"]:
        data["generador"] = {
            "consumo_litrosHora": int(form["consumo_litrosHora"]),
            "kw": int(form["kw"]),
            "costo": float(form["costo"]),
            "tipo": form["tipo"],
        }

    # print(json.dumps(data));

    r = requests.post("http://localhost:8080/proyectoCenso/save", data=json.dumps(data), headers=headers)
    dat = r.json()
    print(f"Status Code: {r.status_code}")
    print(f"Response Content: {r.text}")

    if r.status_code == 200:
        flash("Se ha guardado correctamente", category='info')
    else:
        flash(str(dat["data"]), category='error')
    return redirect("/proyectoCenso/list")


@router.route('/proyectoCenso/delete/<int:id>', methods=["POST"])
def eliminar_censo(id):
    # print("Index a eliminar", id)
    if request.method == 'POST':
        if request.form.get('_method') == 'DELETE':
            r = requests.delete(f"http://localhost:8080/proyectoCenso/delete/{id}")

            if r.status_code == 200:
                flash("Censo eliminado exitosamente.", category='info')
            else:
                flash("No se pudo eliminar el censo.", category='error')
    
    return redirect("/proyectoCenso/list")

# renderiza un formulario segun el estado del switch
@router.route('/proyectoCenso/generador/form')
def view_registro_generador():  
    return render_template('fragmento/generador/registro.html')

@router.route("/proyectoCenso/update/<int:id>")
def view_edicion_registro_censo(id):
     # Obtener la lista de censos
    r = requests.get("http://localhost:8080/proyectoCenso/list")
    
    data_list = r.json()  

    # Buscar el censo por ID
    censo_a_editar = None
    for item in data_list['data']:  # Asegúrate de acceder correctamente a la lista
        if item['idCenso'] == id:
            censo_a_editar = item
            break

    if censo_a_editar is None:
        flash("Censo no encontrado", category='error')
        return redirect("/proyectoCenso/list")

    return render_template('fragmento/proyecto Censo/editar.html', data=censo_a_editar)


@router.route("/proyectoCenso/generador/form/update/<int:id>")
def view_edicion_generador(id):
    r = requests.get("http://localhost:8080/proyectoCenso/list")
    data_list = r.json()

    # Buscar el generador por idCenso
    generador_a_editar = None
    for item in data_list['data']:
        if item['idCenso'] == id and item.get('generador') is not None:
            generador_a_editar = item['generador']
            break

    if generador_a_editar is None:
        flash("Generador no encontrado o no existe", category='error')
        # return redirect("/proyectoCenso/list")

    return render_template('fragmento/generador/editar.html', data=generador_a_editar)


@router.route("/proyectoCenso/info/<int:id>") #Envia idCenso
def view_info_generador(id):
    r = requests.get("http://localhost:8080/proyectoCenso/list")
    data_list = r.json()

    # Buscar el generador por idCenso
    generador_a_mostrar = None
    for item in data_list['data']:
        if item['idCenso'] == id and item.get('generador') is not None:
            generador_a_mostrar = item['generador']
            break

    if generador_a_mostrar is None:
        flash("Generador no encontrado o no existe", category='error')
        # return redirect("/proyectoCenso/list")

    return render_template('fragmento/generador/info.html', data=generador_a_mostrar)

@router.route('/proyectoCenso/update', methods=["POST"])
def actualizar_censo():
    headers = {'Content-type': 'application/json'}
    form = request.form
    data = {
        "idCenso": int(form["idCenso"]),
        "nroIntegrantesFamilia": int(form["nroIntegrantesFamilia"]),
        "descripcion": form["descripcion"],
        "direccion": form["direccion"],
        "haveGenerador": form.get("haveGenerador") == '1',

    }

    if data["haveGenerador"]:
        data["generador"] = {
            "idGenerador": int(form["idGenerador"]),
            "consumo_litrosHora": int(form["consumo_litrosHora"]),
            "kw": int(form["kw"]),
            "costo": float(form["costo"]),
            "tipo": form["tipo"],
        }

    # print(json.dumps(data));

    r = requests.post("http://localhost:8080/proyectoCenso/update", data=json.dumps(data), headers=headers)
    dat = r.json()
    # print(f"Status Code: {r.status_code}")
    # print(f"Response Content: {r.text}")

    if r.status_code == 200:
        flash("Se ha guardado correctamente", category='info')
    else:
        flash(str(dat["data"]), category='error')
    return redirect("/proyectoCenso/list")


# Metodo de Ordenacion
# http://localhost:8080/proyectoCenso/order/quick/1/numero integrante
@router.route('/order/<metodo>/<tipo>/<atributo>')
def view_order_censo(atributo, tipo, metodo):
    try:
        url = f"http://localhost:8080/proyectoCenso/order/{metodo}/{tipo}/{atributo}"

        r = requests.get(url)
        data = r.json()
        return render_template('fragmento/proyecto Censo/lista.html', list=data["data"])
        

    except requests.RequestException as e:
        flash(f"Error de conexión: {str(e)}", category='error')
        return redirect(url_for('/proyectoCenso/list'))


# Metodo de Busqueda
@router.route('/proyectoCenso/list/search/<tipo>/<criterio>/<texto>', methods=['GET'])
def view_search_censo(tipo, criterio, texto):
    url = f"http://localhost:8080/proyectoCenso/search/{tipo}/{criterio}/{texto}" 
    r = requests.get(url)
    data = r.json()
    # print(f"tipo {tipo}, criterio {criterio}, texto {texto}")
    print(data["data"])

    # Verificar si la respuesta es un solo objeto y convertirlo a una lista
    if isinstance(data["data"], dict):  # Si es un solo objeto
        list_data = [data["data"]]  # Convierte a lista
        return render_template('fragmento/proyecto Censo/lista.html', list=list_data)
    
    
    return render_template('fragmento/proyecto Censo/lista.html', list=data["data"])

