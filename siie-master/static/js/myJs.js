/**
 * Created by Luisk on 28/01/2016.
 */
$(document).ready(
    function () {

        /*   $('#id_id_alumno').attr("value", function (indiceArray) {
         //indiceArray tiene el índice de este elemento en el objeto jQuery
         var f = new Date();
         return (f.getFullYear()-'2000');
         });*/
        //terminar para poner foto al subirla
        $("#id_foto").change(function (evento) {
                evento.preventDefault();
                $("#foto").attr('src', '/media/fotos/' + $("#id_foto").val())
                // /$("#foto").attr("src",$())
            }
        )
        var formAjaxSubmit = function (form, modal) {
            $(form).submit(function (e) {
                e.preventDefault();
                $.ajax({
                    type: $(this).attr('method'),
                    url: $(this).attr('action'),
                    data: $(this).serialize(),
                    success: function (xhr, ajaxOptions, thrownError) {
                        if ($(xhr).find('.has-error').length > 0) {
                            $(modal).find('.modal-body').html(xhr);
                            formAjaxSubmit(form, modal);
                        } else {
                            $(modal).modal('toggle');
                        }
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        // handle response errors here
                    }
                });
            });
        }

        if ($("#semestreActivo").val() != 'False') {
            $("#info-semestre").fadeIn()
            $("#crear-semestre-id").fadeOut()
        }


        $('#button-id-addextra').click(function (evento) {

            //$('.modal-body').load('addExtracurricular/', function () {
            $('#myModal').modal('toggle');
            formAjaxSubmit('.modal-body form', '#myModal');
            //})
        })


        $('#button-id-addeval').click(function (evento) {
            //$('.modal-body').load('addExtracurricular/', function () {
            $('#myModal').modal('toggle');
            formAjaxSubmit('.modal-body form', '#myModal');
            //})
        })


        $('#buscar_alumno').on('click', Buscar);
        function Buscar() {
            var semestre = $('#id_semestre').val()
            var expediente = $('#id_expediente').val()
            var nombre = $('#id_nombre').val()
            var apellidoP = $('#id_apellido_paterno').val()
            var apellidoM = $('#id_apellido_materno').val()
            var plan = $('#id_plan').val()

            $.ajax({
                data: {
                    'semestre': semestre,
                    'expediente': expediente,
                    'nombre': nombre,
                    'apellidoP': apellidoP,
                    'apellidoM': apellidoM,
                    'plan': plan
                },
                url: '/academica/alumno-ajax/',
                type: 'get',
                success: function (data) {
                    var objeto = JSON.parse(data)
                    console.log(objeto.length)
                    if (objeto.length == 0) {
                        alert("No existen estudiantes para este criterio de busqueda")
                    }
                    else {
                        var html = "";
                        for (var i = 0; i < objeto.length; i++) {
                            html += ("<tr><td>" + objeto[i].id + "</td><td>" + objeto[i].expediente + "</td><td>" + objeto[i].apellidoP + "</td><td>" + objeto[i].apellidoM + "</td><td>" + objeto[i].nombre + "</td><td>" + objeto[i].semestre + "</td><td>Si</td>" + "<td></td>" + "</tr>")
//ver porque solamente muestra el ultimo en la busqueda

                            $('#id_table-body').html(html)
                        }
                    }

                }

            })

        }

        $('#buscar_extra').on('click', BuscarExtra);
        function BuscarExtra() {
            var clave = $('#id_clave').val()
            var nombre = $('#id_nombre').val()


            $.ajax({
                data: {
                    'clave': clave,
                    'nombre': nombre


                },
                url: '/academica/extracurricular-ajax/',
                type: 'get',
                success: function (data) {
                    var objeto = JSON.parse(data)
                    console.log(objeto.length)
                    if (objeto.length == 0) {
                        alert("Criterio de busqueda no encontrado")
                    }
                    else {
                        var html = "";
                        for (var i = 0; i < objeto.length; i++) {
                            html += ("<tr><td>" + objeto[i].clave + "</td><td>" + objeto[i].nombre + "</td><td>" + "</tr>")


                            $('#id_table-body').html(html)
                        }
                    }

                }

            })

        }


        $('#buscar_semestre').on('click', BuscarS);
        function BuscarS() {
            var clave = $('#id_clave').val()
            var ciclo = $('#id_cicloSep').val()
            var anio = $('#id_anio').val()
            var periodo = $('#id_periodo').val()


            $.ajax({
                data: {
                    'clave': clave,
                    'ciclo': ciclo,
                    'anio': anio,
                    'periodo': periodo,

                },
                url: '/academica/semestre-ajax/',
                type: 'get',
                success: function (data) {
                    var objeto = JSON.parse(data)
                    console.log(objeto.length)
                    if (objeto.length == 0) {
                        alert("Criterio de busqueda no encontrado")
                    }
                    else {
                        var html = "";
                        for (var i = 0; i < objeto.length; i++) {
                            html += ("<tr><td>" + objeto[i].clave + "</td><td>" + objeto[i].anio + "</td><td>" + objeto[i].periodo + "</td><td>" + objeto[i].fecha_inicio + "</td><td>" + objeto[i].fecha_fin + "</td><td>" + objeto[i].vigente + "</td>" + "<td></td>" + "</tr>")
//ver porque solamente muestra el ultimo en la busqueda

                            $('#id_tableSemestre-body').html(html)
                        }
                    }

                }

            })

        }

        //$('#modal-reporte-evafinal').on('click', EnviarDatosEvaFinal);
        //function EnviarDatosEvaFinal() {
        //    var carrera = $('#select_carreras').val()
        //    var materia = $('#select_materias').val()
        //    var ciclo = $('#select_ciclos').val()
        //    var grupo = $('#select_grupos').val()
        //    var semestre = $('#select_semestres').val()
        //
        //
        //
        //    $.ajax({
        //        data: {
        //            'carrera': carrera,
        //            'materia': materia,
        //            'ciclo': ciclo,
        //            'grupo': grupo,
        //            'semestre':semestre
        //
        //        },
        //        url: '/report/repevafinal/',
        //        type: 'get',
        //        success: function (data) {
        //
        //            console.log("SUCCESSS")
        //
        //        }
        //
        //    })
        //
        //}

        //end document ready
    }
);

function Buscar() {
    var anio = document.getElementById('id_semestre').selectedOptions[0].innerHTML.split('-')[0]
    var plan = $('#id_plan').val()
    console.log(anio)

    $.ajax({
        data: {
            'anio': anio,
            'plan': plan,

        },
        url: '/academica/buscarexp-ajax/',
        type: 'get',
        success: function (data) {
            var objeto = JSON.parse(data)
            console.log(objeto)
            $('#id_matricula').attr('value', objeto)

        }

    })


}

$('#select-materias').on('change',Cargar)
function Cargar(){
    var id=$(this).val()
    $.ajax({
        data:{'id':id},
        url:'/academica/matcal-ajax/',
        type:'get',
        success : function(data){
            var object=JSON.parse(data)
            var html=""
             for (var i = 0; i < object.length; i++) {
                  html += ("<tr><td>" + object[i].matricula + "</td><td>" + object[i].nombre + "</td><td>" + object[i].apellido_paterno + "</td><td>" + object[i].apellido_materno + "</td><td><a href=califcreatajax/"+object[i].id+"/ >Actualizar</a>" + "</td></tr>")
                            $('#result-calificaciones').html(html)
             }
        }
    });
}



function cargarPlan() {
    Dajaxice.academica.cargar_plan(Dajax.process);
}


$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }

    }
});




