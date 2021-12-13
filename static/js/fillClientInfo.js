function getClientInfo() {
return new Promise((resolve, reject) => {
    $.ajax({
        url: "/fillClientData",
        type: 'POST',
        // data: JSON.stringify(this.value),
        success: function (data) {
            resolve(data)
        },
        error: function (error) {
            reject(error)
        },
    })
})
}

let p = getClientInfo();   
p.then((data) => {
    for (var key in data){
        var value = data[key];
        let input = document.getElementsByName(key);
        input[0].value = value;
    }
})