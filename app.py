import flask
from flask import Flask
import sirope
import flask_login
import json
from model.userdto import UserDto
from model.postdto import PostDto
from model.commentdto import CommentDto

def create_app():
    flapp = Flask(__name__)
    sirpe = sirope.Sirope()
    lgmg = flask_login.login_manager.LoginManager()
    
    lgmg.init_app(flapp)
    
    flapp.config.from_file("config.json", load=json.load)

    return flapp, sirpe, lgmg


app, srp, lm = create_app()

@lm.user_loader
def user_loader(uid):
    return UserDto.busca(srp, uid)

@lm.unauthorized_handler
def unauthorized():
    return "Usuario incorrecto", 401

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return flask.render_template('500.html'), 500

# Para los libros
@app.route('/404')
def no_existe():
    return flask.render_template('404.html')

@app.route('/')
def index(): 
    
    usr = UserDto.current_user()
    posts = list(srp.load_all(PostDto))
    comentarios = list(srp.load_all(CommentDto))
    
    sust = {
        "usr" : usr,
        "posts" : posts,
        "comentarios" : comentarios
    }
    
    return flask.render_template("index.html", **sust)


@app.route('/profile')
def profile():
    usr = UserDto.current_user()
    posts = list(srp.load_all(PostDto))
    comentarios = list(srp.load_all(CommentDto))
    usuario = usr
    
    if not usr:
        return flask.redirect("/404")
    
    sust = {
        "usr" : usr,
        "usuario": usuario,
        "comentarios" : comentarios,
        "posts" : posts
    }
    
    return flask.render_template("profile.html", **sust)


@app.route('/login', methods=["POST"])
def login():
    txt_usuario = flask.request.form.get("username")
    txt_password = flask.request.form.get("password")
    
    if not (txt_usuario or txt_password):
        flask.flash("Introduce todos los datos")
        return flask.redirect("/login")
    
    usr = UserDto.busca(srp, txt_usuario)
    
    if not usr:
        flask.flash("El usuario no existe")
        return flask.redirect("/login")
    
    if not usr.chk_password(txt_password):
        flask.flash("Clave incorrecta")
        return flask.redirect("/login")
    
    flask_login.login_user(usr)

    return flask.redirect("/")


@app.route('/login')
def login_page():
    return flask.render_template("login.html")


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect("/")


@app.route('/register', methods=["POST"])
def register():
    usuario_txt = flask.request.form.get("username")
    pasword_txt = flask.request.form.get("password")
    email_txt = flask.request.form.get("email")
    
    if not usuario_txt:
        flask.flash("Introduce todos los datos")
        return flask.redirect("/register")
    
    if not pasword_txt:
        flask.flash("Introduce todos los datos")
        return flask.redirect("/register")
    
    if not email_txt:
        flask.flash("Introduce todos los datos")
        return flask.redirect("/register")
    
    usr = UserDto.busca(srp, usuario_txt)
    if not usr:
        usr = UserDto(usuario_txt, pasword_txt, email_txt)
        srp.save(usr)
    else:
        flask.flash("El usuario ya existe")
        return flask.redirect("/register")
            
    flask_login.login_user(usr)

    return flask.redirect("/")


@app.route('/register')
def register_page():
    return flask.render_template("register.html")


@app.route('/post', methods=["POST"])
def post():
    #Obtener los campos del formulario
    txt_titulo = flask.request.form.get("edTitulo")
    txt_autor = flask.request.form.get("edAutor")
    txt_resumen = flask.request.form.get("edResumen")
    portada = flask.request.form.get("edPortada")
    
    if not txt_titulo:
        flask.flash("Introduce todos los datos")
        return flask.redirect("/post")
    
    if not txt_autor:
        flask.flash("Introduce todos los datos")
        return flask.redirect("/post")
    
    if not txt_resumen:
        flask.flash("Introduce todos los datos")
        return flask.redirect("/post")
    
    if not portada:
        flask.flash("Introduce todos los datos")
        return flask.redirect("/post")
    
    #Obtener el usuario
    usr = UserDto.current_user()
    libro = PostDto.busca(srp, txt_titulo)
    
    if not libro:
        # Guardar la publicacion
        post = PostDto(txt_titulo, txt_autor, usr.usuario, portada, txt_resumen)
        srp.save(post)
    else:
        flask.flash("El libro ya existe")
        return flask.redirect("/post")

    return flask.redirect("/")


