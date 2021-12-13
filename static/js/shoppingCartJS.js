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
        success: function (data) {
            resolve(data)
        },
        error: function (error) {
            reject(error)
        },
        })
    })
    p.then((data) => {
        // TO DO:
        // update cart fron-end information when new data is added to backend
        // console.log(data);
    })
});