function updateInputsValues(data){
    for (var key in data){
        var value = data[key];
        // console.log(key)
        // console.log(value)
        // console.log("----")
        let input = document.getElementsByName(key);
        // console.log(value)
        if (key == "description") {
            input[1].value = value;
        } else if(key == "visibility"){
            input[0].checked = value;
        } else{
            input[0].value = value;
        }
        
    }
}

var rad = document.filterForm.id;
if(!(rad.constructor === RadioNodeList)){
    rad = [rad];
}
var prev = null;
for (var i = 0; i < rad.length; i++) {
    rad[i].addEventListener('change', function() {
        // (prev) ? console.log(prev.value): null;
        if (this !== prev) {
            prev = this;
        }
        // console.log(this.value)
        let p = new Promise((resolve, reject) => {
            $.ajax({
                url: "/fillForm",
                type: 'POST',
                data: JSON.stringify(this.value),
                success: function (data) {
                    resolve(data)
                },
                error: function (error) {
                    reject(error)
                },
            })
        })
        p.then((data) => {
            updateInputsValues(data);
        })
    });
}