function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

function buttonMessage(response){
    var elements = document.getElementsByClassName("form-field-wrapper");
    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];
        var inputs = element.children;
        if(inputs[0].value == response.supply_id){
            var cartButton = inputs[2];
            var quantityBox = inputs[1];
            cartButton.innerHTML = "✓ Agregado"
            delay(2000).then(() => {
                cartButton.innerHTML = "Añadir al carrito";
                quantityBox.value = "";
                quantityBox.placeholder = "Cant.";
            });
        }
    }
}

$('form').on('submit', function(e){
	// Stop the form submitting
  	e.preventDefault();
  	// Do whatever it is you wish to do
    let p = new Promise((resolve, reject) => {
    $.ajax({
        url: "/addToShoppingCart",
        type: 'POST',
        data:{
            supply_id: $(this).find("input")[0].value,
            quantity: $(this).find("input")[1].value
        },
        success: function (response) {
            resolve(response)
        },
        error: function (error) {
            reject(error)
        },
        })
    })
    p.then((response) => {
        buttonMessage(response);
        // update cart fron-end information when new data is added to backend
        
        // console.log(data);
    })
});