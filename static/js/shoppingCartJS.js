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

function updateCartInfo(response){
    var elements = document.getElementsByClassName("accordion-section");
    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];
        var divs = element.children;
        var values = divs[1].children[0].children;
        if(values[0].innerText == String(response.supply_id)){
            var completeString = values[1].innerText.split(' ');
            completeString[1] = String(response.quantity);
            var newText = completeString.join(" ");
            values[1].innerText = newText;
        }
    }
    var totalPrice = document.getElementById("totalPrice")
    var completeString = totalPrice.innerText.split(' ');
    completeString[2] = String(response.totalPrice);
    var newText = completeString.join(" ");
    totalPrice.innerText = newText;
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
        updateCartInfo(response);
    })
});