@app.route('/post')
def post_page():
    usr = UserDto.current_user()
    posts = list(srp.load_all(PostDto))
    
    sust = {
        "usr" : usr,
        "posts" : posts
    }
    
    return flask.render_template("post.html", **sust)


@app.route('/libro/<post_titulo>/comment', methods=["GET","POST"])
def comment_post(post_titulo):
    #Obtener los campos del formulario
    txt_comentario = flask.request.form.get("edComentario")
    txt_valoracion = flask.request.form.get("edValoracion")
    libro = post_titulo
    
    existe = PostDto.busca(srp, libro)
    if existe == None:
        return flask.redirect("/404")
    
    #Obtener el usuario
    usr = UserDto.current_user()
    if not usr:
        return flask.redirect("/404")
    
    if flask.request.method == "POST":
        if not txt_comentario:
            flask.flash("Introduce todos los datos")
        elif not txt_valoracion:
            flask.flash("Introduce todos los datos")
        else:    
            # Guardar el comentario
            comment = CommentDto(libro, txt_comentario, usr.usuario, txt_valoracion)
            srp.save(comment)
            
    posts = list(srp.load_all(PostDto))
    comentarios = list(srp.load_all(CommentDto))
    
    sust = {
        "usr" : usr,
        "posts" : posts,
        "comentarios" : comentarios,
        "libro" : libro
    }

    return flask.render_template("libro.html", **sust)


@app.route("/search", methods=["POST"])
def search():
    busqueda = flask.request.form.get("edSearch")
    posts = list(srp.load_all(PostDto))
    
    usr = UserDto.current_user()
    
    sust = {
        "usr" : usr,
        "posts" : posts,
        "busqueda" : busqueda
    }
    
    return flask.render_template("search.html", **sust)


@app.route('/libro')
def libro():
    usr = UserDto.current_user()
    posts = list(srp.load_all(PostDto))
    libro = flask.request.args.get('libro', None)
    comentarios = list(srp.load_all(CommentDto))
    
    existe = PostDto.busca(srp, libro)
    if existe == None:
        return flask.redirect("/404")
    
    sust = {
        "usr" : usr,
        "posts" : posts,
        "comentarios" : comentarios,
        "libro" : libro
    }
    
    return flask.render_template("libro.html", **sust)


@flask_login.login_required
@app.route('/edit', methods=["POST"]) # Editar perfil
def edit():
    #Obtener los campos del formulario
    txt_nombre = flask.request.form.get("edNombre")
    txt_descripcion = flask.request.form.get("edDescripcion")
    foto = flask.request.form.get("edFoto")
    
    usr = UserDto.current_user()
    
    if txt_nombre == None:
        txt_nombre = ""
    
    usr.nombre = txt_nombre
    usr.descripcion = txt_descripcion
    usr.foto = foto
    
    srp.save(usr)
    flask_login.login_user(usr)

    return flask.redirect("/profile")

@flask_login.login_required
@app.route('/edit')
def edit_page():
    usr = UserDto.current_user()
    
    if not usr:
        return flask.redirect("/404")
    
    sust = {
        "usr" : usr
    }
    
    return flask.render_template("edit.html", **sust)


