jQuery( document ).ready(function() {

	// Se inicializan los campos inciales.
	var $tags = $("#id_tags");
	var $tags_elements =  $tags.children("option");
	var $modalform = $("div#modalform");

	$("#id_categoria").after("<div><a href='#' id='categoria'>Agregar</a></div>")
	$modalform.hide();
	$tags.siblings("p.help-block").remove()
	//$tags.css("display", "none");
	$tags.after("<input class=' form-control' id='id_tags_add' maxlength='100' name='id_tags_tag' type='text'>");
	$tags.after("<ul id='id_tags_list' class='id_tags_list'></ul>");

	$( "#categoria" ).on("click", function(){
		$modalform.show("slow");
	});
	$("#cancel-cate").on("click", function(){
		$modalform.hide("slow");
	});
	$( "form.new_cate" ).on("submit", function(){
		var fieldVoid = false;
		$(this).find("input, textarea").not(":submit").each( function(){
			var $this = $(this)
			if ( $.trim( $this.val() ) === "" ){
				$this.css("border-color","#f00")
				fieldVoid = true;
			}
		});
		if ( fieldVoid )
			return false;
	});

	// Funcion que almacena en una lista los tags.
	function checkIfExist( $thisInput ){
		var tagExist = false;
		if ( $thisInput.val().substr($thisInput.val().length - 1) == ",") {
			$tags_list.find("li").each( function() {
				if ($(this).text().slice(0,-2) == $thisInput.val().slice(0, -1))
					tagExist = true;
			});
		} else {
			$tags_list.find("li").each( function() {
				if ( $(this).text().slice(0,-2) == $thisInput.val() )
					tagExist = true;
			});
		}
		console.log(tagExist);
		return tagExist;
	}

	// Se agregan las tag con comas.
	var $tags_list = $("#id_tags_list");
	$("#id_tags_add").on( "keyup", function() {
		var $thisInput = $(this);
		var key = $thisInput.val().substr($thisInput.val().length - 1);
		if ((key == ",") && $thisInput.val().length > 1) {
			if ( !checkIfExist( $thisInput ) )
				$tags_list.append("<li class='isTag'>"+ $thisInput.val().slice(0, -1) +"<b class='delete'> ×</b></li>");
			$thisInput.val("");
		} else if (key==",") {
			$thisInput.val("");
		}
	});
	// Se agregan las tags con tab.
	$("#id_tags_add").on("blur", function(){
		var $thisInput = $(this);
		if ( $thisInput.val() !== "" ){
			if (checkIfExist)
				$tags_list.append("<li class='isTag'>"+ $thisInput.val() +"<b class='delete'> ×</b></li>");
			$thisInput.val("");
		}
	});

	$( "ul.id_tags_list" ).on("click", "b.delete", function() {
		$(this).closest("li").remove();
	});

});
