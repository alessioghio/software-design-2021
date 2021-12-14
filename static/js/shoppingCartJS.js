function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

function accordion() {
    $('.accordion-title').click(function (e) {

        $(this).next().slideToggle('easeOut');
        $(this).toggleClass('active');
        $("accordion-title").toggleClass('active');
        $(".accordion-content").not($(this).next()).slideUp('easeIn');
        $(".accordion-title").not($(this)).removeClass('active');

    });
    $(".accordion-content").addClass("defualt-hidden");

};

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

function updateTotalPrice(response){
    var totalPrice = document.getElementById("totalPrice")
    var completeString = totalPrice.innerText.split(' ');
    completeString[2] = String(response.totalPrice);
    var newText = completeString.join(" ");
    totalPrice.innerText = newText;
}

function updateCartInfo(response){
    var elements = document.getElementsByClassName("accordion-section");
    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];
        var divs = element.children;
        var values = divs[1].children[0].children;
        var existsInCart = false;
        if(values[0].innerText == String(response.supply_id)){
            var completeString = values[1].innerText.split(' ');
            completeString[1] = String(response.quantity);
            var newText = completeString.join(" ");
            values[1].innerText = newText;
            existsInCart = true;
            break;
        }
    }
    if(!existsInCart){
        var removeForm = document.getElementById("removeCartForm");
        // var newProduct = document.createElement("div");
        var newProduct = `<div class="accordion mb-15">
                            <div class="accordion-section">
                                <h6 class="accordion-title white text-left">${response.name}</h6>
                                <div class="accordion-content">
                                    <div class="form-field-wrapper">
                                        <p hidden>${response.supply_id}</p>
                                        <p class="white text-left">Cantidad: ${response.quantity} ${response.unit}</p>
                                        <p class="white text-left">Precio: S/ ${response.price}</p>
                                        <button class="btn btn-md btn-white"  type="submit" onclick="removeFromCart(${response.supply_id})">Quitar</button>
                                    </div>
                                </div>
                            </div>
                        </div>`
        removeForm.insertAdjacentHTML("afterbegin",newProduct);
        accordion();
        updateTotalPrice(response);
    }
}

function removeFromCart(supply_id){
    let p = new Promise((resolve, reject) => {
        $.ajax({
            url: "/removeFromCart",
            type: 'POST',
            data: JSON.stringify(supply_id),
            success: function (response) {
                resolve(response)
            },
            error: function (error) {
                reject(error)
            },
        })
    })
    p.then((response) => {
        // Remove div from list
        var elements = document.getElementsByClassName("accordion mb-15");
        for (var i = 0; i < elements.length; i++) {
            var element = elements[i];
            var divs = element.children[0];
            var values = divs.children[1].children[0].children;
            if(values[0].innerText == String(response.supply_id)){
                element.remove();
            }
        }
        updateTotalPrice(response)
    })
}

$("[id=addCartForm]").on('submit', function(e){
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

$("[id=removeCartForm]").on('submit', function(e){
	// Stop the form submitting
  	e.preventDefault();
});