@app.route('/user_profile/<usuario>') # Perfil demas usuarios
def user_profile(usuario):
    usr = UserDto.current_user()
    usuario = UserDto.busca(srp, usuario)
    posts = list(srp.load_all(PostDto))
    comentarios = list(srp.load_all(CommentDto))
    
    if usuario == None:
        return flask.redirect("/404")
    
    sust = {
        "usr" : usr,
        "usuario": usuario,
        "posts" : posts,
        "comentarios" : comentarios
    }
    
    return flask.render_template("profile.html", **sust)


@flask_login.login_required
@app.route('/edit_libro/<post_titulo>', methods=["POST"]) # Editar libro
def edit_libro(post_titulo):
    #Obtener los campos del formulario
    txt_titulo = flask.request.form.get("edTitulo")
    txt_autor = flask.request.form.get("edAutor")
    txt_resumen = flask.request.form.get("edResumen")
    portada = flask.request.form.get("edPortada")
    libro = post_titulo
    
    #Obtener el usuario
    usr = UserDto.current_user()
    libro = PostDto.busca(srp, post_titulo)
    
    posts = list(srp.load_all(PostDto))
    comentarios = list(srp.load_all(CommentDto))
    
    sust = {
        "usr" : usr,
        "posts" : posts,
        "comentarios" : comentarios,
        "libro" : txt_titulo
    }
    
    if not txt_titulo:
        flask.flash("Introduce todos los datos")
        return flask.render_template("edit_libro.html", **sust)
    elif not txt_autor:
        flask.flash("Introduce todos los datos")
        return flask.render_template("edit_libro.html", **sust)
    elif not txt_resumen:
        flask.flash("Introduce todos los datos")
        return flask.render_template("edit_libro.html", **sust)
    elif not portada:
        flask.flash("Introduce todos los datos")
        return flask.render_template("edit_libro.html", **sust)
    else:
        # Guardar el libro editado
        libro.titulo = txt_titulo
        libro.autor = txt_autor
        libro.resumen = txt_resumen
        libro.imagen = portada

        srp.save(libro)
        posts = list(srp.load_all(PostDto))
        
        sust = {
            "usr" : usr,
            "posts" : posts,
            "comentarios" : comentarios,
            "libro" : txt_titulo
        }
    

        return flask.render_template("libro.html", **sust)

@flask_login.login_required
@app.route('/edit_libro/<post_titulo>')
def edit_libro_page(post_titulo):
    libro = PostDto.busca(srp, post_titulo)
    
    if libro == None:
        return flask.redirect("/404")
    
    #Obtener el usuario
    usr = UserDto.current_user()
    posts = list(srp.load_all(PostDto))
    comentarios = list(srp.load_all(CommentDto))
    
    if libro.usuario != usr.usuario:
        return flask.redirect("/404")
    
    if not usr:
        return flask.redirect("/404")
            
    sust = {
        "usr" : usr,
        "posts" : posts,
        "comentarios" : comentarios,
        "libro" : post_titulo
    }

    return flask.render_template("edit_libro.html", **sust)

@flask_login.login_required
@app.route('/delete_comment/<id>')
def delete_comment(id):
    
    usr = UserDto.current_user()
    if not usr:
        return flask.redirect("/404")

    comentario = CommentDto.busca(srp, id)
    if comentario.usuario != usr.usuario:
        return flask.redirect("/404")
    
    srp.delete(comentario.__oid__)
    
    return flask.redirect("/")

@flask_login.login_required
@app.route('/delete_post/<titulo>')
def delete_post(titulo):

    usr = UserDto.current_user()
    if not usr:
        return flask.redirect("/404")
    
    post = PostDto.busca(srp, titulo)
    if post.usuario != usr.usuario:
        return flask.redirect("/404")
    
    srp.delete(post.__oid__)
    
    comentarios = list(srp.load_all(CommentDto))
    for comentario in comentarios:
        if comentario.libro == titulo:
            srp.delete(comentario.__oid__)
    
    return flask.redirect("/")


if __name__ == '__main__':
    app.run()