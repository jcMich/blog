jQuery(document).ready(function () {
    // Se inicializan los campos inciales.
    var $tags = $("#id_tags");
    var $tags_elements = $tags.children("option");
    var $formBlog = $("#id_title").closest("form");

    /*Motor de tags
    ----------------------------------------------*/
    $tags.siblings("p.help-block").remove();
    $tags.css("display", "none");
    $tags.after("<input class=' form-control' id='id_tags_add' name='id_tags_tag' type='text'>");
    $tags.after("<ul id='id_tags_list' class='id_tags_list'></ul>");
    // Funcion que almacena en una lista los tags.
    function checkIfExist($thisInput) {
        var tagExist = false;
        if ($thisInput.val().substr($thisInput.val().length - 1) == ",") {
            $tags_list.find("li").each(function () {
                if ($(this).text().slice(0, -2) == $.trim($thisInput.val().slice(0, -1).toLowerCase()))
                    tagExist = true;
            });
        } else {
            $tags_list.find("li").each(function () {
                if ($(this).text().slice(0, -2) == $thisInput.val())
                    tagExist = true;
            });
        }
        return tagExist;
    }
    // Se agregan las tag con comas.
    var $tags_list = $("#id_tags_list");
    $("#id_tags_add").on("keyup", function () {
        var $thisInput = $(this);
        var key = $thisInput.val().substr($thisInput.val().length - 1);
        if ((key == ",") && $thisInput.val().length > 1) {
            if (!checkIfExist($thisInput))
                $tags_list.append("<li class='isTag'>" + $.trim($thisInput.val().slice(0, -1).toLowerCase()) + "<b class='delete'> ×</b></li>");
            $thisInput.val("");
        } else if (key == ",") {
            $thisInput.val("");
        }
    });
    // Se agregan las tags con tab.
    $("#id_tags_add").on("blur", function () {
        var $thisInput = $(this);
        if ($thisInput.val() !== "") {
            if (checkIfExist)
                $tags_list.append("<li class='isTag'>" + $thisInput.val() + "<b class='delete'> ×</b></li>");
            $thisInput.val("");
        }
    });

    $("ul.id_tags_list").on("click", "b.delete", function () {
        $(this).closest("li").remove();
    });
    $formBlog.on("submit", function(){
        var $tags = $tags_list.find("li");
        var tag_list = "";
        for (var i = 0; i < $tags.length ; i++) {

            var temp = $tags[i].innerHTML.substr(0, $tags[i].innerHTML.indexOf("<"));
            if (i === 0)
                tag_list += temp.toLowerCase();
            else
                tag_list += "," + temp.toLowerCase();
        }
        $("#id_tags").val(tag_list);
    });
    /* Categorias.
    ----------------------------------------*/
    $formBlog.find("#id_categoria").after("<div><a id='category'>Agregar</a></div>");
    /*$formBlog.before("<div id='modalform'><form class='new_cate' role='form'> \
        <div class='form-group'><label class='control-label' for='id_name'>Nombre</label> \
        <input class='form-control' id='id_name' maxlength='30' name='nombre' type='text'></div> \
        <div class='form-group'><label class='control-label' for='id_description'>Descripcion</label> \
        <textarea class='form-control' cols='40' id='id_description' name='descripcion' rows='10'></textarea>\
        </div><input class='btn-u' type='submit' id='save_data' value='Agregar'><a id='cancel-cate'>Cacelar</a></form></div>"
    );*/
    var $modalform = $("div#modalform");
    $modalform.hide();
    $("#category").on("click", function () {
        $modalform.show("slow");
    });
    $("#cancel-cate").on("click", function () {
        $modalform.hide("slow");
    });
    $("form.new_cate").on("submit", function (event) {
        event.preventDefault();
        var fieldVoid = false,
            self = $(this);

        self.find("input, textarea").not(":submit").each(function () {
            var $this = $(this);
            if ($.trim($this.val()) === "") {
                $this.css("border-color", "#f00");
                fieldVoid = true;
            }
        });
        if (fieldVoid){
            return false;
        } else {
            $.ajax({
                type: "POST",
                url: self.attr("action"),
                data: {
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                    nombre: self.find("#id_nombre").val(),
                    descripcion: self.find("#id_descripcion").val(),
                },
                success: function(result){
                    var category = $("div#modalform #id_nombre").val();
                    $("#id_categoria").append("<option value='" + category + "'>" + category + "</option>");
                    $("#id_categoria").val(category);
                    $modalform.hide("slow");
                    $modalform.find("input:text, textarea").each(function(){
                        $(this).val("");
                    });
                },
                error: function(xhr, result, err){
                        console.log(xhr, err);
                }
            });
        }
    });
    /* FileField
    ----------------------------*/
    if ( $formBlog.length > 0) {
        var $imagen = $("#id_imagen");
        $imagen.before("<input class='btn btn-default' type='button' value='Imagen' style='float:left'><input type='text' placeholder='Buscar...' class='form-control' id='id_imagen_add' style='width: 500px; float:left;'></input>");
        $imagen.hide();
        var $fakeimage = $("#id_imagen_add");
        $fakeimage.on( "click", function(){
            $imagen.click();
        });
        $fakeimage.prev().on( "click", function(){
            $imagen.click();
        });
        $imagen.change(function() {
            var $this = $(this);
            var imagenName = $(this).val();
            $fakeimage.val($this.val());
        });
    }
});

