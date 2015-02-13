    /* Global
    ----------------------------------------------*/
    var ID_MODAL_FORM = "modalform",
        ID_NAME = "id_name",// id tags
        ID_DESCRIPTION = "id_description",
        ID_CATEGORIES = "id_category",
        ID_IMAGE = "id_image",
        ID_TAGS = "id_tags";


var category_post = function() {
    // Se inicializan los campos inciales.
    var $formBlog = $("#id_title").closest("form"),
        $tags = $( "#" + ID_TAGS ),
        $formBlog = $("#id_title").closest("form");

    $('div.django-ckeditor-widget').removeAttr('style');

    /* Motor de tags
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
                $tags_list.append("<li class='isTag'>" + $.trim($thisInput.val().replace(/,/g, '').toLowerCase()) + "<b class='delete'> ×</b></li>");
            $thisInput.val("");
        } else if (key == ",") {
            $thisInput.val("");
        }
    });
    // Se agregan las tags con tab.
    $("#id_tags_add").on("blur", function () {
        var $thisInput = $(this);
        if ($thisInput.val() !== "") {
            if (!checkIfExist($thisInput))
                var new_tag = $thisInput.val();
                $tags_list.append("<li class='isTag'>" + $thisInput.val().replace(/,/g, '').toLowerCase() + "<b class='delete'> ×</b></li>");
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
        $( "#" + ID_TAGS ).val(tag_list);
    });
    /* FileField
    ----------------------------*/
    if ( $formBlog.length > 0) {
        var $imagen = $( "#" + ID_IMAGE);
        $imagen.before("<input class='btn btn-default' type='button' value='Imagen' style='float:left'><input type='text' placeholder='Buscar...' class='form-control' id='id_img_add' style='width: 500px; float:left;'></input>");
        $imagen.hide();
        var $fakeimage = $("#id_img_add");
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
    /*Categories form
    ________________________________*/
    $formBlog.find( "#id_category" ).after("<div><a id='add_category'>Agregar</a></div>");
    var $modalform = $( "div#" + ID_MODAL_FORM );
    $modalform.hide();
    $("#add_category").on("click", function () {
        $modalform.show("slow");
    });
    $("#cancel-cate").on("click", function () {
        $modalform.hide("slow");
    });
    $("form.new-cate").on("submit", function (event) {
        event.preventDefault();
        var fieldVoid = false,
            $form = $(this);

        $form.find("input, textarea").not(":submit").each(function () {
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
                url: $form.attr( "action" ),
                data: $form.serialize(),
                success: function(result){
                    var category = $("div#" + ID_MODAL_FORM + " #" + ID_NAME ).val();
                    $( "#" + ID_CATEGORIES ).append("<option value='" + category + "'>" + category + "</option>");
                    $( "#" + ID_CATEGORIES ).val(category);
                    $modalform.hide("slow");
                    $modalform.find("input:text, textarea").each(function(){
                        $(this).val("");
                    });
                }
            });
        }
    });
};

/* Category template script
_________________________*/
var category_template = function() {
    var $modalform = $( "div#" + ID_MODAL_FORM );
    $modalform.hide();
    $(".del_category").on("click", function(){
        var $row = $(this).closest("tr");
        var category_name = $row.find("p.name").text(),
            category_description = $row.find("p.description").text();

        if(confirm("Se borra la categoria " + category_name
            + " y todo los post relacionados estas seguro")){
            $.ajax({
                type: "POST",
                data: {
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                    category_name: category_name
                },
                success: function(result){
                    console.log(result);
                    $row.remove();
                },
                error: function(xhr, result, err){
                    console.log(xhr);
                }
            });
        }
    });
    $("#show-add").on("click", function(){
        $("#" + ID_MODAL_FORM ).show("slow");
    });
    $("#cancel-cate").on("click", function () {
        $modalform.hide("slow");
    });
    $("form.new-cate").on("submit", function(){
        event.preventDefault();
        var fieldVoid = false,
            $form = $(this);
        $form.find("input, textarea").not(":submit").each(function () {
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
                url: $form.attr( "action" ),
                data: $form.serialize(),
                success: function(result){
                    window.location.reload();
                }
            });
        }
    });
};


/* Entries Update Manage
----------------------*/
// Notice that this is function is outside of the JQuery's "$('Document').ready(function(){});"
    var entries_status = function(){
        var posts = [];
        $("tr.infopost").each(function(){
            var $this = $(this);
            temp = [
                $this.attr("id"),
                $this.find("#id_comment").prop("checked"),
                $this.find("#id_category option:selected").text(),
                $this.find("#id_status option:selected").text()
            ];
            posts.push(temp);
        });
        var $buttons = $("input.savedata");
        $(".categorias, .status, .comentar").on("change", function(){
            var $row = $(this).closest("tr");
            for (var i = 0; i < posts.length; i++) {
                if( posts[i][0] == $row.attr("id")){
                    if (
                        (posts[i][1] != $row.find("#id_comment").prop("checked")) ||
                        (posts[i][2] != $row.find("#id_category option:selected").text()) ||
                        (posts[i][3] != $row.find("#id_status option:selected").text())
                    ){
                        $row.find("input.savedata")
                        .removeAttr("disabled")
                        .addClass("btn-primary");
                    } else {
                        $row.find("input.savedata")
                        .attr("disabled", "true")
                        .removeClass("btn-primary")
                        .addClass("btn-default");
                    }
                }
            };
        });
        $buttons.on("click", function(event){
            event.preventDefault();
            var $this = $(this);
            $.ajax({
                type: "POST",
                url: "/blog/entries/",
                data: {
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                    post_id: $this.siblings("input:hidden").val(),
                    comment: $this.closest("tr").find("#id_comment").prop('checked'),
                    category: $this.closest("tr").find("#id_category option:selected").text(),
                    status: $this.closest("tr").find("#id_status option:selected").val()
                },
                success: function(result){
                    $this.removeClass("btn-primary");
                    $this.addClass("btn-default");
                    var $row = $this.closest("tr");
                    for (var i = 0; i < posts.length; i++) {
                        if( posts[i][0] == $row.attr("id")){
                            posts[i][1] = $row.find("#id_comment").prop("checked");
                            posts[i][2] = $row.find("#id_category option:selected").text();
                            posts[i][3] = $row.find("#id_status option:selected").text();
                        }
                    };
                },
                error: function(xhr, result, err){
                    console.log(xhr)
                }
            });
            $this.attr("disabled", "true");
        });
    };


    /* Social Share
    --------------------------*/
    var get_social_network = {
        'facebook': "http://www.facebook.com/sharer.php?u=" + document.URL,
        'twitter':  "http://twitter.com/share?text=" + document.title + "&url=" + document.URL,
        'gplus': "https://plus.google.com/share?url=" + document.URL
    };

    var social_share = function( object, SITE ) {
        if ( get_social_network[ SITE.toLowerCase() ]) {
            window.open(get_social_network[ SITE.toLowerCase() ], SITE.toUpperCase(), 'height=450, width=500, top=' + ($(window).height() / 2 - 225) + ', left=' + ($(window).width() / 2 - 225));
        }
        return false;
    };

